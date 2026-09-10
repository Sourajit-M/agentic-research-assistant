from graph import build_graph

graph = build_graph()

result = graph.invoke({
    "query": "What are the evaluation metrics for a RAG application in 2026?",
    "sub_questions": [],
    "response": "",
})

for i, sq in enumerate(result["sub_questions"], 1):
    print(f"{i}. {sq}")