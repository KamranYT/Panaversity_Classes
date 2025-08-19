import os
from dotenv import load_dotenv
from tavily import TavilyClient

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_default_openai_client,
    set_tracing_disabled,
)

load_dotenv()

set_tracing_disabled(disabled=True)

# Environment & Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
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
def search(query: str) -> str:
    print("[TOOL...]Searching for:", query)
    response = tavily_client.search(query)
    return str(response)


# 2. Searhc Agent
agent = Agent(
    name="Search Agent",
    model=model,
    tools=[search],
)
runner = Runner.run_sync(agent, "Latest LLM Model released by china?")
print("\n Calling Search Agent\n")
print(runner.final_output)
