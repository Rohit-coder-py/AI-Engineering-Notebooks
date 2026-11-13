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


def intent_node(EmailAgent) -> dict:
    




    


