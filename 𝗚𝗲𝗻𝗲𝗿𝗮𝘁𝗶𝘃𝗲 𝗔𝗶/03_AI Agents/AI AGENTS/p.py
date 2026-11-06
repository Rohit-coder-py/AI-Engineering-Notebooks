import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

load_dotenv()

# ---------- Setup ----------
llm = ChatGroq(model="llama-3.3-70b-versatile")   # koi bhi LLM laga sakte ho
search_tool = TavilySearch(max_results=3)
weather_key = os.getenv("OPENWEATHER_API_KEY")


# ---------- Agents (simple functions) ----------
def search_agent(query):
    response = search_tool.invoke({"query": query})
    text = ""
    for r in response["results"]:
        text += f"**{r['title']}**\n{r['url']}\n{r['content']}\n\n"
    return text


def weather_agent(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    data = requests.get(url, params={"q": city, "appid": weather_key, "units": "metric"}).json()
    if data.get("cod") != 200:
        return f"Weather nahi mila: {data.get('message')}"
    return (
        f"**{city}** ka weather: {data['weather'][0]['description']}, "
        f"temp {data['main']['temp']}°C, "
        f"humidity {data['main']['humidity']}%, "
        f"wind {data['wind']['speed']} m/s"
    )


# ---------- Router: LLM decide karega ----------
def decide(question):
    prompt = f"""You are a router. Decide how to handle the user's question.
Reply ONLY with JSON, nothing else.

- Weather of a city -> {{"agent": "weather", "input": "<city name>"}}
- Needs latest/live info from the internet -> {{"agent": "search", "input": "<search query>"}}
- Normal question you can answer yourself -> {{"agent": "chat", "input": ""}}

Question: {question}"""
    reply = llm.invoke(prompt).content
    try:
        return json.loads(reply.strip().strip("`").replace("json", "", 1))
    except Exception:
        return {"agent": "chat", "input": ""}   # parse fail ho to normal chat


def run_agent(agent, agent_input):
    if agent == "weather":
        return weather_agent(agent_input)
    return search_agent(agent_input)


# ---------- UI ----------
st.title("Multi Agent System")

if "pending" not in st.session_state:
    st.session_state.pending = None

question = st.chat_input("Ask your Question Here : ")

if question:
    st.session_state.pending = None
    decision = decide(question)

    if decision["agent"] == "chat":
        st.chat_message("user").write(question)
        st.chat_message("assistant").write(llm.invoke(question).content)
    else:
        # agent chalane se pehle permission ke liye save kar lo
        st.session_state.pending = {
            "question": question,
            "agent": decision["agent"],
            "input": decision["input"],
        }

# ---------- Permission block ----------
p = st.session_state.pending
if p:
    st.chat_message("user").write(p["question"])

    with st.chat_message("assistant"):
        st.write(f"Iske liye mujhe **{p['agent']} agent** use karna hoga (`{p['input']}`). Allow?")
        col1, col2 = st.columns(2)
        yes = col1.button("Yes")
        no = col2.button("No")

        if yes:
            st.write(run_agent(p["agent"], p["input"]))
            st.session_state.pending = None
        elif no:
            st.write(llm.invoke(p["question"]).content)
            st.session_state.pending = None