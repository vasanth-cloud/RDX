# AI Document Question Answering & Voice Assistant System

## Overview

This project is a Retrieval-Augmented Generation (RAG) based Document Question Answering and Voice Assistant System developed using FastAPI and Python.

The system allows users to upload a document dataset, store document embeddings in ChromaDB, and ask questions through either text or voice. Answers are generated using retrieved document context and Google Gemini, ensuring responses are grounded in the uploaded documents.

## Technologies Used

- Python
- FastAPI
- ChromaDB
- SentenceTransformers
- Google Gemini API
- Pydantic
- python-dotenv
- Uvicorn
- HTML
- CSS
- JavaScript
- Web Speech API

---

## System Architecture

### Document Ingestion Pipeline

```text
JSON Documents
      |
      V
Document Parsing
      |
      V
Generate Embeddings
      |
      V
Store in ChromaDB
```

### Question Answering Pipeline

```text
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
Generate Answer
      |
      V
Return Answer + Sources
```

### Voice Assistant Pipeline

```text
User Voice Input
      |
      V
Speech-to-Text
      |
      V
Question Submission
      |
      V
RAG Pipeline
      |
      V
Answer Generation
      |
      V
Display Response
      |
      V
Text-to-Speech Output
```

---

## Project Structure

```text
RDX/
│
├── app.py
├── requirements.txt
├── .env
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
├── models/
│   └── schemas.py
│
└── templates/
    └── voice.html
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

## Running the Application

```bash
uvicorn app:app --reload
```

Server URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

Voice Assistant Interface:

```text
http://127.0.0.1:8000/voice-ui
```

---

## API Endpoints

### Home Endpoint

**GET /**

Response:

```json
{
  "message": "AI Document QA API Running"
}
```

### Upload Documents

**POST /upload**

Response:

```json
{
  "status": "success",
  "message": "Documents uploaded successfully",
  "total_documents": 50
}
```

### Ask Question

**POST /ask**

Request:

```json
{
  "question": "How often should the machine be cleaned?"
}
```

Response:

```json
{
  "answer": "The machine should be cleaned daily.",
  "sources": [
    "Machine Cleaning Guide"
  ]
}
```

### Voice Assistant UI

**GET /voice-ui**

Provides a browser-based interface supporting:

- Text Questions
- Voice Questions
- AI Responses
- Source References
- Text-to-Speech Output

---

## Features

- Retrieval-Augmented Generation (RAG)
- Document Question Answering
- Semantic Search using Embeddings
- ChromaDB Vector Storage
- Google Gemini Integration
- Source Attribution
- Browser-Based Chat Interface
- Voice Input Support
- Voice Response Support
- FastAPI REST API
- Swagger Documentation
- Environment Variable Security

---

## Similarity Search

The system uses:

- SentenceTransformers for embedding generation
- ChromaDB for vector storage
- Dense vector retrieval
- Top-K semantic similarity search
- Context-aware answer generation

---

## User Interfaces

### Swagger API

```
http://127.0.0.1:8000/docs
```

### Voice Assistant UI

```
http://127.0.0.1:8000/voice-ui
```

Supports:

- Chat-based interaction
- Voice-based interaction
- AI-generated answers
- Source document tracking
- Speech synthesis responses

---

## Future Improvements

- PDF Upload Support
- DOCX Upload Support
- Multiple Document Upload
- User Authentication
- Docker Deployment
- Hybrid Search (BM25 + Vector Search)
- Streaming Responses
- Multi-Language Support
- Conversation Memory
- Mobile-Friendly UI

---

## Author

Developed using FastAPI, ChromaDB, SentenceTransformers, and Google Gemini to provide document-based question answering and voice-assisted interactions.