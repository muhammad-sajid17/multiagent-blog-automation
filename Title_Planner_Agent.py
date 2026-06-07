import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# 1. Define the Structured Output Schema (Matching the n8n Output Parser)
class NewsletterPlan(BaseModel):
    title: str = Field(description="A catchy edition title (<= 80 chars)")
    topics: list[str] = Field(
        description="Exactly 3 concise topics (each 3-5 words) reflecting distinct angles.",
        min_length=3,
        max_length=3
    )


def run_planner_agent(research_results: list) -> dict:
    """
    Takes Tavily research results and generates a structured newsletter plan.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing from environment variables.")

    # Initialize the Gemini model (matching the n8n setup)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",  # Or gemini-1.5-pro/flash depending on your access
        temperature=0.3,  # Lower temperature for planning consistency
        max_retries=2
    )

    # Bind the Pydantic schema to force structured JSON output
    structured_llm = llm.with_structured_output(NewsletterPlan)

    # 2. Set up the Prompts (from your ReadMe)
    system_prompt = """You are an expert newsletter planner. You receive 3–5 short article digests (title, URL, published date, content) from the past week.

Task: 
propose a catchy edition title (≤ 80 chars) and exactly 3 concise topics (each 3–5 words) that reflect distinct angles for our audience of small-business leaders.

Constraints: unique topics; no duplicates; no clickbait; be informative.
Output only via the required schema (no extra text)."""

    user_prompt = "Here are recent articles to consider:\n\n{research_data}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    # 3. Format the data and invoke the chain
    formatted_research = "\n\n".join([str(item) for item in research_results])

    # Create the chain: Prompt -> LLM (with structured output)
    chain = prompt_template | structured_llm

    print("🧠 Planner Agent is analyzing research and drafting topics...")
    result: NewsletterPlan = chain.invoke({"research_data": formatted_research})

    # Return as a standard dictionary for easy passing to the next step
    return result.model_dump()