from graph import build_graph

graph = build_graph()

result = graph.invoke({
    "query": "What are the trade-offs between RAG and long-context LLMs in 2026?",
    "sub_questions": [],
    "search_results": {},
    "response": "",
})

for sub_question, results in result["search_results"].items():
    print(f"\n=== {sub_question} ===")
    for r in results:
        print(f"- {r['title']} ({r['url']})")