from dotenv import load_dotenv
import streamlit as st
import os
import hashlib

import trafilatura
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


load_dotenv()

api_key = os.getenv("GROK_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")


#basic settings

APP_PATH = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_PATH, "assets", "logo.png")

st.set_page_config(page_title="Flipkart Shopping Assistant", page_icon=LOGO_PATH, layout="centered")


#ui styling (yellow + black + purple)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --yellow: #FFD60A;
    --yellow-soft: rgba(255, 214, 10, 0.12);
    --purple: #7C3AED;
    --purple-light: #A78BFA;
    --purple-soft: rgba(124, 58, 237, 0.18);
    --black: #09090F;
    --card: #14141F;
    --card-2: #1B1B2B;
    --border: rgba(255, 255, 255, 0.08);
    --text: #F4F4F8;
    --muted: #9A9AB0;
}

html, body, [class*="css"], .stApp {
    font-family: 'Poppins', sans-serif;
}

/* background */
.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(124, 58, 237, 0.28) 0%, transparent 45%),
        radial-gradient(circle at 90% 10%, rgba(255, 214, 10, 0.10) 0%, transparent 40%),
        var(--black);
    color: var(--text);
}

/* hide default streamlit chrome */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { right: 1rem; }

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 7rem;
    max-width: 780px;
}

/* hero */
.hero {
    text-align: center;
    padding: 2rem 1.2rem 1.6rem 1.2rem;
    margin-bottom: 1.4rem;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.30), rgba(20, 20, 31, 0.9) 55%, rgba(255, 214, 10, 0.10));
    border: 1px solid var(--border);
    box-shadow: 0 10px 40px rgba(124, 58, 237, 0.20);
}
.hero-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    background: var(--yellow);
    color: #000;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 0.9rem;
}
.hero h1 {
    margin: 0;
    padding: 0;
    font-size: 2.3rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.2;
}
.hero h1 span {
    background: linear-gradient(90deg, var(--yellow), var(--purple-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    margin: 0.7rem 0 0 0;
    color: var(--muted);
    font-size: 0.98rem;
}

/* default st.write text */
[data-testid="stMarkdownContainer"] p {
    color: var(--text);
}

/* labels */
[data-testid="stWidgetLabel"] p {
    color: var(--yellow) !important;
    font-weight: 600;
    font-size: 0.95rem;
}

/* url input */
[data-testid="stTextInput"] input {
    background: var(--card);
    color: var(--text);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-size: 0.95rem;
    transition: all 0.2s ease;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--yellow);
    box-shadow: 0 0 0 3px var(--yellow-soft);
}
[data-testid="stTextInput"] input::placeholder {
    color: var(--muted);
}

/* expander (product details) */
[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 4px solid var(--purple);
    border-radius: 14px;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: var(--yellow);
    font-weight: 600;
}
[data-testid="stExpander"] summary:hover {
    color: var(--purple-light);
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li {
    color: var(--text);
}

/* chunks caption */
[data-testid="stCaptionContainer"] {
    display: inline-block;
    margin-top: 0.7rem;
    padding: 4px 14px;
    border-radius: 999px;
    background: var(--purple-soft);
    border: 1px solid rgba(167, 139, 250, 0.35);
}
[data-testid="stCaptionContainer"] p {
    color: var(--purple-light) !important;
    font-size: 0.8rem;
    font-weight: 500;
}

/* chat messages */
[data-testid="stChatMessage"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: var(--text);
}
[data-testid="stChatMessage"] strong {
    color: var(--yellow);
}
[data-testid="stChatMessage"] code {
    background: var(--card-2);
    color: var(--yellow);
    border-radius: 6px;
}
[data-testid="stChatMessage"] table th {
    background: var(--purple-soft);
    color: var(--yellow);
}
[data-testid="stChatMessage"] table td {
    color: var(--text);
}

/* user message = purple tint, assistant message = yellow tint */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, var(--purple-soft), var(--card));
    border-color: rgba(167, 139, 250, 0.35);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: linear-gradient(135deg, var(--yellow-soft), var(--card));
    border-color: rgba(255, 214, 10, 0.30);
}

/* avatars */
[data-testid="stChatMessageAvatarUser"] {
    background: var(--purple) !important;
    color: #fff !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--yellow) !important;
    color: #000 !important;
}

/* chat input */
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: linear-gradient(to top, var(--black) 70%, transparent);
}
[data-testid="stChatInput"] {
    background: var(--card);
    border: 1.5px solid var(--purple);
    border-radius: 18px;
    box-shadow: 0 6px 24px rgba(124, 58, 237, 0.25);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--yellow);
    box-shadow: 0 0 0 3px var(--yellow-soft), 0 6px 24px rgba(255, 214, 10, 0.15);
}
[data-testid="stChatInput"] textarea {
    background: transparent;
    color: var(--text);
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--muted);
}
[data-testid="stChatInput"] button {
    background: var(--yellow);
    color: #000;
    border-radius: 12px;
}
[data-testid="stChatInput"] button:hover {
    background: var(--purple);
    color: #fff;
}

/* alerts (warning / success / error) */
[data-testid="stAlert"] {
    background: var(--yellow-soft);
    border: 1px solid rgba(255, 214, 10, 0.35);
    border-radius: 14px;
}
[data-testid="stAlert"] p {
    color: var(--yellow) !important;
    font-weight: 500;
}

/* spinner */
[data-testid="stSpinner"] p {
    color: var(--purple-light) !important;
}
.stSpinner > div {
    border-top-color: var(--yellow) !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: var(--purple); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: var(--yellow); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-badge">RAG POWERED</div>
    <h1>Flipkart <span>Shopping</span> Assistant</h1>
    <p>Paste any product link and ask anything about it.</p>
</div>
""", unsafe_allow_html=True)

st.write("Your Shopping Assistant")


#models

@st.cache_resource
def get_model():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=api_key,
        temperature=0.3,
        streaming=True)

@st.cache_resource
def refine_model():
    return ChatMistralAI(
        model="ministral-8b-latest",
        api_key=mistral_api_key,
        temperature=0)

#defining embedding models here so we dont need to initialize it everytime we start
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

embedding = get_embedding_model()


#system prompts

#1. For mistral to refine the details for better output
prompt_refine = ChatPromptTemplate([
    ("system", """
I had provided you a product details from flipkart.com
Your work :
Format the provided data make it good and defined structured and send it again
RULES:
Only 1 product at once remove noise from that provided text
Dont leave any details behind include each and evry details in a structured format

Provide structured version of the raw text
And cover each and evry important info provided in that raw text dont miss any 

Important : If the link doesnt belong to any shopping site or doesnt contain any kind of product deatils dont assume just return this link is not valid or whatever the reason is but dont assume anything by your own .
And most important just provide deatils in structured format with not ny extra stuff like here it is and all just product data 
Here is the raw text details :{raw_text}
""") ])

#2. For groq to answer the user's question
prompt_answer = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a product shopping assistant.
Answer the user's question using only the provided product context.
If the answer is not available in the context,
say that the product details do not specify it.
Do not invent product specifications.

Product context:
{context}"""
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])


#chains

refine_chain = prompt_refine | refine_model() | StrOutputParser()
answer_chain = prompt_answer | get_model() | StrOutputParser()


#cached pipeline steps (each runs only once per url)

@st.cache_data(show_spinner="Fetching product page...")
def get_raw_text(url):
    html = trafilatura.fetch_url(url)
    return trafilatura.extract(html) if html else None

@st.cache_data(show_spinner="Refining product details...")
def refine_product(raw_text):
    return refine_chain.invoke({"raw_text": raw_text})

#now  we will follow the rag pipeline now

#1. Document Loaders  -> get_raw_text
#2. Textsplitting
#3. embeddings generation
#4. vectordb
#5. Retreival

@st.cache_resource(show_spinner="Building vector database...")
def build_retriever(document):
    # 2. Text splitting
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(document)

    # 3 + 4. Embeddings + vector database (unique collection per product)
    collection = "product_" + hashlib.md5(document.encode()).hexdigest()[:16]
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embedding,
        collection_name=collection
    )

    # 5. Retriever
    return vectorstore.as_retriever(search_kwargs={"k": 4}), len(chunks)


#get product info

url = st.text_input("Enter website URL: ")

raw_text = get_raw_text(url) if url else None

if raw_text:

    # reset chat when a new product url is entered
    if st.session_state.get("current_url") != url:
        st.session_state.current_url = url
        st.session_state.messages = []

    # 1. Refine the product details only once
    document = refine_product(raw_text)
    with st.expander("Product Details"):
        st.write(document)

    retriever, n_chunks = build_retriever(document)
    st.caption(f"Total No. of Chunks: {n_chunks}")

    # Conversation History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask about this product...")

    if question:
        # Show user message
        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve relevant product information
        results = retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content for doc in results
        )

        # last 6 messages are enough as history (saves tokens + time)
        history = [
            ("human" if m["role"] == "user" else "ai", m["content"])
            for m in st.session_state.messages[-6:]
        ]

        # Stream the answer token by token
        with st.chat_message("assistant"):
            answer = st.write_stream(
                answer_chain.stream({
                    "context": context,
                    "history": history,
                    "question": question
                })
            )

        # Save both messages
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    st.warning("Please enter a valid product URL.")