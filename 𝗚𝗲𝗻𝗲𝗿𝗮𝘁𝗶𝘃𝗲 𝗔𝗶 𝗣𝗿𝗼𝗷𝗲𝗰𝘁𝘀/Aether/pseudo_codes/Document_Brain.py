import os
from dotenv import load_dotenv

import json
import streamlit as st 
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()



#-------------------------------------------------
# Basic Settings
#-------------------------------------------------
model_name = "openai/gpt-oss-20b"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"



system_prompt = """
You are a helpful ai chatbot that helps the user to read analyse their Uplaoded PDF,NOTES and other documents

Your job is to : Analyse the whole uploaded document and answer user question from the provided document

Remeber the rules : Answer only from the uploaded document and if the asked question of user from the uploaded document only

If the asked question is nor from uploaded pdf you can warn user for this 

"""


#initilize the llm

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model = model_name,
    temperature = 0.7,
    api_key = api_key)



# ---------------------------------------


#file_upload
st.write("Document Reader")

file_upload = st.file_uploader("Upload your file :",max_upload_size=100)


if file_upload:
    #reading the pdf

    reader = PdfReader(file_upload)

    st.write(f"Total No. of pages :",len(reader.pages))

    documents = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={"page": page_number + 1}
                )
            )

    #2. Chunking the pdf

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap = 12)

    total_chunks = splitter.split_documents(documents)

    st.write("======================\n")
    st.write("Total No. Of chunks :",len(total_chunks))


    #3. create embeddings of chunks and store them into vector databases

    #load the embeddings model

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME)

    #now create the vector_database

    vector_db = FAISS.from_documents(
        documents=total_chunks,
        embedding=embedding_model)

    st.write("Total Chunks stored : ",vector_db.index.ntotal)


    #now everything is set now user will ask question and we have to answer them
    
    question = st.chat_input("Enter your question here :")
    
    retreived_docs = vector_db.similarity_search(question,k = 4)
    
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    
    #llm part
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt + "\n\nContext:\n{context}")
         , ("human", "{question}") ])
    
    
    chain = prompt | llm
    
    
    response = chain.invoke({
        "context" : context,
        "question": question})
    
    
    #now finally display answers
    
    st.chat_message("user").write(question)

    st.chat_message("assistant").write(response.content)
    
    
    
    
#this part is completeds
    
    
    
    
    
    
    

    
    