# API Documentation

The Scientific Literature Explorer integrates an external API for optional document compression and exposes internal processing modules that handle semantic search, citation extraction, and recommendations.

---

## 1. External API Integration
   
   The system optionally uses the ScaleDown API to compress extracted research paper text before embedding.

### Purpose
- Reduce document size
- Improve embedding efficiency
- Lower processing latency
- Preserve technical meaning

### Endpoint
``` python
url = 'https://api.scaledown.xyz/compress/raw/'
```

### Authentication
The external API requires an API key passed via request headers.
``` python
headers = {
    'x-api-key': 'YOUR_API_KEY',
    'Content-Type': 'application/json'
}
```

The key is loaded securely from a ```.env``` file and is not committed to version control.
``` python
SCALEDOWN_API_KEY=your_api_key_here
```

### Request
Separate your context from your main prompt and set the compression rate to "auto" for the best results.
``` python
payload = {
    "context": "Context about your specific topic or instructions here",
    "prompt": "Your actual query or question here",
    "scaledown": {
        "rate": "auto" # Automatic compression rate optimization
    }
}
```

### Response
The API response provides the compressed prompt along with useful metadata about the operation.
``` python
{
  "compressed_prompt": "Your optimized context here...",
  "original_prompt_tokens": 150,
  "compressed_prompt_tokens": 65,
  "successful": true,
  "latency_ms": 2341,
  "request_metadata": {
    "compression_time_ms": 2341,
    "compression_rate": "auto",
    "prompt_length": 425,
    "compressed_prompt_length": 189
  }
}
```

--- 

## 2. Internal Modules
The system uses modular internal components:

* <b> Text Encoder </b> – Generates embeddings using Sentence Transformers
* <b> Vector Engine </b> – Stores embeddings and performs similarity search
* <b> Paper Compressor </b> – Extracts text and splits into chunks
* <b> Citation Graph </b> – Builds citation visualization using NetworkX
* <b> Recommender </b> – Provides similarity-based paper recommendations

--- 

## 3. Data Flow 
    PDF Upload
       ↓
    paper_compressor.extract_content()
       ↓
    (Optional) ScaleDown_client.compress_paper()
       ↓
    paper_compressor.split_into_chunks()
       ↓
    text_encoder.encode()
       ↓
    vector_engine.add_documents()
       ↓
    --------------------------------------
    User Query
       ↓
    text_encoder.encode()
       ↓
    vector_engine.search()
       ↓
    Display Results

---

## 4. Security
- API keys are stored in `.env`
- `.env` is excluded via `.gitignore`

---

# Summary

The system integrates:

* One external compression API (ScaleDown)
* Modular internal processing APIs
* Embedding based retrieval
* Graph based visualization
