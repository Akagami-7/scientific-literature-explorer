# System Architecture

The system follows a Retrieval-Augmented Generation (RAG) pipeline.

Pipeline:
1. PDF Ingestion & Text Extraction - Extract text content from the uploaded PDF.
2. Chunking and metadata tagging - Split text into smaller chunks and attach metadata.
3. Embedding generation - Convert each chunk into vector embeddings.
4. Vector storage using FAISS - Store embeddings efficiently using FAISS.
5. Semantic search on user query - Convert user query into embedding and retrieve most relevant chunks.
6. Answer generation using LLM with citations - Generate final answer using LLM with proper source citations.
