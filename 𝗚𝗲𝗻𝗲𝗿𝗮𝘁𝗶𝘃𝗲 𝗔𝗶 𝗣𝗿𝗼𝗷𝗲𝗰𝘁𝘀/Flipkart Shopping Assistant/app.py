from dotenv import load_dotenv
import streamlit as st
import os


load_dotenv()

api_key = os.getenv("GROK_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")


from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(
    model="mistral-large-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0
)


#basic settings

APP_PATH = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_PATH, "..", "assets", "logo.png")


st.set_page_config(page_title="Flipkart Shopping Assistant", page_icon=LOGO_PATH, layout="centered")


st.write("Your Shopping Assistant")
#models


@st.cache_resource
def get_model():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=api_key,
        temperature = 0.3)

@st.cache_resource

def refine_model():
    return ChatMistralAI(
    model="ministral-8b-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0)




#get product info

import trafilatura

url = st.text_input("Enter website URL: ")

html = trafilatura.fetch_url(url)
raw_text = trafilatura.extract(html) if html else None

#system prompts

#1. For mistral to refine the details for better output 
from langchain_core.prompts import ChatPromptTemplate

prompt_refine = ChatPromptTemplate([
    ("system", """
I had provided you a product details from flipkart.com
Your work :
Format the provided data make it good and defined structured and send it again
RULES:
Only 1 product at once remove noise from that provided text
Dont leave any details behind include each and evry details in a structured format

Provide structured version of the raw text 

Important : If the link doesnt belong to any shopping site or doesnt contain any kind of product deatils dont assume just return this link is not valid or whatever the reason is but dont assume anything by your own .
And most important just provide deatils in structured format with not ny extra stuff like here it is and all just product data 
Here is the raw text details :{raw_text}
""") ])



#invoke the prompt

chain = prompt_refine | refine_model()

if raw_text:
    response = chain.invoke({"raw_text": raw_text})
    with st.expander("Product Details"):
        st.write(response.content)
    
else:
    st.warning("Could not extract product details. Maybe you had not entered product link yet")


