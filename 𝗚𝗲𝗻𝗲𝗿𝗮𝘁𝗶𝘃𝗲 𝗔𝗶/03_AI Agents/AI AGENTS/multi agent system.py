
import os
import json
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

load_dotenv()

st.title("Multi Agent System")

# 1. Initialize LLM

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# 2. Initialize Agents

search_tool = TavilySearch(max_results=5)

def researcher_agent(question):

    response = search_tool.invoke({"query": question})

    context = ""

    for result in response["results"]:
        context += f"""
        Title: {result['title']}
        URL: {result['url']}
        Content: {result['content']}
        """

    answer = llm.invoke(f"""
    Answer the question using these search results.

    Question: {question}

    Search Results:
    {context}
    """)

    return answer.content


def weather_agent(location):

    url = "https://api.openweathermap.org/data/2.5/weather"

    response = requests.get(url, params={
        "q": location,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    })

    data = response.json()

    weather_data = f"""
    City: {data['name']}
    Temperature: {data['main']['temp']} °C
    Humidity: {data['main']['humidity']}%
    Weather: {data['weather'][0]['description']}
    """

    answer = llm.invoke(f"""
    Explain this weather information clearly:

    {weather_data}
    """)

    return answer.content


# 3. LLM Router

def router(question):

    prompt = f"""
    Classify the user question into one of these:

    normal: General questions
    research: Questions requiring internet search
    weather: Weather related questions

    Return ONLY JSON:

    {{
        "action": "normal",
        "location": null
    }}

    If weather, extract the city name.

    Question: {question}
    """

    response = llm.invoke(prompt)

    return json.loads(response.content)


# 4. User Input

question = st.chat_input("Ask your question")

if question:

    st.chat_message("user").write(question)

    decision = router(question)

    action = decision["action"]

    if action == "normal":

        answer = llm.invoke(question)
        st.chat_message("assistant").write(answer.content)

    elif action == "research":

        if st.button("Allow Researcher Agent?"):

            answer = researcher_agent(question)
            st.write(answer)

    elif action == "weather":

        if st.button("Allow Weather Agent?"):

            answer = weather_agent(decision["location"])
            st.write(answer)
