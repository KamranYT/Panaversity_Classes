import os
from dotenv import load_dotenv
from tavily import TavilyClient

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled
)

# ------------------------------
# ENV & CLIENT SETUP
# ------------------------------
load_dotenv()
set_tracing_disabled(disabled=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# ------------------------------
# TOOLS
# ------------------------------
@function_tool()
async def search(query: str) -> list:
    print("[TOOL...] Searching for:", query)
    try:
        response = await tavily_client.search(query)
        if not response or "results" not in response or len(response["results"]) == 0:
            return ["NO_RESULTS"]
        urls = [r["url"] for r in response["results"]]
        return urls
    except Exception as e:
        print("[ERROR in search]:", str(e))
        return ["ERROR"]


@function_tool()
async def extract_content(urls: list) -> dict:
    print("[TOOL...] Extracting content from URLs:", urls)
    if urls == ["NO_RESULTS"]:
        return {"summaries": [{"url": None, "content": "No reliable sources found."}]}
    if urls == ["ERROR"]:
        return {"summaries": [{"url": None, "content": "Search tool failed due to API error."}]}

    try:
        response = await tavily_client.extract(urls)
        return {
            "summaries": [
                {"url": r["url"], "content": r["raw_content"][:500]}
                for r in response["results"]
            ]
        }
    except Exception as e:
        print("[ERROR in extract]:", str(e))
        return {"summaries": [{"url": None, "content": f"Extraction failed: {e}"}]}

# ------------------------------
# AGENT SETUP
# ------------------------------
agent = Agent(
    name="Research Agent",
    instructions=(
        "You are a professional research assistant.\n"
        "1. Always use `search` first. If it returns 'NO_RESULTS' or 'ERROR', report it clearly.\n"
        "2. If search works, always call `extract_content` on the URLs.\n"
        "3. Summarize findings in 3–5 concise bullet points with sources.\n"
        "4. If extraction fails, still provide a partial answer from search.\n"
        "5. Never mention training data or knowledge cutoff.\n"
    ),
    model=model,
    tools=[search, extract_content],
)

# ------------------------------
# FALLBACK PIPELINE
# ------------------------------
def summarize_with_model(snippets: list, query: str) -> str:
    joined = ""
    for s in snippets[:5]:
        domain = (s["url"] or "").split("/")[2] if s.get("url") else ""
        joined += f"[{domain}] {s.get('content','')}\n\n"

    prompt = (
        "Summarize the findings below into 3–5 crisp bullet points. "
        "Each bullet MUST end with the source domain in parentheses. "
        "Do NOT mention knowledge cutoff. If content is too thin, say 'No reliable sources found.'\n\n"
        f"User query: {query}\n\n"
        f"Findings:\n{joined[:9000]}"
    )

    summarizer = Agent(
        name="Summarizer",
        instructions="Summarize clearly. No tool calls.",
        model=model,
        tools=[],
    )
    out = Runner.run_sync(summarizer, prompt)
    return out.final_output.strip()


def safe_research_pipeline(query: str) -> str:
    urls = Runner.run_sync(agent, {"tool_name": "search", "arguments": {"query": query}}).final_output
    if isinstance(urls, str):
        urls = [u.strip() for u in urls.replace("[", "").replace("]", "").split(",") if u.strip()]
    if not urls:
        return "No reliable sources found."

    extracted = Runner.run_sync(agent, {"tool_name": "extract_content", "arguments": {"urls": urls}}).final_output
    if isinstance(extracted, dict):
        summaries = extracted.get("summaries", [])
    else:
        summaries = []

    if not summaries:
        return "No reliable sources found."

    return summarize_with_model(summaries, query)

# ------------------------------
# RUN QUERY
# ------------------------------
if __name__ == "__main__":
    query = "latest LLM models in China 2025"
    result = Runner.run_sync(agent, query).final_output or ""

    bad_markers = ["knowledge cutoff", "Would you like me to do that?"]
    if any(m.lower() in result.lower() for m in bad_markers) or not result.strip():
        print("\n[GUARD] Falling back to deterministic pipeline...\n")
        result = safe_research_pipeline(query)

    print("\n 🔍 Research Query:", query)
    print("\n 📌 Final Answer:\n")
    print(result)
