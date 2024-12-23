import os
import json
import requests
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
load_dotenv()

# Fetch API key from environment variables
api_key = os.getenv("SERPER_API_KEY")
if not api_key:
    raise ValueError("API key is missing in the .env file")

# Configure the search tool with SerperDevTool
Web_tool = SerperDevTool(
    search_url="https://google.serper.dev/search",  # Correct URL for Serper API
    n_results=2,
    location="Bengaluru",
    api_key=api_key
)
