import os
from dotenv import load_dotenv

from langchain_tavily import TavilySearch

load_dotenv()

# Initialize Tavily Search
search_tool = TavilySearch(
    max_results=5)

# Execute search
response = search_tool.invoke({
    "query": "Latest developments in Artificial Intelligence"
})

print(response)


for result in response["results"]:

    print("Title:", result["title"])

    print("URL:", result["url"])

    print("Content:", result["content"])

    print("Score:", result["score"])

    print("-" * 60)
    
    
    
    
    
    
    
print("-" * 60)
print("/n")

print(response["results"][0]["title"])
print("-" * 60)

print(response["results"][0]["content"])