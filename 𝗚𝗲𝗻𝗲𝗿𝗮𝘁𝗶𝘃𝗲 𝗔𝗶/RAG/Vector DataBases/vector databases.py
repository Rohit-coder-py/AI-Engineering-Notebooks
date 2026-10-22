#next step is to create vctor embeddings of the chunks and store them into vector databases


#convert chunks into embeddings



from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load the PDF
pdf_path = r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Krishi Mitra AI\krishimitra_ai_notes\ai_notes.pdf"

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print("PDF pages loaded:", len(documents))

# Split the PDF into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))

# Load the embedding model
embedding = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B"
)

# Create embeddings and store them in ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db"
)

#  Verify storage
print("Total chunks stored:", vectorstore._collection.count())



result = vectorstore.similarity_search("What is AI?",k=3)

for r in result:
    print(r.page_content)
    
    
from dotenv import load_dotenv

import os


load_dotenv()

api_key = os.getenv("GROK_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")


from langchain_groq import ChatGroq


model = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)


retreiver = vectorstore.as_retriever()        #similarity search


docs = retreiver.invoke("What is AI? ")

for d in docs:
    print(d)

print("\n\n\n\n\n\n Now generating answers using groq ai")
from langchain_core.prompts import ChatPromptTemplate

question = "What is AI?"

docs = retreiver.invoke(question)

context = "\n\n".join(
    doc.page_content for doc in docs
)

prompt = ChatPromptTemplate.from_template("""
Answer the question using the context provided.
If the answer is not present in the context, say so.

Context:
{context}

Question:
{question}
""")

chain = prompt | model

response = chain.invoke({
    "context": context,
    "question": question
})

print("\n--- KrishiMitra AI Answer ---")
print(response.content)