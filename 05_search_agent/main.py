import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from tavily import TavilyClient
# Gemini LLM
# Gemini APi key 

load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)

gemini_api_key = os.environ.get("GEMINI_API_KEY")

tavily_api_key = os.environ.get("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=tavily_api_key)

# 1. Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Model

llm_model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model="gemini-2.5-flash"
)

# Python Function => sync/async
@function_tool()
def get_capital(country: str) -> str:
    capitals = {
        "Pakistan": "Islamabad",
        "India": "New Delhi",
        "China": "Beijing",
        "United States": "Washington, D.C.",
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
    }
    print(f"Getting capital of {country}")
    return capitals.get(country, "Unknown")

@function_tool()
def search(query: str) -> str:
    print("[TOOL...]Searching for:", query)
    response = tavily_client.search(query)
    return response

agent = Agent(
    name="Search Agent",
    model=llm_model,
    tools=[get_capital, search],
)
runner = Runner.run_sync(agent, "Who is Imran Khan")

print(runner.final_output)
# 30:00