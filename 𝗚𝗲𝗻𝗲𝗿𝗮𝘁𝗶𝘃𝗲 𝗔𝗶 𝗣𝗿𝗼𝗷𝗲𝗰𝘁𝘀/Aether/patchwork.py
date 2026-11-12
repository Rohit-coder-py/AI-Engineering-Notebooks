"""
Patchwork Stitched design system for Aether.

Everything here is additive: it styles Streamlit through CSS only.
 - pages/1_About.py calls apply() and uses the .pw-* components below.
 - app.py is NOT modified. If you ever want the stitched borders on the
   chat + history pages too, add these two lines right after
   st.set_page_config(...) in app.py:

       import patchwork
       patchwork.apply()
"""

import streamlit as st


PALETTE = {
    "linen": "#F6EBD6",
    "cream": "#FFF6E3",
    "ink": "#3A2A22",
    "denim": "#34527A",
    "mustard": "#E8B03A",
    "terra": "#B94E32",
    "sage": "#6F8F68",
    "rose": "#D98C97",
    "plum": "#6B4A6E",
}


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&display=swap');

:root {
  --linen:#F6EBD6; --cream:#FFF6E3; --ink:#3A2A22; --thread:#B8946A;
  --denim:#34527A; --denim-l:#DCE6F2;
  --mustard:#E8B03A; --mustard-l:#FBEBC2;
  --terra:#B94E32; --terra-l:#F6D9CD;
  --sage:#6F8F68; --sage-l:#DCE8D5;
  --rose:#D98C97; --rose-l:#F8DDE0;
  --plum:#6B4A6E; --plum-l:#E8DCEB;
}

/* ---------- fabric background ---------- */
.stApp {
  background-color: var(--linen);
  background-image:
    repeating-linear-gradient(0deg, rgba(120,84,50,.05) 0 1px, transparent 1px 4px),
    repeating-linear-gradient(90deg, rgba(120,84,50,.05) 0 1px, transparent 1px 4px);
}
[data-testid="stHeader"] { background: transparent; }

/* ---------- sidebar: quilted strip ---------- */
[data-testid="stSidebar"] {
  background-color: #EAD3A6;
  background-image:
    repeating-linear-gradient(45deg, rgba(255,255,255,.14) 0 2px, transparent 2px 7px),
    repeating-linear-gradient(-45deg, rgba(120,84,50,.06) 0 2px, transparent 2px 7px);
  border-right: 3px dashed var(--thread);
}

/* ---------- headings ---------- */
h1, h2, h3 { color: var(--ink); letter-spacing: -.01em; }
.stApp h1 { border-bottom: 3px dashed rgba(58,42,34,.28); padding-bottom: .35rem; }

/* ---------- sewn buttons ---------- */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
  position: relative;
  background: var(--cream);
  color: var(--ink);
  font-weight: 700;
  border: 2px solid var(--terra);
  border-radius: 12px;
  outline: 2px dashed rgba(185,78,50,.7);
  outline-offset: -6px;
  box-shadow: 0 3px 0 rgba(58,42,34,.2);
  transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
}
.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
  background: var(--mustard-l);
  color: var(--ink);
  border-color: var(--terra);
  transform: translateY(-2px) rotate(-.6deg);
  box-shadow: 0 5px 0 rgba(58,42,34,.22);
}
.stButton > button:active,
[data-testid="stFormSubmitButton"] > button:active { transform: translateY(1px); box-shadow: 0 1px 0 rgba(58,42,34,.2); }

/* ---------- chat messages as fabric patches ---------- */
[data-testid="stChatMessage"] {
  position: relative;
  border-radius: 12px 18px 12px 16px;
  padding: 1rem 1.1rem;
  margin-bottom: .8rem;
  background-color: #FFF3D6;
  border: 2px solid rgba(184,148,106,.55);
  box-shadow: 0 3px 0 rgba(58,42,34,.14);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) { background-color: var(--denim-l); }
[data-testid="stChatMessage"]::after {
  content: ""; position: absolute; inset: 5px; pointer-events: none;
  border: 2px dashed rgba(58,42,34,.28); border-radius: inherit;
}

/* ---------- chat bar (the fixed one defined in app.py) ---------- */
.st-key-chat_bar {
  background: var(--cream) !important;
  border: 2px solid var(--terra) !important;
  border-radius: 16px !important;
  box-shadow: 0 6px 0 rgba(58,42,34,.2), 0 14px 24px -10px rgba(58,42,34,.35) !important;
  outline: 2px dashed rgba(185,78,50,.55);
  outline-offset: -7px;
}
.st-key-chat_bar [data-testid="stForm"] { border: none; padding: 0; }

/* ---------- forms, uploader, expanders, metrics, alerts ---------- */
[data-testid="stForm"] { border: 2px dashed var(--thread); border-radius: 14px; }
[data-testid="stFileUploaderDropzone"] {
  background: var(--cream);
  border: 2px dashed var(--terra);
  border-radius: 14px;
}
[data-testid="stExpander"] details {
  background: #FFF8E7;
  border: 2px dashed var(--sage);
  border-radius: 14px;
}
[data-testid="stMetric"] {
  background: var(--mustard-l);
  border: 2px dashed rgba(58,42,34,.35);
  border-radius: 12px 16px 12px 14px;
  padding: .7rem .9rem;
}
[data-testid="stAlert"] { border: 2px dashed rgba(58,42,34,.35); border-radius: 12px; }
[data-testid="stStatusWidget"], [data-testid="stStatus"] { border: 2px dashed var(--thread); border-radius: 14px; background: #FFF8E7; }
[data-testid="stVerticalBlock"]:has(> [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] [data-testid="stBaseButton-secondary"]) {
  border: 2px dashed var(--thread);
  border-radius: 14px;
  background: #FFF8E7;
}
hr { border: 0 !important; border-top: 3px dashed rgba(58,42,34,.3) !important; background: none !important; height: 0; }

/* ---------- tabs as sewn labels (new + older Streamlit markup) ---------- */
[role="tablist"], [data-baseweb="tab-list"] { gap: 10px; border-bottom: 3px dashed rgba(58,42,34,.28) !important; padding-bottom: 10px; flex-wrap: wrap; }
[role="tab"] {
  background: var(--cream);
  border: 2px dashed var(--thread) !important;
  border-radius: 10px;
  padding: 6px 16px;
  height: auto;
  font-weight: 700;
}
[role="tab"][aria-selected="true"] { background: var(--terra); border-color: var(--cream) !important; outline: 2px dashed var(--terra); outline-offset: 1px; }
[role="tab"][aria-selected="true"] p { color: var(--cream) !important; }
[role="tab"] p { font-weight: 700; }
.react-aria-SelectionIndicator, [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none !important; }

/* =====================================================================
   Reusable patchwork components (.pw-*)
   ===================================================================== */
.pw-wrap { font-family: inherit; color: var(--ink); }

.pw-patch {
  --bg: var(--cream); --fg: var(--ink); --stitch: rgba(58,42,34,.42);
  position: relative;
  padding: 22px 24px;
  color: var(--fg);
  background-color: var(--bg);
  background-image:
    repeating-linear-gradient(45deg, rgba(255,255,255,.16) 0 2px, transparent 2px 6px),
    repeating-linear-gradient(-45deg, rgba(0,0,0,.035) 0 2px, transparent 2px 6px);
  border-radius: 10px 18px 12px 16px;
  box-shadow: 0 3px 0 rgba(58,42,34,.2), 0 14px 22px -12px rgba(58,42,34,.45);
  transition: transform .2s ease;
}
.pw-patch::after {
  content: ""; position: absolute; inset: 7px; pointer-events: none;
  border: 2px dashed var(--stitch); border-radius: inherit;
}
.pw-patch h3, .pw-patch h4 { margin: 0 0 .45rem; color: var(--fg); font-family: inherit; }
.pw-patch p { margin: 0 0 .5rem; line-height: 1.55; color: var(--fg); }
.pw-patch p:last-child { margin-bottom: 0; }
.pw-patch ul { margin: .3rem 0 0; padding-left: 1.15rem; }
.pw-patch li { margin: .25rem 0; line-height: 1.5; color: var(--fg); }
.pw-patch .pw-icon { font-size: 1.9rem; line-height: 1; display: block; margin-bottom: .4rem; }
.pw-patch.denim   { --bg: var(--denim);   --fg: var(--cream); --stitch: rgba(255,246,227,.75); }
.pw-patch.mustard { --bg: var(--mustard); --stitch: rgba(58,42,34,.5); }
.pw-patch.terra   { --bg: var(--terra);   --fg: var(--cream); --stitch: rgba(255,246,227,.75); }
.pw-patch.sage    { --bg: var(--sage);    --fg: #FFFDF5;      --stitch: rgba(255,246,227,.75); }
.pw-patch.rose    { --bg: var(--rose-l);  --stitch: rgba(107,74,110,.5); }
.pw-patch.plum    { --bg: var(--plum);    --fg: var(--cream); --stitch: rgba(255,246,227,.75); }
.pw-patch.denim-l { --bg: var(--denim-l); --stitch: rgba(52,82,122,.55); }
.pw-patch.mustard-l { --bg: var(--mustard-l); --stitch: rgba(184,118,20,.55); }
.pw-patch.sage-l  { --bg: var(--sage-l);  --stitch: rgba(111,143,104,.7); }
.pw-patch.terra-l { --bg: var(--terra-l); --stitch: rgba(185,78,50,.55); }
.pw-patch.plum-l  { --bg: var(--plum-l);  --stitch: rgba(107,74,110,.55); }

.pw-grid { display: grid; gap: 22px; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); margin: 18px 0 8px; }
.pw-grid.two { grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); }
.pw-grid.four { grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); }
.pw-grid > .pw-patch:nth-child(4n+1) { transform: rotate(-.55deg); }
.pw-grid > .pw-patch:nth-child(4n+2) { transform: rotate(.45deg); }
.pw-grid > .pw-patch:nth-child(4n+3) { transform: rotate(-.3deg); }
.pw-grid > .pw-patch:nth-child(4n+4) { transform: rotate(.6deg); }
.pw-grid > .pw-patch:hover { transform: rotate(0) translateY(-3px); }

/* hero */
.pw-hero { display: grid; grid-template-columns: minmax(150px, 230px) 1fr; gap: 28px; align-items: center; padding: 34px 36px; }
.pw-hero img { width: 100%; max-width: 230px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.95) 0 60%, rgba(255,255,255,.0) 72%); }
.pw-hero .pw-kicker { font-family: 'Caveat', cursive; font-size: 1.6rem; color: var(--mustard); line-height: 1; }
.pw-hero h1 { font-size: clamp(2.6rem, 6vw, 4.2rem); line-height: 1; margin: .15rem 0 .6rem !important; color: var(--cream); border: 0 !important; padding: 0 !important; letter-spacing: .04em; }
.pw-hero p.lead { font-size: 1.12rem; max-width: 46rem; }
@media (max-width: 720px) { .pw-hero { grid-template-columns: 1fr; text-align: center; } .pw-hero img { margin: 0 auto; max-width: 160px; } }

/* chips */
.pw-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.pw-chip {
  display: inline-block; padding: 4px 12px; border-radius: 999px; font-weight: 700; font-size: .82rem;
  background: var(--cream); color: var(--ink); border: 2px dashed rgba(58,42,34,.5);
}
.pw-chip.m { background: var(--mustard); } .pw-chip.t { background: var(--terra-l); }
.pw-chip.s { background: var(--sage-l); }   .pw-chip.r { background: var(--rose-l); }

/* section header: arrow tag + title */
.pw-section { margin: 54px 0 6px; }
.pw-tag {
  display: inline-block; padding: 5px 30px 5px 14px; font-family: 'Caveat', cursive; font-size: 1.35rem; font-weight: 700;
  color: var(--cream); background: var(--terra);
  clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 50%, calc(100% - 16px) 100%, 0 100%);
}
.pw-tag.denim { background: var(--denim); } .pw-tag.sage { background: var(--sage); } .pw-tag.plum { background: var(--plum); }
.pw-section h2 { font-size: clamp(1.8rem, 4vw, 2.5rem); margin: .35rem 0 .2rem; color: var(--ink); line-height: 1.1; border: 0 !important; }
.pw-section p.sub { font-size: 1.05rem; max-width: 52rem; margin: 0; color: rgba(58,42,34,.85); }

/* running-stitch divider */
.pw-stitch { height: 0; border-top: 3px dashed rgba(58,42,34,.32); margin: 44px 0 8px; }

/* big number patches */
.pw-stat .num { font-family: 'Fraunces', serif; font-weight: 800; font-size: 2.6rem; line-height: 1; }
.pw-stat .lbl { font-weight: 700; margin-top: .3rem; }
.pw-stat p { font-size: .92rem; }

/* sewn button number */
.pw-num {
  width: 44px; height: 44px; border-radius: 50%; flex: none;
  display: grid; place-items: center; font-weight: 800; font-size: 1.1rem; color: var(--ink);
  background: var(--mustard); border: 3px solid rgba(58,42,34,.6);
  box-shadow: inset 0 0 0 4px rgba(255,255,255,.4), 0 2px 0 rgba(58,42,34,.3);
}
.pw-step { display: flex; gap: 14px; align-items: flex-start; }

/* flow diagram */
.pw-flow { display: flex; flex-direction: column; align-items: center; margin: 22px 0 6px; }
.pw-flow .pw-patch { width: min(560px, 100%); text-align: center; padding: 16px 20px; }
.pw-flow .row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; width: min(900px, 100%); }
.pw-flow .row .pw-patch { width: auto; }
.pw-flow .pw-patch .t { font-weight: 800; font-size: 1.05rem; }
.pw-flow .pw-patch .d { font-size: .88rem; opacity: .95; }
.pw-arrow { height: 34px; width: 0; margin: 8px auto 10px; border-left: 3px dashed var(--ink); position: relative; }
.pw-arrow::after { content: ""; position: absolute; bottom: -8px; left: -9.5px; border: 8px solid transparent; border-top: 10px solid var(--ink); border-bottom: 0; }
.pw-split { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; width: min(900px, 100%); }
.pw-split .pw-arrow { margin: 8px auto 10px; }
@media (max-width: 720px) { .pw-flow .row { grid-template-columns: 1fr; } .pw-split { gap: 20px; } }

/* code + tables */
.pw-wrap code {
  font-family: 'JetBrains Mono', monospace; font-size: .85em; padding: 1px 7px; border-radius: 6px;
  background: rgba(58,42,34,.1); border: 1px dashed rgba(58,42,34,.4); color: inherit; overflow-wrap: anywhere;
}
.pw-patch.denim code, .pw-patch.terra code, .pw-patch.sage code, .pw-patch.plum code { background: rgba(255,255,255,.16); border-color: rgba(255,246,227,.6); }
.pw-table { width: 100%; border-collapse: separate; border-spacing: 0; background: var(--cream); border: 2px dashed var(--thread); border-radius: 14px; overflow: hidden; }
.pw-table th { background: var(--mustard); text-align: left; padding: 10px 14px; font-weight: 800; color: var(--ink); }
.pw-table td { padding: 9px 14px; border-top: 2px dashed rgba(184,148,106,.55); vertical-align: top; color: var(--ink); }
.pw-table tr:nth-child(even) td { background: #FBF0D8; }

.pw-ok { color: #2F6B2F; font-weight: 800; } .pw-bad { color: #A12A1A; font-weight: 800; }
.pw-note { font-family: 'Caveat', cursive; font-size: 1.35rem; color: var(--terra); }
.pw-foot { text-align: center; margin: 56px 0 10px; }
"""


def collapse(markup: str) -> str:
    """Put an HTML block on one line so Markdown never turns it into a code block."""
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


def apply():
    """Inject the Patchwork Stitched stylesheet into the current page."""
    st.markdown("<style>" + collapse(CSS) + "</style>", unsafe_allow_html=True)


def html(markup: str):
    """Render a block of Patchwork HTML (.pw-* components)."""
    st.markdown('<div class="pw-wrap">' + collapse(markup) + "</div>", unsafe_allow_html=True)
