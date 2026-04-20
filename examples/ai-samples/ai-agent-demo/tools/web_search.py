"""
Web search tool using DuckDuckGo (no API key required)
"""

import json

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


def web_search(query: str, max_results: int = 3) -> str:
    """
    Perform live web search using DuckDuckGo (no API key required).

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        JSON string with search results
    """
    if not DDGS_AVAILABLE:
        return json.dumps({
            "error": "ddgs library not installed",
            "message": "Install with: pip install ddgs"
        })

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='us-en', safesearch='on', max_results=max_results))

        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

        return json.dumps({
            "query": query,
            "results": formatted_results,
            "total_results": len(formatted_results)
        })
    except Exception as e:
        return json.dumps({
            "error": f"Search failed: {str(e)}",
            "query": query
        })
