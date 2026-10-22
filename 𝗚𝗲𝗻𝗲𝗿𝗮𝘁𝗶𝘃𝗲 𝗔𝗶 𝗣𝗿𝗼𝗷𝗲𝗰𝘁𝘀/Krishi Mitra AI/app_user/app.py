import os
import hashlib
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

APP_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_PATH, "deep_learning_chroma_db")
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"  # must match create_vectordb.py
LLM_MODEL = "openai/gpt-oss-20b"

st.set_page_config(page_title="KrishiMitra AI", page_icon="🌾", layout="centered")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 820px;}
    .hero {background: linear-gradient(135deg,#2e7d32,#66bb6a); padding: 1.3rem 1.5rem;
           border-radius: 14px; color: white; margin-bottom: 1rem;}
    .hero h1 {margin: 0; font-size: 1.9rem; color: white;}
    .hero p {margin: .3rem 0 0 0; opacity: .92;}
    </style>
    <div class="hero">
        <h1>🌾 KrishiMitra AI</h1>
        <p>Upload a PDF and ask questions about it, or use the default farming guide.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- API key ----------
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
if not api_key:
    st.error("Groq API key not found. Add `GROQ_API_KEY=...` to your `.env` file and restart.")
    st.stop()

HAS_DEFAULT_DB = os.path.isdir(DB_PATH)


# ---------- Cached resources (loaded once) ----------
@st.cache_resource(show_spinner="Loading embedding model...")
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


@st.cache_resource(show_spinner=False)
def load_default_vectorstore():
    return Chroma(persist_directory=DB_PATH, embedding_function=load_embeddings())


@st.cache_resource(show_spinner=False)
def build_upload_vectorstore(_files, key: str):
    """Chunk + embed uploaded PDFs into an in-memory Chroma store (cached by file hash)."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for name, data in _files:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            pages = PyPDFLoader(tmp_path).load()
        finally:
            os.remove(tmp_path)
        for p in pages:
            p.metadata["source"] = name
        chunks.extend(splitter.split_documents(pages))

    chunks = [c for c in chunks if c.page_content.strip()]
    if not chunks:
        return None
    return Chroma.from_documents(
        documents=chunks,
        embedding=load_embeddings(),
        collection_name=f"upload_{key[:24]}",
    )


@st.cache_resource
def load_llm(temperature: float):
    return ChatGroq(model=LLM_MODEL, api_key=api_key, temperature=temperature)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are KrishiMitra AI, a helpful farming assistant.

Answer using the retrieved context.

If the context is unrelated to farming, warn the user that
the uploaded knowledge document may not be suitable for
a farming assistant and recommend uploading a farming
document instead.

If the context does not contain the answer, clearly state
that limitation. Never invent information and never claim
that you searched the internet unless you actually did.

Retrieved context:
{context}""",
    ),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


# ---------- Sidebar ----------
with st.sidebar:
    st.header("📄 Knowledge source")
    uploaded = st.file_uploader(
        "Upload your PDF(s)", type=["pdf"], accept_multiple_files=True,
        help="Remove the file to go back to the default farming guide.",
    )

    vectorstore = None
    source_label = None
    if uploaded:
        files = [(f.name, f.getvalue()) for f in uploaded]
        key = hashlib.sha256(b"".join(d for _, d in files)).hexdigest()
        with st.spinner("Reading and embedding your PDF... (first time only)"):
            try:
                vectorstore = build_upload_vectorstore(files, key)
            except Exception as e:
                st.error(f"Could not read PDF: {e}")
        if vectorstore is None and not st.session_state.get("_x"):
            st.warning("No text found in the PDF (it may be scanned images).")
        source_label = "Uploaded: " + ", ".join(n for n, _ in files)
    if vectorstore is None:
        if HAS_DEFAULT_DB:
            vectorstore = load_default_vectorstore()
            source_label = "Default farming guide"
        else:
            st.error("No default vector DB found. Upload a PDF to start.")
            st.stop()

    st.success(f"Active: {source_label}")

    # reset chat when the knowledge source changes
    if st.session_state.get("active_source") != source_label:
        st.session_state.active_source = source_label
        st.session_state.messages = []

    st.divider()
    st.header("⚙️ Settings")
    k = st.slider("Chunks to retrieve (k)", 1, 10, 4)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    show_sources = st.toggle("Show sources", value=True)
    st.divider()
    try:
        st.caption(f"📚 Chunks in database: {vectorstore._collection.count()}")
    except Exception:
        pass
    st.caption(f"🤖 Model: `{LLM_MODEL}`")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**Try asking:**")
    examples = [
        "What are the best practices for irrigation?",
        "How do I improve soil fertility?",
        "How can I control pests naturally?",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex

# ---------- Chat state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []


def render_sources(sources):
    with st.expander(f"📄 Sources ({len(sources)})"):
        for i, s in enumerate(sources, 1):
            page = s.get("page")
            label = f"Chunk {i}"
            if s.get("file"):
                label += f" · {s['file']}"
            if isinstance(page, int):
                label += f" · page {page + 1}"
            st.markdown(f"**{label}**")
            st.caption(s["text"])


for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍🌾" if msg["role"] == "user" else "🌾"):
        st.markdown(msg["content"])
        if show_sources and msg.get("sources"):
            render_sources(msg["sources"])

# ---------- Input ----------
user_input = st.chat_input("Ask a question about the document...")
question = st.session_state.pop("pending", None) or user_input

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.markdown(question)

    # last 3 exchanges as conversation history (excluding the current question)
    history = [
        ("human" if m["role"] == "user" else "ai", m["content"])
        for m in st.session_state.messages[:-1][-6:]
    ]

    with st.chat_message("assistant", avatar="🌾"):
        try:
            with st.spinner("Searching the document..."):
                docs = vectorstore.similarity_search(question, k=k)

            chain = prompt | load_llm(temperature) | StrOutputParser()
            answer = st.write_stream(
                chain.stream({
                    "context": format_docs(docs),
                    "question": question,
                    "history": history,
                })
            )

            sources = [
                {"text": d.page_content.strip(), "page": d.metadata.get("page"),
                 "file": os.path.basename(str(d.metadata.get("source", "")))}
                for d in docs
            ]
            if show_sources:
                render_sources(sources)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )
        except Exception as e:
            st.error(f"Error: {e}")
