
# ============================================================
# HUMAN-IN-THE-LOOP (HITL) APPROVAL SYSTEM
# ============================================================

# -------------------------
# 1. Import Libraries
# -------------------------

from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Import Groq LLM
from langchain_groq import ChatGroq

# Import tool decorator
# @tool converts a normal Python function into a LangChain Tool
from langchain.tools import tool

# ToolMessage is used to return a response from a tool call
from langchain_core.messages import ToolMessage

# Import LangChain agent creator
from langchain.agents import create_agent

# Import middleware decorator
from langchain.agents.middleware import wrap_tool_call

# Rich is used for colorful terminal output
from rich import print


# ============================================================
# 2. CREATE WEATHER TOOL
# ============================================================

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather of an Indian city.
    """

    # Get API key from .env file
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # Create API URL
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    # Send GET request to OpenWeather API
    response = requests.get(url, timeout=15)

    # Convert API response into Python dictionary
    data = response.json()

    # Check whether API request was successful
    if str(data.get("cod")) != "200":
        return f"Weather error: {data.get('message')}"

    # Extract temperature and weather description
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]

    # Return weather information
    return (
        f"Weather in {city}: "
        f"{description}, {temperature}°C"
    )


# ============================================================
# 3. CREATE NEWS TOOL
# ============================================================

# Import Tavily
from tavily import TavilyClient

# Initialize Tavily using API key
tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """
    Get the latest news about an Indian city.
    """

    # Search the internet using Tavily
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    # Extract search results
    results = response.get("results", [])

    # If no results are found
    if not results:
        return f"No news found for {city}"

    # Create an empty list to store news
    news_list = []

    # Process every search result
    for result in results:

        # Extract title, URL and summary
        title = result.get("title", "No title")
        url = result.get("url", "")
        summary = result.get("content", "")

        # Add information to the list
        news_list.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Summary: {summary[:150]}"
        )

    # Return all news results
    return "\n\n".join(news_list)


# ============================================================
# 4. INITIALIZE GROQ LLM
# ============================================================

llm = ChatGroq(

    # Model used by the agent
    model="openai/gpt-oss-20b",

    # Temperature 0 means more consistent responses
    temperature=0
)


# ============================================================
# 5. HUMAN APPROVAL MIDDLEWARE
# ============================================================

@wrap_tool_call
def human_approval(request, handler):
    """
    This middleware asks the human for permission
    before executing any tool.
    """

    # Get the name of the tool the AI wants to execute
    tool_name = request.tool_call["name"]

    # Get the arguments the AI wants to pass
    tool_args = request.tool_call["args"]

    # Display the tool call to the human
    print("\n[bold yellow]APPROVAL REQUIRED[/bold yellow]")

    print(f"Tool: {tool_name}")
    print(f"Arguments: {tool_args}")

    # Ask the human for approval
    approval = input(
        "\nDo you want to allow this tool? (yes/no): "
    )

    # If human denies the request
    if approval.lower().strip() != "yes":

        print("[bold red]Tool execution DENIED![/bold red]")

        # Return a ToolMessage instead of executing the tool
        return ToolMessage(
            content="The user denied this tool call.",
            tool_call_id=request.tool_call["id"]
        )

    # If human approves the request
    print("[bold green]Tool execution APPROVED![/bold green]")

    # Execute the actual tool
    return handler(request)


# ============================================================
# 6. CREATE AI AGENT
# ============================================================

agent = create_agent(

    # Give the agent its LLM
    model=llm,

    # Give the agent access to these tools
    tools=[
        get_weather,
        get_news
    ],

    # Define the agent's behaviour
    system_prompt="""
    You are a helpful Indian city assistant.

    You can:
    1. Check weather using get_weather.
    2. Find latest news using get_news.

    Use tools whenever necessary.
    Give clear and simple answers.
    """,

    # Register our human approval middleware
    middleware=[
        human_approval
    ]
)


# ============================================================
# 7. CHAT LOOP
# ============================================================

print("\n[bold green]HUMAN APPROVAL CITY AGENT[/bold green]")

print("Type 'exit' to stop the agent.")

while True:

    # Take user input
    user_input = input("\nYou: ")

    # Stop the program if user types exit
    if user_input.lower().strip() == "exit":
        print("Goodbye!")
        break

    # Send user message to the agent
    result = agent.invoke({

        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]

    })

    # Display final AI response
    print("\n[bold cyan]AI Agent:[/bold cyan]")

    print(result["messages"][-1].content)

