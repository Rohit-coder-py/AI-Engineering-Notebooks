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


# ===================================
# UI -- Letterpress Debossed (Streamlit)
# Runs only when launched with `streamlit run app.py`.
# With plain `python app.py` this block is skipped and the CLI works as before.
# ===================================

try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    _running_in_streamlit = get_script_run_ctx() is not None
except Exception:
    _running_in_streamlit = False

if _running_in_streamlit:
    import streamlit as st

    st.set_page_config(page_title="CareerMate AI", page_icon="🎓", layout="centered")

    st.markdown(
        """
        <style>
        :root {
            --bg: #dfe3e8;
            --ink: #8d949e;
            --ink-dark: #6f7782;
            --hi: rgba(255,255,255,0.95);
            --sh: rgba(120,128,140,0.55);
        }

        .stApp { background: var(--bg); }
        header[data-testid="stHeader"] { background: transparent; }
        #MainMenu, footer { visibility: hidden; }

        .block-container { max-width: 760px; padding-top: 3.5rem; }

        /* Letterpress title */
        .lp-title {
            text-align: center;
            font-family: "Georgia", "Times New Roman", serif;
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: 2px;
            color: var(--ink);
            text-shadow: 0 2px 1px var(--hi), 0 -1px 1px var(--sh);
            margin-bottom: 0.2rem;
        }
        .lp-sub {
            text-align: center;
            font-family: "Georgia", serif;
            font-size: 0.95rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--ink);
            text-shadow: 0 1px 1px var(--hi);
            margin-bottom: 2.2rem;
        }

        /* Labels */
        label, .stTextArea label p, .stTextInput label p {
            color: var(--ink-dark) !important;
            font-family: "Georgia", serif !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            text-shadow: 0 1px 1px var(--hi);
        }

        /* Debossed input */
        .stTextInput input, .stTextArea textarea {
            background: var(--bg) !important;
            color: var(--ink-dark) !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 16px !important;
            font-family: "Georgia", serif !important;
            text-shadow: 0 1px 0 var(--hi);
            box-shadow: inset 5px 5px 10px #b9bec6, inset -5px -5px 10px #ffffff !important;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #a6adb6 !important;
            text-shadow: 0 1px 0 var(--hi);
        }
        .stTextInput > div > div, .stTextArea > div > div {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Debossed button */
        .stButton > button, .stFormSubmitButton > button {
            width: 100%;
            background: var(--bg) !important;
            color: var(--ink-dark) !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.7rem 1rem !important;
            font-family: "Georgia", serif !important;
            font-weight: 800 !important;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 1px 0 var(--hi);
            box-shadow: 5px 5px 10px #b9bec6, -5px -5px 10px #ffffff !important;
            transition: all 0.15s ease;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            color: #5d6570 !important;
        }
        .stButton > button:active, .stFormSubmitButton > button:active {
            box-shadow: inset 4px 4px 8px #b9bec6, inset -4px -4px 8px #ffffff !important;
        }

        /* Debossed response card */
        [data-testid="stVerticalBlockBorderWrapper"]:has(.lp-card-title) {
            background: var(--bg);
            border: none !important;
            border-radius: 18px;
            padding: 1.4rem 1.6rem;
            margin-top: 1.5rem;
            color: var(--ink-dark);
            font-family: "Georgia", serif;
            line-height: 1.7;
            text-shadow: 0 1px 0 var(--hi);
            box-shadow: inset 6px 6px 12px #b9bec6, inset -6px -6px 12px #ffffff;
        }
        .lp-card-title {
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-size: 0.85rem;
            margin-bottom: 0.7rem;
            color: var(--ink);
            text-shadow: 0 1px 1px var(--hi);
        }

        /* Form container */
        [data-testid="stForm"] {
            border: none !important;
            background: var(--bg);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 8px 8px 16px #b9bec6, -8px -8px 16px #ffffff;
        }

        .stMarkdown, .stMarkdown p, .stMarkdown li { color: var(--ink-dark); }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="lp-title">CareerMate AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="lp-sub">Career &amp; Internship Assistant</div>',
        unsafe_allow_html=True,
    )

    with st.form("career_form"):
        ui_query = st.text_area(
            "Ask your query",
            placeholder="e.g. How can I improve my resume for a data science internship?",
            height=130,
        )
        ui_submit = st.form_submit_button("Ask")

    if ui_submit and ui_query.strip():
        with st.spinner("Thinking..."):
            ui_result = app.invoke({"messages": [("human", ui_query)]})
        with st.container(border=True):
            st.markdown('<div class="lp-card-title">CareerMate AI</div>', unsafe_allow_html=True)
            st.markdown(ui_result["messages"][-1].content)

    # Stop here so the CLI input() below doesn't block inside Streamlit
    st.stop()


while True:

    user_query =input("Ask yur query (type 'exit' to quit):")

    if user_query.strip().lower() in ("exit", "quit"):
        break

    result = app.invoke({"messages":  [("human", user_query)] } )

    print("\nCareerMate AI:")

    print(result["messages"][-1].content)

    print()