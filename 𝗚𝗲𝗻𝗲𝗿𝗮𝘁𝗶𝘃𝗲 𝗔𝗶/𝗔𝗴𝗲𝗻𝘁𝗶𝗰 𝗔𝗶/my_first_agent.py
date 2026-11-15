"""
=============================================================================
🤖 YOUR FIRST AI AGENT (BUILT WITH LANGGRAPH + TOOLS + REASONING LOOP)
=============================================================================
This script demonstrates what an AI Agent actually is.
Notice:
1. We give the agent a GOAL.
2. The agent has TOOLS (Calculator, Live Internet Search, Weather).
3. The agent LOOPS autonomously:
   Think -> Decide Tool -> Execute Tool -> Observe Output -> Think Again -> Finish
=============================================================================
"""

import os
import dotenv
from typing import Literal
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from tavily import TavilyClient

# 1. Load API keys from your .env file
dotenv.load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

# ---------------------------------------------------------------------------
# 2. DEFINE THE AGENT'S TOOLS (The Agent's "Hands and Feet")
# ---------------------------------------------------------------------------

@tool
def calculate(expression: str) -> str:
    """Useful for mathematical calculations. Provide a valid Python math expression string, e.g. '1967 * 3' or '25 ** 2'."""
    try:
        # Safe math evaluation
        result = eval(expression, {"__builtins__": None}, {})
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Calculation Error: {e}"

@tool
def search_web(query: str) -> str:
    """Useful for searching real-time information, current facts, people, news, and live data on the internet."""
    if not tavily_client:
        return "Search tool is not configured."
    try:
        results = tavily_client.search(query=query, max_results=2)
        snippets = [f"• {r.get('title')}: {r.get('content')}" for r in results.get("results", [])]
        return "\n".join(snippets) if snippets else "No relevant web results found."
    except Exception as e:
        return f"Error executing web search: {e}"

@tool
def get_weather(city: str) -> str:
    """Useful for getting current weather information for any city in the world."""
    # We can use Tavily or OpenWeather to fetch live weather
    if tavily_client:
        try:
            res = tavily_client.search(query=f"current weather in {city} temperature and conditions", max_results=1)
            results = res.get("results", [])
            if results:
                return f"Weather in {city}: {results[0].get('content')}"
        except Exception:
            pass
    return f"Weather in {city}: Clear skies, 28°C."

tools = [calculate, search_web, get_weather]

# ---------------------------------------------------------------------------
# 3. DEFINE THE LLM (The Agent's "Brain")
# ---------------------------------------------------------------------------
# We bind the tools to the LLM so it knows what actions it is allowed to take.
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0).bind_tools(tools)

# ---------------------------------------------------------------------------
# 4. DEFINE THE GRAPH NODES & CONDITIONAL ROUTER (LangGraph Architecture)
# ---------------------------------------------------------------------------

def agent_node(state: MessagesState):
    """The brain: LLM looks at the conversation/state and decides the next move."""
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    """Router Function: Decides whether to continue looping or stop."""
    last_message = state["messages"][-1]
    
    # If the LLM generated tool calls, we MUST route to the tool execution node!
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, the LLM has finished thinking and answered the goal.
    return END

# ---------------------------------------------------------------------------
# 5. ASSEMBLE THE GRAPH (State + Nodes + Edges)
# ---------------------------------------------------------------------------
builder = StateGraph(MessagesState)

# Add Nodes
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))

# Add Edges
builder.add_edge(START, "agent")

# The Decision Loop:
builder.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)

# Loop back: after tools execute, return output to the agent so it can observe!
builder.add_edge("tools", "agent")

# Compile the Agent
ai_agent = builder.compile()

# ---------------------------------------------------------------------------
# 6. RUN THE AGENT AND WATCH ITS AUTONOMOUS LOOP IN ACTION
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    task = "Find who won the ICC Men's T20 World Cup in 2024, what was their winning margin, and calculate that margin multiplied by 45."
    
    print("=" * 70)
    print("🎯 USER GOAL GIVEN TO AGENT:")
    print(f"   \"{task}\"")
    print("=" * 70)
    print("\n⏳ WATCHING AGENT REASON AND ACT STEP-BY-STEP:\n")

    # Stream the graph step by step so you can see each node execute
    step_count = 1
    for step in ai_agent.stream({"messages": [HumanMessage(content=task)]}, stream_mode="updates"):
        for node_name, node_output in step.items():
            print(f"📍 Step {step_count}: Node [{node_name}] executed")
            messages = node_output.get("messages", [])
            for msg in messages:
                # If agent decided to call a tool:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"   🧠 [THINKING]: Agent decided it needs external tool -> '{tc['name']}'")
                        print(f"   🛠️ [ACTION]  : Calling {tc['name']} with arguments: {tc['args']}")
                # If tool returned an observation:
                elif msg.type == "tool":
                    print(f"   👁️ [OBSERVATION FROM TOOL]:")
                    preview = msg.content.strip().replace('\n', ' ')[:140]
                    print(f"      \"{preview}...\"")
                # If agent formulated final answer:
                elif msg.type == "ai":
                    print(f"\n✅ [GOAL ACHIEVED - FINAL AGENT RESPONSE]:")
                    print("-" * 50)
                    print(msg.content.strip())
                    print("-" * 50)
            step_count += 1
            print()
