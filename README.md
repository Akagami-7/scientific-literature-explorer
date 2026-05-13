# Scientific Literature Explorer

#### Try the demo here: 
[Scientific Literature Explorer Demo](https://scientific-literature-explorer.streamlit.app/)

---

## Description
The Scientific Literature Explorer is a deep research Q&A system that helps users understand research papers quickly.
Instead of reading long PDFs, users can:
- Upload papers
- Search for concepts using semantic search
- View the most relevant sections
- Explore citation relationships
- Receive similarity based recommendations

---

## Project Objective
The goal of this project is to:
* Enable semantic search within academic papers
* Improve research exploration using embeddings
* Visualize citation relationships
* Demonstrate a scalable retrieval based architecture
* Reduce literature review time using intelligent search

---

## How it works
### 1. Upload papers
Users upload research papers in PDF format.

The system:
- Extracts text from the PDF
- Cleans formatting
- Preserves page level references

**Tools used:**
- `PyPDF2`

> [!NOTE]
> <b> Optional ScaleDown Compression </b>
>
> 
> If enabled, the system compresses the extracted text using ScaleDown API to:
> - Reduce document size
> - Optimize processing time
> - Preserve technical meaning

### 2. Split Text into Chunks
Research papers are very long, so the text is split into smaller parts.

- Each chunk is about 800–1200 characters
- Very small or irrelevant lines are ignored
- Chunks preserve contextual meaning

This helps in tracking where the information came from.

### 3. Create Embeddings
Each text chunk is converted into vector representation called embeddings.

- These embeddings represent the meaning of the text
- Similar text has similar embeddings

**Tools used:**
<!-- - ScaleDownAI Embeddings-->
- Sentence Transformers

### 4. Store Data
Embeddings and corresponding text chunks are stored in a vector index.

Stored data includes:
- Text chunks
- Chunk embeddings
- Citation markers
- Paper metadata

Vector similarity search is performed using cosine similarity.

### 5. Enter a query
When a user enters a query:
- The query is converted into an embedding
- Cosine similarity is computed between the query and stored chunks.
- Top relevant sections are returned.
- Matching terms are highlighted in the interface

This method is called **embedding based semantic search**.

### 6. Generate Answer with Citations
The system extracts citation markers such as:
```
[1], [3], [7]
```
Using these markers, a simple citation network graph is generated to visualize:
+ The uploaded paper
+ Its referenced works

Tool used:
```
NetworkX
```

### 7. Display Result
The system includes a basic recommendation module:
* Paper embeddings are stored in memory.
* Cosine similarity is used to rank similar papers.
* Top-K similar papers are suggested.

---

## System Flow
```
PDF
  ↓
Text Extraction
  ↓
(Optional) ScaleDown Compression
  ↓
Cleaning & Chunking
  ↓
SentenceTransformer Embeddings
  ↓
Vector Storage
  ↓
-----------------------------------------
User Query
  ↓
Query Embedding
  ↓
Cosine Similarity
  ↓
Top Relevant Chunks
  ↓
Display Results + Citation Graph + Recommendations

```

---

## Tools and Technologies
| Purpose | Tool |
|-------|------|
| PDF to Text | PyPDF2 |
| Text Processing | Python |
| Compression | ScaleDownAPI |
| Embeddings | Sentence Transformers |
| Similarity | Cosine Similarity |
| Graph Visualization | NetworkX |
| Frontend & Backend | Streamlit |
<!--| Embeddings | ScaleDownAI / Sentence Transformers |-->
<!--| Vector storage | FAISS |->>
<!--| Language model | Ollama |-->

---

## Neural Networks
This project uses **pre-trained neural networks** for:
- Creating embeddings using Sentence Transformers
- Semantic similarity comparison for intelligent retrieval

---

## Creative/Planned Feature
Planned improvements include:

* Multipaper indexing and cross paper comparison
* Enhanced citation graph analytics
* Research trend detection
* Hybrid retrieval (keyword + semantic)
* Figure extraction and CNN based visual analysis

---

## Summary
Scientific Literature Explorer demonstrates how embedding-based semantic search can improve academic paper exploration.  
It is useful for students and researchers who want faster and more intelligent access to research content.
