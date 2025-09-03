import os
import asyncio
from dotenv import load_dotenv
from tavily import AsyncTavilyClient
from dataclasses import dataclass

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    ModelSettings,
    RunContextWrapper
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

@dataclass
class UserInput:
    query: str
    urls: list

@function_tool
async def search(local_context: RunContextWrapper[UserInput], query: str) -> str:
    print("\n\n""Some Data: ", local_context.context.query, "\n\n")
    print("[TOOL...]Searching for:", query)
    response = await tavily_client.search(query, max_results=5)
    return response

@function_tool
async def extract_content(local_context: RunContextWrapper[UserInput], urls: list) -> dict:
    print("\n\n""Some Data: ", local_context.context.query, "\n\n")
    print("[TOOL...]Extracting content from URLs:", urls)
    response = await tavily_client.extract(urls)

    return response


# 2. Search Agent
agent = Agent(
    name="Search Agent",
    model=model,
    tools=[search, extract_content],
    instructions=(
    "You are a deep search agent. "
    "First, use the search tool to find relevant results. "
    "Then, always call extract_content on the URLs to gather detailed content "
    "before giving the final answer."
),
    model_settings=ModelSettings(temperature=1.9, tool_choice="auto", max_tokens=1000)
)

user_query = input("Enter your query: ")

async def call_agent():
    user_input = UserInput(query=user_query, urls=[])
    output = await Runner.run(
        starting_agent=agent,
        input=user_query,
        context=user_input
    )
    print("\n Calling Search Agent\n")
    print(output.final_output)
asyncio.run(call_agent())
