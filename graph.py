from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes import echo_node

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("echo", echo_node)

    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)

    return builder.compile()