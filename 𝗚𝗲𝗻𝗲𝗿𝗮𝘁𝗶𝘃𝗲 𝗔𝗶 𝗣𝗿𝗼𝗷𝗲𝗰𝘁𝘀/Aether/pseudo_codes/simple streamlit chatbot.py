import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

st.title("Groq Chatbot")

question = st.chat_input("Ask anything...")

if question:

    st.chat_message("user").write(question)

    response = llm.invoke(question)

    st.chat_message("assistant").write(response.content)