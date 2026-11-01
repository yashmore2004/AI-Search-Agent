"""
Simple AI Agent — LangChain + Groq (free LLM) + Tavily (free web search)
--------------------------------------------------------------------
What this agent does:
  1. You type a question.
  2. The LLM (running on Groq) decides whether it needs to search the
     web to answer, and if so, calls the Tavily search tool.
  3. It reads the search results and gives you a final answer.

Both API keys used here are free — no credit card required.
See README.md for how to get them.
"""

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

# 1. Load the API keys from the .env file in this folder
load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    raise SystemExit("Missing GROQ_API_KEY. Copy .env.example to .env and fill it in.")
if not os.environ.get("TAVILY_API_KEY"):
    raise SystemExit("Missing TAVILY_API_KEY. Copy .env.example to .env and fill it in.")

# 2. Set up the "brain" — a free Groq-hosted model
llm = ChatGroq(
    model="openai/gpt-oss-120b",  # fast, free, good enough for this agent
    temperature=0,                 # 0 = more focused/factual, less creative
)

# 3. Give the agent a tool: live web search
search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

# 4. Build the agent — it decides on its own when to use the search tool
agent = create_agent(
    model=llm,
    tools=[search_tool],
    system_prompt=(
        "You are a helpful research assistant. "
        "Use the search tool when a question needs current or factual "
        "information you are not sure about. Keep answers concise and "
        "mention where the information came from."
    ),
)


def ask(question: str) -> str:
    """Send one question to the agent and return its final answer."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Simple search agent. Type a question, or 'quit' to exit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        if not question:
            continue
        answer = ask(question)
        print(f"\nAgent: {answer}\n")
