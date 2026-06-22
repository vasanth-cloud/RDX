from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import google.generativeai as genai
import os

from models.schemas import QuestionRequest
from services.parser import load_json
from services.embeddings import store_documents
from services.vector_store import (
    collection,
    embedding_model
)

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="AI Document QA",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Home Endpoint
# -----------------------------
@app.get("/")
def home():

    return {
        "message": "AI Document QA API Running"
    }

# -----------------------------
# Voice UI Endpoint
# -----------------------------
@app.get("/voice-ui", response_class=HTMLResponse)
def voice_ui():

    with open(
        "templates/voice.html",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()
# -----------------------------
# Upload Documents
# -----------------------------
@app.post("/upload")
def upload_document():

    try:

        documents = load_json(
            r"uploads\all_documents.json"
        )

        # Avoid duplicate uploads
        if collection.count() > 0:

            return {
                "status": "success",
                "message": "Documents already uploaded",
                "total_documents": collection.count()
            }

        store_documents(documents)

        return {
            "status": "success",
            "message": "Documents uploaded successfully",
            "total_documents": len(documents)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# -----------------------------
# Ask Question
# -----------------------------
@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        # Question Embedding
        query_embedding = embedding_model.encode(
            request.question
        ).tolist()

        # Similarity Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        retrieved_docs = results["documents"][0]

        # No Results
        if not retrieved_docs:

            return {
                "answer": "There is not enough information in the uploaded documents.",
                "sources": []
            }

        # Build Context
        context = "\n\n".join(
            retrieved_docs
        )

        # Prompt
        prompt = f"""
You are an AI assistant for textile printing machines.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If the answer is not available in the context, reply exactly:
"There is not enough information in the uploaded documents."

Context:
{context}

Question:
{request.question}

Answer:
"""

        # Gemini Response
        response = model.generate_content(
            prompt
        )

        answer = response.text.strip()

        # Not Found Case
        if "There is not enough information" in answer:

            return {
                "answer": answer,
                "sources": []
            }

        # Sources
        sources = []

        for item in results["metadatas"][0]:

            if item["source"] not in sources:
                sources.append(
                    item["source"]
                )

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        return {
            "answer": "Error while processing request.",
            "sources": [],
            "error": str(e)
        }