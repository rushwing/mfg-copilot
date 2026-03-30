# RAG Service

This service is the single retrieval interface for upper layers.

Rule:
- agents do not talk to Milvus and Elasticsearch directly
- agents call one retrieval contract exposed by `rag-service`

Why:
- retrieval composition changes over time
- Milvus and Elasticsearch may be queried together, separately, or with reranking
- agents should not need to know which backing store produced each candidate set

Expected responsibilities:
- retrieve from Milvus and Elasticsearch
- fuse and rerank results
- attach citations and provenance
- expose one normalized retrieval response contract to orchestrator and agents

