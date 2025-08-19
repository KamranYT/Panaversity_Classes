### 01_Deep_Research_Agent

An educational research agent that uses a Gemini-compatible client via `openai-agents` and the Tavily Search API to find sources and summarize findings. This folder contains runnable examples that demonstrate:

- Configuring `AsyncOpenAI` with Google Gemini (OpenAI-compatible) endpoint
- Defining tools (functions) the agent can call (e.g., search)
- Orchestrating a simple research workflow and printing results

#### Contents
- `main.py`: Demonstrates a basic agent setup and simple tool-calling example (math and/or search).
- `app.py`: Focused research example using Tavily search to answer a question about recent LLMs in China.

Note: Some experimental scripts may exist locally but are intentionally ignored by Git to keep secrets and scratch work out of version control.

---

### Requirements
- Python 3.13+
- `uv` (recommended) or `venv + pip`
- Accounts/keys as needed:
  - Google AI Studio key for Gemini (OpenAI-compatible endpoint)
  - Tavily API key for search

Install `uv` (once):
```bash
pipx install uv  # or: pip install --user uv
```

---

### Environment variables
Create a `.env` file in this folder with:
```dotenv
GEMINI_API_KEY=your_google_ai_studio_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional (some examples reference it)
OPENAI_API_KEY=your_openai_api_key
```

Tips:
- `.env` is ignored by Git in the repository root `.gitignore`.
- Keep API keys private; do not commit them.

---

### Quick start

Using `uv` (recommended):
```bash
cd 00_Projects/01_Deep_Research_Agent
uv sync                # install dependencies from pyproject/uv.lock
echo GEMINI_API_KEY=your_key > .env
echo TAVILY_API_KEY=your_tavily_key >> .env

# Run examples
uv run python main.py
uv run python app.py
```

Using `venv + pip`:
```bash
cd 00_Projects/01_Deep_Research_Agent
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Git Bash/CMD:      . .venv/Scripts/activate
pip install -e .
python main.py
```

---

### How it works (high level)
1. Load environment variables from `.env` using `python-dotenv`.
2. Create an `AsyncOpenAI` client configured with your `GEMINI_API_KEY` and the Gemini-compatible `base_url` (`https://generativelanguage.googleapis.com/v1beta/openai/`).
3. Wrap the model with `OpenAIChatCompletionsModel` from `openai-agents`.
4. Define function tools (e.g., `search`) and register them with the `Agent`.
5. Run the agent with a prompt; the library will call tools as needed and return a final output.
6. For research, the Tavily client is used to perform web search and (optionally) extraction, and the model summarizes findings.

Key libraries used:
- `openai-agents`: high-level agent orchestration around OpenAI-compatible APIs
- `tavily-python`: search and extraction APIs

---

### Troubleshooting
- 401/403 or auth errors: Check `.env` values, key validity, and copy/paste issues (extra spaces or quotes).
- Empty or low-quality results: Tavily might return few sources for some queries; try rephrasing.
- Network/proxy issues: If behind a proxy, configure your environment (e.g., `HTTP_PROXY`/`HTTPS_PROXY`).
- Python version errors: Ensure Python 3.13 is selected. With `uv`, you can install/manage Python versions via `uv python install 3.13`.
- Windows line-ending warnings in Git (CRLF/LF): Harmless and can be ignored.

---

### Security and hygiene
- Do not share or commit API keys. The project `.gitignore` excludes `.env`, virtualenvs, caches, and logs.
- Consider using separate keys for development versus production.

---

### License
Educational/demo content for class use.


