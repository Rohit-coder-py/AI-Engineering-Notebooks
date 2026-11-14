# Conditional edges allow LangGraph to decide which node should execute next based on the output of a routing function.

#lets learn about routers

# Way 1 — Rule-based Router (Python Logic)
# 
# Beginner-friendly
# In this approach, you write the routing conditions yourself using Python.
# 
# The LLM is not involved in making the routing decision.


# Example project: Customer Support Router

# Imagine a customer sends a message:
# - "My payment failed" → Payment Support
# - "I want to return my product" → Refund Support
# - "Where is my order?" → Order Tracking



# ============================================================
# LANGGRAPH: RULE-BASED CONDITIONAL ROUTER
# ============================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ------------------------------------------------------------
# 1. DEFINE STATE
# ------------------------------------------------------------

class SupportState(TypedDict):
    query: str
    category: str
    response: str


# ------------------------------------------------------------
# 2. CREATE NODES
# ------------------------------------------------------------

def payment_support(state: SupportState):

    print("Payment Support Activated")

    return {
        "response": "We will help you resolve your payment issue."
    }


def refund_support(state: SupportState):

    print("Refund Support Activated")

    return {
        "response": "We will help you with your refund."
    }


def order_support(state: SupportState):

    print("Order Support Activated")

    return {
        "response": "Here is your order tracking assistance."
    }


def general_support(state: SupportState):

    print("General Support Activated")

    return {
        "response": "How can we help you?"
    }


# ------------------------------------------------------------
# 3. CREATE ROUTER FUNCTION
# ------------------------------------------------------------

def router(state: SupportState):

    query = state["query"].lower()

    if "payment" in query:
        return "payment"

    elif "refund" in query or "return" in query:
        return "refund"

    elif "order" in query or "tracking" in query:
        return "order"

    else:
        return "general"


# ------------------------------------------------------------
# 4. BUILD GRAPH
# ------------------------------------------------------------

graph = StateGraph(SupportState)


# Add Nodes
graph.add_node("payment", payment_support)
graph.add_node("refund", refund_support)
graph.add_node("order", order_support)
graph.add_node("general", general_support)


# Add Conditional Edges
graph.add_conditional_edges(START,router,{"payment": "payment","refund": "refund","order": "order","general": "general"})


# Connect Nodes to END
graph.add_edge("payment", END)
graph.add_edge("refund", END)
graph.add_edge("order", END)
graph.add_edge("general", END)


# Compile Graph
app = graph.compile()


# ------------------------------------------------------------
# 5. EXECUTE GRAPH
# ------------------------------------------------------------

result = app.invoke({
    "query": "I want to return my product",
    "category": "",
    "response": ""
})


# ------------------------------------------------------------
# 6. DISPLAY RESULT
# ------------------------------------------------------------

print("\nFINAL RESPONSE:")
print(result["response"])
print("\nDETECTED CATEGORY:", router(result))








print("\n")

print("*" * 55)

print("Way 1 Manual End ")
print("=" * 50)
print("\n")






#way 2 - llm chooses which nodes to execute

# In this approach, instead of writing all the routing rules yourself, you ask an LLM to understand the user's query and classify it.
# 
# The LLM decides which category the query belongs to.


# ============================================================
# LANGGRAPH: LLM-BASED CONDITIONAL ROUTER
# ============================================================

from typing import TypedDict, Literal
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

load_dotenv()


# ------------------------------------------------------------
# 1. INITIALIZE LLM
# ------------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.9
)


# ------------------------------------------------------------
# 2. DEFINE STATE
# ------------------------------------------------------------

class SupportState(TypedDict):
    query: str
    category: str
    response: str


# ------------------------------------------------------------
# 3. CREATE LLM CLASSIFIER NODE
# ------------------------------------------------------------

def classifier(state: SupportState):

    prompt = f"""
    You are a customer support query classifier.

    Classify the following customer query into exactly
    ONE of these categories:

    1. payment
    2. refund
    3. order
    4. general

    Guidelines:

    - payment: Payment failures, deducted money,
      transaction issues, payment not completed.

    - refund: Refund requests, returning products,
      cancellation-related refund requests.

    - order: Order tracking, delivery status,
      shipping and order confirmation.

    - general: Any other query.

    Customer Query:
    {state["query"]}

    Return ONLY one category name.
    """

    result = llm.invoke(prompt)

    category = result.content.strip().lower()

    allowed_categories = [
        "payment",
        "refund",
        "order",
        "general"
    ]

    if category not in allowed_categories:
        category = "general"

    print("LLM Classified Category:", category)

    return {
        "category": category
    }


# ------------------------------------------------------------
# 4. CREATE ROUTER FUNCTION
# ------------------------------------------------------------

def router(state: SupportState):

    return state["category"]


# ------------------------------------------------------------
# 5. CREATE SUPPORT NODES
# ------------------------------------------------------------

def payment_support(state: SupportState):

    print("Payment Support Activated")

    return {
        "response": "Payment issue detected. We will help resolve it."
    }


def refund_support(state: SupportState):

    print("Refund Support Activated")

    return {
        "response": "Refund request detected. We will help you."
    }


def order_support(state: SupportState):

    print("Order Support Activated")

    return {
        "response": "Order-related query detected. We will assist you."
    }


def general_support(state: SupportState):

    print("General Support Activated")

    return {
        "response": "General support activated. How can we help?"
    }


# ------------------------------------------------------------
# 6. BUILD GRAPH
# ------------------------------------------------------------

graph = StateGraph(SupportState)


# Add Nodes
graph.add_node("classifier", classifier)

graph.add_node("payment", payment_support)
graph.add_node("refund", refund_support)
graph.add_node("order", order_support)
graph.add_node("general", general_support)


# Starting Edge
graph.add_edge(START, "classifier")


# Conditional Edges
graph.add_conditional_edges(
    "classifier",
    router,
    {
        "payment": "payment",
        "refund": "refund",
        "order": "order",
        "general": "general"
    }
)


# Connect Support Nodes to END
graph.add_edge("payment", END)
graph.add_edge("refund", END)
graph.add_edge("order", END)
graph.add_edge("general", END)


# Compile Graph
app = graph.compile()


# ------------------------------------------------------------
# 7. EXECUTE GRAPH
# ------------------------------------------------------------

result = app.invoke({
    "query": "My money was deducted but my order was not confirmed.",
    "category": "",
    "response": ""
})


# ------------------------------------------------------------
# 8. DISPLAY RESULT
# ------------------------------------------------------------

print("\nFINAL RESULT:")
print("Category:", result["category"])
print("Response:", result["response"])
