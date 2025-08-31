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
    set_tracing_disabled
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
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def search(query: str) -> str:
    print("[TOOL...]Searching for:", query)
    response = tavily_client.search(query)

# 1. Create Agent and register tools
agent: Agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant. "
        "Always use tools for math questions. Always follow DMAS rule (division, multiplication, addition, subtraction). "
        "Explain answers clearly and briefly for beginners."
    ),
    model=model,
    tools=[multiply, sum],
)

# Run Agent
result = Runner.run_sync(agent, "What is 19 + 34 * 34")

print("\n Calling Agent\n")
print(result.final_output)

# 2. Searhc Agent
agent = Agent(
    name="Searhc Agent",
    model=model,
    tools=[search],
)
runner = Runner.run_sync(agent, "Who is USA President?")
print("\n Calling Search Agent\n")
print(runner.final_output)