"""
create_agent is a high-level abstraction provided by LangChain that automates everything
we manually implemented in our agent. Instead of writing the loop, handling tool calls,
managing messages, and deciding when to stop, we simply define the model and the tools, and
the framework takes care of the entire execution process internally. The core logic remains the
same the LLM still decides which tool to use, tools still fetch external data, and results are
passed back for final response generation but all of this happens behind the scenes. The main
difference is that our manual approach gives full control and visibility over each step, while
create_agent hides this complexity to make development faster, cleaner, and easier to scale.

"""

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


