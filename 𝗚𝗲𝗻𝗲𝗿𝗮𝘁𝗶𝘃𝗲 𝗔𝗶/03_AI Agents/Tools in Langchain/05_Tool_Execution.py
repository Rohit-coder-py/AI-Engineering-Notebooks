import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# Loading environment variables
load_dotenv()

# Initializing LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)


# 1. TOOL BUILDING

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


# 2. TOOL BINDING WITH LLM

llm_with_tools = llm.bind_tools([multiply])


# 3. TOOL CALLING

messages = [
    HumanMessage(content="What is 25 multiplied by 40?")
]

response = llm_with_tools.invoke(messages)

print("Tool Calls:", response.tool_calls)


# 4. TOOL EXECUTION

messages.append(response)

for tool_call in response.tool_calls:

    if tool_call["name"] == "multiply":

        result = multiply.invoke(tool_call["args"])

        print("Tool Result:", result)

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )


# Sending tool result back to LLM

final_response = llm_with_tools.invoke(messages)

print("\nFinal Answer:")
print(final_response.content)

#==========================================================
ress = multiply.invoke({"a": 10, "b": 90})

print(ress)











# ====================================================
# cretaing multiple tools

#========================================================


import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

# Initializing LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)


# 1. TOOL BUILDING

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract the second number from the first number."""
    return a - b


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        return "Cannot divide by zero"
    return a / b


@tool
def get_text_length(text: str) -> int:
    """Return the number of characters in a text."""
    return len(text)


# 2. TOOL BINDING WITH LLM

tools = [multiply, add, subtract, divide, get_text_length]

llm_with_tools = llm.bind_tools(tools)


# Creating a tool registry
tool_registry = {
    tool.name: tool for tool in tools
}


# 3. TOOL CALLING

messages = [
    HumanMessage(
        content="Multiply 25 by 40 and also calculate the length of 'LangChain'."
    )
]

response = llm_with_tools.invoke(messages)

print("Tool Calls:", response.tool_calls)


# 4. TOOL EXECUTION

messages.append(response)

for tool_call in response.tool_calls:

    selected_tool = tool_registry[tool_call["name"]]

    result = selected_tool.invoke(tool_call["args"])

    print(f"\nTool Name: {tool_call['name']}")
    print("Tool Result:", result)

    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )
    )


# Sending tool results back to LLM

final_response = llm_with_tools.invoke(messages)

print("\nFinal Answer:")
print(final_response.content)




print("-"*8)
print(tool_registry)