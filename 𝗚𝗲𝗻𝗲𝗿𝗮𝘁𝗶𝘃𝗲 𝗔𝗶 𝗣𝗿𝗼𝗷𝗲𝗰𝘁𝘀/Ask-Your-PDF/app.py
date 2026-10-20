"""
app.py  —  the Streamlit user interface of Ask Your PDF
Run it with:  streamlit run app.py
"""

import html
import io
import os

import streamlit as st

import core

# ----------------------------------------------------------------------
# Paths (built from this file's location, so they work on any computer)
# ----------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "assets", "logo.png")
STYLE_PATH = os.path.join(APP_DIR, "assets", "style.css")
SAMPLE_PDF_PATH = os.path.join(APP_DIR, "sample_data", "Intro_to_LLMs.pdf")

STARTER_QUESTIONS = [
    "What is this document about?",
    "What are the key points?",
    "Explain the main concepts in simple words.",
]

st.set_page_config(page_title="Ask Your PDF", page_icon=LOGO_PATH, layout="wide")

# Load our custom colours / styling
with open(STYLE_PATH, encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Session state = the app's memory between clicks
# ----------------------------------------------------------------------
defaults = {
    "chat": [],               # all messages: {"role", "content", "sources"}
    "vector_store": None,     # FAISS index of the current PDF
    "stats": None,            # pages / chunks / words
    "file_id": None,          # which PDF is loaded
    "process_key": None,      # PDF + chunk settings that were used
    "use_sample": False,      # is the sample PDF selected?
    "uploader_key": 0,        # changing it clears the upload box
    "queued_question": None,  # question coming from a starter button
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


@st.cache_resource(show_spinner="Loading the embedding model (only the first time)...")
def get_embedding_model():
    """Load the embedding model once and reuse it for every user and every PDF."""
    return core.load_embedding_model()


def start_over():
    """Forget the current PDF and chat, and clear the upload box."""
    st.session_state.chat = []
    st.session_state.vector_store = None
    st.session_state.stats = None
    st.session_state.file_id = None
    st.session_state.process_key = None
    st.session_state.use_sample = False
    st.session_state.uploader_key += 1


# ----------------------------------------------------------------------
# Sidebar: upload + settings
# ----------------------------------------------------------------------
with st.sidebar:
    st.image(LOGO_PATH, width=130)
    st.markdown("### 📂 1. Add your PDF")

    uploaded = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        key=f"uploader_{st.session_state.uploader_key}",
        label_visibility="collapsed",
    )

    if st.button("✨ Try the sample PDF", use_container_width=True):
        st.session_state.use_sample = True

    st.markdown("### ⚙️ 2. Settings")
    with st.expander("Answer quality", expanded=False):
        temperature = st.slider(
            "Temperature", 0.0, 1.0, 0.2, 0.1,
            help="Controls randomness. Low = focused and factual, high = more creative.",
        )
        top_k = st.slider(
            "Chunks to retrieve (k)", 1, 8, 4,
            help="How many PDF chunks are sent to the AI with every question.",
        )
    with st.expander("Chunking (advanced)", expanded=False):
        chunk_size = st.slider(
            "Chunk size", 500, 2000, 1000, 100,
            help="How many characters each chunk contains.",
        )
        chunk_overlap = st.slider(
            "Chunk overlap", 0, 400, 150, 50,
            help="Characters shared between neighbouring chunks so no sentence is cut in half.",
        )

    st.markdown("### 🧰 3. Actions")
    if st.button("🧹 Clear chat", use_container_width=True):
        st.session_state.chat = []
    if st.button("🔄 Start over", use_container_width=True):
        start_over()
        st.rerun()

    st.caption(f"Model: `{core.MODEL_NAME}` via Groq\n\nEmbeddings: `all-MiniLM-L6-v2`")


# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Ask Your <span>PDF</span></h1>
        <p>Upload any PDF and chat with it. Every answer comes with its source page.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Safety check: is the API key available?
# ----------------------------------------------------------------------
if not core.get_api_key():
    st.error(
        "🔑 **GROQ_API_KEY not found.** Create a file named `.env` next to `app.py` "
        "and add this line:  `GROQ_API_KEY=your_key_here`  (get a free key at console.groq.com)."
    )
    st.stop()

# ----------------------------------------------------------------------
# Decide which PDF to use (upload has priority over the sample)
# ----------------------------------------------------------------------
pdf_name, pdf_bytes = None, None
if uploaded is not None:
    pdf_name, pdf_bytes = uploaded.name, uploaded.getvalue()
elif st.session_state.use_sample:
    with open(SAMPLE_PDF_PATH, "rb") as sample_file:
        pdf_name, pdf_bytes = os.path.basename(SAMPLE_PDF_PATH), sample_file.read()

# ----------------------------------------------------------------------
# Landing page (shown until a PDF is added)
# ----------------------------------------------------------------------
if pdf_bytes is None:
    st.markdown(
        """
        <div class="card-row">
            <div class="card blue"><div class="icon">📄</div><h4>Upload</h4>
                <p>Drop any text-based PDF: notes, papers, reports, manuals.</p></div>
            <div class="card red"><div class="icon">💬</div><h4>Ask</h4>
                <p>Type your question in plain English, just like you would ask a friend.</p></div>
            <div class="card navy"><div class="icon">📌</div><h4>Verify</h4>
                <p>Get answers with page numbers and the exact text they came from.</p></div>
        </div>
        <div class="steps">
            <h3>How it works</h3>
            <ol>
                <li><b>Read</b> the PDF and extract the text of every page</li>
                <li><b>Split</b> the text into small overlapping chunks</li>
                <li><b>Embed</b> each chunk into a vector and store it in FAISS</li>
                <li><b>Retrieve</b> the chunks most similar to your question</li>
                <li><b>Generate</b> an answer from those chunks with an LLM on Groq</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("👈 Upload a PDF in the sidebar, or click **Try the sample PDF** to see it in action.")
    st.stop()

# ----------------------------------------------------------------------
# Process the PDF (only when the file or the chunk settings change)
# ----------------------------------------------------------------------
file_id = (pdf_name, len(pdf_bytes))
process_key = (file_id, chunk_size, chunk_overlap)

if st.session_state.process_key != process_key:
    if chunk_overlap >= chunk_size:
        st.error("Chunk overlap must be smaller than chunk size. Please change it in the sidebar.")
        st.stop()

    try:
        with st.spinner("📖 Reading your PDF and building the search index..."):
            pages, total_pages = core.read_pdf(io.BytesIO(pdf_bytes))

            if not pages:
                st.warning(
                    "⚠️ I couldn't find any text in this PDF. It may be a scanned document "
                    "(images only). Please try a PDF with selectable text."
                )
                st.stop()

            chunks = core.split_into_chunks(pages, chunk_size, chunk_overlap)
            vector_store = core.build_vector_store(chunks, get_embedding_model())
    except Exception as error:
        st.error(f"❌ Could not read this PDF: {error}")
        st.stop()

    # A new file means a fresh conversation
    if st.session_state.file_id != file_id:
        st.session_state.chat = []

    st.session_state.vector_store = vector_store
    st.session_state.stats = {
        "pages": total_pages,
        "chunks": len(chunks),
        "words": sum(len(page.page_content.split()) for page in pages),
    }
    st.session_state.file_id = file_id
    st.session_state.process_key = process_key

# ----------------------------------------------------------------------
# Document summary cards
# ----------------------------------------------------------------------
stats = st.session_state.stats
st.markdown(
    f"""
    <div class="stat-row">
        <div class="stat"><span>📄 File</span><b>{pdf_name}</b></div>
        <div class="stat"><span>📑 Pages</span><b>{stats['pages']}</b></div>
        <div class="stat"><span>🧩 Chunks</span><b>{stats['chunks']}</b></div>
        <div class="stat"><span>📝 Words</span><b>{stats['words']:,}</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)


def show_sources(sources):
    """Show the PDF chunks that were used to create an answer."""
    pages = sorted({s["page"] for s in sources if isinstance(s["page"], int)})
    page_text = ", ".join(str(p) for p in pages)
    with st.expander(f"📚 Sources: page {page_text}"):
        for rank, source in enumerate(sources, start=1):
            st.markdown(f"**Match #{rank}** · Page {source['page']}")
            # Show the chunk as one clean line of text (html.escape keeps PDF symbols safe)
            one_line = html.escape(source["text"].replace("\n", " "))
            st.markdown(f'<div class="source-text">{one_line}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Get the new question (typed in the box, or clicked from a starter button)
# ----------------------------------------------------------------------
question = st.chat_input("Ask a question about your PDF...")
if question is None and st.session_state.queued_question:
    question = st.session_state.queued_question
st.session_state.queued_question = None

# ----------------------------------------------------------------------
# Chat history
# ----------------------------------------------------------------------
for message in st.session_state.chat:
    avatar = LOGO_PATH if message["role"] == "assistant" else "🧑‍🎓"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("sources"):
            show_sources(message["sources"])

# Starter questions (only while the chat is empty and nothing is being answered)
if not st.session_state.chat and not question:
    st.markdown("##### 💡 Not sure where to start? Try one of these:")
    columns = st.columns(len(STARTER_QUESTIONS))
    for column, starter in zip(columns, STARTER_QUESTIONS):
        if column.button(starter, use_container_width=True):
            st.session_state.queued_question = starter
            st.rerun()

# ----------------------------------------------------------------------
# New question -> retrieve chunks -> ask the LLM -> show the answer
# ----------------------------------------------------------------------
if question and question.strip():
    question = question.strip()

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(question)

    with st.chat_message("assistant", avatar=LOGO_PATH):
        try:
            with st.spinner("🔎 Searching the PDF and thinking..."):
                chunks = core.find_relevant_chunks(st.session_state.vector_store, question, top_k)
                model = core.get_model(temperature)
                answer = core.ask_pdf(model, question, chunks, st.session_state.chat)

            # If the PDF does not contain the answer, don't show unrelated sources
            if "couldn't find that" in answer.lower():
                chunks = []

            st.markdown(answer)
            if chunks:
                show_sources(chunks)

            # Save both messages so they appear after the next rerun
            st.session_state.chat.append({"role": "user", "content": question})
            st.session_state.chat.append({"role": "assistant", "content": answer, "sources": chunks})
        except Exception as error:
            st.error(
                f"⚠️ Something went wrong while getting the answer: {error}\n\n"
                "Check your API key and internet connection, then try again."
            )

# ----------------------------------------------------------------------
# Download the conversation
# ----------------------------------------------------------------------
if st.session_state.chat:
    with st.sidebar:
        st.download_button(
            "⬇️ Download chat (.txt)",
            data=core.chat_to_text(st.session_state.chat, pdf_name),
            file_name="ask_your_pdf_chat.txt",
            use_container_width=True,
        )
