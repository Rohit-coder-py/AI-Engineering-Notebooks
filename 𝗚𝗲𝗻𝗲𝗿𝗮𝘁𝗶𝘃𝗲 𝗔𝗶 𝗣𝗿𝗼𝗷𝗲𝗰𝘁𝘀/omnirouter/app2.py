"""
AETHER - Your AI Workplace (simple version)

Kaise kaam karta hai (poora flow):
    User ka sawal
        -> Planner Agent  (decide karta hai kaunsa tool chalana hai)
              - document_analyst_tool : PDF se jawab nikalta hai
              - researcher_agent      : internet se research karta hai
        -> Writer Agent   (planner ka output sundar format mein likhta hai)
        -> Screen par answer

File ke sections:
    1. Imports aur settings
    2. Session state (app ki memory)
    3. Chat helper functions
    4. PDF processing
    5. Tools (research + document)
    6. Agents (planner + writer)
    7. Pages (sidebar, history, chat)
    8. Main - sab kuch yahin se chalta hai
"""

# =====================================================================
# 1. IMPORTS AUR SETTINGS
# =====================================================================
import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from tavily import TavilyClient

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Streamlit ka sabse pehla command yehi hona chahiye
LOGO_PATH = os.path.join(os.getcwd(), "assets", "logo.png")
st.set_page_config(page_title="AETHER - YOUR AI WORKPLACE", page_icon=LOGO_PATH, layout="centered")

# --- Settings (kuch badalna ho to sirf yahan badlo) ---
MODEL_NAME = "openai/gpt-oss-20b"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000        # PDF ke tukde ki size
CHUNK_OVERLAP = 150      # tukdon ke beech overlap
RETRIEVAL_K = 4          # sawal ke liye kitne tukde dhundhne hain

# --- Main LLM ---
llm = ChatGroq(
    model=MODEL_NAME,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
)

# --- Tavily (web search) ---
search_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@st.cache_resource  # model sirf ek baar load hoga
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


embedding_model = get_embeddings()


# =====================================================================
# 2. SESSION STATE (app ki memory - page refresh par bhi bachi rehti hai)
# =====================================================================
DEFAULT_STATE = {
    "chats": {},               # saari chats
    "current_chat_id": None,   # abhi kaunsi chat khuli hai
    "active_page": "chat",     # "chat" ya "history"
    "vector_db": None,         # PDF ka FAISS database
    "pdf_signature": None,     # PDF pehchanne ke liye (naam + size)
    "pdf_name": None,
    "pdf_pages": 0,
    "pdf_chunks": 0,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================================
# 3. CHAT HELPER FUNCTIONS
# =====================================================================
def create_new_chat():
    chat_id = str(uuid.uuid4())  # random unique id
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.active_page = "chat"


def get_current_chat():
    """Current chat wapas deta hai. Agar nahi hai to nayi bana deta hai."""
    chat_id = st.session_state.current_chat_id
    if chat_id not in st.session_state.chats:
        create_new_chat()
        chat_id = st.session_state.current_chat_id
    return st.session_state.chats[chat_id]


def clear_pdf_state():
    st.session_state.vector_db = None
    st.session_state.pdf_signature = None
    st.session_state.pdf_name = None
    st.session_state.pdf_pages = 0
    st.session_state.pdf_chunks = 0


# =====================================================================
# 4. PDF PROCESSING
# =====================================================================
def process_pdf(pdf_file):
    """PDF padho -> tukdon mein todo -> FAISS database banao."""
    reader = PdfReader(pdf_file)

    # Step 1: har page ka text nikalo
    documents = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"page": page_number, "source": pdf_file.name},
                )
            )

    if not documents:
        st.error("No extractable text found. This may be a scanned PDF.")
        return

    # Step 2: bade text ko chhote chunks mein todo
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)

    # Step 3: chunks ko vectors mein badlo aur FAISS mein store karo
    st.session_state.vector_db = FAISS.from_documents(documents=chunks, embedding=embedding_model)
    st.session_state.pdf_name = pdf_file.name
    st.session_state.pdf_pages = len(reader.pages)
    st.session_state.pdf_chunks = len(chunks)


# =====================================================================
# 5. TOOLS (agent inhe call karta hai)
# =====================================================================
@tool
def researcher_agent(topic: str) -> str:
    """Performs detailed research on the provided topic using Tavily Search."""
    response = search_client.search(
        query=f"Perform detailed research on {topic}",
        search_depth="advanced",
        max_results=4,
    )
    results = response.get("results", [])

    if not results:
        return f"No research results found for {topic}."

    lines = []
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "No URL available")
        summary = r.get("content", "No content available")[:500]
        lines.append(f"Title: {title}\nURL: {url}\nSummary: {summary}...")

    return f"Research Results on: {topic}\n\n" + "\n\n".join(lines)


DOC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a helpful document question-answering assistant.
Answer the user's question using ONLY the context below.

Rules:
1. Do not invent facts or use outside knowledge.
2. If the answer is not in the context, say you could not find it in the uploaded document.
3. Keep the answer clear and easy to understand.
4. Mention page numbers when giving sources.

Context:
{context}
"""),
    ("human", "{question}"),
])


@tool
def document_analyst_tool(question: str) -> str:
    """Answers questions about the uploaded PDF document using retrieved document context."""
    vector_db = st.session_state.vector_db
    if vector_db is None:
        return "No document has been uploaded yet. Please upload a PDF first."

    # Sawal se milte-julte chunks dhundho
    found_chunks = vector_db.similarity_search(question, k=RETRIEVAL_K)

    # Unhe ek text mein jodo (page number ke saath)
    context = "\n\n".join(
        f"Page: {doc.metadata.get('page', 'Unknown')}\nContent: {doc.page_content}"
        for doc in found_chunks
    )

    # LLM se jawab likhwao
    answer = (DOC_PROMPT | llm).invoke({"context": context, "question": question})
    return answer.content


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Agar koi tool fail ho to app crash na ho, error message wapas jaye."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Error executing tool: {e}",
            tool_call_id=request.tool_call["id"],
        )


# =====================================================================
# 6. AGENTS
# =====================================================================
def build_planner_agent(pdf_loaded: bool):
    """Planner: sawal samjhe aur sahi tool chune. PDF hai to document tool bhi milega."""
    if pdf_loaded:
        tools = [document_analyst_tool, researcher_agent]
        tool_info = (
            "- document_analyst_tool: answers questions from the uploaded PDF.\n"
            "- researcher_agent: performs web research on a topic.\n"
            "Use document_analyst_tool for anything about the PDF.\n"
            "Use researcher_agent for external research.\n"
            "Use both if the user needs the PDF and external research."
        )
    else:
        tools = [researcher_agent]
        tool_info = (
            "- researcher_agent: performs web research on a topic.\n"
            "Use researcher_agent for external research."
        )

    system_prompt = f"""
You are a Planner Agent.
Understand the user's request and decide which tools to run.

Available tools:
{tool_info}

Rules:
- Do not call unnecessary tools.
- If no tool is required, answer directly.
- Keep page numbers and source details from tool results.
- Pass all collected information in your final response.
"""
    return create_agent(
        model=llm,
        tools=tools,
        middleware=[handle_tool_errors],
        system_prompt=system_prompt,
    )


WRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a Professional Writer Agent.
Convert the information from the Planner Agent into a well-structured response.

Rules:
- Use headings, bullet points, and tables where they help.
- Stay clear and professional.
- Do not add information that the Planner Agent did not provide.
- Preserve important facts and details.
"""),
    ("human", """
User Question:
{question}

Information from Planner Agent:
{planner_output}

Generate the final response.
"""),
])

writer_agent = WRITER_PROMPT | llm


def run_multi_agent(user_input: str) -> str:
    """Planner chalao, phir Writer chalao, final answer wapas do."""
    pdf_loaded = st.session_state.vector_db is not None

    # Step 1: Planner
    st.write("Using Planner Agent...")
    planner = build_planner_agent(pdf_loaded)
    planner_result = planner.invoke({"messages": [HumanMessage(content=user_input)]})
    planner_output = planner_result["messages"][-1].content

    # Step 2: Writer
    st.write("Using Writer Agent...")
    writer_result = writer_agent.invoke({"question": user_input, "planner_output": planner_output})
    return writer_result.content


# =====================================================================
# 7. PAGES (screen par kya dikhana hai)
# =====================================================================
def render_sidebar():
    with st.sidebar:
        st.title("AETHER")

        if st.button("＋ New Chat", use_container_width=True):
            create_new_chat()
            st.rerun()

        if st.button("◷ Recent Chats", use_container_width=True):
            st.session_state.active_page = "history"
            st.rerun()

        st.divider()
        st.header("📄 Document")
        pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

        if pdf_file is None:
            clear_pdf_state()
            return

        # Same PDF dobara process na ho, isliye signature check
        signature = f"{pdf_file.name}-{pdf_file.size}"
        st.write(pdf_file.name)

        if signature != st.session_state.pdf_signature:
            try:
                with st.spinner("Reading and processing your PDF..."):
                    process_pdf(pdf_file)
                    if st.session_state.vector_db is not None:
                        st.session_state.pdf_signature = signature
            except Exception as error:
                st.error(f"Error while processing the PDF: {error}")

        if st.session_state.vector_db is not None:
            st.success("PDF ready!")


def render_history_page():
    st.title("Recent Chats")
    st.caption("Open a previous conversation or start a new one.")

    if not st.session_state.chats:
        st.info("No conversations yet. Start a new chat to see it here.")
        return

    # Sabse nayi chat sabse upar
    sorted_chats = sorted(
        st.session_state.chats.items(),
        key=lambda item: item[1]["updated_at"],
        reverse=True,
    )

    for chat_id, chat in sorted_chats:
        if chat["messages"]:
            last = str(chat["messages"][-1]["content"]).replace("\n", " ")
            preview = last[:110] + ("..." if len(last) > 110 else "")
        else:
            preview = "No messages yet"

        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.subheader(chat["title"])
                st.caption(f'{chat["updated_at"].strftime("%b %d, %Y · %I:%M %p")}  |  {preview}')
            with col2:
                if st.button("Open", key=f"open_{chat_id}", use_container_width=True):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.active_page = "chat"
                    st.rerun()


CHAT_BAR_CSS = """
<style>
.st-key-chat_bar {
    position: fixed; bottom: 1rem; left: 50%;
    transform: translateX(-50%);
    width: min(860px, calc(100vw - 2rem));
    z-index: 999; background: white; padding: 12px;
    border: 1px solid #ddd; border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
}
.st-key-chat_bar button { border-radius: 10px; }
section.main .block-container { padding-bottom: 100px; }
</style>
"""


def render_chat_page():
    chat = get_current_chat()
    st.title(chat["title"])

    # PDF ki info
    if st.session_state.vector_db is not None:
        with st.expander(f"📄 Document ready: {st.session_state.pdf_name}", expanded=False):
            c1, c2, c3 = st.columns(3)
            c1.metric("Pages", st.session_state.pdf_pages)
            c2.metric("Chunks", st.session_state.pdf_chunks)
            c3.metric("Stored vectors", st.session_state.vector_db.index.ntotal)
    else:
        st.caption("Upload a PDF from the sidebar to enable the Document Analyst.")

    # Purane messages dikhao
    for message in chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Neeche wali input bar
    st.markdown(CHAT_BAR_CSS, unsafe_allow_html=True)
    with st.container(key="chat_bar"):
        with st.form("chat_form"):
            col1, col2 = st.columns([6, 0.8])
            user_input = col1.text_input("Prompt", placeholder="Ask something...", label_visibility="collapsed")
            submitted = col2.form_submit_button("➤")

    if submitted and user_input.strip():
        handle_user_message(chat, user_input.strip())


def handle_user_message(chat, user_input):
    # Pehla message chat ka title ban jaata hai
    if not chat["messages"]:
        clean = user_input.replace("\n", " ")
        chat["title"] = clean[:45] + ("..." if len(clean) > 45 else "")

    chat["messages"].append({"role": "user", "content": user_input})

    # Agents chalao aur progress dikhao
    with st.chat_message("assistant"):
        with st.status("Processing your request...", expanded=True) as status:
            try:
                response = run_multi_agent(user_input)
                status.update(label="Task completed!", state="complete", expanded=False)
            except Exception as error:
                response = f"Sorry, something went wrong: {error}"
                status.update(label="Request failed", state="error", expanded=False)
        st.markdown(response)

    chat["messages"].append({"role": "assistant", "content": response})
    chat["updated_at"] = datetime.now()
    st.rerun()


# =====================================================================
# 8. MAIN - yahan se app chalta hai
# =====================================================================
if not st.session_state.chats:
    create_new_chat()

render_sidebar()

if st.session_state.active_page == "history":
    render_history_page()
else:
    render_chat_page()