import os
import json
import requests
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment variables
api_key = os.getenv("SERPER_API_KEY")
if not api_key:
    raise ValueError("API key is missing in the .env file")

# Debug: Print the API key
# print("Loaded API Key:", api_key)

# Configure the search tool with SerperDevTool
Web_tool = SerperDevTool(
    search_url="https://google.serper.dev/search",  # Correct URL for Serper API
    n_results=2,
    location="Bengaluru",
    api_key=api_key
)

# Perform a search query using SerperDevTool
# try:
#     search_query = "apple inc"
#     print(f"Executing search query: {search_query}")
#     results = Web_tool.run(search_query=search_query)
    
#     # Debug: Check if results are empty
#     if not results:
#         print("No results returned. Check API key or query.")
#     else:
#         print("Search Results:")
#         print(json.dumps(results, indent=2))
# except requests.exceptions.RequestException as e:
#     print(f"HTTP request error: {e}")
# except Exception as e:
#     print(f"An error occurred: {e}")
