## 🔎💥 Deep Research Agent

Make your computer do wild research runs so you don't have to. Minimal setup. Maximum vibes. 🚀🧠

### ⚡ Quick Start
1) Install uv → Windows (PowerShell): `iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex`

2) Sync deps → `uv sync`

3) Run it →
- `uv run python main.py`
- or (if venv active) `python main.py`

### 🎛️ Optional Config
Set env vars before running (if your script uses them):
- PowerShell: `$Env:OPENAI_API_KEY = "your_key_here"`
- bash: `export OPENAI_API_KEY="your_key_here"`

Example (if args supported):
```
uv run python main.py --query "quantum networking" --depth 3
```

### 🗺️ What’s Inside
```
main.py         # the brain
pyproject.toml  # deps & metadata (uv)
uv.lock         # exact versions
.python-version # python version
.venv/          # local venv (optional)
```

### 🛠️ Pro Tips
- No activate? No problem → use `uv run`.
- Missing uv? Reopen terminal after install.
- Need more power? `uv add <package>`

### 📜 License
Pick one you like (MIT recommended). Add a `LICENSE` file.


