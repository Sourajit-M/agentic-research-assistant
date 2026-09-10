from graph import build_graph

graph = build_graph()

result = graph.invoke({"query": "Reply with exactly one word: pong", "response": ""})
print(result["response"])