# Project: AI Research & Content Generator
# 
# Objective: The AI researches a topic, generates structured content, and asks a human to approve it before producing the final output.


#Archeitrecture :

"""
# Human-in-the-Loop (HITL) Sequential Workflow

START
   |
   v
User provides a topic
   |
   v
**research_node**
Research the given topic using an LLM
   |
   v
**content_node**
Generate structured content
   |
   v
**human_review_node**
HITL — interrupt()
Human reviews the generated content
   |
   v
  Decision
   |
   ├── Approved ──> **final_node** ──> END
   |
   └── Rejected ──> **revise_node**
                         |
                         v
                  **human_review_node**
                         |
                         v
                      Decision"""



#---------------------------------------------------------------------------------



import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# Initialize Tavily Search
search_tool = TavilySearch(
    max_results=5
)


# ==========================================
# 2. DEFINE WORKFLOW STATE
# ==========================================

class ContentState(TypedDict):
    topic: str
    research: str
    draft: str
    decision: str
    feedback: str
    final_content: str


# ==========================================
# 3. DEFINE WORKFLOW NODES
# ==========================================

# Research Node
def research_node(state: ContentState):

    print("\nResearching topic...")

    topic = state["topic"]

    results = search_tool.invoke({
        "query": topic
    })

    return {
        "research": str(results)
    }


# Content Generation Node
def content_node(state: ContentState):

    print("\nGenerating LinkedIn post...")

    prompt = f"""
    You are a professional LinkedIn content writer.

    Topic:
    {state["topic"]}

    Research:
    {state["research"]}

    Generate an engaging and informative LinkedIn post.

    Include:
    - A strong opening hook
    - Valuable insights
    - Clear explanations
    - A meaningful conclusion
    - Relevant hashtags
    """

    response = llm.invoke(prompt)

    return {
        "draft": response.content
    }


# Human Review Node
def human_review_node(state: ContentState):

    print("\nWaiting for human approval...")

    human_response = interrupt({
        "message": "Review the generated LinkedIn post.",
        "draft": state["draft"],
        "options": ["approve", "reject"]
    })

    return {
        "decision": human_response["decision"],
        "feedback": human_response.get("feedback", "")
    }


# Revision Node
def revise_node(state: ContentState):

    print("\nRevising content using human feedback...")

    prompt = f"""
    Previous LinkedIn post:
    {state["draft"]}

    Human feedback:
    {state["feedback"]}

    Revise the LinkedIn post according to the feedback.
    Return only the improved post.
    """

    response = llm.invoke(prompt)

    return {
        "draft": response.content
    }


# Final Node
def final_node(state: ContentState):

    print("\nContent approved successfully!")

    return {
        "final_content": state["draft"]
    }


# ==========================================
# 4. CONDITIONAL ROUTING
# ==========================================

def route_after_review(state: ContentState):

    if state["decision"] == "approve":
        return "approved"

    return "revise"


# ==========================================
# 5. BUILD LANGGRAPH WORKFLOW
# ==========================================

workflow = StateGraph(ContentState)

# Register nodes
workflow.add_node("research", research_node)
workflow.add_node("generate", content_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("revise", revise_node)
workflow.add_node("final", final_node)


# Sequential connections
workflow.add_edge(START, "research")
workflow.add_edge("research", "generate")
workflow.add_edge("generate", "human_review")


# Conditional connections
workflow.add_conditional_edges(
    "human_review",
    route_after_review,
    {
        "approved": "final",
        "revise": "revise"
    }
)

# Revision returns to human review
workflow.add_edge("revise", "human_review")

# Final connection
workflow.add_edge("final", END)


# ==========================================
# 6. COMPILE WITH CHECKPOINTER
# ==========================================

memory = MemorySaver()

graph = workflow.compile(
    checkpointer=memory
)


# ==========================================
# 7. INITIALIZE WORKFLOW
# ==========================================

config = {
    "configurable": {
        "thread_id": "content-001"
    }
}

initial_state = {
    "topic": "The Future of Artificial Intelligence",
    "research": "",
    "draft": "",
    "decision": "",
    "feedback": "",
    "final_content": ""
}


# ==========================================
# 8. EXECUTE WORKFLOW
# ==========================================

result = graph.invoke(
    initial_state,
    config=config
)


# ==========================================
# 9. HUMAN APPROVAL AND RESUMPTION
# ==========================================

while graph.get_state(config).next:

    # Display interrupted draft
    snapshot = graph.get_state(config)

    print("\n" + "=" * 50)
    print("GENERATED LINKEDIN POST")
    print("=" * 50)

    print(snapshot.values["draft"])

    print("\n1. Approve")
    print("2. Reject")

    choice = input("\nEnter your choice (1/2): ")

    if choice == "1":

        response = {
            "decision": "approve",
            "feedback": ""
        }

    elif choice == "2":

        feedback = input(
            "\nWhat changes do you want? "
        )

        response = {
            "decision": "reject",
            "feedback": feedback
        }

    else:

        print("Invalid choice. Try again.")
        continue

    # Resume interrupted workflow
    result = graph.invoke(
        Command(resume=response),
        config=config
    )


# ==========================================
# 10. DISPLAY FINAL CONTENT
# ==========================================

print("\n" + "=" * 50)
print("FINAL APPROVED LINKEDIN POST")
print("=" * 50)

print(result["final_content"])
