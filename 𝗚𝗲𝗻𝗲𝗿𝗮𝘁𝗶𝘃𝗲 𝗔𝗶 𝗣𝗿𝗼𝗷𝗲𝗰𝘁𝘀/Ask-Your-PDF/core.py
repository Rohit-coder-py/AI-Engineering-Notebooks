
import os

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the secret API key from the .env file
load_dotenv()


# ----------------------------------------------------------------------
# Settings (change them here if you want to try other models)
# ----------------------------------------------------------------------
MODEL_NAME = "openai/gpt-oss-20b"                              # chat model (runs on Groq)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # embedding model (runs locally, free)
MAX_HISTORY_MESSAGES = 6   # only the last 6 messages are sent to the LLM (keeps cost + speed under control)


# ----------------------------------------------------------------------
# The system prompt (a reusable prompt template with a {context} variable)
# ----------------------------------------------------------------------
SYSTEM_PROMPT = """You are "Ask Your PDF", a careful and friendly document assistant.

Answer the user's question using ONLY the context taken from their PDF below.

Rules:
1. If the answer is not in the context, say clearly: "I couldn't find that in your PDF."
   Do not use outside knowledge and do not guess.
2. Mention the page number(s) your answer comes from, for example (Page 3).
3. Keep answers clear and concise. Use bullet points when they make the answer easier to read.
4. Use the earlier conversation only to understand follow-up questions.

Context from the PDF:
{context}
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
])


# ----------------------------------------------------------------------
# Step 1: Read the PDF
# ----------------------------------------------------------------------
def read_pdf(pdf_file):
    """Read a PDF and return (pages, total_pages).

    `pages` is a list of LangChain Documents - one per page that contains text.
    Each Document remembers its page number in `metadata`, so we can show
    the source of every answer later.
    """
    reader = PdfReader(pdf_file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:  # skip empty pages (for example scanned images)
            pages.append(Document(page_content=text, metadata={"page": page_number}))

    return pages, len(reader.pages)


# ----------------------------------------------------------------------
# Step 2: Split the pages into small chunks
# ----------------------------------------------------------------------
def split_into_chunks(pages, chunk_size=1000, chunk_overlap=150):
    """Cut long pages into smaller overlapping chunks.

    Why? An LLM has a limited context window, and small chunks make
    the search more accurate. The overlap stops a sentence from being
    cut in half and losing its meaning.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(pages)


# ----------------------------------------------------------------------
# Step 3: Embeddings + vector store
# ----------------------------------------------------------------------
def load_embedding_model():
    """Load the Hugging Face embedding model (downloaded once, then runs locally)."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        encode_kwargs={"normalize_embeddings": True},  # makes the match score easy to read
    )


def build_vector_store(chunks, embedding_model):
    """Turn every chunk into a vector and store them all in FAISS."""
    return FAISS.from_documents(chunks, embedding_model)


# ----------------------------------------------------------------------
# Step 4: Retrieval - find the chunks that match the question
# ----------------------------------------------------------------------
def find_relevant_chunks(vector_store, question, k=4):
    """Return the k chunks that are most similar to the question.

    FAISS gives a *distance* (smaller = closer). Because our vectors are
    normalised, we can turn it into an easy 0-100 % "match" score.
    """
    results = vector_store.similarity_search_with_score(question, k=k)

    chunks = []
    for doc, distance in results:
        match = max(0.0, min(1.0, 1 - float(distance) / 2))
        chunks.append({
            "text": doc.page_content,
            "page": doc.metadata.get("page", "?"),
            "match": match,
        })
    return chunks


# ----------------------------------------------------------------------
# Step 5: Ask the LLM
# ----------------------------------------------------------------------
def get_api_key():
    return os.getenv("GROQ_API_KEY")


def get_model(temperature=0.2):
    """Create the Groq chat model. Low temperature = focused, factual answers."""
    return ChatGroq(
        model=MODEL_NAME,
        api_key=get_api_key(),
        temperature=temperature,
    )


def history_to_messages(chat_history):
    """Convert our saved chat (list of dicts) into LangChain message objects.

    Only the last MAX_HISTORY_MESSAGES are kept, so the conversation
    can never grow forever and hit the token limit.
    """
    messages = []
    for item in chat_history[-MAX_HISTORY_MESSAGES:]:
        if item["role"] == "user":
            messages.append(HumanMessage(content=item["content"]))
        else:
            messages.append(AIMessage(content=item["content"]))
    return messages


def ask_pdf(model, question, chunks, chat_history):
    """Build the full prompt (system + context + history + question) and get the answer."""
    # 1. Put the retrieved chunks into one block of text, with page numbers
    context = "\n\n".join(f"[Page {c['page']}]\n{c['text']}" for c in chunks)

    # 2. Fill the {context} variable of the system prompt template
    system_messages = prompt_template.invoke({"context": context}).to_messages()

    # 3. system message + recent chat history + the new question
    messages = system_messages + history_to_messages(chat_history) + [HumanMessage(content=question)]

    # 4. Ask the model
    response = model.invoke(messages)
    return response.content


# ----------------------------------------------------------------------
# Extra: export the conversation as plain text
# ----------------------------------------------------------------------
def chat_to_text(chat_history, pdf_name):
    lines = [f"Ask Your PDF - chat about: {pdf_name}", "=" * 50, ""]
    for item in chat_history:
        speaker = "You" if item["role"] == "user" else "Assistant"
        lines.append(f"{speaker}: {item['content']}")
        lines.append("")
    return "\n".join(lines)
