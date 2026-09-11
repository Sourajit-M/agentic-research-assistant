from graph import build_graph
from rag_store import retrieve

graph = build_graph()

result = graph.invoke({
    "query": "What are the trade-offs between RAG and long-context LLMs in 2026?",
    "sub_questions": [],
    "search_results": {},
    "response": "",
})

print("\n--- Test retrieval ---")
for hit in retrieve("cost of running RAG systems", top_k=3):
    print(f"[{hit['score']:.3f}] {hit['title']} — {hit['text'][:80]}...")