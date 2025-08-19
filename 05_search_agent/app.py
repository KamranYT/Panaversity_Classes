import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool

# 🔧 Load environment variables
load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)

# 🔑 API Key for Gemini
gemini_api_key = os.environ.get("GEMINI_API_KEY")

# 🌐 Set up Gemini LLM Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 🤖 Gemini Chat Model
llm_model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model="gemini-2.5-flash"
)

# 🛠️ Tool: Read Kamran's Portfolio
@function_tool()
def read_portfolio(path: str = "/") -> str:
    """
    Fetch and extract readable text from Kamran's portfolio site.
    Example usage: read_portfolio("/") or read_portfolio("/projects")
    """
    base_url = "https://mk02-portfolio.vercel.app"
    full_url = f"{base_url}{path}"
    print(f"[TOOL] Fetching content from: {full_url}")

    try:
        res = requests.get(full_url, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return clean_text[:2000]  # Limit to 2000 characters
    except Exception as e:
        return f"Error fetching portfolio content: {str(e)}"

# 🤖 Agent using only the read_portfolio tool
agent = Agent(
    name="Portfolio Reader",
    model=llm_model,
    tools=[read_portfolio],
)

# 🧪 Run a test message
runner = Runner.run_sync(agent, "Turn Kamran’s homepage into a tweet thread.")
print("\n🤖 Gemini:\n", runner.final_output)
