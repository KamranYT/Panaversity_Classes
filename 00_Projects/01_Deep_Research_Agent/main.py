import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient
from dataclasses import dataclass
import datetime

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    ModelSettings,
    RunContextWrapper,
    ItemHelpers
)

# 🔹 Load environment variables
_: bool = load_dotenv(find_dotenv())

# 🔹 Environment & Clients
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
tavily_client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# 🔹 Model
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# 🔹 User Input
@dataclass
class UserInput:
    query: str
    urls: list

# 🔹 Tools
@function_tool
async def search(local_context: RunContextWrapper[UserInput], query: str) -> str:
    print("\n\nUser_Asked_Question:", local_context.context.query, "\n\n")
    print("[TOOL...] Searching for:", query)
    response = await tavily_client.search(query, max_results=5)
    return response

@function_tool
async def extract_content(local_context: RunContextWrapper[UserInput], urls: list) -> dict:
    print("\n[TOOL...] Extracting content from URLs:", urls, "\n")
    response = await tavily_client.extract(urls)
    return response

# 🔹 Dynamic instruction for Deep Research Agent
async def deep_search_prompt(
    special_context: RunContextWrapper,
    agent: Agent
) -> str:
    await asyncio.sleep(0.1)
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

# 🔹 Sub-Agent (Deep Research Agent)
deep_research_agent: Agent = Agent(
    name="Deep Research Agent",
    model=model,
    tools=[search, extract_content],
    instructions=deep_search_prompt,
    model_settings=ModelSettings(
        temperature=1.0,
        tool_choice="auto",
        max_tokens=1000
    )
)

# Convert to tool
deep_research_tool = deep_research_agent.as_tool(
    tool_name="deep_research_agent",
    tool_description="A deep research agent that searches online, extracts content, and provides structured answers."
)

# 🔹 Lead Agent (Orchestrator)
lead_agent: Agent = Agent(
    name="Lead Agent",
    model=model,
    instructions="You are the lead agent. You decide when to call the deep research agent to help answer user queries.",
    tools=[deep_research_tool],
    model_settings=ModelSettings(
        temperature=0.7,
        tool_choice="auto",
        max_tokens=800
    )
)

# 🔹 Run Lead Agent
user_query = input("Enter your query: ")

async def run_lead_agent():
    user_input = UserInput(query=user_query, urls=[])
    output = Runner.run_streamed(
        starting_agent=lead_agent,
        input=user_query,
        context=user_input
    )
    print("\n🚀 Calling Lead Agent\n")

    async for event in output.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"\n\n-- Message output:\n {ItemHelpers.text_message_output(event.item)}")

    print("=== Run complete ===")

if __name__ == "__main__":
    asyncio.run(run_lead_agent())
