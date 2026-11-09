import os
from dotenv import load_dotenv

import json
import hashlib
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
# Neobrutalism Style
#-------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --nb-bg: #FFFBEB;
    --nb-ink: #000000;
    --nb-yellow: #FFD93D;
    --nb-pink: #FF6B9D;
    --nb-blue: #4D96FF;
    --nb-green: #6BCB77;
    --nb-white: #FFFFFF;
    --nb-border: 3px solid #000000;
    --nb-shadow: 6px 6px 0px #000000;
    --nb-shadow-sm: 4px 4px 0px #000000;
}

/* ---------- App background ---------- */
.stApp {
    background-color: var(--nb-bg);
    background-image:
        linear-gradient(rgba(0,0,0,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px);
    background-size: 32px 32px;
    font-family: 'Space Grotesk', sans-serif;
    color: var(--nb-ink);
}

header[data-testid="stHeader"] {
    background: var(--nb-yellow);
    border-bottom: var(--nb-border);
}

.stMainBlockContainer {
    max-width: 860px;
    padding-top: 3rem;
}

/* ---------- Text ---------- */
html, body, p, span, label, li, div {
    font-family: 'Space Grotesk', sans-serif;
}
p, label, li, span {
    color: var(--nb-ink);
}

/* Each st.write block becomes a brutalist card */
div[data-testid="stElementContainer"]:has(> div[data-testid="stMarkdown"]) {
    background: var(--nb-white);
    border: var(--nb-border);
    box-shadow: var(--nb-shadow-sm);
    padding: 0.6rem 1.1rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

/* first block = title banner */
div[data-testid="stMainBlockContainer"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:first-child:has(> div[data-testid="stMarkdown"]) {
    background: var(--nb-pink);
    box-shadow: var(--nb-shadow);
    transform: rotate(-1deg);
    padding: 1rem 1.4rem;
    margin-bottom: 1.2rem;
}
div[data-testid="stMainBlockContainer"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:first-child:has(> div[data-testid="stMarkdown"]) p {
    font-size: 2.2rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -1px;
    margin: 0;
}

/* ---------- File uploader ---------- */
div[data-testid="stFileUploader"] label p {
    font-weight: 700;
    font-size: 1.1rem;
    text-transform: uppercase;
}
section[data-testid="stFileUploaderDropzone"] {
    background: var(--nb-yellow);
    border: var(--nb-border);
    border-style: dashed;
    border-radius: 0;
    box-shadow: var(--nb-shadow);
    padding: 1.2rem;
}
section[data-testid="stFileUploaderDropzone"] * {
    color: var(--nb-ink) !important;
    font-weight: 500;
}
section[data-testid="stFileUploaderDropzone"] button {
    background: var(--nb-blue);
    color: var(--nb-ink);
    border: var(--nb-border);
    border-radius: 0;
    box-shadow: var(--nb-shadow-sm);
    font-weight: 700;
    text-transform: uppercase;
    transition: transform 0.1s, box-shadow 0.1s;
}
section[data-testid="stFileUploaderDropzone"] button:hover {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #000000;
    background: var(--nb-green);
    color: var(--nb-ink);
}
section[data-testid="stFileUploaderDropzone"] button:active {
    transform: translate(4px, 4px);
    box-shadow: 0px 0px 0px #000000;
}

/* uploaded file chip */
div[data-testid="stFileUploaderFile"] {
    background: var(--nb-white);
    border: var(--nb-border);
    box-shadow: var(--nb-shadow-sm);
    margin-top: 0.8rem;
    padding: 0.3rem 0.6rem;
}

/* ---------- Spinner / alerts ---------- */
div[data-testid="stAlert"] {
    background: var(--nb-white);
    border: var(--nb-border);
    border-radius: 0;
    box-shadow: var(--nb-shadow-sm);
}

/* ---------- Chat messages ---------- */
div[data-testid="stChatMessage"] {
    border: var(--nb-border);
    border-radius: 0;
    box-shadow: var(--nb-shadow);
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    background: var(--nb-white);
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--nb-blue);
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: var(--nb-green);
}
div[data-testid="stChatMessage"] p {
    font-weight: 500;
    font-size: 1.02rem;
}
div[data-testid="stChatMessageAvatarUser"],
div[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--nb-yellow);
    border: var(--nb-border);
    border-radius: 0;
    color: var(--nb-ink);
}

/* ---------- Chat input ---------- */
div[data-testid="stBottom"],
div[data-testid="stBottom"] > div {
    background: var(--nb-bg);
}
div[data-testid="stChatInput"] {
    background: var(--nb-white);
    border: var(--nb-border);
    border-radius: 0;
    box-shadow: var(--nb-shadow);
}
div[data-testid="stChatInput"] textarea {
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    color: var(--nb-ink);
}
div[data-testid="stChatInput"] button {
    background: var(--nb-pink);
    border: var(--nb-border);
    border-radius: 0;
    color: var(--nb-ink);
    box-shadow: 3px 3px 0px #000000;
}
div[data-testid="stChatInput"] button:hover {
    background: var(--nb-yellow);
}

/* ---------- Code ---------- */
code, pre {
    font-family: 'Space Mono', monospace;
    background: var(--nb-yellow) !important;
    color: var(--nb-ink) !important;
    border: 2px solid #000000;
    border-radius: 0 !important;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 14px; height: 14px; }
::-webkit-scrollbar-track { background: var(--nb-bg); border-left: var(--nb-border); }
::-webkit-scrollbar-thumb { background: var(--nb-pink); border: var(--nb-border); }

/* ---------- Selection ---------- */
::selection { background: var(--nb-yellow); color: var(--nb-ink); }
</style>
""", unsafe_allow_html=True)


#-------------------------------------------------
# Basic Settings
#-------------------------------------------------

model_name = "openai/gpt-oss-20b"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
api_key = os.getenv("GROQ_API_KEY")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
RETRIEVAL_K = 4


#-------------------------------------------------
# System Prompt
#-------------------------------------------------

system_prompt = """
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


#-------------------------------------------------
# Cached Model Resources
#-------------------------------------------------

@st.cache_resource
def load_llm(model, key):

    return ChatGroq(
        model=model,
        temperature=0.2,
        api_key=key
    )


@st.cache_resource
def get_embeddings(model_name):

    return HuggingFaceEmbeddings(
        model_name=model_name
    )


# Check API key before initializing the LLM.
if not api_key:
    st.error("GROQ_API_KEY was not found. Add it to your .env file.")
    st.stop()


llm = load_llm(model_name, api_key)
embedding_model = get_embeddings(EMBEDDING_MODEL_NAME)


#-------------------------------------------------
# Prompt Template
#-------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{question}")
    ]
)


#-------------------------------------------------
# Session State Initialization
#-------------------------------------------------

# Session state keeps values available across Streamlit reruns.
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "processed_file_hash" not in st.session_state:
    st.session_state.processed_file_hash = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_pages" not in st.session_state:
    st.session_state.document_pages = 0

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = 0


#-------------------------------------------------
# Basic UI
#-------------------------------------------------

st.write("Document Reader")

file_upload = st.file_uploader(
    "Upload your file :",
    type=["pdf"],
    max_upload_size=100
)


#-------------------------------------------------
# Document Ingestion Pipeline
#-------------------------------------------------

if file_upload:

    # Read the uploaded file bytes once.
    file_bytes = file_upload.getvalue()

    # A file hash identifies the actual file content.
    # It prevents rebuilding FAISS on every Streamlit rerun.
    current_file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Process only when the uploaded file is new or changed.
    if current_file_hash != st.session_state.processed_file_hash:

        try:
            with st.spinner("Reading and processing your document..."):

                # 1. Read the PDF.
                reader = PdfReader(file_upload)

                st.write(f"Total No. of pages :", len(reader.pages))

                documents = []

                for page_number, page in enumerate(reader.pages):

                    text = page.extract_text()

                    if text and text.strip():

                        documents.append(
                            Document(
                                page_content=text,
                                metadata={
                                    "page": page_number + 1,
                                    "source": file_upload.name
                                }
                            )
                        )

                if not documents:
                    st.error(
                        "No extractable text was found in this PDF. "
                        "It may be a scanned PDF and require OCR."
                    )
                    st.stop()

                # 2. Split the extracted text into chunks.
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=CHUNK_SIZE,
                    chunk_overlap=CHUNK_OVERLAP
                )

                total_chunks = splitter.split_documents(documents)

                if not total_chunks:
                    st.error("No text chunks were created from this PDF.")
                    st.stop()

                st.write("======================\n")
                st.write("Total No. Of chunks :", len(total_chunks))

                # 3. Create the FAISS vector database.
                vector_db = FAISS.from_documents(
                    documents=total_chunks,
                    embedding=embedding_model
                )

                # Store the completed vector database in session state.
                st.session_state.vector_db = vector_db
                st.session_state.processed_file_hash = current_file_hash
                st.session_state.document_pages = len(reader.pages)
                st.session_state.document_chunks = len(total_chunks)

                # A new document should start a new chat.
                st.session_state.messages = []

                st.success("Document processed successfully!")

        except Exception as error:
            st.error(f"An error occurred while processing the PDF: {error}")
            st.stop()

    else:
        # The same file is already processed.
        st.info("This document is already processed and ready for questions.")

    # Display document information from session state.
    if st.session_state.vector_db is not None:
        st.write("Total No. of pages :", st.session_state.document_pages)
        st.write("Total No. Of chunks :", st.session_state.document_chunks)
        st.write(
            "Total Chunks stored :",
            st.session_state.vector_db.index.ntotal
        )


#-------------------------------------------------
# Chat History Display
#-------------------------------------------------

# Render previous messages after every Streamlit rerun.
for message in st.session_state.messages:

    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)


#-------------------------------------------------
# Question Answering Pipeline
#-------------------------------------------------

if st.session_state.vector_db is not None:

    question = st.chat_input("Enter your question here :")

    if question:

        # Retrieve the existing vector database.
        vector_db = st.session_state.vector_db

        # 1. Retrieve relevant document chunks.
        retrieved_docs = vector_db.similarity_search(
            question,
            k=RETRIEVAL_K
        )

        # 2. Prepare context with page metadata.
        context = "\n\n".join(
            [
                f"Page: {doc.metadata.get('page', 'Unknown')}\n"
                f"Content: {doc.page_content}"
                for doc in retrieved_docs
            ]
        )

        # 3. Invoke the RAG chain with conversation history.
        chain = prompt | llm

        try:
            with st.spinner("Generating answer..."):

                response = chain.invoke(
                    {
                        "context": context,
                        "question": question,
                        "chat_history": st.session_state.messages
                    }
                )

            # 4. Save the user question and assistant answer.
            st.session_state.messages.append(
                HumanMessage(content=question)
            )

            st.session_state.messages.append(
                AIMessage(content=response.content)
            )

            # Display the latest exchange immediately.
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                st.write(response.content)

        except Exception as error:
            st.error(f"An error occurred while generating the answer: {error}")

else:
    st.info("Upload a PDF to start asking questions.")


#-------------------------------------------------
# End of Application
#-------------------------------------------------
