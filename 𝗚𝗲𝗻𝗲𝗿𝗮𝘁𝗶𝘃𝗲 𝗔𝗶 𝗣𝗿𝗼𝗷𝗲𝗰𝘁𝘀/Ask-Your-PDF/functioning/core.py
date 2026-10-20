import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pypdf import PdfReader

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Ask Your PDF\assets\logo.png"

MODEL_NAME = "openai/gpt-oss-20b"

model = ChatGroq(model=MODEL_NAME)

print(APP_DIR)
print(LOGO_PATH)

st.set_page_config(page_title="Ask Your PDF",page_icon=LOGO_PATH,layout="centered")

st.title("Ask your PDF")

logo = r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Ask Your PDF\assets\logo.png"

st.image(logo, width=200)

pdf = st.file_uploader("Upload your files here", type=["pdf"])

if pdf:

    reader = PdfReader(pdf)

    st.write("Analysing...")

    pages = reader.pages
    st.write(f"Reading {len(pages)} pages from your pdf...")

    content = []

    for page in pages:
        content.append(page.extract_text() or "")

    pdf_content = "\n".join(content)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Read and analyse the provided PDF content.

        Answer questions using ONLY the information in the PDF.
        If the answer is not available in the PDF, inform the user
        that the information is not present in the document.
        Do not use outside knowledge or the internet.
        """),
        ("human", """
        PDF Content:
        {pdf_content}

        User Question:
        {question}
        """)
    ])

    chain = prompt | model

    ques = st.text_input("Ask your question here:")

    if st.button("Submit"):
        if ques.strip():
            
            with st.spinner("Finding your answer..."):
                result = chain.invoke({"pdf_content": pdf_content,"question": ques})

            st.write(result.content)
        else:
            st.warning("Please enter your question.")
