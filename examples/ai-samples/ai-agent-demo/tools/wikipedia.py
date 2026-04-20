"""
Wikipedia search tool (no API key required)
"""

import json


def search_wikipedia(query: str, sentences: int = 3) -> str:
    """
    Search Wikipedia and return article summary.

    Args:
        query: The topic or article title to search for
        sentences: Number of sentences in summary

    Returns:
        JSON string with Wikipedia article summary
    """
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia('ToolCallingChatUI/1.0', 'en')
        page = wiki.page(query)

        if not page.exists():
            return json.dumps({"error": f"No Wikipedia page found for '{query}'"})

        summary = page.summary[:500] + "..." if len(page.summary) > 500 else page.summary

        return json.dumps({
            "query": query,
            "title": page.title,
            "summary": summary,
            "url": page.fullurl
        })
    except Exception as e:
        return json.dumps({"error": f"Wikipedia search failed: {str(e)}"})
