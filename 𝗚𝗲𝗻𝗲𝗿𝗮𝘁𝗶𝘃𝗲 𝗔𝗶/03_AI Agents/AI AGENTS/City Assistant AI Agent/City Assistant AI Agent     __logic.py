from dotenv import load_dotenv
import os
import requests

load_dotenv()

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

from rich import print
from tavily import TavilyClient


@tool
def get_weather(city: str) -> str:
    """Get the current weather of an Indian city."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    response = requests.get(url, timeout=15)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Weather error: {data.get('message')}"

    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]

    return f"Weather in {city}: {description}, {temperature}°C"


tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get the latest news about an Indian city."""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for result in results:
        title = result.get("title", "No title")
        url = result.get("url", "")
        summary = result.get("content", "")

        news_list.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Summary: {summary[:150]}"
        )

    return "\n\n".join(news_list)


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


@wrap_tool_call
def human_approval(request, handler):

    tool_name = request.tool_call["name"]
    tool_args = request.tool_call["args"]

    print("\n[bold yellow]APPROVAL REQUIRED[/bold yellow]")

    print(f"Tool: {tool_name}")
    print(f"Arguments: {tool_args}")

    approval = input(
        "\nDo you want to allow this tool? (yes/no): "
    )

    if approval.lower().strip() != "yes":

        print("[bold red]Tool execution DENIED![/bold red]")

        return ToolMessage(
            content="The user denied this tool call.",
            tool_call_id=request.tool_call["id"]
        )

    print("[bold green]Tool execution APPROVED![/bold green]")

    return handler(request)


agent = create_agent(
    model=llm,
    tools=[
        get_weather,
        get_news
    ],
    system_prompt="""
    You are a helpful Indian city assistant.

    You can:
    1. Check weather using get_weather.
    2. Find latest news using get_news.

    Use tools whenever necessary.
    Give clear and simple answers.
    """,
    middleware=[
        human_approval
    ]
)


print("\n[bold green]HUMAN APPROVAL CITY AGENT[/bold green]")
print("Type 'exit' to stop the agent.")

while True:

    user_input = input("\nYou: ")

    if user_input.lower().strip() == "exit":
        print("Goodbye!")
        break

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    print("\n[bold cyan]AI Agent:[/bold cyan]")
    print(result["messages"][-1].content)