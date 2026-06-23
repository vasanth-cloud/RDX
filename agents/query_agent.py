import time

from agents.state import AgentState
from services.agent_monitor import log_agent


def query_agent(
    state: AgentState
):

    start = time.time()

    try:

        print("\n[QUERY AGENT]")

        state["search_query"] = (
            state["question"]
        )

        execution_time = (
            time.time() - start
        )

        print(
            f"Query Agent Time: {execution_time:.2f}s"
        )

        log_agent(
            "query_agent",
            execution_time,
            "success"
        )

        return state

    except Exception:

        execution_time = (
            time.time() - start
        )

        log_agent(
            "query_agent",
            execution_time,
            "failed"
        )

        raise