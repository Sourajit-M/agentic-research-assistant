from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes import planner_node

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("planner", planner_node)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", END)

    return builder.compile()