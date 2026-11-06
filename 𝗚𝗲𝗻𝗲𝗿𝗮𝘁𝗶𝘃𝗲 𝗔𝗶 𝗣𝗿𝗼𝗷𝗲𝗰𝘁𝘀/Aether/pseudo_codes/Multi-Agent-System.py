import os
from dotenv import load_dotenv

import json
import streamlit as st


load_dotenv()

st.write("Multi Agent System")

#1 we need to create our researcher bot/agent


from langchain_tavily import TavilySearch

tavily_api = os.getenv("TAVILY_API_KEY")


search_tool = TavilySearch(
    max_results = 5)


question = st.chat_input("Ask your Question Here : ")

if question:
    st.chat_message("user").write(question)
    
    response = search_tool.invoke({"query" : question})
    
    with st.chat_message("assistant"):

        for i, result in enumerate(response["results"], start=1):

            st.write(f"### Search Result {i}")

            st.write("**Title:**", result["title"])
            st.write("**URL:**", result["url"])
            st.write("**Description:**", result["content"])

            st.divider()

