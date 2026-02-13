# System Architecture

Scientific Literature Explorer follows a modular, embedding based retrieval architecture designed for efficient academic paper analysis.
The system processes user uploaded PDFs and enables semantic search, citation visualization, and similarity based recommendations.

---

## High Level Architecture

<img src="../assets/system_achitecture.png" alt="High Level Architecture" width="400"/>

---

##  Pipeline
| S.No. | Operation | Process |
| --- | --- | --- |
| 1 | **PDF Upload** | User uploads a research paper (PDF) via Streamlit interface |
| 2 | **Text Extraction** | Text is extracted from the PDF using PyPDF2 |
| 3 | **Optional Compression** | If enabled, extracted text is sent to the ScaleDown API. The document is compressed while preserving technical meaning |
| 4 | **Text Chunking** | The full text is divided into meaningful chunks. Each chunk is approximately 800–1200 characters |
| 5 | **Embedding generation** | Each chunk is converted into a 768 dimensional vector using Sentence Transformers |
| 6 | **Vector storage** | Chunk embeddings are stored in the Vector Engine. Associated metadata (text + source) is stored alongside vectors |
| 7 | **User Query Processing** | The query is converted into an embedding. Cosine similarity is computed between the query vector and stored chunk vectors |
| 8 | **Semantic Retrieval** | Top-K most similar chunks are retrieved and relevant sections are displayed with highlighted matching terms |
| 9 | **Citation Graph Generation** | Extracted citation markers are used to build a NetworkX graph. Extracted citation markers are used to build a NetworkX graph |
| 10 | **Recommendation Generation** | A paper level embedding is computed (mean of chunk embeddings). Top recommendations are displayed |
