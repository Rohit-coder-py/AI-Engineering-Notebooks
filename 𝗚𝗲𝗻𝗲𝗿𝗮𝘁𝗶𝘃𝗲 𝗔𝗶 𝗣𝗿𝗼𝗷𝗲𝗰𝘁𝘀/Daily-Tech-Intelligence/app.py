"""
Daily Technology Intelligence — Streamlit front-end.

Run with:
    streamlit run app.py

Built by Rohit Jha as a capstone project.
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------
# Page setup (must run before anything renders)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Daily Technology Intelligence — Rohit Jha",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.config import (  # noqa: E402
    APP_NAME,
    APP_OWNER,
    APP_TAGLINE,
    NEWS_WINDOW_DAYS,
    SECTIONS,
    VERSION,
)
from src.graph import run_briefing  # noqa: E402
from src.tools import extract_links  # noqa: E402

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
CSS = """
<style>
:root {
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --accent: #0f62fe;
    --accent-soft: #eef4ff;
}
.block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1080px; }

.hero {
    background: linear-gradient(135deg, #0b1220 0%, #16233d 55%, #1d3a6e 100%);
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    color: #f8fafc;
    margin-bottom: 1.6rem;
    box-shadow: 0 18px 40px -22px rgba(15, 23, 42, .55);
}
.hero h1 { color: #ffffff; font-size: 2.05rem; margin: 0 0 .35rem 0; letter-spacing: -.02em; }
.hero .owner { color: #93c5fd; font-weight: 600; font-size: .95rem; letter-spacing: .08em; text-transform: uppercase; }
.hero p { color: #cbd5e1; margin: .55rem 0 0 0; font-size: 1rem; max-width: 62ch; }
.hero .pills { margin-top: 1.1rem; display: flex; flex-wrap: wrap; gap: .5rem; }
.hero .pill {
    background: rgba(255,255,255,.09); border: 1px solid rgba(255,255,255,.16);
    color: #e2e8f0; padding: .28rem .7rem; border-radius: 999px; font-size: .78rem;
}

.card {
    border: 1px solid var(--line); border-radius: 14px; padding: 1.05rem 1.2rem;
    background: #ffffff; height: 100%;
}
.card h4 { margin: 0 0 .35rem 0; font-size: .98rem; color: var(--ink); }
.card p { margin: 0; color: var(--muted); font-size: .88rem; line-height: 1.5; }
.card-grid {
    display: grid; gap: .9rem; margin: .4rem 0 1.6rem 0;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
}

.meta-row { display: flex; gap: .6rem; flex-wrap: wrap; margin: .2rem 0 1.2rem 0; }
.meta-chip {
    border: 1px solid var(--line); background: #fff; border-radius: 999px;
    padding: .32rem .8rem; font-size: .8rem; color: var(--muted);
}
.meta-chip b { color: var(--ink); }

/* Report typography */
h1, h2, h3, h4 { color: var(--ink); letter-spacing: -.01em; }
h2 { border-bottom: 2px solid var(--accent-soft); padding-bottom: .35rem; margin-top: 2.2rem; }
h3 { margin-top: 1.7rem; }
blockquote {
    border-left: 3px solid var(--accent); background: var(--accent-soft);
    padding: .7rem 1rem; border-radius: 0 8px 8px 0; color: #334155;
}
table { font-size: .88rem; }
thead th { background: #f1f5f9 !important; }
code { font-size: .84rem; }
hr { margin: 2rem 0; border-color: var(--line); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
DEFAULTS = {
    "report": None,
    "state": None,
    "generated_at": None,
    "elapsed": None,
    "error": None,
}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
def key_status() -> tuple[bool, bool]:
    return (
        bool(os.getenv("GROQ_API_KEY", "").strip()),
        bool(os.getenv("TAVILY_API_KEY", "").strip()),
    )


with st.sidebar:
    st.markdown(f"### 🛰️ {APP_NAME}")
    st.caption(f"v{VERSION} · built by {APP_OWNER}")

    has_groq, has_tavily = key_status()
    if has_groq and has_tavily:
        st.success("API keys loaded", icon="✅")
    else:
        st.error("Missing API keys", icon="🔑")
        if not has_groq:
            st.caption("• `GROQ_API_KEY` not found")
        if not has_tavily:
            st.caption("• `TAVILY_API_KEY` not found")
        st.caption("Add them to `.env` in the project folder, then reload.")

    st.divider()

    st.markdown("**Briefing settings**")
    window = st.slider(
        "News window (days)",
        min_value=1,
        max_value=7,
        value=NEWS_WINDOW_DAYS,
        help="Only articles published within this window are considered.",
    )
    stories = st.slider(
        "Max stories per section",
        min_value=3,
        max_value=8,
        value=5,
        help="More stories means a longer report and more tokens.",
    )

    active = st.multiselect(
        "Sections to include",
        options=[s.title for s in SECTIONS],
        default=[s.title for s in SECTIONS],
        help="Deselecting sections saves time and tokens.",
    )
    if not active:
        st.warning("Select at least one section.")

    st.divider()
    generate = st.button(
        "⚡ Generate today's briefing",
        type="primary",
        use_container_width=True,
        disabled=not (has_groq and has_tavily) or not active,
    )
    if st.session_state.report:
        if st.button("🗑️ Clear report", use_container_width=True):
            for key, value in DEFAULTS.items():
                st.session_state[key] = value
            st.rerun()

    st.divider()
    st.caption(
        "Sources: Tavily news, arXiv, GitHub, Hacker News.  \n"
        "Every link is validated against the fetched pool before publication."
    )


# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------
st.markdown(
    f"""
<div class="hero">
  <div class="owner">Capstone · {APP_OWNER}</div>
  <h1>{APP_NAME}</h1>
  <p>{APP_TAGLINE} Generated on demand, verified before you read it, and written
  to teach you something every day.</p>
  <div class="pills">
    <span class="pill">7 sections</span>
    <span class="pill">Link verification</span>
    <span class="pill">Editor agent</span>
    <span class="pill">Learning corner</span>
    <span class="pill">Zero fabrication policy</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Generation
# --------------------------------------------------------------------------
def _progress_ui():
    status = st.status("Starting the pipeline…", expanded=True)
    bar = st.progress(0.0)
    text = st.empty()

    # The pipeline reports progress from worker threads. Streamlit only lets
    # threads touch the UI if they carry the script's run context, so capture
    # it here (main thread) and attach it to whichever thread calls update().
    try:
        from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
        ctx = get_script_run_ctx()
    except Exception:  # noqa: BLE001
        add_script_run_ctx, ctx = None, None

    def update(message: str, pct: float) -> None:
        if ctx is not None and add_script_run_ctx is not None:
            add_script_run_ctx(threading.current_thread(), ctx)
        try:
            bar.progress(min(max(pct, 0.0), 1.0))
            text.markdown(f"**{message}**")
        except Exception:  # noqa: BLE001
            # A progress-bar glitch must never kill the briefing.
            pass

    return status, update


if generate:
    started = time.time()
    status, progress = _progress_ui()
    try:
        state = run_briefing(progress=progress, days=window, max_stories=stories, sections=active)
        st.session_state.state = state
        st.session_state.report = state.get("report", "")
        st.session_state.generated_at = datetime.now()
        st.session_state.elapsed = round(time.time() - started, 1)
        st.session_state.error = None
        status.update(label="Briefing ready", state="complete", expanded=False)
    except Exception as exc:  # noqa: BLE001
        st.session_state.error = str(exc)
        status.update(label="Pipeline failed", state="error", expanded=True)
        st.exception(exc)

if st.session_state.error and not st.session_state.report:
    st.error(st.session_state.error)
    st.info(
        "Common causes: an invalid API key, a Groq rate limit, or no network access. "
        "Check the sidebar key status and try again."
    )


# --------------------------------------------------------------------------
# Landing content (no report yet)
# --------------------------------------------------------------------------
if not st.session_state.report:
    st.markdown(
        """
<div class="card-grid">
  <div class="card">
    <h4>🔍 Real sources only</h4>
    <p>Articles come from Tavily news, arXiv, GitHub and Hacker News,
    restricted to official company blogs and credible outlets.</p>
  </div>
  <div class="card">
    <h4>🛡️ Verified, not assumed</h4>
    <p>Every link must exist in the fetched pool, and every number must appear
    in the source. An editor agent then reviews the writing.</p>
  </div>
  <div class="card">
    <h4>🎓 Built to teach</h4>
    <p>Each briefing ends with a learning corner, a vocabulary table and a
    small experiment you can build the same day.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("### How it works")
    st.markdown("""
1. **Ingest** — a targeted news query per topic, plus arXiv, GitHub and Hacker News.
2. **Normalise** — duplicate and near-duplicate stories are clustered; the
   best-sourced version wins and multi-outlet coverage raises importance.
3. **Write** — seven section writers run in parallel, each restricted to its
   own slice of the source pool.
4. **Verify** — a deterministic checker rejects any link that was not actually
   fetched and any statistic that is not in the source, then spot-checks claims
   against the live page text.
5. **Edit** — an editor agent reviews accuracy, labelling and structure, and
   sends weak sections back for one rewrite.
6. **Assemble** — executive summary, learning corner, vocabulary and sources.
        """)
    st.info("Press **⚡ Generate today's briefing** in the sidebar to begin. First run takes about 1–3 minutes.")
    st.stop()


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
state = st.session_state.state or {}
report = st.session_state.report

elapsed = st.session_state.elapsed
stamp = st.session_state.generated_at.strftime("%d %b %Y, %H:%M") if st.session_state.generated_at else "—"
total_stories = sum(
    len(re.findall(r"^###\s+", body, flags=re.M))
    for body in state.get("sections", {}).values()
)
revised = sum(1 for v in state.get("reviews", {}).values() if v.get("verdict") == "revise")

st.markdown(
    f"""
<div class="meta-row">
  <span class="meta-chip">🕒 <b>{stamp}</b></span>
  <span class="meta-chip">📄 <b>{total_stories}</b> stories</span>
  <span class="meta-chip">🔗 <b>{len(extract_links(report))}</b> source links</span>
  <span class="meta-chip">✍️ <b>{revised}</b> section(s) revised by editor</span>
  <span class="meta-chip">⏱️ <b>{elapsed or '—'}s</b></span>
</div>
""",
    unsafe_allow_html=True,
)

tab_report, tab_sources, tab_verify, tab_raw = st.tabs(
    ["📰 Briefing", "🔗 Sources", "🛡️ Verification", "🧾 Raw & export"]
)

with tab_report:
    st.markdown(report, unsafe_allow_html=False)

with tab_sources:
    links = extract_links(report)
    if not links:
        st.info("No source links found in this report.")
    else:
        by_domain: dict[str, list[str]] = {}
        for url in links:
            host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
            by_domain.setdefault(host, []).append(url)
        st.markdown(f"**{len(links)} unique sources across {len(by_domain)} domains.**")
        for host in sorted(by_domain):
            with st.expander(f"{host}  ·  {len(by_domain[host])} link(s)"):
                for url in by_domain[host]:
                    st.markdown(f"- [{url}]({url})")

with tab_verify:
    audits = state.get("audits", {})
    reviews = state.get("reviews", {})
    rows = []
    for section in SECTIONS:
        audit = audits.get(section.id, {})
        review = reviews.get(section.id, {})
        body = state.get("sections", {}).get(section.id, "")
        rows.append(
            {
                "Section": section.title,
                "Stories": len(re.findall(r"^###\s+", body, flags=re.M)),
                "Links checked": audit.get("checked", 0),
                "Hard issues": len(audit.get("hard", [])),
                "Notes": len(audit.get("soft", [])),
                "Editor verdict": review.get("verdict", "—"),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.markdown("#### What was actually checked")
    st.markdown(
        """
- **Link integrity** — every URL must exist in the articles fetched for this run.
  Anything else is rejected and the section is rewritten.
- **Source presence** — each story must carry at least one `Sources` block.
- **Claim overlap** — the sentence making the claim is compared with the live
  text of the cited page. Weak overlap is flagged to the editor.
- **Editor review** — a separate model checks accuracy, rumour labelling and
  required structure, then requests a rewrite if needed.

**What this does not do:** it does not prove a company's claim is true. A vendor
saying "state of the art" is reported as a vendor claim, not as fact.
        """
    )

    issues = []
    for sid, audit in audits.items():
        for item in audit.get("hard", []):
            issues.append(("Hard", sid, item))
        for item in audit.get("soft", []):
            issues.append(("Note", sid, item))
    if issues:
        with st.expander(f"Audit log ({len(issues)} entries)"):
            for level, sid, item in issues:
                st.markdown(f"- **{level}** · `{sid}` · {item}")
    else:
        st.success("No audit issues recorded for this run.")

with tab_raw:
    st.markdown("#### Download")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "⬇️ Download Markdown",
            data=report,
            file_name=f"tech-briefing-{datetime.now():%Y-%m-%d}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with d2:
        payload = {
            "generated_at": stamp,
            "stories": total_stories,
            "candidates": len(state.get("candidates", [])),
            "sections": list(state.get("sections", {}).keys()),
            "audits": {
                k: {"hard": v.get("hard", []), "soft": v.get("soft", []), "checked": v.get("checked", 0)}
                for k, v in state.get("audits", {}).items()
            },
            "reviews": state.get("reviews", {}),
            "report_markdown": report,
        }
        st.download_button(
            "⬇️ Download JSON",
            data=json.dumps(payload, indent=2, default=str),
            file_name=f"tech-briefing-{datetime.now():%Y-%m-%d}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("#### Raw Markdown")
    st.code(report[:20000], language="markdown")

st.markdown("---")
st.caption(
    f"{APP_NAME} v{VERSION} · built by {APP_OWNER} · "
    "Tavily + arXiv + GitHub + Hacker News → LangGraph → deterministic audit → editor agent"
)