import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def run_initial_research(niche: str) -> list:
    """
    Performs initial research on a given niche using Tavily API.
    Returns a list of search results containing titles, URLs, and summaries.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing from environment variables.")

    client = TavilyClient(api_key=api_key)

    # Executing search tailored for recent news matching the n8n blueprint
    response = client.search(
        query=niche,
        topic="news",
        days=7,
        max_results=3,
        include_raw_content=False
    )

    return response.get("results", [])