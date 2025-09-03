import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_default_openai_client,
    set_tracing_disabled,
)

_: bool = load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)

# Environment & Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# Model Configuration
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", openai_client=external_client
)


@function_tool()
async def search(query: str) -> str:
    """Search the web for the given query and return the top result."""
    return "No Results found"

#  Search Agent
agent = Agent(
    name="Search Agent",
    instructions=(
    "You are a research assistant. "
    "When you use the `extract_content` tool, the raw text may include navigation or irrelevant sections. "
    "Always summarize the extracted content into clean, concise insights. "
    "Focus only on the main points relevant to the user’s question, not menus or boilerplate text. "
    "Keep answers short, clear, and structured."
),
    model=model,
    tools=[search],
)

runner = Runner.run_sync(agent, "Latest LLM Model released by china?")
print("\n Calling Search Agent\n")
print(runner.final_output)
