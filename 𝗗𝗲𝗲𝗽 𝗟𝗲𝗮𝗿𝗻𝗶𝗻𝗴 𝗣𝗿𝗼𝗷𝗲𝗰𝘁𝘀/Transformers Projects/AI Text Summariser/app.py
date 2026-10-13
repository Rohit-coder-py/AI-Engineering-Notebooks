"""
AI Text Summariser — Streamlit app
Model : sshleifer/distilbart-cnn-12-6 (Hugging Face Transformers + PyTorch)
Run   : streamlit run app.py

Built on top of ai_test_summerizer.ipynb (notebook is untouched).
The app re-uses the same model and the same "dynamic length" idea from the
notebook's final `summarize_text` function, and adds long-text chunking,
a token inspector and a model-info panel.
"""

import html
import re
import time
from datetime import datetime

import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
MODEL_INPUT_LIMIT = 1024  # BART positional-embedding limit (tokens)
CHUNK_TOKENS = 900  # safe chunk size for long documents

st.set_page_config(
    page_title="AI Text Summariser",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

SAMPLES = {
    "AI overview": (
        "Artificial Intelligence is transforming many industries, including healthcare, "
        "education, transportation, and finance. Machine learning enables computers to learn "
        "patterns from data, while deep learning uses neural networks to solve complex tasks.\n\n"
        "Transformer models have significantly improved natural language processing. They use "
        "attention mechanisms to understand relationships between tokens in a sequence. Models "
        "based on the Transformer architecture can summarize documents, translate languages, "
        "answer questions, and generate human-like text.\n\n"
        "Businesses increasingly use AI to automate repetitive tasks, analyze information, and "
        "improve decision-making. However, responsible AI development requires attention to "
        "privacy, fairness, transparency, and reliability."
    ),
    "Climate news": (
        "Global temperatures have continued to rise over the past decade, with scientists "
        "reporting that the last ten years were the warmest on record. Rising temperatures are "
        "melting glaciers and polar ice caps, which in turn is causing sea levels to rise and "
        "threatening coastal cities around the world. Extreme weather events such as heatwaves, "
        "floods, and wildfires have become more frequent and more severe.\n\n"
        "Governments and companies are responding by investing in renewable energy. Solar and "
        "wind power capacity has grown rapidly, and electric vehicles now make up a growing "
        "share of new car sales. Experts say that while progress is encouraging, emissions must "
        "fall much faster this decade if the world is to meet its climate targets.\n\n"
        "Cities are also adapting by building flood defences, planting trees to reduce urban "
        "heat, and redesigning transport systems to cut pollution. Researchers stress that "
        "adaptation and emission cuts must go hand in hand to protect vulnerable communities."
    ),
    "Space exploration": (
        "Space agencies and private companies are entering a new era of exploration. Reusable "
        "rockets have dramatically reduced the cost of reaching orbit, making it possible to "
        "launch satellites, cargo, and crews far more often than before. Plans are underway to "
        "return astronauts to the Moon and to build a long-term presence there as a stepping "
        "stone toward Mars.\n\n"
        "Robotic missions continue to reveal new details about the solar system. Rovers study "
        "the geology of Mars, probes visit asteroids to collect samples, and powerful space "
        "telescopes look back billions of years to observe the first galaxies. Scientists hope "
        "these missions will help answer whether life ever existed beyond Earth.\n\n"
        "The growth of the commercial space sector is also creating new industries, from "
        "satellite internet to space tourism, while raising questions about orbital debris and "
        "the need for international rules to keep space safe and sustainable."
    ),
}

LENGTH_PRESETS = {
    "Short": (40, 10),
    "Balanced": (60, 20),  # same values used in the notebook
    "Detailed": (130, 40),
    "Custom": None,
}

# ─────────────────────────────────────────────────────────────────────────────
# Styling
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root{
  --bg:#0a0c11; --panel:#12161e; --panel2:#171c26; --line:#262d3b;
  --text:#ece9e2; --muted:#9aa3b5;
  --gold:#d9a94a; --emerald:#2fd1a0; --sapphire:#5b94f5; --rose:#ee5f7a; --violet:#a98bfa;
}
html, body, [class*="css"], .stApp { font-family:'Inter',sans-serif; color:var(--text); }
.stApp { background:
   radial-gradient(1100px 500px at 8% -10%, rgba(217,169,74,.10), transparent 60%),
   radial-gradient(900px 500px at 100% 0%, rgba(91,148,245,.10), transparent 60%),
   var(--bg); }
header[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:2rem; max-width:1250px; }
section[data-testid="stSidebar"]{ background:#0d1017; border-right:1px solid var(--line); }
section[data-testid="stSidebar"] *{ color:var(--text); }
h1,h2,h3{ font-family:'Cormorant Garamond',serif !important; letter-spacing:.2px; color:var(--text) !important; }
label, .stMarkdown p, .stCaption, [data-testid="stWidgetLabel"] p{ color:var(--text) !important; }
small, .stCaption, [data-testid="stCaptionContainer"]{ color:var(--muted) !important; }

/* Hero */
.hero{ padding:1.6rem 1.8rem; border:1px solid var(--line); border-radius:18px;
  background:linear-gradient(135deg, rgba(217,169,74,.10), rgba(91,148,245,.07) 55%, rgba(47,209,160,.07));
  margin-bottom:1.2rem; }
.hero .eyebrow{ font-family:'JetBrains Mono',monospace; font-size:.74rem; letter-spacing:.22em;
  color:var(--gold); text-transform:uppercase; }
.hero h1{ font-size:3rem; line-height:1.05; margin:.3rem 0 .4rem 0; }
.hero h1 span{ background:linear-gradient(90deg,var(--gold),var(--rose)); -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; }
.hero p{ color:var(--muted); font-size:1.02rem; margin:0; max-width:760px; }
.pill{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.72rem; padding:.22rem .6rem;
  border-radius:999px; border:1px solid var(--line); margin:.7rem .4rem 0 0; color:var(--text); background:var(--panel); }
.pill.g{ border-color:rgba(217,169,74,.5); color:var(--gold);} .pill.e{ border-color:rgba(47,209,160,.5); color:var(--emerald);}
.pill.s{ border-color:rgba(91,148,245,.5); color:var(--sapphire);} .pill.r{ border-color:rgba(238,95,122,.5); color:var(--rose);}

/* Cards */
.card{ background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:1.2rem 1.4rem; }
.summary-card{ border-left:4px solid var(--gold); background:linear-gradient(180deg,var(--panel2),var(--panel)); }
.summary-card .label{ font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:.18em;
  color:var(--gold); text-transform:uppercase; margin-bottom:.5rem; }
.summary-card .body{ font-family:'Cormorant Garamond',serif; font-size:1.5rem; line-height:1.5; color:var(--text); }
.chunk{ font-size:.92rem; color:var(--text); border-left:3px solid var(--sapphire); padding:.4rem .9rem; margin:.5rem 0;
  background:var(--panel); border-radius:0 10px 10px 0; }

.metrics{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:.8rem; margin:1rem 0; }
.metric{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:.8rem 1rem; }
.metric .k{ font-family:'JetBrains Mono',monospace; font-size:.68rem; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
.metric .v{ font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:700; line-height:1.15; }
.metric.g .v{color:var(--gold);} .metric.e .v{color:var(--emerald);} .metric.s .v{color:var(--sapphire);}
.metric.r .v{color:var(--rose);} .metric.v2 .v{color:var(--violet);}

.tok{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.8rem; padding:.12rem .45rem;
  margin:.15rem .12rem; border-radius:6px; border:1px solid transparent; color:#0a0c11; font-weight:500; }
.t0{background:#d9a94a;} .t1{background:#2fd1a0;} .t2{background:#5b94f5;} .t3{background:#ee5f7a;} .t4{background:#a98bfa;}

/* Inputs */
.stTextArea textarea{ background:var(--panel) !important; color:var(--text) !important; border:1px solid var(--line) !important;
  border-radius:12px !important; font-size:.98rem; line-height:1.55; }
.stTextArea textarea:focus{ border-color:var(--gold) !important; box-shadow:0 0 0 1px var(--gold) !important; }
.stButton>button, .stDownloadButton>button{ border-radius:12px; border:1px solid var(--line); background:var(--panel2);
  color:var(--text); font-weight:500; transition:all .15s; }
.stButton>button:hover, .stDownloadButton>button:hover{ border-color:var(--gold); color:var(--gold); }
.stButton>button[kind="primary"]{ background:linear-gradient(90deg,var(--gold),#e8c070); color:#14110a; border:none; font-weight:600; }
.stButton>button[kind="primary"]:hover{ filter:brightness(1.08); color:#14110a; }
.stTabs [data-baseweb="tab-list"]{ gap:.3rem; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"]{ font-family:'JetBrains Mono',monospace; font-size:.82rem; color:var(--muted); padding:.6rem 1rem; }
.stTabs [aria-selected="true"]{ color:var(--gold) !important; }
.stTabs [data-baseweb="tab-highlight"]{ background:var(--gold) !important; }
div[data-testid="stExpander"]{ background:var(--panel); border:1px solid var(--line); border-radius:12px; }
hr{ border-color:var(--line); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Model loading (cached – loads only once per server process)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """Load tokenizer + seq2seq model (same checkpoint as the notebook)."""
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device).eval()
    return tokenizer, model, device


# ─────────────────────────────────────────────────────────────────────────────
# Summarisation logic
# ─────────────────────────────────────────────────────────────────────────────
def count_tokens(tokenizer, text: str) -> int:
    return len(tokenizer.encode(text, add_special_tokens=True))


def summarize_chunk(tokenizer, model, device, text, max_len, min_len, num_beams, no_repeat, rep_penalty):
    """Summarise one piece of text that fits inside the model window.

    Uses the notebook's dynamic-length rule so very short inputs don't crash or
    produce a summary longer than the input itself.
    """
    import torch

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=MODEL_INPUT_LIMIT)
    n_in = inputs["input_ids"].shape[1]

    max_len = min(max_len, max(8, n_in - 2))
    min_len = min(min_len, max(1, max_len // 3))

    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        ids = model.generate(
            **inputs,
            max_length=max_len,
            min_length=min_len,
            num_beams=num_beams,
            do_sample=False,
            no_repeat_ngram_size=no_repeat,
            repetition_penalty=rep_penalty,
            early_stopping=True,
        )
    return tokenizer.decode(ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True).strip()


def split_into_chunks(tokenizer, text, limit=CHUNK_TOKENS):
    """Greedy sentence packing so every chunk stays under `limit` tokens."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
    chunks, current, current_len = [], [], 0
    for sent in sentences:
        n = len(tokenizer.encode(sent, add_special_tokens=False))
        if n > limit:  # a single monster sentence – hard-cut it by tokens
            ids = tokenizer.encode(sent, add_special_tokens=False)
            for i in range(0, len(ids), limit):
                part = tokenizer.decode(ids[i : i + limit])
                if current:
                    chunks.append(" ".join(current))
                    current, current_len = [], 0
                chunks.append(part)
            continue
        if current_len + n > limit and current:
            chunks.append(" ".join(current))
            current, current_len = [], 0
        current.append(sent)
        current_len += n
    if current:
        chunks.append(" ".join(current))
    return chunks


def run_summary(tokenizer, model, device, text, max_len, min_len, num_beams, no_repeat, rep_penalty, merge_pass):
    start = time.perf_counter()
    total_tokens = count_tokens(tokenizer, text)
    chunk_summaries = []

    if total_tokens <= MODEL_INPUT_LIMIT - 24:
        final = summarize_chunk(tokenizer, model, device, text, max_len, min_len, num_beams, no_repeat, rep_penalty)
        n_chunks = 1
    else:
        chunks = split_into_chunks(tokenizer, text)
        n_chunks = len(chunks)
        bar = st.progress(0.0, text=f"Long text detected — summarising {n_chunks} chunks…")
        for i, ch in enumerate(chunks, 1):
            chunk_summaries.append(
                summarize_chunk(tokenizer, model, device, ch, max_len, min_len, num_beams, no_repeat, rep_penalty)
            )
            bar.progress(i / n_chunks, text=f"Summarised chunk {i}/{n_chunks}")
        bar.empty()
        final = " ".join(chunk_summaries)
        if merge_pass and count_tokens(tokenizer, final) > max_len:
            merged_in = final
            if count_tokens(tokenizer, merged_in) > MODEL_INPUT_LIMIT - 24:
                merged_in = tokenizer.decode(
                    tokenizer.encode(merged_in, add_special_tokens=False)[: MODEL_INPUT_LIMIT - 24]
                )
            final = summarize_chunk(tokenizer, model, device, merged_in, max_len, min_len, num_beams, no_repeat, rep_penalty)

    elapsed = time.perf_counter() - start
    return {
        "summary": final,
        "chunks": chunk_summaries,
        "n_chunks": n_chunks,
        "in_tokens": total_tokens,
        "out_tokens": count_tokens(tokenizer, final),
        "in_words": len(text.split()),
        "out_words": len(final.split()),
        "seconds": elapsed,
    }


# ─────────────────────────────────────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────────────────────────────────────
def metric(label, value, color):
    return f'<div class="metric {color}"><div class="k">{label}</div><div class="v">{value}</div></div>'


def set_sample(name):
    st.session_state["input_text"] = SAMPLES[name]


def clear_text():
    st.session_state["input_text"] = ""


if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "history" not in st.session_state:
    st.session_state["history"] = []
if "result" not in st.session_state:
    st.session_state["result"] = None

# ─────────────────────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="hero">
  <div class="eyebrow">Transformers · Abstractive summarisation</div>
  <h1>AI Text <span>Summariser</span></h1>
  <p>Paste an article, upload a text file, and get a concise abstractive summary generated by a
  distilled BART transformer — with a look inside the tokenizer and the model.</p>
  <span class="pill g">{MODEL_NAME}</span><span class="pill e">PyTorch</span>
  <span class="pill s">Hugging Face</span><span class="pill r">Encoder–Decoder</span>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar – generation settings
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    preset = st.radio("Summary length", list(LENGTH_PRESETS), index=1, horizontal=True)
    if LENGTH_PRESETS[preset] is None:
        max_len = st.slider("max_length (tokens)", 20, 300, 60, 5)
        min_len = st.slider("min_length (tokens)", 5, 150, 20, 5)
        if min_len >= max_len:
            st.warning("min_length should be smaller than max_length — adjusting automatically.")
            min_len = max(1, max_len - 5)
    else:
        max_len, min_len = LENGTH_PRESETS[preset]
        st.caption(f"max_length = **{max_len}**, min_length = **{min_len}** tokens")

    with st.expander("Advanced generation"):
        num_beams = st.slider("num_beams", 1, 8, 4, help="1 = greedy. More beams = better quality but slower.")
        no_repeat = st.slider("no_repeat_ngram_size", 0, 5, 3, help="Blocks repeated n-grams. 0 disables.")
        rep_penalty = st.slider("repetition_penalty", 1.0, 2.0, 1.0, 0.05)
        merge_pass = st.checkbox("Merge pass for long texts", value=True,
                                 help="For long inputs: summarise chunk summaries once more into a single summary.")
    st.caption("Decoding is deterministic (`do_sample=False`), same as in the notebook.")
    st.divider()
    st.markdown("### 📚 Try a sample")
    for name in SAMPLES:
        st.button(name, key=f"s_{name}", on_click=set_sample, args=(name,))
    st.divider()
    st.caption("First launch downloads the model (~1.2 GB) and may take a minute. After that it is cached.")

# ─────────────────────────────────────────────────────────────────────────────
# Load model
# ─────────────────────────────────────────────────────────────────────────────
try:
    with st.spinner("Loading transformer model… (first run downloads weights)"):
        tokenizer, model, device = load_model()
except Exception as exc:  # noqa: BLE001
    st.error(
        "Could not load the model. Check your internet connection and that "
        "`torch`, `transformers<5` and `sentencepiece` are installed "
        "(`pip install -r requirements.txt`)."
    )
    st.exception(exc)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────
tab_sum, tab_tok, tab_model, tab_hist, tab_about = st.tabs(
    ["✦ Summarise", "🔬 Token Inspector", "🧠 Model Lab", "🕘 History", "📖 How it works"]
)

# ── Tab 1: Summarise ─────────────────────────────────────────────────────────
with tab_sum:
    up = st.file_uploader("Upload a .txt or .md file (optional)", type=["txt", "md"])
    if up is not None:
        key = f"{up.name}-{up.size}"
        if st.session_state.get("_loaded_file") != key:
            st.session_state["input_text"] = up.getvalue().decode("utf-8", errors="ignore")
            st.session_state["_loaded_file"] = key

    text = st.text_area(
        "Article / text to summarise",
        key="input_text",
        height=280,
        placeholder="Paste your article here…  (or pick a sample from the sidebar)",
    )
    n_words = len(text.split())
    c1, c2, c3 = st.columns([1.3, 1, 3])
    run = c1.button("✦ Summarise", type="primary")
    c2.button("Clear", on_click=clear_text)
    c3.caption(f"{n_words:,} words · {len(text):,} characters")

    if run:
        if n_words < 5:
            st.warning("Please enter at least a few sentences to summarise.")
        else:
            with st.spinner("Generating summary…"):
                res = run_summary(tokenizer, model, device, text.strip(), max_len, min_len,
                                  num_beams, no_repeat or None, rep_penalty, merge_pass)
            res["time"] = datetime.now().strftime("%d %b %Y, %H:%M")
            res["original"] = text.strip()
            st.session_state["result"] = res
            st.session_state["history"].insert(0, res)

    res = st.session_state["result"]
    if res:
        st.markdown(
            f'<div class="card summary-card"><div class="label">Summary</div>'
            f'<div class="body">{html.escape(res["summary"])}</div></div>',
            unsafe_allow_html=True,
        )
        ratio = 100 * (1 - res["out_words"] / max(1, res["in_words"]))
        st.markdown(
            '<div class="metrics">'
            + metric("Original words", f'{res["in_words"]:,}', "s")
            + metric("Summary words", f'{res["out_words"]:,}', "g")
            + metric("Reduced by", f"{max(0, ratio):.0f}%", "e")
            + metric("Input tokens", f'{res["in_tokens"]:,}', "v2")
            + metric("Chunks", res["n_chunks"], "r")
            + metric("Time", f'{res["seconds"]:.1f}s', "s")
            + "</div>",
            unsafe_allow_html=True,
        )
        if res["chunks"]:
            with st.expander(f"Per-chunk summaries ({len(res['chunks'])})"):
                for i, cs in enumerate(res["chunks"], 1):
                    st.markdown(f'<div class="chunk"><b>Chunk {i}</b> — {html.escape(cs)}</div>',
                                unsafe_allow_html=True)
        st.download_button("⬇ Download summary (.txt)", res["summary"],
                           file_name="summary.txt", mime="text/plain")

# ── Tab 2: Token inspector (notebook: tokenizer inspection) ──────────────────
with tab_tok:
    st.markdown("### Token Inspector")
    st.caption("See how the BART tokenizer breaks text into sub-word tokens and IDs — "
               "the same inspection done in the notebook.")
    probe = st.session_state["input_text"].strip() or SAMPLES["AI overview"]
    if not st.session_state["input_text"].strip():
        st.info("Showing the sample text. Paste your own text in the Summarise tab to inspect it.")
    tokens = tokenizer.tokenize(probe)
    token_ids = tokenizer.encode(probe)
    used = len(token_ids)

    st.markdown(
        '<div class="metrics">'
        + metric("Total tokens", f"{used:,}", "g")
        + metric("Words", f"{len(probe.split()):,}", "s")
        + metric("Tokens / word", f"{used / max(1, len(probe.split())):.2f}", "e")
        + metric("Model window", f"{MODEL_INPUT_LIMIT:,}", "v2")
        + "</div>",
        unsafe_allow_html=True,
    )
    st.progress(min(1.0, used / MODEL_INPUT_LIMIT),
                text=f"{used:,} / {MODEL_INPUT_LIMIT:,} tokens of the model window used")
    if used > MODEL_INPUT_LIMIT:
        st.warning("Text is longer than the model window — the app will automatically split it into chunks.")

    show_n = st.slider("Tokens to display", 10, min(400, max(11, len(tokens))), min(60, len(tokens)))
    chips = "".join(
        f'<span class="tok t{i % 5}">{html.escape(t.replace("Ġ", "▁").replace("Ċ", "↵"))}</span>'
        for i, t in enumerate(tokens[:show_n])
    )
    st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
    st.caption("`▁` marks a token that starts a new word. Rare words are split into several sub-word pieces.")

    df = pd.DataFrame({"position": range(show_n), "token": tokens[:show_n],
                       "token_id": token_ids[1 : show_n + 1]})
    with st.expander("Token → ID table"):
        st.dataframe(df, hide_index=True)
    st.code(f"First 20 token IDs: {token_ids[:20]}", language="text")

# ── Tab 3: Model lab (notebook: model/config inspection) ─────────────────────
with tab_model:
    st.markdown("### Model Lab")
    st.caption("Architecture details read directly from the loaded model config.")
    cfg = model.config
    n_params = sum(p.numel() for p in model.parameters())
    st.markdown(
        '<div class="metrics">'
        + metric("Parameters", f"{n_params / 1e6:.0f}M", "g")
        + metric("Encoder layers", cfg.encoder_layers, "e")
        + metric("Decoder layers", cfg.decoder_layers, "r")
        + metric("Hidden size", cfg.d_model, "s")
        + metric("Attention heads", cfg.encoder_attention_heads, "v2")
        + metric("Vocab size", f"{cfg.vocab_size:,}", "g")
        + "</div>",
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    with left:
        st.markdown("**Pipeline components**")
        st.table(pd.DataFrame({
            "Component": ["Task", "Checkpoint", "Architecture", "Tokenizer class", "Model class", "Device"],
            "Value": ["summarization", MODEL_NAME, cfg.model_type, type(tokenizer).__name__,
                      type(model).__name__, str(device).upper()],
        }))
    with right:
        st.markdown("**Default generation settings**")
        gc = getattr(model, "generation_config", None)
        rows = {
            "num_beams": getattr(gc, "num_beams", "—"),
            "max_length": getattr(gc, "max_length", "—"),
            "min_length": getattr(gc, "min_length", "—"),
            "length_penalty": getattr(gc, "length_penalty", "—"),
            "no_repeat_ngram_size": getattr(gc, "no_repeat_ngram_size", "—"),
        }
        st.table(pd.DataFrame({"Parameter": list(rows), "Value": [str(v) for v in rows.values()]}))
    st.info("**DistilBART** is a smaller BART: the 12-layer encoder is kept, but the decoder is "
            "distilled from 12 layers down to 6, making it faster with only a small drop in quality.")

# ── Tab 4: History ───────────────────────────────────────────────────────────
with tab_hist:
    st.markdown("### Session History")
    hist = st.session_state["history"]
    if not hist:
        st.caption("Your summaries from this session will appear here.")
    else:
        if st.button("Clear history"):
            st.session_state["history"] = []
            st.rerun()
        for i, h in enumerate(hist, 1):
            preview = h["original"][:70].replace("\n", " ")
            with st.expander(f"#{len(hist) - i + 1} · {h['time']} · {preview}…"):
                st.markdown("**Summary**")
                st.write(h["summary"])
                st.caption(f"{h['in_words']} → {h['out_words']} words · {h['seconds']:.1f}s · {h['n_chunks']} chunk(s)")

# ── Tab 5: How it works ──────────────────────────────────────────────────────
with tab_about:
    st.markdown("### How it works")
    a, b = st.columns(2)
    with a:
        st.markdown(
            """
**1 · Tokenise** — text is split into sub-word tokens and mapped to integer IDs.

**2 · Encode** — the transformer *encoder* reads all tokens at once using self-attention,
building a context-aware representation of the article.

**3 · Decode** — the *decoder* writes the summary one token at a time, attending to the encoder
output. This is **abstractive** summarisation: it writes new sentences instead of copying them.

**4 · Beam search** — several candidate summaries are explored in parallel and the best one is kept.
"""
        )
    with b:
        st.markdown(
            """
**Parameters used**

| Parameter | Meaning |
|---|---|
| `max_length` / `min_length` | Bounds on summary length (tokens) |
| `num_beams` | Beam-search width (1 = greedy) |
| `no_repeat_ngram_size` | Prevents repeated phrases |
| `repetition_penalty` | Discourages repeated tokens |
| `do_sample=False` | Deterministic output |

**Long documents** — the model reads at most 1,024 tokens. Longer text is split into
sentence-aligned chunks, each is summarised, and an optional merge pass condenses the result.
"""
        )
