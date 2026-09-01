"""
Simple dark theme -- clean, minimal, no heavy animations.

Color tokens:
    --bg        #0E1117   app background
    --card      #171B24   card background
    --border    #2A2F3A   hairline border
    --ink       #E6E9EF   primary text
    --ink-muted #9AA3B2   secondary text
    --accent    #22D3EE   accent (cyan)
    --success   #34D399   "NORMAL" result
    --alert     #FB7185   "PNEUMONIA" result
"""

from __future__ import annotations

import streamlit as st

_CSS = """
<style>
    :root {
        --card: #171B24;
        --border: #2A2F3A;
        --ink: #E6E9EF;
        --ink-muted: #9AA3B2;
        --accent: #22D3EE;
        --success: #34D399;
        --alert: #FB7185;
        --radius: 12px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---------- Card ---------- */
    .xr-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
    }
    .xr-eyebrow {
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--accent);
        font-weight: 700;
        margin-bottom: 0.4rem;
        display: block;
    }
    .xr-muted { color: var(--ink-muted); font-size: 0.93rem; line-height: 1.6; }

    /* ---------- Pills ---------- */
    .xr-pill-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
    .xr-pill {
        background: var(--card);
        color: var(--ink);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.3rem 0.9rem;
        font-size: 0.82rem;
    }

    /* ---------- Status badge ---------- */
    .xr-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.35rem 0.9rem;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .xr-dot { width: 9px; height: 9px; border-radius: 50%; }
    .xr-dot.ready { background: var(--success); }
    .xr-dot.warn { background: var(--alert); }

    /* ---------- Result banner ---------- */
    .xr-result {
        border-radius: var(--radius);
        padding: 1.5rem 1.7rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
        background: var(--card);
        border-left: 4px solid var(--border);
    }
    .xr-result.normal { border-left-color: var(--success); }
    .xr-result.pneumonia { border-left-color: var(--alert); }
    .xr-result-label { font-size: 1.7rem; font-weight: 700; margin: 0.1rem 0 0.2rem 0; }
    .xr-result.normal .xr-result-label { color: var(--success); }
    .xr-result.pneumonia .xr-result-label { color: var(--alert); }
    .xr-result-confidence { font-size: 1rem; color: var(--ink-muted); }

    /* ---------- Probability bars ---------- */
    .xr-prob-row { margin-bottom: 0.7rem; }
    .xr-prob-label {
        display: flex; justify-content: space-between;
        font-size: 0.85rem; color: var(--ink); margin-bottom: 0.3rem;
    }
    .xr-prob-track {
        background: #0E1117; border-radius: 999px; height: 10px;
        overflow: hidden; border: 1px solid var(--border);
    }
    .xr-prob-fill { height: 100%; border-radius: 999px; background: var(--accent); }

    /* ---------- Workflow steps ---------- */
    .xr-flow { display: flex; align-items: center; flex-wrap: wrap; gap: 0.4rem; margin: 0.6rem 0 1.2rem 0; }
    .xr-flow-step {
        background: var(--card); border: 1px solid var(--border);
        border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.85rem;
    }
    .xr-flow-arrow { color: var(--accent); font-weight: 700; }

    /* ---------- Disclaimer ---------- */
    .xr-disclaimer {
        background: var(--card);
        border-left: 3px solid var(--accent);
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        font-size: 0.85rem;
        color: var(--ink-muted);
        line-height: 1.55;
    }

    /* ---------- Hero ---------- */
    .xr-hero {
        border-bottom: 1px solid var(--border);
        padding: 0 0 1.5rem 0;
        margin-bottom: 1.5rem;
    }
    .xr-hero h1 {
        font-size: 2.1rem;
        margin-bottom: 0.5rem;
        color: var(--ink);
    }
    .xr-hero p {
        color: var(--ink-muted);
        font-size: 1rem;
        max-width: 46rem;
        line-height: 1.6;
    }

    /* ---------- Streamlit metrics ---------- */
    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.8rem 1rem;
    }
</style>
"""


def inject_global_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="xr-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(ready: bool, ready_text: str = "Model Ready", warn_text: str = "Setup Required") -> None:
    dot_class = "ready" if ready else "warn"
    text = ready_text if ready else warn_text
    st.markdown(
        f'<div class="xr-status"><span class="xr-dot {dot_class}"></span>{text}</div>',
        unsafe_allow_html=True,
    )


def card_open(eyebrow: str | None = None) -> None:
    eyebrow_html = f'<span class="xr-eyebrow">{eyebrow}</span>' if eyebrow else ""
    st.markdown(f'<div class="xr-card">{eyebrow_html}', unsafe_allow_html=True)


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def pill_row(items: list[str]) -> None:
    pills = "".join(f'<span class="xr-pill">{item}</span>' for item in items)
    st.markdown(f'<div class="xr-pill-row">{pills}</div>', unsafe_allow_html=True)


def workflow(steps: list[str]) -> None:
    parts = []
    for i, step in enumerate(steps):
        parts.append(f'<div class="xr-flow-step">{step}</div>')
        if i != len(steps) - 1:
            parts.append('<div class="xr-flow-arrow">&#8594;</div>')
    st.markdown(f'<div class="xr-flow">{"".join(parts)}</div>', unsafe_allow_html=True)


def disclaimer_banner(text: str) -> None:
    st.markdown(f'<div class="xr-disclaimer">&#9432;&nbsp; {text}</div>', unsafe_allow_html=True)


def result_banner(label: str, confidence: float) -> None:
    css_class = "normal" if label.upper() == "NORMAL" else "pneumonia"
    icon = "&#10003;" if css_class == "normal" else "&#9888;"
    st.markdown(
        f"""
        <div class="xr-result {css_class}">
            <span class="xr-eyebrow">Prediction</span>
            <div class="xr-result-label">{icon}&nbsp; {label.title()}</div>
            <div class="xr-result-confidence">Confidence: {confidence:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def probability_bars(class_probabilities: dict[str, float]) -> None:
    for label, pct in sorted(class_probabilities.items(), key=lambda kv: -kv[1]):
        st.markdown(
            f"""
            <div class="xr-prob-row">
                <div class="xr-prob-label"><span>{label.upper()}</span><span>{pct:.2f}%</span></div>
                <div class="xr-prob-track"><div class="xr-prob-fill" style="width:{pct:.2f}%"></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
