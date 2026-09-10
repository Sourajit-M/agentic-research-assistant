import time
from ddgs import DDGS
from state import SearchResult

def web_search(query: str, max_results: int = 5, retries: int = 2) -> list[SearchResult]:
    """Search the web for a query. Returns an empty list on repeated failure
    rather than raising, so one bad sub-question doesn't kill the whole run."""
    for attempt in range(retries + 1):
        try:
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(query, max_results=max_results))
            return [
                SearchResult(
                    title=r.get("title", ""),
                    url=r.get("href", ""),
                    snippet=r.get("body", ""),
                )
                for r in raw_results
            ]
        except Exception as e:
            if attempt < retries:
                time.sleep(2 ** attempt)  # 1s, then 2s backoff
            else:
                print(f"Search failed for '{query}' after {retries + 1} attempts: {e}")
                return []