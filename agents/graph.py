from langgraph.graph import StateGraph
from langgraph.graph import END

from agents.state import AgentState

from agents.query_agent import query_agent
from agents.retrieval_agent import retrieval_agent
from agents.validation_agent import validation_agent
from agents.answer_agent import answer_agent


workflow = StateGraph(
    AgentState
)

workflow.add_node(
    "query_agent",
    query_agent
)

workflow.add_node(
    "retrieval_agent",
    retrieval_agent
)

workflow.add_node(
    "validation_agent",
    validation_agent
)

workflow.add_node(
    "answer_agent",
    answer_agent
)

workflow.set_entry_point(
    "query_agent"
)

workflow.add_edge(
    "query_agent",
    "retrieval_agent"
)

workflow.add_edge(
    "retrieval_agent",
    "validation_agent"
)

workflow.add_edge(
    "validation_agent",
    "answer_agent"
)

workflow.add_edge(
    "answer_agent",
    END
)

graph = workflow.compile()