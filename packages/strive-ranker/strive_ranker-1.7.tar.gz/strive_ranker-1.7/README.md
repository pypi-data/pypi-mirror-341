STRIVE: Semantic Tokenized Ranking via Vectorization & Embeddings

```python
from strive.reranker import Reranker, EmbeddingType, deduplicate_results

textual_reranker = Reranker(embedding_type=EmbeddingType.textual)
semantic_reranker = Reranker(embedding_type=EmbeddingType.semantic)

# Supports English and Portuguese
corpus = [
    "O presidente anunciou novas políticas econômicas.",
    "Houve exonerações no governo recentemente.",
    "Os nomes dos exonerados ainda não foram divulgados.",
    "O mercado financeiro reagiu positivamente às mudanças.",
    "O congresso discutirá reformas tributárias esta semana."
]

query = "danças"

# Build the index with the given corpus
textual_results = textual_reranker.rerank_documents(query, corpus, top_k=50)
semantic_results = semantic_reranker.rerank_documents(query, corpus, top_k=50)
merged_results = textual_results + semantic_results

# Deduplicate the results
deduplicated_results = deduplicate_results(merged_results, top_k=2)

print(deduplicated_results)
# [('Os nomes dos exonerados ainda não foram divulgados.', 0.30326954502292763), ('Houve exonerações no governo recentemente.', 0.30326954502292763)]
```