# Simple AI Search Agent (LangChain + Groq + Tavily)

A small AI agent that answers questions and searches the web on its own
when it needs current information. Everything here is free.

- **LLM:** Groq (hosts fast, free open models like Llama 3.3 — no credit card)
- **Search tool:** Tavily (1,000 free searches/month — no credit card)
- **Framework:** LangChain's `create_agent`

## 1. Get your free API keys

1. **Groq:** go to https://console.groq.com/keys, sign up, click "Create API Key".
2. **Tavily:** go to https://app.tavily.com, sign up, copy the API key from
   your dashboard (free "Researcher" plan, 1,000 credits/month).

Keys and free-tier limits can change — check each site if something here
looks out of date. Groq also retires model names every few months; if
`agent.py` ever errors with `model_not_found` or `does not exist`, that's
why — see "If a model stops working" below.

## 2. Set up the project

```bash
# create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# add your keys
cp .env.example .env
# then open .env and paste in your GROQ_API_KEY and TAVILY_API_KEY
```

## 3. Run it

```bash
python agent.py
```

Try asking it something that needs a live search, for example:
- "What's the latest gold (XAUUSD) price news today?"
- "Who won the most recent F1 race?"
- "Summarize this week's news on LangChain."

And something it can answer without searching:
- "What is the capital of France?"

Watch the terminal — the agent decides for itself when to call the search
tool versus answering from what it already knows.

## How it works (for your resume / interview)

1. `ChatGroq` is the model — it does the thinking.
2. `TavilySearch` is a **tool** — a function the model can choose to call.
3. `create_agent` wires them into a loop: the model reads your question,
   decides whether it needs the tool, calls it if so, reads the result,
   and repeats until it has a final answer.
4. This loop — think, act, observe, repeat — is what makes it an "agent"
   rather than a one-shot chatbot call.

## If a model stops working

Groq periodically retires models to make room for newer, faster ones —
this already happened once to this project (an earlier version of
`agent.py` used `llama-3.3-70b-versatile`, which Groq shut down on
16 Aug 2026). If you ever see an error like:

```
groq.NotFoundError: ... model_not_found ... does not exist or you do not have access to it
```

the model name in `agent.py` has been retired. Fix:

1. Go to https://console.groq.com/docs/models for the current list of
   free models.
2. Open `agent.py` and change the `model="..."` line to one of them.

## Ideas to extend it (good for making the project your own)

- Add a second tool, e.g. a calculator function, so the agent picks
  between search and math depending on the question.
- Add memory so it remembers earlier questions in the same session.
- Wrap it in a small Streamlit or Flask page instead of the terminal.
