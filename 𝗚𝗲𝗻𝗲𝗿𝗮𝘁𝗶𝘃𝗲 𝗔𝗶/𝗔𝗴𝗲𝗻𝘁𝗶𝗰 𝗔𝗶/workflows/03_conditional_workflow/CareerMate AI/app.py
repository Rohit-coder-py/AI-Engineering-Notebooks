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
    query: str
    messages: Annotated[list, add_messages]
    query_type: str
    retrieved_context: str
    
    
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

    "Return ONLY one word: resume, interview, or general."
    
    "Only reply in one word stripped and in lower case "
    "Return ONLY one word: resume, interview, or general. "
    "Only reply in lowercase.")
    
    response = llm.invoke(classifier_prompt)

    query_type = response.content.strip().lower()

    return {
        "query_type": query_type
    }


#node 2 - resume_node -Retrieves resume PDF context 


def resume_node(state: CarrerState) -> dict:
    """Retrieves relevant chunks from the resume and portfolio PDF."""

    query = state["messages"][-1].content

    docs = resume_retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return {"retrieved_context": context}

#node 3 - interview_node -Retrieves interview PDF context 

def interview_node(state: CarrerState) -> dict:
    """Retrieves relevant chunks from the interview preparation PDF."""

    query = state["messages"][-1].content

    docs = interview_retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return {"retrieved_context": context}


#node 4 - general_node - without any retrival  


def general_node(state: CarrerState) -> dict:
    """Handles general career and internship-related queries."""

    query = state["messages"][-1].content

    return {"retrieved_context": "NO_RETRIEVAL_NEEDED"}


#node 5 - final_response_generator - generates final response after getting the retrived content



from langchain_core.messages import AIMessage


def final_response_node(state: CarrerState) -> dict:
    """Generates the final response using the retrieved context."""

    query = state["messages"][-1].content

    context = state["retrieved_context"]

    prompt = f"""
    You are CareerMate AI, an intelligent Career and Internship Assistant.

    Your task is to help students with career development,
    resume building, interview preparation, and internship guidance.

    User Query:
    {query}

    Retrieved Context:
    {context}

    Instructions:
    - Answer the user's query clearly and professionally.
    - If relevant context is available, use it to generate your answer.
    - Do not invent facts or claim that information comes from the PDF
      if it is not present in the retrieved context.
    - If the retrieved context is empty, answer using your general knowledge.
    - Provide practical examples and actionable suggestions wherever useful.
    - Keep the response relevant to the user's question.
    """

    response = llm.invoke(prompt)

    return {
        "messages": [AIMessage(content=response.content)]
    }


#all nodes are created now its time to create a router function

def route_query(state: CarrerState) -> str:
    """Routes the query to the appropriate node based on query_type."""

    query_type = state["query_type"]

    if query_type == "resume":
        return "resume_node"

    elif query_type == "interview":
        return "interview_node"

    else:
        return "general_node"
    
    
#everything done now next step is : Graph Construction
    
graph = StateGraph(CarrerState)


# Register all nodes

graph.add_node("classifier_node", classifier_node)

graph.add_node("resume_node", resume_node)

graph.add_node("interview_node", interview_node)

graph.add_node("general_node", general_node)

graph.add_node("final_response_node", final_response_node)



#now step step is too add edges

graph.add_edge(START , "classifier_node")

graph.add_conditional_edges("classifier_node",route_query)


graph.add_edge("interview_node","final_response_node")
graph.add_edge("resume_node","final_response_node")
graph.add_edge("general_node","final_response_node")


graph.add_edge("final_response_node",END)


app = graph.compile()


user_query =input("Ask yur query:")

result = app.invoke({"messages":  [("human", user_query)] } )

print("\nCareerMate AI:")

print(result["messages"][-1].content)

 
