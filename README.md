# Scientific Literature Explorer

## Description
The Scientific Literature Explorer is a deep research Q&A system that helps users understand research papers quickly.
Instead of reading long PDFs, users can upload papers, ask questions, and get their respective answers along with proper citations.

---

## Project Objective
It allows users to:
- Upload research papers (PDFs)
- Ask questions related to those papers
- Get answers with references to the original papers

---

## How it works
### 1. Upload papers
Users upload research papers in PDF format.

The system:
- Reads the PDF
- Extracts the text content

**Tools used:**
- `pdfplumber`

### 2. Split Text into Chunks
Research papers are very long, so the text is split into smaller parts.

- Each chunk is about 300–500 words
- Each chunk keeps details like:
  - Paper title
  - Authors
  - Section name

This helps in tracking where the information came from.

### 3. Create Embeddings
Each text chunk is converted into numbers called embeddings.

- These embeddings represent the meaning of the text
- Similar text has similar embeddings

**Tools used:**
- ScaleDownAI Embeddings
- Sentence Transformers

### 4. Store Data
All embeddings and related information are stored in a vector database.

**Tools used:**
- `FAISS`

Stored data includes:
- Embeddings
- Text chunks
- Citation details

### 5. Ask a Question
When a user asks a question:
- The question is also converted into an embedding
- The system finds the most relevant text chunks

This method is called **semantic search**.

### 6. Generate Answer with Citations
The system sends:
- The user question
- The relevant chunks

to a language model.

The model:
- Generates an answer
- Uses only the retrieved text
- Mentions the paper sources

This approach is known as **Retrieval-Augmented Generation (RAG)**.

### 7. Display Result
The final output shows:
- A short and clear answer
- Bullet points if needed
- Paper title, authors, and year as citation

---

## Creative/Unique Feature
### Detect Imagery using CNNs
Unlike traditional literature review tools that rely only on textual information, this project incorporates a **CNN-based visual understanding module** to analyze figures, plots, and diagrams from research papers.

- Figures are extracted from PDFs and processed using Convolutional Neural Networks (CNNs)
- Visual embeddings are generated for charts, graphs, and architectural diagrams
- Figure embeddings are fused with textual embeddings during retrieval and answer generation

---

## System Flow
```
PDFs → Text → Chunks → Embeddings → Vector Database
↓
User Question → Embedding → Search → LLM → Answer + Citations
```

---

## Tools and Technologies
| Purpose | Tool |
|-------|------|
| PDF to text | pdfplumber |
| Embeddings | ScaleDownAI / Sentence Transformers |
| Vector storage | FAISS |
| Language model | Ollama |
| Backend | FastAPI |
| Frontend | Streamlit |

---

## Neural Networks
This project uses **pre-trained neural networks** for:
- Creating embeddings
- Generating answers

---

## Summary
Scientific Literature Explorer makes academic research easier by combining semantic search and citation-based question answering.  
It is useful for students, researchers, and academic projects where quick and reliable understanding of papers is required.
