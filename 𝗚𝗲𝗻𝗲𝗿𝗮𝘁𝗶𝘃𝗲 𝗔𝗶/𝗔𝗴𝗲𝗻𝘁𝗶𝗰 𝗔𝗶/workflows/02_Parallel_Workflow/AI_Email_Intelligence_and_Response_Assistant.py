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

#========================================================
# UI SECTION (added) - Streamlit - Torn Paper Edge style

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if get_script_run_ctx(suppress_warning=True) is not None:

    st.set_page_config(page_title="AI Email Intelligence Assistant", page_icon="✉️")


    
    ui_css = """
    <style>
    /* page background (kraft paper desk) */
    .stApp { background: #d8c9aa; }
    .block-container { max-width: 900px; }

    /* paper card with torn top and bottom edge */
    div[class*="st-key-torn"] {
        background: linear-gradient(to bottom, #e4d6b8 0, #fbf7ee 12px, #fbf7ee calc(100% - 12px), #e4d6b8 100%);
        padding: 36px 30px;
        margin-bottom: 22px;
        clip-path: polygon(0.0% 5px, 2.8% 2px, 5.6% 6px, 8.3% 10px, 11.1% 0px, 13.9% 1px, 16.7% 8px, 19.4% 1px, 22.2% 5px, 25.0% 9px, 27.8% 0px, 30.6% 8px, 33.3% 3px, 36.1% 0px, 38.9% 1px, 41.7% 6px, 44.4% 6px, 47.2% 1px, 50.0% 3px, 52.8% 1px, 55.6% 8px, 58.3% 6px, 61.1% 0px, 63.9% 9px, 66.7% 1px, 69.4% 3px, 72.2% 10px, 75.0% 10px, 77.8% 9px, 80.6% 0px, 83.3% 9px, 86.1% 9px, 88.9% 6px, 91.7% 0px, 94.4% 3px, 97.2% 0px, 100.0% 8px, 100.0% calc(100% - 2px), 97.2% calc(100% - 4px), 94.4% calc(100% - 6px), 91.7% calc(100% - 2px), 88.9% calc(100% - 8px), 86.1% calc(100% - 1px), 83.3% calc(100% - 9px), 80.6% calc(100% - 4px), 77.8% calc(100% - 8px), 75.0% calc(100% - 10px), 72.2% calc(100% - 2px), 69.4% calc(100% - 1px), 66.7% calc(100% - 9px), 63.9% calc(100% - 9px), 61.1% calc(100% - 10px), 58.3% calc(100% - 3px), 55.6% calc(100% - 5px), 52.8% calc(100% - 1px), 50.0% calc(100% - 8px), 47.2% calc(100% - 1px), 44.4% calc(100% - 9px), 41.7% calc(100% - 0px), 38.9% calc(100% - 9px), 36.1% calc(100% - 3px), 33.3% calc(100% - 7px), 30.6% calc(100% - 10px), 27.8% calc(100% - 8px), 25.0% calc(100% - 6px), 22.2% calc(100% - 5px), 19.4% calc(100% - 7px), 16.7% calc(100% - 9px), 13.9% calc(100% - 7px), 11.1% calc(100% - 5px), 8.3% calc(100% - 4px), 5.6% calc(100% - 3px), 2.8% calc(100% - 2px), 0.0% calc(100% - 3px));
    }

    /* text colours inside the cards */
    div[class*="st-key-torn"] p,
    div[class*="st-key-torn"] li,
    div[class*="st-key-torn"] label { color: #2f2a24; }
    div[class*="st-key-torn"] h1,
    div[class*="st-key-torn"] h2,
    div[class*="st-key-torn"] h3 { color: #a63d2f; }

    /* email input box */
    div[class*="st-key-torn"] textarea { background: #ffffff; color: #2f2a24; }

    /* button with a small torn edge too */
    .stButton > button {
        background: #a63d2f;
        color: #ffffff;
        border: none;
        border-radius: 0;
        clip-path: polygon(0.0% 1px, 7.1% 4px, 14.3% 4px, 21.4% 1px, 28.6% 2px, 35.7% 4px, 42.9% 3px, 50.0% 4px, 57.1% 0px, 64.3% 4px, 71.4% 0px, 78.6% 3px, 85.7% 2px, 92.9% 4px, 100.0% 1px, 100.0% calc(100% - 1px), 92.9% calc(100% - 3px), 85.7% calc(100% - 4px), 78.6% calc(100% - 4px), 71.4% calc(100% - 3px), 64.3% calc(100% - 3px), 57.1% calc(100% - 1px), 50.0% calc(100% - 1px), 42.9% calc(100% - 1px), 35.7% calc(100% - 4px), 28.6% calc(100% - 3px), 21.4% calc(100% - 0px), 14.3% calc(100% - 0px), 7.1% calc(100% - 1px), 0.0% calc(100% - 4px));
    }
    .stButton > button:hover { background: #862f23; color: #ffffff; }
    </style>
    """

    st.markdown(ui_css, unsafe_allow_html=True)


    

    if "ui_result" not in st.session_state:
        st.session_state["ui_result"] = None


    

    with st.container(key="torn_header"):
        st.markdown("# ✉️ AI Email Intelligence & Response Assistant")
        st.markdown("Paste an email and get its intent, priority level and a suggested reply.")


    
    with st.container(key="torn_input"):
        ui_email = st.text_area("Email", placeholder="Paste your email here...", height=250)
        ui_clicked = st.button("Analyze Email")


    

    if ui_clicked:
        if ui_email.strip() == "":
            st.warning("Please paste an email first.")
        else:
            with st.spinner("Agents are working..."):
                st.session_state["ui_result"] = app.invoke({
                    "raw_email": ui_email,
                    "aggregator_agent": {}
                })


    

    ui_result = st.session_state["ui_result"]

    if ui_result is not None:

        
        ui_final = ui_result["aggregator_agent"]

        with st.container(key="torn_intent"):
            st.markdown("## 🎯 Email Intent")
            st.markdown(ui_final.get("intent_result", "Not available"))

        

        with st.container(key="torn_priority"):
            st.markdown("## 🚦 Email Priority")
            st.markdown(ui_final.get("priority_result", "Not available").replace("\n", "  \n"))

        with st.container(key="torn_reply"):
            st.markdown("## 💬 Suggested Email Response")
            st.markdown(ui_final.get("email_response", "Not available").replace("\n", "  \n"))


    

    st.stop()

#========================================================
# END OF UI SECTION
#========================================================


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
