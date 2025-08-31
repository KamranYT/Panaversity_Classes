import os
from dotenv import load_dotenv
from tavily import AsyncTavilyClient
from dataclasses import dataClass

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    ModelSettings
)

load_dotenv()

set_tracing_disabled(disabled=True)

# Environment & Client Setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
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


@function_tool
async def search(query: str) -> str:
    print("[TOOL...]Searching for:", query)
    response = await tavily_client.search(query, max_results=5)
    return response

@function_tool
async def extract_content(urls: list) -> dict:
    print("[TOOL...]Extracting content from URLs:", urls)
    response = await tavily_client.extract(urls)

    return response


# 2. Search Agent
agent = Agent(
    name="Search Agent",
    model=model,
    tools=[search, extract_content],
    instructions="You are a deep search agent.",
    model_settings=ModelSettings(temperature=1.9, tool_choice="auto", max_tokens=1000)
)
runner = Runner.run_sync(agent, "Research on the impact of Agentic AI White collar Jobs?")
print("\n Calling Search Agent\n")
print(runner.final_output)
