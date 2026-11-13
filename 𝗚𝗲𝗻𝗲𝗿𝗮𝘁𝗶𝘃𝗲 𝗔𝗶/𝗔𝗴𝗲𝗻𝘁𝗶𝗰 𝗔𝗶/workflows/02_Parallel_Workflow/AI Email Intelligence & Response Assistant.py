# Project Overview :

# Input: An email.
# 
# Three agents execute simultaneously:

# - Intent Agent: Identifies the purpose of the email.
# - Priority Agent: Evaluates urgency and importance.
# - Response Agent: Generates a suitable response draft.



# Final Output: Email summary, priority level and suggested reply.



# ======================================================



import os
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START , END

load_dotenv()

#llm

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.25)



#first thing is to create a state

# class Email_agent(TypedDict) -> dict:
#     raw_email : str
#     intent_response : str
#     priority_response : str
#     final_response : str
#     
    
    
    
#We can use reducers

# Reducer ka kaam: Jab multiple parallel agents ek hi state key ko update karte hain, toh unke outputs ko combine karna.



#reducer


def merge_dicts(existing : dict , new: dict) -> dict :
    if existing is None:
        return new
    
    return {**existing , **new}



class EmailAgent(TypedDict):
    raw_email: str
    aggregator_agent: Annotated[ dict [str,  str ] , merge_dicts]
    
    


    
#now created reducers and States now next step is to create our multiple nodes
# 1- Intent Agent: Identifies the purpose of the email.
# 2- Priority Agent: Evaluates urgency and importance.
# 3- Response Agent: Generates a suitable response draft.


#node 1 - intent

def intent_node(state :EmailAgent) -> dict:
    
    """Step 1: Find out the intent of the email"""
    
    
    intent_prompt =  f"""
    You are a helpful ai chatbot that helps people to find the intent behind the email provided
    
    Your role is to find the intent of the provided email.
    
    Provided Raw Email :{state["raw_email"]}
    """
    
    response = llm.invoke(intent_prompt)
    
    return {"aggregator_agent" : { "intent_result" : response.content }}


#node 2 - priority

def priority_node(state : EmailAgent) -> dict:
    
    priority_prompt = f"""
    You are an expert email prioritization assistant.

    Your task is to evaluate the urgency and importance of the given email and assign a clear priority level.

    Raw Email:
    {state["raw_email"]}

    Instructions:
    1. Analyze the content carefully.
    2. Consider factors like deadlines, explicit urgency words, sender importance, business impact, and time sensitivity.
    3. Assign one of the following priority levels:
       - Critical
       - High
       - Medium
       - Low

    Respond in this exact format:

    Priority: <Critical / High / Medium / Low>
    Reasoning: <1-2 sentence explanation>
    """
    
    response = llm.invoke(priority_prompt)
    
    return {"aggregator_agent" :  { "priority_result" : response.content} }



#node 3 - Response Agent: Generates a suitable response draft


def response_node(state : EmailAgent) -> dict :
    
    response_prompt = f"""
    You are a professional email response assistant.

    Your task is to write a clear, polite, and appropriate reply based on the original email

    Original Email:
    {state["raw_email"]}


    Guidelines:
    - Keep the tone professional and friendly.
    - Address the main points of the original email.
    - Be concise (preferably 4–8 sentences).
    - If the email requires action or information, acknowledge it clearly.
    - Do not invent information that is not present in the original email.

    Output only the email reply (no extra commentary).
    """
    
    res = llm.invoke(response_prompt)
    
    return {"aggregator_agent" :  {"email_response" : res.content} }





#all 3 nodes created successfully


graph =  StateGraph(EmailAgent)


graph.add_node("Intent_Finder", intent_node)
graph.add_node("Priority_Finder", priority_node)
graph.add_node("Email_Generator", response_node)



#add edges (parallel - FAN-In and FAN-OUT)
# 1. FAN-OUT (START → Multiple Nodes)

graph.add_edge(START , "Intent_Finder")
graph.add_edge(START , "Priority_Finder")
graph.add_edge(START , "Email_Generator")

#langgraph will automatically detect the parallel workflow


# 2. FAN-IN (Multiple Nodes → One Node)

graph.add_edge( "Intent_Finder" , END)
graph.add_edge( "Priority_Finder" , END)
graph.add_edge( "Email_Generator" , END)




app = graph.compile()

user_email = """**From:** Sarah Mitchell  
Subject:** URGENT: Project Submission Deadline

Hi Alex,

The client presentation is scheduled for tomorrow morning, and we still need the final project report.

Please review the latest figures, correct any errors, and send me the completed report by 3:00 PM today.

This is our final deadline before the presentation. Please let me know immediately if you face any issues.

Thanks,  
Sarah"""


result = app.invoke({
    "raw_email": user_email,
    "aggregator_agent": {}   #becuase reducers
    })

# print(result)



final_result = result["aggregator_agent"]

# Formatted Output
print("\n" + "=" * 60)
print("           AI EMAIL INTELLIGENCE REPORT")
print("=" * 60)

print("\n[ EMAIL INTENT ]")
print("-" * 60)
print(final_result.get("intent_result", "Not available"))

print("\n[ EMAIL PRIORITY ]")
print("-" * 60)
print(final_result.get("priority_result", "Not available"))

print("\n[ SUGGESTED EMAIL RESPONSE ]")
print("-" * 60)
print(final_result.get("email_response", "Not available"))

print("\n" + "=" * 60)
print("             ANALYSIS COMPLETED")
print("=" * 60)



print("\n -----------------")

print(final_result)

    




    


