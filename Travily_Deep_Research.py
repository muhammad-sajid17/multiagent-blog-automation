import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def deep_research_topic(topic: str) -> list:
    """
    Runs a deep Tavily search for a specific topic, fetching raw web content.
    Returns a list of articles with their raw text.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing from environment variables.")

    client = TavilyClient(api_key=api_key)

    # Matching the ReadMe constraints: 1 month old, max 5 results, raw content enabled
    response = client.search(
        query=topic,
        search_depth="advanced",
        days=30,
        max_results=5,
        include_raw_content=True
    )

    return response.get("results", [])