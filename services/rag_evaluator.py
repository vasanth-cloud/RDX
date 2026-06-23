import time


def evaluate_rag(question, answer, contexts):

    return {
        "retrieved_docs": len(contexts),
        "context_length": sum(
            len(c) for c in contexts
        ),
        "answer_length": len(answer),
        "status": "success"
    }