import os
import time

import google.generativeai as genai

from agents.state import AgentState
from services.agent_monitor import log_agent

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def answer_agent(state: AgentState):

    start = time.time()

    try:

        print("\n==============================")
        print("[ANSWER AGENT STARTED]")
        print("==============================")

        if state.get("answer"):
            return state

        prompt = f"""
You are an AI assistant for textile printing machines.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If answer is unavailable reply exactly:
There is not enough information in the uploaded documents.

Context:
{state["context"]}

Question:
{state["question"]}

Answer:
"""

        print(
            "Generating response using Gemini..."
        )

        response = model.generate_content(
            prompt
        )

        state["answer"] = (
            response.text.strip()
        )

        print("\nGenerated Answer:")
        print(state["answer"])

        print(
            f"\nContext Length: {len(state['context'])} characters"
        )

        execution_time = (
            time.time() - start
        )

        print(
            f"Answer Agent Time: {execution_time:.2f}s"
        )

        log_agent(
            "answer_agent",
            execution_time,
            "success"
        )

        print("==============================")
        print("[ANSWER AGENT COMPLETED]")
        print("==============================")

        return state

    except Exception as e:

        execution_time = (
            time.time() - start
        )

        log_agent(
            "answer_agent",
            execution_time,
            "failed"
        )

        print(
            f"Answer Agent Error: {e}"
        )

        raise