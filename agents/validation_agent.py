import time

from agents.state import AgentState
from services.agent_monitor import log_agent


def validation_agent(
    state: AgentState
):

    start = time.time()

    try:

        print("\n[VALIDATION AGENT]")

        if not state["retrieved_docs"]:

            state["answer"] = (
                "There is not enough information in the uploaded documents."
            )

        execution_time = (
            time.time() - start
        )

        print(
            f"Validation Agent Time: {execution_time:.2f}s"
        )

        log_agent(
            "validation_agent",
            execution_time,
            "success"
        )

        return state

    except Exception:

        execution_time = (
            time.time() - start
        )

        log_agent(
            "validation_agent",
            execution_time,
            "failed"
        )

        raise