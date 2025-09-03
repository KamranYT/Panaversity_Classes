## 🔎💥 Deep Research Agent

Make your computer do wild research runs so you don't have to. Minimal setup. Maximum vibes. 🚀🧠

### 🧩 Project Details (Only)

#### 🎯 Purpose
Turn a single research prompt into a structured, multi-step investigation: gather sources, extract key points, and produce a concise summary with citations.

#### 🧠 How It Works (High Level)
- Takes a topic or question.
- Expands it into sub-questions for deeper coverage.
- Searches the web and collects candidate sources.
- Extracts and ranks the most relevant insights.
- Generates a final brief with references.

#### 📥 Inputs
- A research prompt/topic (e.g., "State of quantum networking in 2025").
- Optional knobs: depth, max sources, output length.  
Note: Exact flags/args depend on `main.py` implementation.

#### 📤 Outputs
- A short, skimmable brief with bullet points.
- Inline citations and a sources list.
- Optional structured JSON (headings, key points, links) if enabled.

#### 🏗️ Internals (Conceptual)
- Orchestrator in `main.py` coordinates the flow.
- Pluggable steps for: query expansion, search, scraping, summarization.
- Deterministic installs via `pyproject.toml` + `uv.lock`.

#### 🧭 Scope & Non-Goals
- Aimed at breadth-first + selective depth research, not exhaustive literature reviews.
- Summaries are for rapid understanding, not academic citation.

#### 🚧 Limitations
- Dependent on availability/quality of online sources.
- May require API keys for some providers.

#### 🗺️ Roadmap Ideas
- Source de-duplication & credibility scoring.
- Multi-agent critique loop for higher accuracy.
- Export to Markdown/PDF.
- Config file for reproducible runs.

### 📦 What’s Inside
```
main.py         # orchestrates the research flow
pyproject.toml  # project metadata & dependencies (uv)
uv.lock         # pinned versions for reproducibility
.python-version # python version target
.venv/          # local venv (optional)
```

### 📜 License
Pick one you like (MIT recommended). Add a `LICENSE` file.


