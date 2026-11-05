# ============================================================
# HUMAN-IN-THE-LOOP (HITL) APPROVAL CITY AGENT - STREAMLIT UI
# Run with:  streamlit run app.py
# ============================================================

# -------------------------
# 1. Import Libraries
# -------------------------

from dotenv import load_dotenv
import os
import threading
import time
import requests
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Import Groq LLM
from langchain_groq import ChatGroq

# @tool converts a normal Python function into a LangChain Tool
from langchain.tools import tool

# ToolMessage is used to return a response from a tool call
from langchain_core.messages import ToolMessage

# Import LangChain agent creator
from langchain.agents import create_agent

# Import middleware decorator
from langchain.agents.middleware import wrap_tool_call

# Import Tavily
from tavily import TavilyClient


# ============================================================
# 2. PAGE CONFIG
# ============================================================

st.set_page_config(page_title="City Assistant Agent", page_icon="🏙️")


# ============================================================
# 3. APPROVAL GATE
# Streamlit has no terminal input(), so the middleware waits
# on this shared gate until the user clicks Approve / Deny.
# ============================================================

class ApprovalGate:
    def __init__(self):
        self.pending = None              # tool call waiting for a decision
        self.event = threading.Event()   # set when the user decides
        self.approved = False            # the user's decision


@st.cache_resource
def get_gate():
    return ApprovalGate()


gate = get_gate()


# ============================================================
# 4. TOOLS
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
# 5. HUMAN APPROVAL MIDDLEWARE
# ============================================================

@wrap_tool_call
def human_approval(request, handler):
    """
    This middleware asks the human for permission
    before executing any tool.
    """

    # Get the name and arguments of the tool the AI wants to execute
    tool_name = request.tool_call["name"]
    tool_args = request.tool_call["args"]

    # Show the request in the UI and wait for the human's decision
    gate.event.clear()
    gate.pending = {"name": tool_name, "args": tool_args}
    gate.event.wait()

    # If human denies the request
    if not gate.approved:
        return ToolMessage(
            content="The user denied this tool call.",
            tool_call_id=request.tool_call["id"]
        )

    # If human approves the request, execute the actual tool
    return handler(request)


# ============================================================
# 6. CREATE AI AGENT (built once and cached)
# ============================================================

@st.cache_resource
def build_agent():
    llm = ChatGroq(

        # Model used by the agent
        model="openai/gpt-oss-20b",

        # Temperature 0 means more consistent responses
        temperature=0
    )

    return create_agent(
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


agent = build_agent()


# ============================================================
# 7. BACKGROUND RUNNER
# The agent runs in a thread so the UI can show the approval
# prompt while the agent is paused inside the middleware.
# ============================================================

def run_agent(user_input, job):
    try:
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        })
        job["answer"] = result["messages"][-1].content
    except Exception as e:
        job["answer"] = f"Error: {e}"


# ============================================================
# 8. UI
# ============================================================

st.title("🏙️ Human Approval City Agent")
st.caption("Ask about weather or news of an Indian city. Every tool call needs your approval.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "job" not in st.session_state:
    st.session_state.job = None

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

job = st.session_state.job

# Chat input (disabled while the agent is working)
user_input = st.chat_input("Ask something...", disabled=job is not None)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    gate.pending = None
    job = {"answer": None}
    job["thread"] = threading.Thread(target=run_agent, args=(user_input, job), daemon=True)
    job["thread"].start()
    st.session_state.job = job
    st.rerun()

# Handle a running job
if job is not None:
    if job["thread"].is_alive():

        # Agent is waiting for human approval
        if gate.pending:
            with st.chat_message("assistant"):
                st.warning("APPROVAL REQUIRED")
                st.write(f"**Tool:** {gate.pending['name']}")
                st.write(f"**Arguments:** {gate.pending['args']}")
                st.write("Do you want to allow this tool?")

                col1, col2 = st.columns(2)
                if col1.button("✅ Yes, allow", use_container_width=True):
                    gate.approved = True
                    gate.pending = None
                    gate.event.set()
                    st.rerun()
                if col2.button("❌ No, deny", use_container_width=True):
                    gate.approved = False
                    gate.pending = None
                    gate.event.set()
                    st.rerun()
        else:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    time.sleep(0.4)
            st.rerun()

    else:
        # Agent finished - show the final AI response
        st.session_state.messages.append({"role": "assistant", "content": job["answer"]})
        st.session_state.job = None
        st.rerun()