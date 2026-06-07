import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def write_section(topic: str, research_results: list) -> str:
    """
    Uses Gemini to write a standalone newsletter section based on the deep research.
    """
    # Using 'flash' to safely bypass the strict free-tier rate limits of 'pro'
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        max_retries=2
    )

    system_prompt = """You are a professional newsletter section writer. Write ONE self-contained section (350–500 words) for small-business leaders.

Requirements:
- Start with an H2 heading matching the Topic (e.g., "## {topic}").
- Synthesize facts from the provided sources (don't invent).
- Inline-cite claims with superscript markers like [1], [2].
- After the prose, add a short "Sources" list: [n] Title — Domain (linked).
- Tone: clear, expert, engaging. No overall intro or conclusion; just this section.
- Output plain Markdown (the editor will convert to HTML)."""

    user_prompt = "Topic: {topic}\n\nUse these sources to write one standalone section:\n\n{research_data}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    # Convert the list of research dictionaries into a readable string block
    formatted_research = "\n\n".join([str(item) for item in research_results])

    # Create the chain and invoke the LLM
    chain = prompt_template | llm
    result = chain.invoke({"topic": topic, "research_data": formatted_research})

    return result.content