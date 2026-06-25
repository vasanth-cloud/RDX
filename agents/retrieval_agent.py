import time

from agents.state import AgentState

from services.bm25_store import BM25Store
from services.hybrid_search import HybridSearch
from services.parser import load_json
from services.agent_monitor import log_agent

documents = load_json("uploads/all_documents.json")

bm25_store = BM25Store()
bm25_store.build(documents)

hybrid_search = HybridSearch(
    bm25_store
)


def retrieval_agent(state: AgentState):

    start = time.time()

    try:

        print("\n[RETRIEVAL AGENT]")

        results = hybrid_search.search(
            state["search_query"]
        )

        state["retrieved_docs"] = results

        state["context"] = "\n\n".join(
            [
                doc["text"]
                for doc in results
            ]
        )

        state["sources"] = []

        for doc in results:

            if doc["source"] not in state["sources"]:

                state["sources"].append(
                    doc["source"]
                )

        execution_time = (
            time.time() - start
        )

        print(
            f"Retrieved {len(results)} documents"
        )

        print(
            f"Retrieval Agent Time: {execution_time:.2f}s"
        )

        log_agent(
            "retrieval_agent",
            execution_time,
            "success"
        )

        return state

    except Exception as e:

        execution_time = (
            time.time() - start
        )

        log_agent(
            "retrieval_agent",
            execution_time,
            "failed"
        )

        print(
            f"Retrieval Agent Error: {e}"
        )

        raise