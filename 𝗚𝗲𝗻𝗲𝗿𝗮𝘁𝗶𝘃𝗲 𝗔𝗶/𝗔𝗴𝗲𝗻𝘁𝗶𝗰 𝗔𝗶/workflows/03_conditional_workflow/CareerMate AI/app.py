"""
Al Career & Internship Assistant  -- CarrerMate AI

An assistant that helps students prepare for internships and jobs.

Conditional paths:

. Resume and portfolio RAG
· Interview preparation RAG
. General career questions - LLM
"""


# ===================================

import os
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()


#basic settings
api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)



#initilizing embeddings models

import filelock
import huggingface_hub.utils._fixes as fixes

# Thonny FileLock compatibility workaround
_original_filelock = filelock.FileLock

def compatible_filelock(lock_file, timeout=-1, **kwargs):
    kwargs.pop("mode", None)
    return _original_filelock(lock_file, timeout=timeout)

fixes.FileLock = compatible_filelock

embeddings = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B")

#basic settings

APP_PATH = os.getcwd()

interview_PATH = os.path.join(APP_PATH, "knowledge_base", "interview_preparation_guide.pdf")

resume_PATH = os.path.join(APP_PATH, "knowledge_base", "resume_portfolio_guide.pdf")
#--------------------------------------------------

#This function loads PDF documents, splits them into chunks, converts them into embeddings,
#stores them in a FAISS vector database, and returns a retriever to fetch the 4 most relevant chunks for a given query.


def build_retriver(pdf_path : str):
    
    loader = PyPDFLoader(pdf_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 100)
    
    chunks = splitter.split_documents(document)

    vectorstore = FAISS.from_documents(chunks,embeddings)

    return vectorstore.as_retriever(search_kwargs = {"k":4})

interview_retriever = build_retriver(interview_PATH)
resume_retriever = build_retriver(resume_PATH)

    
    
# now we created a rag pipeline now next step is to create a state


    
class CarrerState(TypedDict):
    query : str
    messages : Annoted[list,add_messages]
    query_type = str
    retreived_context : str
    
    
    
#lets create nodes
    
    
# Node 1 - Classifier Node : To decide which pdf to retreive


def classifier_node(state : CarrerState) -> dict :
    """Look at the user provided query and decides which pdf to retrive from knowledge_base"""
    
    
    last_message = state["messages"][-1].content
    
    classifier_prompt = (
    "You are a query classifier for CareerMate AI.\n\n"

    "Classify the student query into exactly ONE category:\n"
    "'resume', 'interview', or 'general'.\n\n"

    "Rules:\n"
    "- Use 'resume' for resume building, CV writing, "
    "portfolio creation, and resume improvement.\n"

    "- Use 'interview' for interview preparation, "
    "technical interviews, HR interviews, and interview skills.\n"

    "- Use 'general' for internship guidance, internship applications, "
    "career advice, job opportunities, greetings, and all other queries.\n\n"

    f"Student Query: {last_message}\n\n"

    "Return ONLY one word: resume, interview, or general.")
    
    response = llm.invoke(classifier_prompt)

    query_type = response.content.strip().lower()

    return {
        "query_type": query_type
    }





