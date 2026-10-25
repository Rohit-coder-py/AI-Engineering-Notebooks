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
#now  we will follow the rag pipeline now
    
#1. Document Loaders
#2. Textsplitting
#3.embeddings generation
#4.vectordb
#5.Retreival





from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

#defining embedding models here so we dont need to initialize it everytime we start

@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="Qwen/Qwen3-Embedding-0.6B"
    )

embedding = get_embedding_model()

if raw_text:
    
    # 1. Refine the product details only once
    response = chain.invoke({"raw_text": raw_text})
    document = response.content
    with st.expander("Product Details"):
        st.write(document)

    # 2. Text splitting
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=245,
        chunk_overlap=4
    )

    token_chunks = splitter.split_text(document)

    st.write("Total No. of Chunks:", len(token_chunks))

    # 3. Generate embeddings
    #already generated

    # 4. Create vector database
    vectorstore = Chroma.from_texts(
        texts=token_chunks,
        embedding=embedding,
    )

    st.success("Vector database created successfully!")
    
    
    #5. Retreival
    
# 5. Retrieval
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3})

    question = st.text_input("Ask about this product:")

    if question:
        results = retriever.invoke(question)

        st.subheader("Retrieved Information")

        for i, doc in enumerate(results, start=1):
            st.write(f"Chunk {i}")
            st.write(doc.page_content)

    
    

else:
    st.warning("Please enter a valid product URL.")