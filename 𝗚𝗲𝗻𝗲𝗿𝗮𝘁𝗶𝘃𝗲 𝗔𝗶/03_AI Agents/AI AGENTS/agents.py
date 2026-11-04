
import os
import requests

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_tavily import TavilySearch

load_dotenv()

# Initializing LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)


# ==========================================
# 1. TOOL BUILDING
# ==========================================

# Initializing Tavily
tavily = TavilySearch(max_results=5)


@tool
def tavily_search(query: str):
    """Search the internet for latest news and information about a city."""
    return tavily.invoke({"query": query})


@tool
def get_weather(city: str):
    """Get current weather information for a given city using OpenWeatherMap."""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        return f"Weather API error: {response.text}"

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


# Testing tools individually
print(tavily_search.invoke({"query": "Latest news in Lucknow"}))

print(get_weather.invoke({"city": "Lucknow"}))
