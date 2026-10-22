import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

APP_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_PATH, "deep_learning_chroma_db")

api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found in .env")

# Use the SAME embedding model that created your database.
embeddings = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B"
)

# Load the existing vector database.
vectorstore = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embeddings
)

# Retrieve relevant chunks.
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# LLM
model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    temperature=0.2
)

# Prompt
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
{context}"""
    ),
    ("human", "{question}")
])


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {
        "context": retriever | format_docs,
        "question": lambda x: x["question"]
    }
    | prompt
    | model
    | StrOutputParser()
)


# Chat loop
print("KrishiMitra AI is ready!")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() in {"exit", "quit"}:
        break

    if not question:
        continue

    try:
        answer = rag_chain.invoke({"question": question})
        print("\nKrishiMitra AI:", answer, "\n")

    except Exception as e:
        print("Error:", e)