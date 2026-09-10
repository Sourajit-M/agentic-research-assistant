from typing import TypedDict

class SearchResult(TypedDict):
    title: str
    url: str
    snippet: str

class GraphState(TypedDict):
    query: str
    sub_questions: list[str]
    search_results: dict[str, list[SearchResult]]
    response: str