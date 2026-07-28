"""
Reusable HTML snippets for the Fraud Sentinel app. Each function
returns a markdown/HTML string meant to be passed to
st.markdown(..., unsafe_allow_html=True).
"""

import random


def hero(title: str, subtitle: str, ticker_rows=None) -> str:
    ticker_html = ""
    if ticker_rows:
        items = " &nbsp;•&nbsp; ".join(ticker_rows)
        ticker_html = f'''
        <div class="ticker-outer">
            <div class="ticker-track">{items} &nbsp;•&nbsp; {items}</div>
        </div>
        '''
    return f'''
    <div class="hero-wrap">
        <div class="eyebrow">Credit Card Fraud Detection &nbsp;·&nbsp; PyTorch ANN</div>
        <div class="hero-title">{title}</div>
        <div class="hero-sub">{subtitle}</div>
        {ticker_html}
    </div>
    '''


def build_ticker_rows(sample_df, n=14):
    """Build mock scrolling ticker strings from real sample transactions."""
    rows = []
    df = sample_df.sample(min(n, len(sample_df)), random_state=random.randint(0, 10_000)) \
        if len(sample_df) > n else sample_df
    for _, r in df.iterrows():
        tag = '<span class="flag">FLAGGED</span>' if r["is_fraud"] == 1 else '<span class="ok">CLEARED</span>'
        rows.append(f'{r["category"]} · ${r["amt"]:.2f} · {r["state"]} · {tag}')
    return rows


def metric_card(label: str, value: str, sub: str = "", accent: str = "gold") -> str:
    cls = "" if accent == "gold" else accent
    return f'''
    <div class="metric-card {cls}">
        <div class="m-label">{label}</div>
        <div class="m-value">{value}</div>
        <div class="m-sub">{sub}</div>
    </div>
    '''


def card_row(cards_html: list) -> str:
    return f'<div class="card-row">{"".join(cards_html)}</div>'


def panel_open(title: str = "") -> str:
    heading = f"<h4>{title}</h4>" if title else ""
    return f'<div class="panel">{heading}'


def panel_close() -> str:
    return "</div>"


def verdict_seal(probability: float, threshold: float) -> str:
    is_fraud = probability >= threshold
    pct = f"{probability*100:.1f}%"
    seal_cls = "flag" if is_fraud else "safe"
    tag = "Risk Score" if is_fraud else "Risk Score"
    title = "Flagged as Suspicious" if is_fraud else "Cleared as Legitimate"
    title_cls = "flag" if is_fraud else "safe"
    desc = (
        f"The model estimates a <b>{pct}</b> probability of fraud, at or above "
        f"the current <b>{threshold*100:.0f}%</b> decision threshold. Recommend manual review."
        if is_fraud else
        f"The model estimates a <b>{pct}</b> probability of fraud, below the current "
        f"<b>{threshold*100:.0f}%</b> decision threshold. No action needed."
    )
    return f'''
    <div class="seal-wrap">
        <div class="seal {seal_cls}">
            <div class="seal-pct">{pct}</div>
            <div class="seal-tag">{tag}</div>
        </div>
        <div>
            <div class="verdict-title {title_cls}">{title}</div>
            <div class="verdict-desc">{desc}</div>
        </div>
    </div>
    '''


def pill(text: str) -> str:
    return f'<span class="pill">{text}</span>'


def gold_rule() -> str:
    return '<hr class="gold-rule" />'


def footer_note(text: str) -> str:
    return f'<div class="footer-note">{text}</div>'
