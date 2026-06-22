from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import google.generativeai as genai
import os
from fastapi.responses import StreamingResponse

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

chat_memory = {}

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
# -----------------------------
# Ask Question
# -----------------------------
@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        # Get chat history
        history = chat_memory.get(
            request.session_id,
            []
        )

        # Build conversational search query
        search_query = request.question

        if history:
            search_query = (
                "\n".join(history[-4:])
                + "\nUser: "
                + request.question
            )

        # Question Embedding
        query_embedding = embedding_model.encode(
            search_query
        ).tolist()

        # Similarity Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        retrieved_docs = results["documents"][0]

        if not retrieved_docs:

            return {
                "answer": "There is not enough information in the uploaded documents.",
                "sources": []
            }

        context = "\n\n".join(
            retrieved_docs
        )

        conversation_context = "\n".join(
            history[-10:]
        )

        prompt = f"""
Previous Conversation:
{conversation_context}

You are an AI assistant for textile printing machines.

Rules:
1. Answer ONLY using the provided context.
2. Use previous conversation only to understand references such as:
   - it
   - that
   - this machine
   - previous topic
3. Do NOT use outside knowledge.
4. If the answer is not available in the context, reply exactly:
"There is not enough information in the uploaded documents."

Context:
{context}

Question:
{request.question}

Answer:
"""

        response = model.generate_content(
            prompt
        )

        answer = response.text.strip()

        # Save conversation
        history.append(
            f"User: {request.question}"
        )

        history.append(
            f"Assistant: {answer}"
        )

        chat_memory[
            request.session_id
        ] = history

        if "There is not enough information" in answer:

            return {
                "answer": answer,
                "sources": []
            }

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

@app.post("/ask-stream")
async def ask_stream(request: QuestionRequest):

    try:

        history = chat_memory.get(
            request.session_id,
            []
        )

        search_query = request.question

        if history:
            search_query = (
                "\n".join(history[-4:])
                + "\nUser: "
                + request.question
            )

        query_embedding = embedding_model.encode(
            search_query
        ).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        retrieved_docs = results["documents"][0]

        if not retrieved_docs:

            async def no_data():
                yield "There is not enough information in the uploaded documents."

            return StreamingResponse(
                no_data(),
                media_type="text/plain"
            )

        context = "\n\n".join(
            retrieved_docs
        )

        conversation_context = "\n".join(
            history[-10:]
        )

        prompt = f"""
Previous Conversation:
{conversation_context}

You are an AI assistant for textile printing machines.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.

Context:
{context}

Question:
{request.question}

Answer:
"""

        async def generate():

            full_answer = ""

            response = model.generate_content(
                prompt,
                stream=True
            )

            for chunk in response:

                if chunk.text:

                    full_answer += chunk.text

                    yield chunk.text

            history.append(
                f"User: {request.question}"
            )

            history.append(
                f"Assistant: {full_answer}"
            )

            chat_memory[
                request.session_id
            ] = history

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )

    except Exception as e:

        async def error():
            yield f"Error: {str(e)}"

        return StreamingResponse(
            error(),
            media_type="text/plain"
        )