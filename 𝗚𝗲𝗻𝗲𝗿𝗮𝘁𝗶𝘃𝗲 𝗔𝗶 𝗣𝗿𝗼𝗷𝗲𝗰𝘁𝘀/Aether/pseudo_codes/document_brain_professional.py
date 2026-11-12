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
            st.session_state.document_pages = len(reader.pages)
            st.session_state.document_chunks = len(total_chunks)

            # A new document should start a new chat.
            st.session_state.messages = []

            st.success("Document processed successfully!")

    except Exception as error:
        st.error(f"An error occurred while processing the PDF: {error}")
        st.stop()

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