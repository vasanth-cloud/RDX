# AI Document Question Answering System

## Overview

This project is a Retrieval-Augmented Generation (RAG) based document question-answering system developed using FastAPI and Python.

The system allows users to upload a document dataset, stores document embeddings in ChromaDB, and answers questions based only on the uploaded document content.

---

## Technologies Used

- Python
- FastAPI
- ChromaDB
- SentenceTransformers
- Google Gemini API
- Pydantic
- python-dotenv
- Uvicorn

---

## Architecture

Document Upload

JSON Document
        |
        V
Document Parsing
        |
        V
Generate Embeddings
        |
        V
Store in ChromaDB

Question Answering

User Question
        |
        V
Generate Query Embedding
        |
        V
Similarity Search (Top-K)
        |
        V
Retrieve Relevant Documents
        |
        V
Gemini LLM
        |
        V
Return Answer + Sources

---

## Project Structure

```

RDX/
│
├── app.py
├── .env
├── requirements.txt
│
├── uploads/
│   └── all_documents.json
│
├── chroma_db/
│
├── services/
│   ├── parser.py
│   ├── embeddings.py
│   └── vector_store.py
│
└── models/
└── schemas.py

```

---

## Installation

### Create Virtual Environment

Windows

```

python -m venv venv
venv\Scripts\activate

```

---

### Install Dependencies

```

pip install -r requirements.txt

```

---

### Create .env File

```

GEMINI_API_KEY=your_api_key

```

---

## Run the Application

```

uvicorn app:app --reload

```

Server URL:

```

http://127.0.0.1:8000

```

Swagger Documentation:

```

http://127.0.0.1:8000/docs

```

---

## API Endpoints

### Upload Documents

POST

```

/upload

```

Response

```json
{
    "status": "success",
    "message": "Documents uploaded successfully",
    "total_documents": 50
}
```

---

### Ask Question

POST

```

/ask

```

Request

```json
{
    "question": "How often should the machine be cleaned?"
}
```

Response

```json
{
    "answer": "The machine should be cleaned daily.",
    "sources": [
        "Machine Cleaning Guide"
    ]
}
```

---

## Features

- Upload document dataset
- Generate vector embeddings
- Store embeddings in ChromaDB
- Semantic similarity search
- Retrieval-Augmented Generation (RAG)
- Source document tracking
- API key protection using .env
- Swagger API documentation

---

## Similarity Search

This project uses:

- SentenceTransformers for embedding generation
- ChromaDB for vector storage
- Dense vector retrieval
- Top-K semantic similarity search

---

## Future Improvements

- PDF Upload Support
- DOCX Support
- Multiple Document Upload
- User Authentication
- Docker Deployment
- Hybrid Search (BM25 + Vector Search)
