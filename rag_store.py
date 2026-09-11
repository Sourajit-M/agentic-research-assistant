from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
COLLECTION_NAME = "research_snippets"

embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
qdrant = QdrantClient(":memory:")


def _reset_collection():
    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )


def index_search_results(search_results: dict) -> int:
    """Embeds every snippet and stores it fresh for this run. Returns count indexed."""
    _reset_collection()

    points = []
    point_id = 0
    for sub_question, results in search_results.items():
        for r in results:
            if not r["snippet"]:
                continue
            vector = embedder.encode(r["snippet"]).tolist()
            points.append(PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "sub_question": sub_question,
                    "title": r["title"],
                    "url": r["url"],
                    "text": r["snippet"],
                },
            ))
            point_id += 1

    if points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)


def retrieve(query_text: str, top_k: int = 5, sub_question: str | None = None) -> list[dict]:
    """Retrieve the most relevant chunks. Optionally filter to one sub-question's evidence pool."""
    query_filter = None
    if sub_question:
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        query_filter = Filter(
            must=[FieldCondition(key="sub_question", match=MatchValue(value=sub_question))]
        )

    hits = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=embedder.encode(query_text).tolist(),
        query_filter=query_filter,
        limit=top_k,
    ).points

    return [
        {"text": h.payload["text"], "title": h.payload["title"], "url": h.payload["url"], "score": h.score}
        for h in hits
    ]