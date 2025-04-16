import os, importlib.resources
os.environ['NLTK_DATA'] = str(importlib.resources.files('strive').joinpath('resources/nltk_data'))

import re, string, unicodedata, faiss, fasttext, numpy as np, bm25s, copy
from sklearn.feature_extraction.text import HashingVectorizer
from nltk.stem import RSLPStemmer, PorterStemmer
from collections import defaultdict
from model2vec import StaticModel
from nltk.corpus import stopwords
from functools import lru_cache
from enum import Enum

langdetect_model_path = str(importlib.resources.files('strive').joinpath('resources/lid.176.ftz'))

PUNCTUATION_TABLE = str.maketrans('', '', string.punctuation)
NON_PRINTABLE = set(string.printable)
REGEX_X = re.compile(r'\\x[0-9a-fA-F]{2}')
REGEX_WHITESPACE = re.compile(r'\s+')

def deduplicate_results(ranked_results, top_k=100):
    # Convert ranked results to a dictionary with weights
    results_dict = defaultdict(list)
    for result in ranked_results:
        results_dict[result[0]].append(result[1])

    # Get the max score for each sentence
    max_scores = {}
    for sentence, scores in results_dict.items():
        max_scores[sentence] = max(scores)
    
    # Sort the sentences by their max score, descending
    sorted_sentences = sorted(max_scores.items(), key=lambda x: x[1], reverse=True)

    # Cut to top_k
    deduplicated_results = sorted_sentences[:top_k]

    return deduplicated_results

class EmbeddingType(Enum):
    textual = 1
    semantic = 2

class Reranker:
    """ Semantic Tokenized Re-Ranking via Vectorization & Embeddings """

    def __init__(self, embedding_type: EmbeddingType = EmbeddingType.textual):
        self.langdetect_model = fasttext.load_model(langdetect_model_path)

        self.embedding_type = embedding_type
        self.dimension = 128

        self.portuguese_stemmer = RSLPStemmer()
        self.english_stemmer = PorterStemmer()

        self.pt_stopwords = set(stopwords.words('portuguese'))
        self.en_stopwords = set(stopwords.words('english'))

        if embedding_type == EmbeddingType.semantic:
            self.vectorizer = StaticModel.from_pretrained("minishlab/potion-base-4M")
        else:
            self.vectorizer = HashingVectorizer(
                analyzer='char_wb',
                ngram_range=(1, 4), # Capture longer subword patterns
                n_features=self.dimension,
                alternate_sign=False # Better for similarity matching
            )

    def _detect_language(self, text):
        detected_lang = self.langdetect_model.predict(text.replace('\n', ' '), k=1)[0][0]
        result = str(detected_lang).replace('__label__', '')
        if result == 'pt':
            return 'pt'
        return 'en'
    
    @lru_cache(maxsize=500000)
    def _stemming(self, word, lang):
        return self.portuguese_stemmer.stem(word) if lang == 'pt' else self.english_stemmer.stem(word)

    @lru_cache(maxsize=500000)
    def _normalize_text(self, text):
        text = unicodedata.normalize('NFKD', text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        text = text.translate(PUNCTUATION_TABLE)
        text = ''.join(c for c in text if c in NON_PRINTABLE)
        text = REGEX_X.sub('', text)
        text = REGEX_WHITESPACE.sub(' ', text).strip()
        return text

    @lru_cache(maxsize=500000)
    def _remove_punctuation_only(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text

    def _vectorize_sentences(self, texts):
        if self.embedding_type == EmbeddingType.semantic:
            return self.vectorizer.encode(texts)
        else:
            X = self.vectorizer.transform(texts)
            dense_matrix = X.toarray()
            return dense_matrix

    def _is_stopword(self, word, lang):
        return word in self.pt_stopwords if lang == 'pt' else word in self.en_stopwords
    
    def rerank_documents(self, query, documents, top_k=100):
        try:
            query = query.lower()
            documents = [document.lower() for document in documents]
            tokenized_corpus = {}

            corpus = documents
            corpus_lang = self._detect_language(' '.join(corpus))

            for corpus_index, sentence in enumerate(corpus):
                sentence_tokens = self._remove_punctuation_only(sentence).split()
                for token_index, token in enumerate(sentence_tokens):
                    stemmed_token = self._stemming(token, corpus_lang)
                    normalized_stemmed_token = self._normalize_text(stemmed_token)
                    if not normalized_stemmed_token or self._is_stopword(token, corpus_lang) or len(normalized_stemmed_token) <= 2:
                        continue

                    tokenized_corpus[f"{corpus_index}_{token_index}"] = normalized_stemmed_token

            corpus_tokens = list(tokenized_corpus.values())

            faiss_index = faiss.IndexFlatIP(self.dimension)

            index_map = {}
            counter = 0
            vectors = []

            for key, sentence in tokenized_corpus.items():
                index_map[counter] = key
                vectors.append(sentence)
                counter += 1

            vectors = self._vectorize_sentences(vectors)
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            vectors = vectors / norms
            faiss_index.add(vectors)

            query_tokens = self._remove_punctuation_only(query).split()
            # Remove stopwords
            query_tokens = [ token for token in query_tokens if self._normalize_text(token) and not self._is_stopword(token, corpus_lang) ]
            query_tokens = [ self._stemming(token, corpus_lang) for token in query_tokens ]
            query_tokens = [ self._normalize_text(token) for token in query_tokens ]
            query_tokens = [ t for t in query_tokens if len(t) > 2 ]

            term_frequencies = {}

            for qt in query_tokens:
                term_frequencies[qt] = corpus_tokens.count(qt)

            # Remove terms with zero frequency
            original_term_frequencies = copy.deepcopy(term_frequencies)
            term_frequencies = { term: freq for term, freq in term_frequencies.items() if freq > 0 }

            if not term_frequencies:
                term_frequencies = original_term_frequencies
                term_frequencies = { k: 1 for k in term_frequencies.keys() }

            power_factor = 1.2  # Adjust this value to increase the emphasis on lower frequency terms

            # Calculate the inverse of term frequencies with a power factor
            inverse_frequencies = {term: (1/freq) ** power_factor for term, freq in term_frequencies.items()}

            # Normalize the weights so they sum to 1 (optional)
            total_weight = sum(inverse_frequencies.values())
            normalized_weights = {term: weight / total_weight for term, weight in inverse_frequencies.items()}

            seen_base_ids = set()
            results = []

            for qt in list(term_frequencies.keys()):
                token_vector = self._vectorize_sentences([qt])

                token_score_multiplier = normalized_weights[qt]

                # Normalize
                norm = np.linalg.norm(token_vector)
                token_vector = token_vector / norm

                search_results = faiss_index.search(token_vector, top_k // (len(query_tokens) * 2))
                search_result_indexes = search_results[1][0].tolist()
                search_result_scores = search_results[0][0].tolist()

                # Interpolate both
                for sri, score in zip(search_result_indexes, search_result_scores):
                    if sri == -1:
                        continue

                    true_id = index_map[sri]
                    recovered_id = int(true_id.split("_")[0])
                    if recovered_id not in seen_base_ids:
                        results.append((recovered_id, score * token_score_multiplier))
                        seen_base_ids.add(recovered_id)

            # Sort results by score, descending
            results.sort(key=lambda x: x[1], reverse=True)

            filtered_results = results[:top_k]

            # Retrieve the sentences from the index map
            final_results = [ (corpus[corpus_index], score) for corpus_index, score in filtered_results ]

            return final_results
        except Exception:
            try:
                # Fallback to BM25
                corpus_lang = self._detect_language(' '.join(corpus))
                corpus_tokens = bm25s.tokenize(documents, stopwords=corpus_lang)

                # Create the BM25 model and index the corpus
                retriever = bm25s.BM25()
                retriever.index(corpus_tokens)

                query_tokens = bm25s.tokenize(query)
                results, scores = retriever.retrieve(query_tokens, k=top_k)

                results = []
                for i in range(results.shape[1]):
                    doc, score = results[0, i], scores[0, i]
                    sentence = corpus[doc]
                    results.append((doc, score))
                
                return results
            except Exception:
                return []
