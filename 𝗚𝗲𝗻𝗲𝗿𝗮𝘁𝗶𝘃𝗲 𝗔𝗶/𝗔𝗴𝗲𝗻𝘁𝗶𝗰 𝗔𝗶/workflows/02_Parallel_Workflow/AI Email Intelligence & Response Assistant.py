### Project Overview :

# Input: An email.
# 
# Three agents execute simultaneously:

# - Intent Agent: Identifies the purpose of the email.
# - Priority Agent: Evaluates urgency and importance.
# - Response Agent: Generates a suitable response draft.



# Final Output: Email summary, priority level and suggested reply.



# ======================================================



import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START , END

load_dotenv()

#llm

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7)

