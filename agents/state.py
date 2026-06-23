from typing import TypedDict, List


class AgentState(TypedDict):

    question: str
    search_query: str

    retrieved_docs: List[dict]

    context: str

    answer: str

    sources: List[str]