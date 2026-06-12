from fastapi import FastAPI
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
# Upload Endpoint
# -----------------------------
@app.post("/upload")
def upload_document():

    try:
        documents = load_json(r"uploads\all_documents.json")

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
# Ask Endpoint
# -----------------------------
@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        # Generate embedding for question
        query_embedding = embedding_model.encode(
            request.question
        ).tolist()

        # Search Vector Database
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        # Get retrieved documents
        retrieved_docs = results["documents"][0]

        # Build context
        context = "\n\n".join(retrieved_docs)

        # Prompt
        prompt = f"""
You are an AI assistant for textile printing machines.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. If the answer is not available, reply exactly:
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

        # If no information found
        if "There is not enough information" in answer:

            return {
                "answer": answer,
                "sources": []
            }

        # Collect source names
        sources = []

        for item in results["metadatas"][0]:
            sources.append(
                item["source"]
            )

        # Return response
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
# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def home():

    return {
        "message": "AI Document QA API Running"
    }