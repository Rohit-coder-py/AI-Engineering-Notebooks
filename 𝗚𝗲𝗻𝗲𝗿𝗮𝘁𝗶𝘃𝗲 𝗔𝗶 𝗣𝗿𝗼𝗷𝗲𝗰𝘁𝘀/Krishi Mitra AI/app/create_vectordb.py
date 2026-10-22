
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Load PDF
pdf_path = r"C:\Users\rohit\Downloads\farming_guide_10_pages.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("PDF pages loaded:", len(documents))

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))

# 3. Load embedding model
embedding = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B"
)

# 4. Store chunks and embeddings in ChromaDB
# Use a separate database directory for this PDF
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./deep_learning_chroma_db"
)

print("Total chunks stored:", vectorstore._collection.count())

# 5. Load Groq API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# 6. Load Groq LLM
model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    temperature=0
)

# 7. Retrieve relevant chunks
question = "What is AI?"

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

docs = retriever.invoke(question)

print("\n--- Retrieved Chunks ---")

for i, doc in enumerate(docs, start=1):
    print(f"\nChunk {i}:")
    print(doc.page_content)

# 8. Prepare context
context = "\n\n".join(
    doc.page_content for doc in docs
)

# 9. Generate answer using Groq
prompt = ChatPromptTemplate.from_template("""
Answer the question using the context provided.

If the context does not contain enough information,
clearly say so. Do not invent facts.

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
