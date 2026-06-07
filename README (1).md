# 🤖 Agentic Newsroom
### A Multi-Agent Automation System for Autonomous Research and Newsletter Generation

> **Authors:** Muhammad Sajid (23-SE-17) · Zubair Ghaffar (23-SE-15)  
> **Institution:** Software Engineering Department, UET Taxila  
> **Course:** Artificial Intelligence — Dr. Kanwal Yousaf

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Agent Roles](#agent-roles)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the System](#running-the-system)
- [Project Structure](#project-structure)
- [Pipeline Walkthrough](#pipeline-walkthrough)
- [Phase 2: Social Media Pipeline](#phase-2-social-media-pipeline)
- [Troubleshooting](#troubleshooting)

---

## Overview

The **Agentic Newsroom** is a fully autonomous, multi-agent AI system that transforms a single unstructured niche topic (sent via Telegram) into a fully researched, written, formatted, and published newsletter — with a Human-in-the-Loop approval gate before any public content goes live.

**What it does, end to end:**

1. Receives a niche topic from a user via Telegram (e.g., *"AI in Healthcare 2025"*)
2. Researches the topic using real-time web search (Tavily API)
3. Plans a newsletter structure using a Planner AI agent (title + 3 distinct topics)
4. Conducts deep research on each topic in **parallel**
5. Writes 3 professional newsletter sections concurrently
6. Formats everything into responsive HTML via an Editor AI agent
7. Stages the draft in **Gmail** for human review
8. On approval, publishes live to **Blogger**
9. Generates platform-specific social media copy (Twitter, LinkedIn, Telegram)
10. Broadcasts approved social posts directly to a **Telegram Channel**

---

## System Architecture

```
User (Telegram)
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                   PERCEPTION & ACTION TOOLKIT               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │ Tavily Search│  │ Telegram Bot │  │ Gmail OAuth API    │ │
│  │ API          │  │ Input/Output │  │ Blogger API v3     │ │
│  └──────────────┘  └──────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
      │                    Queries / Results
      ▼
┌─────────────────────────────────────────────────────────────┐
│                BRAIN (COGNITION & PROCESS CONTROL)          │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────────┐  │
│  │   Planner   │   │   Writer    │   │     Editor       │  │
│  │    Agent    │   │   Agents    │   │      Agent       │  │
│  │  (flash-   │   │   x3 in     │   │   (flash-lite)   │  │
│  │   lite)     │   │  parallel   │   │                  │  │
│  └─────────────┘   └─────────────┘   └──────────────────┘  │
│           Powered by: Google Gemini 2.5 Flash Family        │
└─────────────────────────────────────────────────────────────┘
      │                    Read / Write
      ▼
┌─────────────────────────────────────────────────────────────┐
│                   MEMORY & VALIDATION                       │
│  ┌──────────────────────┐   ┌───────────────────────────┐  │
│  │    JSON Schema       │   │   Markdown Aggregation    │  │
│  │  (Pydantic Models)   │   │   (3 sections → 1 doc)    │  │
│  └──────────────────────┘   └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
 Approved HTML Draft → Audience (Blogger + Social Media)
```

---

## Agent Roles

| Agent | File | Model | Temperature | Responsibility |
|---|---|---|---|---|
| **Planner** | `Title_Planner_Agent.py` | gemini-2.5-flash-lite | 0.3 | Analyzes research → outputs structured title + 3 topics (JSON) |
| **Writer x3** | `Section_Writer_Agent.py` | gemini-2.5-flash | 0.4 | Writes 1 cited Markdown section per topic (runs in parallel) |
| **Editor** | `HTML_Editor_Agent.py` | gemini-2.5-flash-lite | 0.2 | Converts Markdown sections → responsive HTML newsletter |
| **Social** | `Social_Agent.py` | gemini-2.5-flash-lite | 0.7 | Generates Twitter, LinkedIn, and Telegram post copy |

---

## Prerequisites

- Python 3.10+
- A Google account with Blogger enabled at [blogger.com](https://www.blogger.com)
- Google Cloud project with Gmail API + Blogger API enabled
- Telegram account + a bot token from [@BotFather](https://t.me/BotFather)
- Tavily API account at [tavily.com](https://tavily.com)
- Google AI API key at [ai.google.dev](https://ai.google.dev)

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/agentic-newsroom.git
cd agentic-newsroom
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

Required packages:
```
python-telegram-bot>=20.0
langchain-google-genai
google-generativeai
tavily-python
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
python-dotenv
pydantic
```

---

## Configuration

**1. Create a `.env` file** in the project root:

```env
# Google Gemini LLM
GOOGLE_API_KEY=your_google_ai_api_key_here

# Tavily Web Search
TAVILY_API_KEY=your_tavily_api_key_here

# Telegram Bot
TELEGRAM_TOKEN=your_telegram_bot_token_here

# Optional: Telegram Channel for Phase 2 broadcasting
# Get channel ID by adding @userinfobot to your channel
TELEGRAM_CHANNEL_ID=@your_channel_username
```

**2. Set up Google OAuth credentials**

- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a project → enable **Gmail API** and **Blogger API**
- Create OAuth 2.0 credentials (Desktop application type)
- Download the credentials JSON file and save it as `credentials.json` in the project root

**3. First-run authentication**

On first run, a browser window will open for Google OAuth consent. Approve both scopes:
- `https://www.googleapis.com/auth/gmail.compose`
- `https://www.googleapis.com/auth/blogger`

A `token.json` file will be created automatically for subsequent runs.

---

## Running the System

```bash
python main.py
```

Expected startup output:
```
Starting Multi-Agent System Core...
System is online! Waiting for Telegram messages...
----------------------------------------
```

**Using the bot:**

1. Open Telegram and find your bot
2. Send `/start` for a welcome message
3. Send any niche topic, for example:
   - `AI in Healthcare 2025`
   - `Sustainable Energy for Small Businesses`
   - `The Future of Remote Work Technology`
4. Watch the pipeline status updates appear in real time
5. Check your Gmail Drafts for the generated newsletter
6. Use the **Approve & Publish** or **Reject** buttons in Telegram
7. On approval, review and approve each social media post individually

---

## Project Structure

```
agentic-newsroom/
│
├── main.py                        # Entry point — Telegram bot initialization
├── Telegram_Bot_Trigger.py        # Pipeline orchestrator & HITL handler
│
├── Travily_Niche_Research.py      # Step 2: Broad initial news research
├── Title_Planner_Agent.py         # Step 3: Planner Agent (title + 3 topics)
├── Topics_Split.py                # Step 4: Parallel split-out orchestrator
├── Travily_Deep_Research.py       # Step 4: Deep per-topic research
├── Section_Writer_Agent.py        # Step 5: Section Writer Agent
├── HTML_Editor_Agent.py           # Step 6: Editor Agent (Markdown → HTML)
├── Gmail_Draft.py                 # Step 7: Gmail draft staging
├── Blogger_Published.py           # Step 8: Blogger live publication
├── Social_Agent.py                # Step 9-10: Social media copy generation
│
├── credentials.json               # Google OAuth credentials (DO NOT COMMIT)
├── token.json                     # Auto-generated OAuth token (DO NOT COMMIT)
├── .env                           # API keys (DO NOT COMMIT)
├── .gitignore
└── requirements.txt
```

> ⚠️ **Security:** Never commit `credentials.json`, `token.json`, or `.env` to version control. Add all three to `.gitignore`.

---

## Pipeline Walkthrough

```
[User] → Telegram: "AI in Healthcare 2025"
    │
    ├─[Step 1] Telegram receives niche topic
    │
    ├─[Step 2] Tavily Niche Research
    │          → 3 recent news articles retrieved (past 7 days)
    │
    ├─[Step 3] Planner Agent (gemini-2.5-flash-lite)
    │          → JSON Output: { "title": "...", "topics": ["...", "...", "..."] }
    │
    ├─[Step 4] Parallel Split-Out (asyncio.gather)
    │          ├── Topic 1 → Deep Tavily Search (5 articles, 30 days)
    │          ├── Topic 2 → Deep Tavily Search (5 articles, 30 days)
    │          └── Topic 3 → Deep Tavily Search (5 articles, 30 days)
    │
    ├─[Step 5] Parallel Section Writing (gemini-2.5-flash)
    │          ├── Writer Agent 1 → Markdown Section 1 (350-500 words + citations)
    │          ├── Writer Agent 2 → Markdown Section 2 (350-500 words + citations)
    │          └── Writer Agent 3 → Markdown Section 3 (350-500 words + citations)
    │
    ├─[Step 6] Editor Agent (gemini-2.5-flash-lite)
    │          → Responsive HTML newsletter + subject line
    │
    ├─[Step 7] Gmail Draft API
    │          → Draft staged → Draft ID stored in DRAFTS_STORE
    │          → Telegram: [✅ Approve & Publish] [❌ Reject]
    │
    ├─[Step 8] On Approval → Blogger API v3
    │          → Live post published → Public URL returned
    │
    ├─[Step 9] Social Agent (gemini-2.5-flash-lite)
    │          → Twitter post (<280 chars + hashtags)
    │          → LinkedIn post (Hook-Value-Action)
    │          → Telegram promo (emoji-rich, concise)
    │
    └─[Step 10] Per-Platform HITL Approval
               → Telegram post approved → Broadcast to channel
               → Twitter/LinkedIn posts → Displayed for manual posting
```

---

## Phase 2: Social Media Pipeline

After a successful Blogger publication, the system automatically enters Phase 2:

- **Twitter/X:** A punchy, curiosity-driven tweet under 280 characters with 2-3 relevant hashtags and the blog URL appended
- **LinkedIn:** A professional post with an introductory hook, bullet-point value summary, and call-to-action hashtags
- **Telegram Channel:** An emoji-rich, community-focused announcement that gets broadcast directly to your configured channel upon approval

To enable live Telegram Channel broadcasting, add the bot as an **Admin** to your channel and set `TELEGRAM_CHANNEL_ID` in your `.env` file. Without this, the system will simulate the broadcast within your private chat.

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `GOOGLE_API_KEY is missing` | Missing `.env` variable | Add `GOOGLE_API_KEY` to `.env` |
| `TAVILY_API_KEY is missing` | Missing `.env` variable | Add `TAVILY_API_KEY` to `.env` |
| `No blogs found` | No Blogger blog exists | Create a blog at blogger.com first |
| OAuth browser doesn't open | Headless/server environment | Run locally first to generate `token.json`, then copy it to server |
| `token.json` scope error | Old token with missing scopes | Delete `token.json` and re-authenticate |
| Telegram `Can't parse entities` | Markdown formatting conflict | Already resolved — `parse_mode` stripped from social posts |
| `429 Rate limit` on Gemini | Too many concurrent calls | Model routing already handles this; add `time.sleep(1)` if issue persists |
| Gmail draft not appearing | Wrong email account in OAuth | Delete `token.json`, re-authenticate with the correct account |

---

*Built with LangChain · Google Gemini · Tavily · python-telegram-bot · Gmail API · Blogger API*
