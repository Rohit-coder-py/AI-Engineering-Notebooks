import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from rich import print

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

#create custom tool
@tool
def char_length(text:str) -> int :
    """Returns the number of character"""
    return len(text)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

#lets bind the tool to llm

llm_bind =llm.bind_tools([char_length])


res = llm_bind.invoke("hello")

print(res)