from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import google.generativeai as genai
import os
from pathlib import Path
from fastapi.responses import StreamingResponse
from agents.graph import graph
from models.schemas import QuestionRequest
from services.parser import load_json
from services.bm25_store import BM25Store
from services.hybrid_search import HybridSearch
from services.rag_evaluator import evaluate_rag
from services.embeddings import store_documents
from services.vector_store import (
    collection,
    embedding_model
)

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_FILE = BASE_DIR / "uploads" / "all_documents.json"
VOICE_TEMPLATE = BASE_DIR / "templates" / "voice.html"
CHAT_TEMPLATE = BASE_DIR / "templates" / "chat.html"

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
bm25_store = BM25Store()
hybrid_search = HybridSearch(bm25_store)

try:
    documents = load_json(
        DOCUMENTS_FILE
    )

    bm25_store.build(documents)

    print(
        f"BM25 initialized with {len(documents)} documents"
    )

except Exception as e:

    print(
        f"BM25 initialization failed: {e}"
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
@app.get("/", response_class=HTMLResponse)
def home():

    with open(
        CHAT_TEMPLATE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


@app.get("/health")
def health():

    return {
        "message": "AI Document QA API Running"
    }

# -----------------------------
# Voice UI Endpoint
# -----------------------------
@app.get("/voice-ui", response_class=HTMLResponse)
def voice_ui():

    with open(
        VOICE_TEMPLATE,
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
            DOCUMENTS_FILE
        )

        # Always build BM25
        bm25_store.build(documents)

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

        print("\n================================")
        print("LANGGRAPH WORKFLOW STARTED")
        print("================================")

        result = graph.invoke(
            {
                "question": request.question,
                "search_query": search_query,
                "retrieved_docs": [],
                "context": "",
                "answer": "",
                "sources": []
            }
        )

        answer = result["answer"]

        sources = result["sources"]

        print("\n================================")
        print("LANGGRAPH WORKFLOW COMPLETED")
        print("================================")

        # -------------------------
        # RAG EVALUATION
        # -------------------------

        try:

            evaluation = evaluate_rag(
                question=request.question,
                answer=answer,
                contexts=[
                    doc["text"]
                    for doc in result["retrieved_docs"]
                ]
            )

            print("\n========== RAG EVALUATION ==========")

            print(
                f"Retrieved Docs: {evaluation['retrieved_docs']}"
            )

            print(
                f"Context Length: {evaluation['context_length']}"
            )

            print(
                f"Answer Length: {evaluation['answer_length']}"
            )

            print(
                f"Status: {evaluation['status']}"
            )

            print("====================================")

        except Exception as eval_error:

            print(
                f"RAG Evaluation Error: {eval_error}"
            )

            evaluation = None

        # -------------------------
        # SAVE MEMORY
        # -------------------------

        history.append(
            f"User: {request.question}"
        )

        history.append(
            f"Assistant: {answer}"
        )

        chat_memory[
            request.session_id
        ] = history

        # -------------------------
        # RESPONSE
        # -------------------------

        return {
            "answer": answer,
            "sources": sources,
            "evaluation": evaluation
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

        async def generate():

            print("\n================================")
            print("LANGGRAPH STREAM WORKFLOW STARTED")
            print("================================")

            result = graph.invoke(
                {
                    "question": request.question,
                    "search_query": search_query,
                    "retrieved_docs": [],
                    "context": "",
                    "answer": "",
                    "sources": []
                }
            )

            answer = result["answer"]

            print("\n================================")
            print("LANGGRAPH STREAM WORKFLOW COMPLETED")
            print("================================")

            history.append(
                f"User: {request.question}"
            )

            history.append(
                f"Assistant: {answer}"
            )

            chat_memory[
                request.session_id
            ] = history

            words = answer.split()

            for word in words:

                yield word + " "

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )

    except Exception as e:

        error_message = str(e)

        async def error():

            yield f"Error: {error_message}"

        return StreamingResponse(
            error(),
            media_type="text/plain"
        )
