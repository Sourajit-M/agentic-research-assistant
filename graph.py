from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes import planner_node, researcher_node, indexer_node

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("planner", planner_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("indexer", indexer_node)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "indexer")
    builder.add_edge("indexer", END)

    return builder.compile()