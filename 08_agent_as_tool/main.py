import os
from dotenv import load_dotenv, find_dotenv

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    ModelSettings,

)

load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)

# Environment & Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/"

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# Model Configuration
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", openai_client=external_client
)

user_query = input("Enter your query: ")

agent: Agent = Agent(
    name="Deep Research Agent",
    model=model,
    instructions="Helpful assistant",
    model_settings=ModelSettings(
        temperature=1.0,
        max_tokens=1000
        # removed tool_choice
    )
)


try:
    result = Runner.run_sync(agent, user_query)
    print("\nCALLING AGENT\n")
    print(result.final_output)
except Exception as e:
    print("Agent error:", e)

print("\nCALLING AGENT\n")
print(result.final_output)