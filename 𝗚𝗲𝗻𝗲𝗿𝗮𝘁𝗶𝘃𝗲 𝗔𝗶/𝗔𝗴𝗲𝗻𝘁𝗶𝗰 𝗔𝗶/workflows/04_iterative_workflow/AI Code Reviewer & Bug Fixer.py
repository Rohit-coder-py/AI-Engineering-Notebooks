"""
AI Code Reviewer & Bug Fixer
My top recommendation
- Review submitted code.
- Identify bugs and code-quality issues.
- Generate fixes.
- Run tests and improve code until tests pass.
"""

#we will use 2 models for this project

# 1.  Grok - to generate
# 2. Mistral - to review
# =======================================

import os
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode


load_dotenv()


#basic settings
grok_api_key = os.getenv("GROQ_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")



writer_llm = ChatGroq(model="openai/gpt-oss-20b",api_key=grok_api_key,temperature = 0.2)

reviewer_mistral = ChatMistralAI(model="mistral-small-latest",api_key=mistral_api_key,temperature=0.1)

search_tool = TavilySearch(
    max_results=3,
    api_key=tavily_api_key)



tools = [search_tool]

writer_llm_with_tools = writer_llm.bind_tools(tools)


#now lets create a state


class CodeState(TypedDict):
    code : str
    messages : Annotated[lsit , add_messages]
    
