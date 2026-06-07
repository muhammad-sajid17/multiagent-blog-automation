import asyncio
from Travily_Deep_Research import deep_research_topic
from Section_Writer_Agent import write_section


async def process_single_topic(topic: str) -> str:
    """
    A sequential pipeline for a single topic: Research -> Write.
    We run the synchronous functions in an executor so they don't block the async loop.
    """
    loop = asyncio.get_running_loop()

    print(f"   -> 🔎 Deep researching: '{topic}'...")
    research = await loop.run_in_executor(None, deep_research_topic, topic)

    print(f"   -> ✍️ Writing section for: '{topic}'...")
    section = await loop.run_in_executor(None, write_section, topic, research)

    return section


async def generate_all_sections(topics: list[str]) -> list[str]:
    """
    The 'Split Out' orchestrator. Takes the list of topics and processes them in parallel.
    Returns a list of the finalized markdown sections.
    """
    print("\n[Split Out Node] Distributing topics for parallel processing...")

    # Create an async task for each topic
    tasks = [process_single_topic(topic) for topic in topics]

    # Execute all 3 tasks at the exact same time and gather the results
    sections = await asyncio.gather(*tasks)

    return sections

