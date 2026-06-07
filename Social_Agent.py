from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class SocialCopy(BaseModel):
    twitter: str = Field(description="A punchy tweet under 280 characters with relevant hashtags.")
    linkedin: str = Field(
        description="A professional, structured LinkedIn post with an introductory hook, key bullet points, and hashtags.")
    telegram_promo: str = Field(description="An exciting summary designed for a Telegram announcement channel.")


def run_social_agent(title: str, content: str) -> dict:
    print("📱 Running Social Summary Agent (gemini-2.5-flash-lite)...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.7)
    parser = JsonOutputParser(pydantic_object=SocialCopy)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "ROLE: You are an Elite Social Media Copywriter and Growth Marketer.\n"
            "TASK: Distill a newsletter article into 3 highly engaging, platform-specific social posts to drive traffic.\n"
            "CONSTRAINTS:\n"
            "- Twitter: Max 280 characters. Create a strong curiosity hook. Use 2-3 relevant hashtags.\n"
            "- LinkedIn: Professional but engaging tone. Use a 'Hook, Value, Action' structure. Utilize bullet points if helpful.\n"
            "- Telegram: Community-focused, exciting, and concise. Use emojis effectively to break up text.\n"
            "- CRITICAL: Do NOT include URLs or links in your copy (they will be appended programmatically later).\n"
            "OUTPUT: {format_instructions}"
        )),
        ("human", "Article Title: {title}\n\nArticle Content:\n{content}")
    ])
    chain = prompt | llm | parser
    return chain.invoke({"title": title,
                         "content": content,
                         "format_instructions": parser.get_format_instructions()
                         })