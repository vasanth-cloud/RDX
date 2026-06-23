# AI Document Question Answering & Voice Assistant System

## Overview

This project is a Retrieval-Augmented Generation (RAG) based AI Document Question Answering and Voice Assistant System built using FastAPI, ChromaDB, SentenceTransformers, Google Gemini, and LangGraph.

The system allows users to upload documents, perform Hybrid Search using BM25 and Vector Search, ask questions through text or voice, and receive context-aware responses grounded in the uploaded documents.

The application supports Conversational Memory, Streaming Responses, Multi-Agent Workflows, Agent Monitoring, and Basic RAG Evaluation.

---

# Features

## Document Intelligence

- JSON Document Ingestion
- Document Parsing
- Semantic Search
- ChromaDB Vector Storage
- Source Tracking

---

## Hybrid Search

Combines:

- BM25 Keyword Search
- ChromaDB Vector Search

### Benefits

- Better retrieval accuracy
- Handles exact keyword matches
- Handles semantic similarity
- Improved context retrieval

### Workflow

```text
User Query
     |
     +----> BM25 Search
     |
     +----> Vector Search
               |
               V
      Combined Results
```

---

## AI Question Answering

- Retrieval-Augmented Generation (RAG)
- Gemini-Powered Answers
- Context-Aware Responses
- Source Citation Support
- Grounded Answer Generation

---

## Conversational Memory

Supports:

- Session-Based Chat Memory
- Follow-Up Questions
- Context Awareness
- Browser Session Persistence

### Example

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

---

## Voice Assistant

Supports:

- Speech-to-Text
- Text-to-Speech
- Voice Questions
- Voice Responses
- Browser Microphone Integration

---

## Streaming Responses

Real-time answer streaming using FastAPI StreamingResponse.

### Workflow

```text
Gemini Stream
      |
      V
FastAPI StreamingResponse
      |
      V
Browser UI
```

---

# LangGraph Multi-Agent Workflow

The system uses LangGraph for agent orchestration.

### Workflow

```text
User Question
      |
      V
Query Agent
      |
      V
Retrieval Agent
      |
      V
Validation Agent
      |
      V
Answer Agent
      |
      V
Final Response
```

---

## Query Agent

Responsibilities:

- Process User Question
- Handle Conversation Context
- Prepare Search Query

---

## Retrieval Agent

Responsibilities:

- Perform Hybrid Search
- Retrieve Relevant Documents
- Build Context
- Track Sources

Uses:

- BM25
- ChromaDB
- SentenceTransformers

---

## Validation Agent

Responsibilities:

- Validate Retrieved Documents
- Check Context Availability
- Ensure Retrieval Success

---

## Answer Agent

Responsibilities:

- Generate Final Answer
- Use Gemini LLM
- Restrict Answers to Context
- Prevent Unsupported Responses

---

# Agent Monitoring

Tracks execution time of each agent.

### Example Logs

```text
[QUERY AGENT]
Time: 0.01s

[RETRIEVAL AGENT]
Time: 0.22s

[VALIDATION AGENT]
Time: 0.00s

[ANSWER AGENT]
Time: 2.64s
```

### Benefits

- Performance Monitoring
- Workflow Debugging
- Production Observability
- Agent-Level Analysis

---

# Basic RAG Evaluation

Evaluates retrieval and answer generation quality.

### Metrics

- Retrieved Documents Count
- Context Length
- Answer Length
- Processing Status

### Example

```json
{
  "retrieved_docs": 5,
  "context_length": 3646,
  "answer_length": 110,
  "status": "success"
}
```

---

# Technologies Used

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

## AI & RAG

- Google Gemini
- SentenceTransformers
- ChromaDB
- BM25
- LangGraph

## Frontend

- HTML
- CSS
- JavaScript
- Web Speech API

## Environment Management

- python-dotenv

---

# Architecture

## Document Ingestion Pipeline

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

---

## Hybrid Retrieval Pipeline

```text
User Question
      |
      +----> BM25 Search
      |
      +----> Vector Search
      |
      V
Merged Results
      |
      V
Context Construction
```

---

## Multi-Agent RAG Pipeline

```text
User Question
      |
      V
Query Agent
      |
      V
Retrieval Agent
      |
      V
Validation Agent
      |
      V
Answer Agent
      |
      V
Gemini Response
```

---

## Voice Assistant Pipeline

```text
Voice Input
      |
      V
Speech-to-Text
      |
      V
Hybrid RAG
      |
      V
Gemini
      |
      V
Text-to-Speech
```

---

# Project Structure

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
│   ├── vector_store.py
│   ├── bm25_store.py
│   ├── hybrid_search.py
│   └── rag_evaluator.py
│
├── agents/
│   ├── state.py
│   ├── graph.py
│   ├── query_agent.py
│   ├── retrieval_agent.py
│   ├── validation_agent.py
│   └── answer_agent.py
│
├── models/
│   └── schemas.py
│
└── templates/
    └── voice.html
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

# Running the Application

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

# API Endpoints

## Home

```http
GET /
```

---

## Upload Documents

```http
POST /upload
```

---

## Ask Question

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

---

## Streaming Question Answering

```http
POST /ask-stream
```

Features:

- Streaming Responses
- LangGraph Workflow
- Hybrid Search
- Conversational Memory

---

## Voice Assistant Interface

```http
GET /voice-ui
```

Supports:

- Voice Questions
- Voice Responses
- Session Memory
- Follow-Up Questions

---

# Current Capabilities

✅ ChromaDB Vector Search

✅ BM25 Search

✅ Hybrid Search

✅ Conversational Memory

✅ Voice Assistant

✅ Streaming Responses

✅ LangGraph Multi-Agent Workflow

✅ Agent Monitoring

✅ Basic RAG Evaluation

---

# Future Improvements

- Hallucination Detection Agent
- Query Rewriter Agent
- SQLite Persistent Memory
- PDF Upload Support
- DOCX Upload Support
- OCR Support
- Multi-Language Support
- AgentOps Monitoring
- Docker Deployment
- AWS Deployment
- RAGAS Evaluation
- User Authentication

---

# Author

Developed using FastAPI, ChromaDB, BM25, SentenceTransformers, Google Gemini, and LangGraph to build a Hybrid Search Multi-Agent Conversational RAG System with Voice Assistant capabilities.