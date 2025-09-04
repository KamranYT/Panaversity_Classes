import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient
from dataclasses import dataclass
import datetime
from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    ModelSettings,
    RunContextWrapper,
    ItemHelpers
)

_: bool = load_dotenv(find_dotenv())

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
    print("\n\n""User_Asked_Question: ", local_context.context.query, "\n\n")
    print("[TOOL...]Searching for:", query)
    response = await tavily_client.search(query, max_results=5)
    return response

@function_tool
async def extract_content(local_context: RunContextWrapper[UserInput], urls: list) -> dict:
    print("\n[TOOL...]Extracting content from URLs:", urls,"\n")
    response = await tavily_client.extract(urls)

    return response

user_query = input("Enter your query: ")

# Dynamic instruction for Deep Search Agent
async def deep_search_prompt(
    special_context: RunContextWrapper,
    agent: Agent
) -> str:
    # Simulate async work (like DB lookup, API call, etc.)
    await asyncio.sleep(0.1)

    # Get query from context
    query = getattr(special_context.context, "query", None)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""
    You are {agent.name}, a deep search agent.
    Current time: {current_time}.
    
    Instructions:
    1. Always use the search tool first to find relevant results.
    2. Always call extract_content on the URLs to gather detailed content.
    3. After extracting, provide a comprehensive and well-structured final answer.
    
    User query: {query}
    """

agent: Agent = Agent(
    name="Deep Research Agent",
    model=model,
    tools=[search, extract_content],
    instructions=deep_search_prompt,  # 👈 dynamic async instructions
    model_settings=ModelSettings(
        temperature=1.0,
        tool_choice="auto",
        max_tokens=1000
    )
)

async def call_agent():
    user_input = UserInput(query=user_query, urls=[])
    output = Runner.run_streamed(
        starting_agent=agent,
        input=user_query,
        context=user_input
    )
    print("\n Calling Search Agent\n")

    async for event in output.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"\n\n-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")

asyncio.run(call_agent())
