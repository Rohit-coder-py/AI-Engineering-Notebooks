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


# =====================================
# Basic Settings
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
st.write("Document Brain")

file_upload = st.file_uploader("Upload your file :",max_upload_size=100)


if file_upload:
    #reading the pdf

    reader = PdfReader(file_upload)

    st.write(f"Total No. of pages :",len(reader.pages))

    documents = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            documents.append(Document(
                page_content=text,metadata={"page": page_number + 1}))

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

    if question:

        retreived_docs = vector_db.similarity_search(question,k = 4)

        context = "\n\n".join([doc.page_content for doc in retreived_docs])


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




#this part is completes
        
        
#remaining in this file : Source citation with page numbers 