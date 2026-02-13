# Scientific Literature Explorer

## Description
The Scientific Literature Explorer is a deep research Q&A system that helps users understand research papers quickly.
Instead of reading long PDFs, users can:
- Upload papers
- Search for concepts using semantic search
- View the most relevant sections
- Explore citation relationships
- View the most relevant sections

---

## Project Objective
The goal of this project is to:
* Enable semantic search within academic papers
* Improve research exploration using embeddings
* Visualize citation relationships
* Demonstrate a scalable architecture for future research intelligence systems

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

### 2. Split Text into Chunks
Research papers are very long, so the text is split into smaller parts.

- Each meaningful chunk is about 800–1200 characters
- Very small or irrelevant lines are ignored

This helps in tracking where the information came from.

### 3. Create Embeddings
Each text chunk is converted into vector representation called embeddings.

- These embeddings represent the meaning of the text
- Similar text has similar embeddings

**Tools used:**
- ScaleDownAI Embeddings
- Sentence Transformers

### 4. Store Data
Embeddings are stored in memory and compared using cosine similarity.

Stored data includes:
- Text chunks
- Chunk embeddings
- Citation markers
- Paper metadata

### 5. Enter a query
When a user enters a query:
- The query is converted into an embedding
- Cosine similarity is computed between the query and stored chunks.
- Top relevant sections are returned.
- Matching terms are highlighted in the interface

This method is called **semantic search**.

### 6. Generate Answer with Citations
The system extracts citation markers such as:
```
[1], [3], [7]
```
Using these markers, a simple citation network graph is generated to visualize:
+ The uploaded paper
+ Its referenced works

### 7. Display Result
The system includes a basic recommendation module:
* Paper embeddings are stored in memory.
* Cosine similarity is used to rank similar papers.
* Top-K similar papers are suggested.

---

## Creative/Planned Feature
### Detect Imagery using CNNs
As a future enhancement, the system can be extended to include CNN-based visual analysis.

Unlike traditional literature review tools that rely only on textual information, this project incorporates a **CNN-based visual understanding module** to analyze figures, plots, and diagrams from research papers.

- Figures are extracted from PDFs and processed using Convolutional Neural Networks (CNNs)
- Visual embeddings are generated for charts, graphs, and architectural diagrams
- Figure embeddings are fused with textual embeddings during retrieval and answer generation

---

## System Flow
```
PDF → Text Extraction → Cleaning → Chunking → Embeddings → Storage
                                   ↓
User Query → Query Embedding → Cosine Similarity → Top Relevant Chunks
                                   ↓
Display Results + Citation Graph + Recommendations
```

---

## Tools and Technologies
| Purpose | Tool |
|-------|------|
| PDF to Text | PyPDF2 |
| Text Processing | Python |
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

## Summary
Scientific Literature Explorer demonstrates how embedding-based semantic search can improve academic paper exploration.  
It is useful for students and researchers who want faster and more intelligent access to research content.
