import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
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
        <p>Your farming assistant, answering from your farming guide.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- API key ----------
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
if not api_key:
    st.error("Groq API key not found. Add `GROQ_API_KEY=...` to your `.env` file and restart.")
    st.stop()

if not os.path.isdir(DB_PATH):
    st.error(f"Vector database not found at `{DB_PATH}`. Run `create_vectordb.py` first.")
    st.stop()


# ---------- Cached resources (loaded once) ----------
@st.cache_resource(show_spinner="Loading embedding model and knowledge base...")
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)


@st.cache_resource
def load_llm(temperature: float):
    return ChatGroq(model=LLM_MODEL, api_key=api_key, temperature=temperature)


vectorstore = load_vectorstore()

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
            label = f"Chunk {i}" + (f" · page {page + 1}" if isinstance(page, int) else "")
            st.markdown(f"**{label}**")
            st.caption(s["text"])


for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍🌾" if msg["role"] == "user" else "🌾"):
        st.markdown(msg["content"])
        if show_sources and msg.get("sources"):
            render_sources(msg["sources"])

# ---------- Input ----------
user_input = st.chat_input("Ask a farming question...")
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
            with st.spinner("Searching your farming guide..."):
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
                {"text": d.page_content.strip(), "page": d.metadata.get("page")}
                for d in docs
            ]
            if show_sources:
                render_sources(sources)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )
        except Exception as e:
            st.error(f"Error: {e}")
