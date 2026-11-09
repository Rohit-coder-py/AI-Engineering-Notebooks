import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
import json
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from tavily import TavilyClient
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import ToolMessage, HumanMessage

load_dotenv()



## basic settings

api_key_groq= os.getenv("GROQ_API_KEY")

#paths

APP_DIR = os.getcwd()
LOGO_PATH = os.path.join(APP_DIR, "assets", "logo.png")
#model names

# Basic Settings
model_name = "openai/gpt-oss-20b"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


#initlize the llm


llm = ChatGroq(
    model = model_name,
    api_key = api_key_groq,
    temperature = 0.7)


#======================================================================



st.set_page_config(page_title="AETHER - YOUR AI WORKPLACE", page_icon=LOGO_PATH, layout="centered")
st.header("Aether APP Dashboard")


@st.cache_resource
def get_embeddings(name):
    return HuggingFaceEmbeddings(model_name=name)

embedding_model = get_embeddings(EMBEDDING_MODEL_NAME)

for key, default in {
    "vector_db": None,
    "pdf_signature": None,
    "pdf_name": None,
    "pdf_pages": 0,
    "pdf_chunks": 0,}.items():
    if key not in st.session_state:
        st.session_state[key] = default


with st.sidebar:
    st.header("📄 Document")
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if pdf_file is None:
        st.session_state.vector_db = None
        st.session_state.pdf_signature = None
        st.session_state.pdf_name = None
        st.session_state.pdf_pages = 0
        st.session_state.pdf_chunks = 0

    else:
        signature = f"{pdf_file.name}-{pdf_file.size}KB"
        st.write(signature)

        
        if signature != st.session_state.pdf_signature:
            try:
                with st.spinner("Reading and processing your PDF..."):
                    reader = PdfReader(pdf_file)

                    documents = []
                    for page_number, page in enumerate(reader.pages):
                        text = page.extract_text()
                        if text and text.strip():
                            documents.append(
                                Document(
                                    page_content=text,
                                    metadata={
                                        "page": page_number + 1,
                                        "source": pdf_file.name}))

                    if not documents:
                        st.error("No extractable text found. This may be a scanned PDF.")
                    else:
                        splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=150
                        )
                        chunks = splitter.split_documents(documents)

                        st.session_state.vector_db = FAISS.from_documents(
                            documents=chunks,
                            embedding=embedding_model
                        )
                        st.session_state.pdf_signature = signature
                        st.session_state.pdf_name = pdf_file.name
                        st.session_state.pdf_pages = len(reader.pages)
                        st.session_state.pdf_chunks = len(chunks)

            except Exception as error:
                st.error(f"Error while processing the PDF: {error}")

        if st.session_state.vector_db is not None:
            st.success("PDF ready!")


if st.session_state.vector_db is not None:
    st.subheader(f"📄 {st.session_state.pdf_name}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Pages", st.session_state.pdf_pages)
    c2.metric("Chunks", st.session_state.pdf_chunks)
    c3.metric("Stored vectors", st.session_state.vector_db.index.ntotal)
else:
    st.info("Upload a PDF from the sidebar to enable the Document Analyst.")


# Custom Chat Input Bar
st.markdown("""
<style>
.st-key-chat_bar {
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    width: min(860px, calc(100vw - 2rem));
    z-index: 999;
    background: white;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
}

.st-key-chat_bar button {
    border-radius: 10px;
}

.st-key-chat_bar [data-testid="stSelectbox"] {
    min-width: 110px;
}

section.main .block-container {
    padding-bottom: 100px;
}
</style>
""", unsafe_allow_html=True)

with st.container(key="chat_bar"):
    with st.form("chat_form"):
        col1, col2, col3 = st.columns([1.2, 4, 0.6])

        with col1:
            selected_model = st.selectbox(
                "Model",
                ["openai/gpt-oss-20b"],
                label_visibility="collapsed"
            )

        with col2:
            user_input = st.text_input(
                "Prompt",
                placeholder="Ask something...",
                label_visibility="collapsed"
            )

        with col3:
            submitted = st.form_submit_button("➤")

#alll tools
#1 researcher tools

search_tool = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def researcher_agent(topic: str) -> str:
    """Performs detailed research on the provided topic using Tavily Search."""

    response = search_tool.search(
        query=f"Perform detailed research on {topic}",
        search_depth="advanced",
        max_results=4
    )

    results = response.get("results", [])

    if not results:
        return f"No research results found for {topic}."

    research_results = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "No URL available")
        snippet = r.get("content", "No content available")

        research_results.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Summary: {snippet[:500]}..."
        )

    return (
        f"Research Results on: {topic}\n\n"
        + "\n\n".join(research_results)
    )

#2 . Document Analyst

RETRIEVAL_K = 4

doc_system_prompt = """
You are a helpful document question-answering assistant.

Your job is to analyse the uploaded PDF, notes, and other documents
and answer the user's questions using the retrieved document context.

Rules:
1. Answer using only the information provided in the context.
2. Do not invent facts or use outside knowledge to fill missing information.
3. If the context does not contain the answer, clearly say that you
   could not find the answer in the uploaded document.
4. Keep the answer clear, relevant, and easy to understand.
5. Use the page information included in the context when mentioning sources.

Context:
{context}
"""

doc_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", doc_system_prompt),
        ("human", "{question}")
    ]
)


@tool
def document_analyst_tool(question: str) -> str:
    """Answers questions about the uploaded PDF document using retrieved document context."""

    vector_db = st.session_state.get("vector_db")

    if vector_db is None:
        return "No document has been uploaded yet. Please upload a PDF first."

    retrieved_docs = vector_db.similarity_search(
        question,
        k=RETRIEVAL_K
    )

    context = "\n\n".join(
        [
            f"Page: {doc.metadata.get('page', 'Unknown')}\n"
            f"Content: {doc.page_content}"
            for doc in retrieved_docs
        ]
    )

    chain = doc_prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content



# TOOL CALL MIDDLEWARE
@wrap_tool_call
def handle_tool_errors(request, handler):

    try:
        return handler(request)

    except Exception as e:

        return ToolMessage(
            content=f"Error executing tool: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )
    
    

#3. Planner Agent

def build_planner_agent(pdf_loaded: bool):

  
    tools = [researcher_agent]
    tools_description = "1. researcher_agent: Performs web research on a topic."
    rules = "- Use researcher_agent for external research."

    
    if pdf_loaded:
        tools.insert(0, document_analyst_tool)
        tools_description = (
            "1. document_analyst_tool: Answers questions from the uploaded PDF.\n"
            "    2. researcher_agent: Performs web research on a topic."
        )
        rules = (
            "- Use document_analyst_tool for anything about the uploaded PDF.\n"
            "    - Use researcher_agent for external research.\n"
            "    - Use both tools if the user needs information from\n"
            "      the PDF and external research."
        )

    return create_agent(
        model=llm,
        tools=tools,  
        middleware=[handle_tool_errors],
        system_prompt=f"""
    You are a Planner Agent.

    Your job is to analyze the user's request and decide
    which tools need to be executed.

    Available tools:

    {tools_description}

    Rules:
    - Understand the user's request first.
    {rules}
    - Do not call unnecessary tools.
    - If no tool is required, answer accordingly.
    - After executing the required tools, collect their results.
    - Keep page numbers and source details from the tool results.
    - Pass the collected information in your final response.
    """)


#wRITER AGENT

writer_prompt = ChatPromptTemplate.from_messages(
    [(
            "system",
            """
            You are a Professional Writer Agent.

            Your job is to convert the information provided
            by the Planner Agent into a well-structured response.

            Rules:
            - Organize information properly.
            - Use meaningful headings and subheadings.
            - Use bullet points wherever required.
            - Use tables when they improve readability.
            - Maintain clarity and professionalism.
            - Do not add information that is not provided
              by the Planner Agent.
            - Preserve important facts and details.
            """
        ),
        (
            "human",
            """
            User Question:
            {question}

            Information from Planner Agent:
            {planner_output}

            Generate the final response.
            """)])

writer_agent = writer_prompt | llm



#all agents are imported suceesfully

#MAIN EXECUTION FUNCTION (writer+planner)

def run_multi_agent(user_input):

    
    planner_agent = build_planner_agent(st.session_state.vector_db is not None)

    st.write("Using Planner Agent...")

    planner_response = planner_agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)]})

    planner_output = planner_response["messages"][-1].content

    # 2. Writer Agent
    st.write("Using Writer Agent...")

    writer_response = writer_agent.invoke(
        {
            "question": user_input,
            "planner_output": planner_output
        }
    )

    return writer_response.content



if submitted and user_input:

    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):

        with st.status("Processing your request...",
                       expanded=True) as status:

            response = run_multi_agent(user_input)

            status.update(
                label="Task completed!",
                state="complete",
                expanded=False
            )

        st.write(response)