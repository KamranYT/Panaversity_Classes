## Panaversity Classes – AI Agents and Examples

A multi-project repository with small examples and class materials around building agents using `openai-agents` with Google Gemini compatibility and the Tavily search API. Each subfolder is a standalone mini-project.

### Repository layout
- `05_search_agent/` – Search agent demo using Gemini + Tavily. Also contains a portfolio reader example with `requests` + `beautifulsoup4`.
- `07_hello_agent/` – Minimal "hello" example.
- `08_class/` – Class demo wired to Gemini-compatible client.
- `class_10/` – Another minimal "hello" example.
- `00_Projects/01_Deep_Research_Agent/` – A more complete research agent with search + extraction pipelines.

### Requirements
- Python 3.13+ (as declared in most `pyproject.toml` files)
- Recommended: `uv` (fast Python package manager) to install and run projects
- Git

Install `uv` (one-time):
```bash
pipx install uv  # or: pip install --user uv
```

### Environment variables
Some projects require API keys provided via a `.env` file in the project folder.

Common variables:
```dotenv
# Required for projects using Gemini-compatible client
GEMINI_API_KEY=your_google_ai_studio_api_key

# Required for projects using Tavily search
TAVILY_API_KEY=your_tavily_api_key

# Optional (some samples reference it)
OPENAI_API_KEY=your_openai_api_key
```

Notes:
- `.env` files are ignored by Git (see the repo `.gitignore`). Do not commit secrets.
- Get a Gemini key from Google AI Studio. Get a Tavily key from Tavily.

---

## Project quick starts

Below, choose either the `uv` workflow (recommended) or the standard `venv + pip` alternative.

### 05_search_agent
- Purpose: Demonstrates a simple search agent with Gemini + Tavily, and a portfolio reader tool using `requests` + `beautifulsoup4`.
- Environment: needs `GEMINI_API_KEY` and `TAVILY_API_KEY`.

Using uv:
```bash
cd 05_search_agent
uv sync               # installs from pyproject.toml/uv.lock
cp .env.example .env || true  # if you have one; otherwise create .env per template above
uv run python main.py  # runs the search agent example
# Alternative demo:
uv run python app.py   # runs the portfolio reader demo
```

Using venv + pip:
```bash
cd 05_search_agent
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .          # or: pip install -r requirements if you create one
python main.py
```

### 07_hello_agent
- Purpose: Minimal console "hello" example.
- Environment: none required.

```bash
cd 07_hello_agent
uv sync
uv run python main.py
```

### 08_class
- Purpose: Class demo wired to Gemini-compatible client.
- Environment: `GEMINI_API_KEY` (and optionally `OPENAI_API_KEY`).

```bash
cd 08_class
uv sync
echo GEMINI_API_KEY=your_key > .env
uv run python main.py
```

### class_10
- Purpose: Minimal console "hello" example.
- Environment: none required.

```bash
cd class_10
uv sync
uv run python main.py
```

### 00_Projects/01_Deep_Research_Agent
- Purpose: More complete research agent using Gemini + Tavily with a search and extraction pipeline.
- Environment: `GEMINI_API_KEY`, `TAVILY_API_KEY`.

Run any of the demos (pick one):
```bash
cd 00_Projects/01_Deep_Research_Agent
uv sync
echo GEMINI_API_KEY=your_key > .env
echo TAVILY_API_KEY=your_tavily_key >> .env

# Examples
uv run python main.py
uv run python app.py
uv run python 5C.py
```

---

## Troubleshooting
- API 401/403 errors: Verify your `.env` values and that the keys are active.
- Windows CRLF/LF warnings in Git: Harmless. You can set `git config core.autocrlf true` on Windows if desired.
- Missing dependencies or module import errors: Re-run `uv sync` (or reinstall your venv). Confirm you’re running from the correct subfolder.
- Python version: Ensure you have Python 3.13 available. With `uv`, you can run `uv python install 3.13`.

## Git hygiene
- This repo’s `.gitignore` excludes common secrets (`.env*`), virtual environments, caches, logs, and local DB files. Keep keys out of commits.

## License
Educational/demo content. Add a license if you plan to redistribute.

## Credits
- Built for Panaversity classes and demos, using `openai-agents`, Gemini-compatible APIs, Tavily, and standard Python tooling.

"# panaversity_classes" 
