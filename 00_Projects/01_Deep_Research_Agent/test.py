import os
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

response = tavily_client.search("Agentic Ai", max_results=1)
    
print("[TOOL...]Search completed.", response)