from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


def run_art_director_agent(title: str, topics: list) -> str:
    """Generates a high-quality, descriptive text-to-image prompt based on the newsletter theme."""
    # Using 2.5-flash-lite for lightweight descriptive prompt engineering
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.6)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an elite AI Art Director. Your job is to write a highly detailed, descriptive image generation "
            "prompt (for DALL-E 3 or Midjourney) that represents a technology/business newsletter edition.\n\n"
            "Guidelines:\n"
            "- Style: Clean, modern, editorial tech illustration, isometric vector art, or minimalist 3D render.\n"
            "- Avoid text, words, or logos inside the image.\n"
            "- Specify lighting, vibrant professional color palettes, and clear central subjects.\n"
            "- Output ONLY the final prompt string. Do not include introductory text, conversational remarks, or markdown code blocks."
        )),
        ("human", "Newsletter Title: {title}\nCore Topics Covered: {topics}")
    ])

    chain = prompt | llm
    return chain.invoke({"title": title, "topics": ", ".join(topics)}).content