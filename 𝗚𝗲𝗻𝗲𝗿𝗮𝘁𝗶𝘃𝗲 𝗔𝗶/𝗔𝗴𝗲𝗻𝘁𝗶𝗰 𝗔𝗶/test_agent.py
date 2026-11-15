import os
import dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from tavily import TavilyClient

dotenv.load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def calculate(expression: str) -> str:
    """Useful for mathematical calculations. Provide a valid Python math expression like '25 * 40'."""
    try:
        # safely evaluate expression with math operations
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error calculating: {e}"

@tool
def search_web(query: str) -> str:
    """Useful for searching real-time information, current facts, people, news, and weather on the internet."""
    try:
        results = tavily_client.search(query=query, max_results=2)
        snippets = [f"- {r['title']}: {r['content']}" for r in results.get("results", [])]
        return "\n".join(snippets) if snippets else "No results found."
    except Exception as e:
        return f"Search error: {e}"

tools = [calculate, search_web]
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

agent = create_react_agent(model, tools)

print("--- Running AI Agent on complex multi-step question ---")
question = "Who is the current CEO of Microsoft, what year was he born, and what is his birth year multiplied by 3?"
print(f"Goal: {question}\n")

result = agent.invoke({"messages": [("user", question)]})

for message in result["messages"]:
    if hasattr(message, "tool_calls") and message.tool_calls:
        for tc in message.tool_calls:
            print(f"🛠️ [Agent Decided To Call Tool]: {tc['name']} with args {tc['args']}")
    elif message.type == "tool":
        print(f"👁️ [Observation from Tool]: {message.content[:150]}...")
    elif message.type == "ai":
        print(f"\n🧠 [Agent Response]:\n{message.content}")
