# AI Document Question Answering & Voice Assistant System

## Overview

This project is a Retrieval-Augmented Generation (RAG) based Document Question Answering and Voice Assistant System developed using FastAPI and Python.

The system allows users to upload documents, generate vector embeddings, store them in ChromaDB, and ask questions through text or voice. Responses are generated using Google Gemini and are grounded in the uploaded document content.

The application also supports conversational memory, enabling follow-up questions within the same chat session.

---

## Features

### Document Intelligence

- Document ingestion from JSON datasets
- Semantic search using vector embeddings
- ChromaDB vector storage
- Context-aware retrieval
- Source tracking

### AI Question Answering

- Retrieval-Augmented Generation (RAG)
- Gemini-powered answer generation
- Answers restricted to uploaded document content
- Context-based response generation

### Conversational Memory

- Session-based chat memory
- Follow-up question support
- Context-aware retrieval using conversation history
- Browser session persistence using Session ID

Example:

```text
User:
How often should the machine be cleaned?

Assistant:
The machine should be cleaned daily.

User:
What happens if I skip it?

Assistant:
Understands that "it" refers to machine cleaning.
```

### Voice Assistant

- Speech-to-Text input
- Text-to-Speech responses
- Voice-based document querying
- Browser microphone support

### User Interface

- Chat-based web interface
- Voice interaction
- Real-time answer display
- Session-aware conversations

---

## Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI & RAG

- Google Gemini
- SentenceTransformers
- ChromaDB

### Frontend

- HTML
- CSS
- JavaScript
- Web Speech API

### Environment Management

- python-dotenv

---

## Architecture

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

### Conversational RAG Pipeline

```text
User Question
      |
      V
Session Memory
      |
      V
Conversation-Aware Query
      |
      V
Embedding Generation
      |
      V
ChromaDB Retrieval
      |
      V
Context Construction
      |
      V
Gemini LLM
      |
      V
Answer Generation
      |
      V
Memory Update
```

### Voice Assistant Pipeline

```text
Voice Input
      |
      V
Speech-to-Text
      |
      V
Question Processing
      |
      V
Conversational RAG
      |
      V
Answer Generation
      |
      V
Text-to-Speech
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

---

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

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

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

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

Voice Assistant UI:

```text
http://127.0.0.1:8000/voice-ui
```

---

## API Endpoints

### Home

```http
GET /
```

Response:

```json
{
  "message": "AI Document QA API Running"
}
```

---

### Upload Documents

```http
POST /upload
```

Response:

```json
{
  "status": "success",
  "message": "Documents uploaded successfully",
  "total_documents": 50
}
```

---

### Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "How often should the machine be cleaned?",
  "session_id": "user-session-id"
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

---

### Voice Assistant Interface

```http
GET /voice-ui
```

Features:

- Text Questions
- Voice Questions
- Voice Responses
- Session Memory
- Context-Aware Follow-up Questions

---

## Conversational Memory

The system maintains session-specific memory using browser-generated session IDs.

Memory is used for:

- Follow-up questions
- Context understanding
- Conversation continuity
- Retrieval enhancement

Example:

```text
Question 1:
How often should the machine be cleaned?

Question 2:
What happens if I skip it?
```

The system understands that "it" refers to machine cleaning.

---

## Similarity Search

The application uses:

- SentenceTransformers for embedding generation
- ChromaDB for vector storage
- Dense vector retrieval
- Top-K semantic search
- Conversation-aware retrieval

---

## Security

- API keys stored using environment variables
- No hardcoded credentials
- CORS support enabled

---

## Future Improvements

- Streaming Responses
- PDF Upload Support
- DOCX Upload Support
- OCR Support
- Multi-language Support
- SQLite Persistent Memory
- User Authentication
- Docker Deployment
- AWS Deployment
- Hybrid Search (BM25 + Vector Search)
- LangGraph Multi-Agent Workflow
- RAG Evaluation Metrics (RAGAS)

---

## Author

Developed using FastAPI, ChromaDB, SentenceTransformers, and Google Gemini to build a Conversational RAG-based Document Question Answering and Voice Assistant System.