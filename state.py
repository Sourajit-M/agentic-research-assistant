from typing import TypedDict

class GraphState(TypedDict):
    query: str
    sub_questions: list[str]
    response: str