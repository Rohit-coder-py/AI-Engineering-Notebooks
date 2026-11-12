import base64
import io
import os
import re
import sys
from html import escape
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))  # lets this page import patchwork.py however it is launched

import patchwork  # noqa: E402

load_dotenv()

LOGO_PATH = ROOT_DIR / "assets" / "logo.png"
APP_PATH = ROOT_DIR / "app.py"

st.set_page_config(page_title="About · AETHER", page_icon=str(LOGO_PATH), layout="wide")
patchwork.apply()



# ----------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------
@st.cache_data
def logo_data_uri(path: str, size: int = 360) -> str:
    """Shrink the logo and embed it, so the hero patch needs no static file server."""
    image = Image.open(path).convert("RGBA")
    image.thumbnail((size, size))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


@st.cache_data
def read_live_config(path: str) -> dict:
    """Read the real settings straight from app.py so this page never goes out of date."""
    defaults = {
        "model": "openai/gpt-oss-20b",
        "embedding": "sentence-transformers/all-MiniLM-L6-v2",
        "temperature": "0.2",
        "chunk_size": "1000",
        "chunk_overlap": "150",
        "retrieval_k": "4",
        "max_results": "4",
    }
    patterns = {
        "model": r'model_name\s*=\s*"([^"]+)"',
        "embedding": r'EMBEDDING_MODEL_NAME\s*=\s*"([^"]+)"',
        "temperature": r"temperature\s*=\s*([\d.]+)",
        "chunk_size": r"chunk_size\s*=\s*(\d+)",
        "chunk_overlap": r"chunk_overlap\s*=\s*(\d+)",
        "retrieval_k": r"RETRIEVAL_K\s*=\s*(\d+)",
        "max_results": r"max_results\s*=\s*(\d+)",
    }
    try:
        source = Path(path).read_text(encoding="utf-8")
    except OSError:
        return defaults
    found = dict(defaults)
    for key, pattern in patterns.items():
        match = re.search(pattern, source)
        if match:
            found[key] = match.group(1)
    return found


def patch(title, body, color="", icon=""):
    icon_html = f'<span class="pw-icon">{icon}</span>' if icon else ""
    return f'<div class="pw-patch {color}">{icon_html}<h3>{title}</h3>{body}</div>'


def section(tag, title, sub, tag_color=""):
    return (
        f'<div class="pw-section"><span class="pw-tag {tag_color}">{tag}</span>'
        f"<h2>{title}</h2><p class='sub'>{sub}</p></div>"
    )


cfg = read_live_config(str(APP_PATH))


# ----------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------
patchwork.html(f"""
<div class="pw-patch denim pw-hero">
  <img src="{logo_data_uri(str(LOGO_PATH))}" alt="Aether logo">
  <div>
    <div class="pw-kicker">stitched together from many small specialists</div>
    <h1>AETHER</h1>
    <p class="lead">Your AI workplace. Ask questions about your own PDF, research the live web,
    and get one clean, well-structured answer, written by a small team of AI agents that
    plan, search, read and write for you.</p>
    <div class="pw-chips">
      <span class="pw-chip m">Multi-agent</span>
      <span class="pw-chip t">RAG over your PDF</span>
      <span class="pw-chip s">Live web research</span>
      <span class="pw-chip r">Grounded answers</span>
      <span class="pw-chip">Streamlit</span>
    </div>
  </div>
</div>
""")


# ----------------------------------------------------------------------
# WHAT IS AETHER
# ----------------------------------------------------------------------
patchwork.html(
    section(
        "The big picture",
        "So, what is Aether?",
        "A normal chatbot is one model answering everything from memory. Aether splits the job "
        "between specialists, the same way a small office would, so answers come from "
        "<b>your documents</b> and <b>fresh sources</b> instead of guesswork.",
    )
    + '<div class="pw-grid four">'
    + f"""
    <div class="pw-patch mustard pw-stat"><div class="num">4</div><div class="lbl">specialist agents</div>
      <p>Planner, Researcher, Document Analyst and Writer.</p></div>
    <div class="pw-patch sage pw-stat"><div class="num">2</div><div class="lbl">knowledge sources</div>
      <p>Your uploaded PDF and the live web.</p></div>
    <div class="pw-patch terra pw-stat"><div class="num">{escape(cfg['retrieval_k'])}</div><div class="lbl">passages per question</div>
      <p>The most relevant PDF chunks are retrieved for every question.</p></div>
    <div class="pw-patch plum pw-stat"><div class="num">1</div><div class="lbl">final answer</div>
      <p>Planned, researched and then written up in a clean format.</p></div>
    """
    + "</div>"
)


# ----------------------------------------------------------------------
# PART 1: USER VIEW
# ----------------------------------------------------------------------
patchwork.html(
    section(
        "Part 1",
        "Why you would use Aether",
        "The user's point of view: what it does for you, without any jargon.",
    )
    + '<div class="pw-grid">'
    + patch(
        "Talk to your PDF",
        "<p>Upload a PDF in the sidebar and ask anything about it. Aether answers only from your "
        "document and points to the <b>page numbers</b>, so you can check every claim yourself.</p>",
        "denim-l",
        "📄",
    )
    + patch(
        "Research the live web",
        "<p>Need something that is not in your file? Aether searches the web in real time, reads the "
        "top sources and summarises them with titles and links.</p>",
        "mustard-l",
        "🌐",
    )
    + patch(
        "Use both in one question",
        "<p>Ask something like <i>“compare what my report says about X with the latest news on X”</i>. "
        "The Planner decides to use the document <b>and</b> the web, then merges both.</p>",
        "sage-l",
        "🧵",
    )
    + patch(
        "Answers that look finished",
        "<p>A dedicated Writer agent turns raw findings into a tidy response: headings, bullet points "
        "and tables whenever they make things easier to read.</p>",
        "terra-l",
        "✨",
    )
    + patch(
        "Keeps your conversations",
        "<p>Every chat is saved in <b>Recent Chats</b> and titled from your first message, so you can "
        "jump back to an earlier thread or start a fresh one with <b>New Chat</b>.</p>",
        "plum-l",
        "🗂️",
    )
    + patch(
        "You see it working",
        "<p>While Aether thinks, a live status panel shows which agent is active "
        "(<i>Using Planner Agent… Using Writer Agent…</i>), so nothing feels like a black box.</p>",
        "rose",
        "👀",
    )
    + "</div>"
)

patchwork.html(
    '<div class="pw-stitch"></div>'
    + '<div class="pw-grid two">'
    + """
    <div class="pw-patch cream">
      <h3>Try it in 3 stitches</h3>
      <div class="pw-step" style="margin-top:12px"><div class="pw-num">1</div>
        <p><b>Upload (optional).</b> Drop a text-based PDF in the sidebar. Wait for <i>“PDF ready!”</i>.</p></div>
      <div class="pw-step" style="margin-top:12px"><div class="pw-num">2</div>
        <p><b>Ask.</b> Type a question in the bar at the bottom and press ➤.</p></div>
      <div class="pw-step" style="margin-top:12px"><div class="pw-num">3</div>
        <p><b>Read &amp; verify.</b> Check the page numbers or source links that come with the answer.</p></div>
    </div>
    <div class="pw-patch mustard-l">
      <h3>Prompts worth trying</h3>
      <ul>
        <li>“Summarise the uploaded PDF in 5 bullet points.”</li>
        <li>“What does the document say about <i>your topic</i>? Mention page numbers.”</li>
        <li>“What are the latest developments in <i>your topic</i>? Give me a short table.”</li>
        <li>“Compare what my PDF says about <i>X</i> with the latest news on <i>X</i>.”</li>
      </ul>
    </div>
    """
    + "</div>"
    + '<div class="pw-grid two" style="margin-top:6px">'
    + """
    <div class="pw-patch sage-l">
      <h3>Who is it for?</h3>
      <ul>
        <li><b>Students</b> studying from notes, papers and textbooks.</li>
        <li><b>Professionals</b> digging through long reports, policies or contracts.</li>
        <li><b>Researchers</b> who want a document-grounded answer and a web check side by side.</li>
      </ul>
    </div>
    <div class="pw-patch rose">
      <h3>Good to know (honest limits)</h3>
      <ul>
        <li>Only <b>text-based PDFs</b> work. Scanned images need OCR first.</li>
        <li>One PDF at a time. Chats live in your browser session, so a refresh starts clean.</li>
        <li>The uploader lives on the chat page, so opening this About page clears the loaded PDF. Re-upload it when you go back.</li>
        <li>The PDF is processed in memory, but the passages used to answer, and your web queries, are sent to the
            Groq and Tavily APIs. Avoid highly confidential files.</li>
      </ul>
    </div>
    """
    + "</div>"
)


# ----------------------------------------------------------------------
# PART 2: TECHNICAL VIEW
# ----------------------------------------------------------------------
patchwork.html(
    section(
        "Part 2",
        "Under the hood",
        "The technical point of view: how the agents, the RAG pipeline and the interface fit together.",
        "denim",
    )
)

tab_arch, tab_rag, tab_agents, tab_state, tab_stack = st.tabs(
    ["🧭 Architecture", "📚 RAG pipeline", "🤖 Agents & tools", "🧠 State & UI", "🧰 Stack & config"]
)

with tab_arch:
    patchwork.html(f"""
    <div class="pw-flow">
      <div class="pw-patch cream"><div class="t">👤 User prompt</div>
        <div class="d">Typed in the chat bar (Streamlit form)</div></div>
      <div class="pw-arrow"></div>
      <div class="pw-patch denim"><div class="t">🧭 Planner Agent</div>
        <div class="d">LangChain <code>create_agent</code> · decides which tools to call · keeps page numbers &amp; sources</div></div>
      <div class="pw-split"><div class="pw-arrow"></div><div class="pw-arrow"></div></div>
      <div class="row">
        <div class="pw-patch sage"><div class="t">📄 document_analyst_tool</div>
          <div class="d">RAG: FAISS top-{escape(cfg['retrieval_k'])} chunks → grounded prompt → LLM<br>(only offered when a PDF is loaded)</div></div>
        <div class="pw-patch mustard"><div class="t">🌐 researcher_agent</div>
          <div class="d">Tavily advanced web search → {escape(cfg['max_results'])} sources → titles, URLs, summaries</div></div>
      </div>
      <div class="pw-split"><div class="pw-arrow"></div><div class="pw-arrow"></div></div>
      <div class="pw-patch denim-l"><div class="t">🗒️ Planner output</div>
        <div class="d">Collected facts, tool results, page numbers, links</div></div>
      <div class="pw-arrow"></div>
      <div class="pw-patch terra"><div class="t">✍️ Writer Agent</div>
        <div class="d"><code>ChatPromptTemplate | llm</code> · structures the final answer, adds nothing new</div></div>
      <div class="pw-arrow"></div>
      <div class="pw-patch cream"><div class="t">💬 Answer in the chat</div>
        <div class="d">Rendered as Markdown and stored in the chat history</div></div>
    </div>
    """)
    patchwork.html(
        '<div class="pw-grid two">'
        + patch(
            "Why two stages (Planner, then Writer)?",
            "<p><b>Separation of concerns.</b> The Planner only cares about <i>what information is needed</i> "
            "and which tool provides it. The Writer only cares about <i>how to present it</i>. "
            "Each prompt stays short, focused and easy to debug.</p>",
            "denim-l",
        )
        + patch(
            "Why tools instead of one big prompt?",
            "<p>Tools let the model <b>fetch facts on demand</b> rather than guess. The Planner is rebuilt for every "
            "request, and the PDF tool is only attached if a document is actually loaded, so the model can never "
            "call a tool that has nothing to read.</p>",
            "sage-l",
        )
        + "</div>"
    )

with tab_rag:
    steps = [
        ("Extract", "<code>pypdf.PdfReader</code> reads each page. Pages with no text are skipped; if nothing is extractable "
                    "the user is told the PDF may be scanned."),
        ("Wrap", "Each page becomes a LangChain <code>Document</code> with metadata <code>page</code> and <code>source</code>, "
                 "which is what makes page-numbered answers possible."),
        ("Chunk", f"<code>RecursiveCharacterTextSplitter</code> with <b>chunk_size={escape(cfg['chunk_size'])}</b> and "
                  f"<b>chunk_overlap={escape(cfg['chunk_overlap'])}</b> keeps ideas together and avoids cutting sentences "
                  "at chunk borders."),
        ("Embed", f"<code>{escape(cfg['embedding'])}</code> via <code>HuggingFaceEmbeddings</code> turns every chunk into a "
                  "384-dimension vector. The model is loaded once with <code>st.cache_resource</code>."),
        ("Index", "<code>FAISS.from_documents</code> stores the vectors in memory inside <code>st.session_state</code>. "
                  "Nothing is written to disk, and removing the PDF clears it."),
        ("Retrieve", f"<code>similarity_search(question, k={escape(cfg['retrieval_k'])})</code> fetches the closest chunks. "
                     "They are placed into a strict prompt: <i>answer only from the context, say so if it is missing, "
                     "cite page numbers.</i>"),
    ]
    cards = "".join(
        f'<div class="pw-patch {c}"><div class="pw-step" style="align-items:center;margin-bottom:10px">'
        f'<div class="pw-num">{i}</div><h4 style="margin:0">{name}</h4></div><p>{text}</p></div>'
        for i, (name, text, c) in enumerate(
            [(n, t, c) for (n, t), c in zip(steps, ["denim-l", "mustard-l", "sage-l", "terra-l", "plum-l", "rose"])],
            start=1,
        )
    )
    patchwork.html(f'<div class="pw-grid">{cards}</div>')
    patchwork.html(
        '<div class="pw-grid two" style="margin-top:4px">'
        + patch(
            "How hallucinations are kept in check",
            "<ul><li>The Document Analyst prompt forbids outside knowledge.</li>"
            "<li>If the context lacks the answer, it must say it could not find it.</li>"
            "<li>The Planner keeps page numbers, and the Writer is told not to add facts.</li>"
            f"<li>Low temperature (<b>{escape(cfg['temperature'])}</b>) keeps wording stable.</li></ul>",
            "sage",
        )
        + patch(
            "Re-indexing logic",
            "<p>A signature made of <code>file name + size</code> is compared with the last one. "
            "The PDF is only re-processed when that signature changes, so ordinary Streamlit reruns "
            "stay fast.</p>",
            "mustard",
        )
        + "</div>"
    )

with tab_agents:
    patchwork.html(
        '<div class="pw-grid">'
        + patch(
            "🧭 Planner Agent",
            "<ul><li>Built with <code>create_agent</code>, rebuilt on every request.</li>"
            "<li>Tools list is dynamic: <code>document_analyst_tool</code> only if a PDF is loaded.</li>"
            "<li>Rules in its system prompt: do not call unnecessary tools, use both when needed, preserve sources.</li></ul>",
            "denim",
        )
        + patch(
            "🌐 Researcher",
            "<ul><li><code>@tool researcher_agent(topic)</code> wraps <code>TavilyClient.search</code>.</li>"
            f"<li><code>search_depth=\"advanced\"</code>, <code>max_results={escape(cfg['max_results'])}</code>.</li>"
            "<li>Returns title, URL and a trimmed summary (500 characters) per result.</li></ul>",
            "mustard",
        )
        + patch(
            "📄 Document Analyst",
            "<ul><li><code>@tool document_analyst_tool(question)</code> reads the FAISS index from session state.</li>"
            "<li>Runs <code>doc_prompt | llm</code> on the retrieved context.</li>"
            "<li>Returns a friendly message if no PDF has been uploaded.</li></ul>",
            "sage",
        )
        + patch(
            "✍️ Writer",
            "<ul><li>No tools, just <code>writer_prompt | llm</code>.</li>"
            "<li>Receives the original question plus the Planner output.</li>"
            "<li>Adds headings, bullets and tables, but is forbidden to invent information.</li></ul>",
            "terra",
        )
        + patch(
            "🛡️ Error middleware",
            "<ul><li><code>@wrap_tool_call</code> catches any tool exception.</li>"
            "<li>Returns it as a <code>ToolMessage</code> so the agent can recover instead of crashing.</li>"
            "<li>Top-level <code>try/except</code> still shows a friendly error in the chat.</li></ul>",
            "plum",
        )
        + patch(
            "🧩 Shared LLM",
            f"<ul><li><code>ChatGroq</code> with <code>{escape(cfg['model'])}</code>.</li>"
            f"<li>Temperature <b>{escape(cfg['temperature'])}</b> for consistent, factual output.</li>"
            "<li>One client instance shared by the Planner, Document Analyst and Writer.</li></ul>",
            "rose",
        )
        + "</div>"
    )

with tab_state:
    patchwork.html(
        '<div class="pw-grid two">'
        + patch(
            "Session state (the app's memory)",
            "<ul><li><code>chats</code>: dictionary of conversations, keyed by a <code>uuid4</code> id.</li>"
            "<li><code>current_chat_id</code> and <code>active_page</code>: which chat and which view (chat / history) is open.</li>"
            "<li><code>vector_db</code>, <code>pdf_name</code>, <code>pdf_pages</code>, <code>pdf_chunks</code>, "
            "<code>pdf_signature</code>: everything about the loaded PDF.</li></ul>",
            "denim-l",
        )
        + patch(
            "Interface behaviour",
            "<ul><li>Sidebar: New Chat, Recent Chats, PDF uploader with processing spinner.</li>"
            "<li>Document expander shows pages, chunks and stored vectors.</li>"
            "<li><code>st.status</code> streams agent progress, then collapses on completion.</li>"
            "<li>A fixed, custom chat bar (CSS on <code>.st-key-chat_bar</code>) keeps the input always reachable.</li></ul>",
            "mustard-l",
        )
        + "</div>"
    )

with tab_stack:
    rows = [
        ("Interface", "Streamlit", "Multi-page app, session state, chat UI, status widgets"),
        ("Orchestration", "LangChain 1.x", "<code>create_agent</code>, tools, middleware, prompt templates"),
        ("LLM", f"Groq · {escape(cfg['model'])}", f"Fast hosted inference, temperature {escape(cfg['temperature'])}"),
        ("Web research", "Tavily", "Search API built for LLM agents"),
        ("Embeddings", escape(cfg["embedding"]), "Local sentence-transformer, 384 dimensions"),
        ("Vector store", "FAISS (in memory)", "Similarity search over PDF chunks"),
        ("PDF parsing", "pypdf", "Page-by-page text extraction"),
        ("Config", "python-dotenv", "API keys loaded from <code>.env</code>"),
    ]
    body = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    patchwork.html(f'<table class="pw-table"><tr><th>Layer</th><th>Technology</th><th>Role in Aether</th></tr>{body}</table>')

    groq_ok = bool(os.getenv("GROQ_API_KEY"))
    tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
    mark = lambda ok: '<span class="pw-ok">✔ configured</span>' if ok else '<span class="pw-bad">✘ missing</span>'
    patchwork.html(
        '<div class="pw-grid two" style="margin-top:22px">'
        + patch(
            "Live settings",
            "<p>Read directly from <code>app.py</code>, so this list always matches the running code.</p>"
            f"<ul><li>Chunk size / overlap: <b>{escape(cfg['chunk_size'])} / {escape(cfg['chunk_overlap'])}</b></li>"
            f"<li>Retrieved chunks (k): <b>{escape(cfg['retrieval_k'])}</b></li>"
            f"<li>Web results: <b>{escape(cfg['max_results'])}</b></li>"
            f"<li>Temperature: <b>{escape(cfg['temperature'])}</b></li></ul>",
            "sage-l",
        )
        + patch(
            "Environment check",
            "<p>Keys are never shown, only whether they were found.</p>"
            f"<ul><li><code>GROQ_API_KEY</code>: {mark(groq_ok)}</li>"
            f"<li><code>TAVILY_API_KEY</code>: {mark(tavily_ok)}</li></ul>",
            "mustard-l",
        )
        + "</div>"
    )


# ----------------------------------------------------------------------
# ROADMAP + FOOTER
# ----------------------------------------------------------------------
patchwork.html(
    section(
        "What's next",
        "Loose threads for the next patch",
        "Ideas that would make Aether even stronger.",
        "sage",
    )
    + '<div class="pw-grid four">'
    + patch("🧐 Critic agent", "<p>A reviewer that fact-checks the Writer's draft against the sources before it is shown.</p>", "plum-l")
    + patch("💾 Saved chats", "<p>Persist conversations (SQLite) so history survives a refresh.</p>", "denim-l")
    + patch("⚡ Streaming", "<p>Show the answer token by token for a snappier feel.</p>", "mustard-l")
    + patch("📚 Multi-PDF", "<p>Index several documents and filter retrieval by source.</p>", "sage-l")
    + "</div>"
    + '<div class="pw-foot"><div class="pw-stitch"></div>'
    '<span class="pw-note">Aether · Generative AI Capstone · stitched with care</span></div>'
)
