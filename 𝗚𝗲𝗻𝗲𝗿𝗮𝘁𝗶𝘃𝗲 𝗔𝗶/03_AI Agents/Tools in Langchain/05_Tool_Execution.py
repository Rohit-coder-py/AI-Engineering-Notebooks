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


ress = multiply.invoke({"a": 10, "b": 90})

print(ress)