import os
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# 1. Define the Structured Output Schema (Matches n8n Editor Schema)
class FinalNewsletter(BaseModel):
    subject: str = Field(description="An email subject (<= 80 chars, no emojis).")
    content: str = Field(description="VALID, responsive HTML body only (no <!DOCTYPE>, <html>, or <head>).")


def run_editor_agent(title: str, sections: list[str]) -> dict:
    """
    Takes the planned title and the generated Markdown sections,
    and formats them into a final HTML newsletter and subject line.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing from environment variables.")

    # Using Flash to prevent rate-limit crashes
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.2,  # Low temperature for strict HTML structure
        max_retries=2
    )

    structured_llm = llm.with_structured_output(FinalNewsletter)

    system_prompt = """You are the newsletter editor and layout stylist.

**Input:** one title candidate and 3 Markdown sections with [n] footnotes.

**Output:**
1. **subject** — an email subject (≤ 80 chars, no emojis).
2. **content** — a VALID, responsive HTML **body only** (no `<!DOCTYPE>`, `<html>`, or `<head>`).

**HTML Requirements:**
* Structure: include a header with the title + current date {current_date}, a short intro paragraph, the 3 sections (convert Markdown to HTML), a "Key Sources" section that deduplicates and numbers links, and a short friendly sign-off.
* Typography: use `<h1>/<h2>`, `<p>`, `<ul>/<ol>`, `<a>`. Apply inline CSS for readability (max-width container, readable font size and line-height).
* Links: anchors must include `rel="noopener noreferrer"` and `target="_blank"`.
* Accessibility: semantic headings; include `alt` text if images appear (don't invent images).
* Restrictions: no external CSS/JS, no tracking pixels."""

    user_prompt = "Title: {title}\n\nSections: \n{sections_text}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    # Join the 3 sections with wide spacing (matching the n8n expression)
    joined_sections = "\n\n\n\n".join(sections)
    current_date = datetime.now().strftime("%A, %B %d, %Y")

    chain = prompt_template | structured_llm

    print("\n   -> 🎨 Editor Agent is styling the newsletter into HTML...")
    result: FinalNewsletter = chain.invoke({
        "current_date": current_date,
        "title": title,
        "sections_text": joined_sections
    })

    return result.model_dump()