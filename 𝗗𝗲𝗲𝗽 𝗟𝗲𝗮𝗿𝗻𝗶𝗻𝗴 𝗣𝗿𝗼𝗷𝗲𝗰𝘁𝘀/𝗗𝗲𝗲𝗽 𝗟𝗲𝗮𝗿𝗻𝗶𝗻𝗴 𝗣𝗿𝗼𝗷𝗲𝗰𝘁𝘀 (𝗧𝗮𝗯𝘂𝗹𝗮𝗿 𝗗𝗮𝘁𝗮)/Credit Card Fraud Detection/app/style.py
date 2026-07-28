"""
Visual identity for the Fraud Sentinel app.

Design direction: dark, premium, tech-forward "bank vault ledger" —
deep charcoal-navy background, brass-gold / emerald / oxblood jewel
accents, Cormorant Garamond for display type, JetBrains Mono for
data/numbers, Inter for body copy. Signature element: an ambient
scrolling transaction ticker behind the hero, and a circular
"verdict seal" badge used on the Predict page.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-void: #05070B;
    --bg-base: #0A0E14;
    --bg-panel: #131824;
    --bg-panel-raised: #1A2130;
    --line: rgba(201, 162, 39, 0.18);
    --line-soft: rgba(237, 234, 224, 0.08);
    --gold: #C9A227;
    --gold-bright: #E4C55E;
    --emerald: #1E8A6E;
    --emerald-bright: #2FBF89;
    --oxblood: #7A1F2B;
    --oxblood-bright: #D1495B;
    --text-hi: #F3F0E6;
    --text-mid: #C8C3B8;
    --text-low: #8A8F9C;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(ellipse 900px 500px at 8% -5%, rgba(201,162,39,0.10), transparent 60%),
        radial-gradient(ellipse 900px 600px at 95% 10%, rgba(30,138,110,0.10), transparent 55%),
        radial-gradient(ellipse 1200px 800px at 50% 110%, rgba(122,31,43,0.10), transparent 60%),
        var(--bg-base);
    color: var(--text-hi);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-panel) 0%, var(--bg-base) 100%) !important;
    border-right: 1px solid var(--line) !important;
}
[data-testid="stSidebar"] * { color: var(--text-mid) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: var(--gold-bright) !important;
    font-family: 'Cormorant Garamond', serif !important;
}

/* Sidebar radio nav -> card-style buttons */
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: var(--bg-panel-raised);
    border: 1px solid var(--line-soft);
    border-radius: 8px;
    padding: 10px 14px !important;
    margin-bottom: 6px;
    transition: all 0.15s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    border-color: var(--gold);
    background: rgba(201,162,39,0.08);
}
[data-testid="stSidebar"] [role="radiogroup"] label[data-baseweb="radio"] div:first-child {
    border-color: var(--gold) !important;
}

/* ---------- Headings ---------- */
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--text-hi) !important;
    letter-spacing: 0.01em;
}
h1 { font-weight: 700 !important; }
h2, h3 { font-weight: 600 !important; }

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.3rem;
}

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(180deg, var(--bg-panel-raised), var(--bg-panel)) !important;
    color: var(--gold-bright) !important;
    border: 1px solid var(--gold) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em;
    transition: all 0.15s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    box-shadow: 0 0 16px rgba(201,162,39,0.35) !important;
    border-color: var(--gold-bright) !important;
    color: var(--bg-void) !important;
    background: var(--gold-bright) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), var(--gold-bright)) !important;
    color: var(--bg-void) !important;
    font-weight: 700 !important;
}

/* ---------- Inputs ---------- */
.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input, .stTextInput input {
    background: var(--bg-panel-raised) !important;
    border: 1px solid var(--line-soft) !important;
    color: var(--text-hi) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stSlider [data-baseweb="slider"] div div div { background: var(--gold) !important; }

/* ---------- Hero ---------- */
.hero-wrap {
    position: relative;
    border: 1px solid var(--line);
    border-radius: 16px;
    background: linear-gradient(155deg, var(--bg-panel) 0%, var(--bg-base) 100%);
    padding: 2.6rem 2.4rem 1.6rem 2.4rem;
    overflow: hidden;
    margin-bottom: 1.6rem;
}
.hero-wrap::before {
    content: "";
    position: absolute; inset: 0;
    background-image: repeating-linear-gradient(180deg, transparent, transparent 27px, rgba(255,255,255,0.015) 28px);
    pointer-events: none;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.1rem;
    font-weight: 700;
    line-height: 1.05;
    margin: 0.1rem 0 0.5rem 0;
    background: linear-gradient(100deg, var(--gold-bright), var(--text-hi) 55%, var(--emerald-bright));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: var(--text-mid);
    font-size: 1.05rem;
    max-width: 640px;
    line-height: 1.55;
    margin-bottom: 1.4rem;
}

.ticker-outer {
    border-top: 1px solid var(--line-soft);
    border-bottom: 1px solid var(--line-soft);
    padding: 8px 0;
    overflow: hidden;
    white-space: nowrap;
    margin-top: 0.6rem;
}
.ticker-track {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-low);
    animation: ticker-scroll 38s linear infinite;
}
.ticker-track span.ok { color: var(--emerald-bright); }
.ticker-track span.flag { color: var(--oxblood-bright); }
@keyframes ticker-scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
@media (prefers-reduced-motion: reduce) {
    .ticker-track { animation: none; }
}

/* ---------- Metric cards ---------- */
.card-row { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 1.2rem; }
.metric-card {
    flex: 1 1 180px;
    background: var(--bg-panel);
    border: 1px solid var(--line-soft);
    border-left: 3px solid var(--gold);
    border-radius: 10px;
    padding: 16px 18px;
}
.metric-card.emerald { border-left-color: var(--emerald); }
.metric-card.oxblood { border-left-color: var(--oxblood); }
.metric-card .m-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-low);
    margin-bottom: 6px;
}
.metric-card .m-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text-hi);
}
.metric-card .m-sub { font-size: 0.78rem; color: var(--text-low); margin-top: 4px; }

/* ---------- Panels / sections ---------- */
.panel {
    background: var(--bg-panel);
    border: 1px solid var(--line-soft);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.panel h4 { margin-top: 0 !important; }

/* ---------- Verdict seal (signature element) ---------- */
.seal-wrap { display: flex; align-items: center; gap: 26px; flex-wrap: wrap; }
.seal {
    width: 128px; height: 128px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column;
    font-family: 'JetBrains Mono', monospace;
    position: relative;
    flex-shrink: 0;
}
.seal.safe {
    background: radial-gradient(circle at 35% 30%, rgba(47,191,137,0.18), var(--bg-panel) 70%);
    border: 2px solid var(--emerald-bright);
    box-shadow: 0 0 26px rgba(47,191,137,0.35);
}
.seal.flag {
    background: radial-gradient(circle at 35% 30%, rgba(209,73,91,0.20), var(--bg-panel) 70%);
    border: 2px solid var(--oxblood-bright);
    box-shadow: 0 0 26px rgba(209,73,91,0.4);
    animation: pulse-flag 1.8s ease-in-out infinite;
}
@keyframes pulse-flag {
    0%, 100% { box-shadow: 0 0 20px rgba(209,73,91,0.35); }
    50% { box-shadow: 0 0 34px rgba(209,73,91,0.6); }
}
.seal .seal-pct { font-size: 1.5rem; font-weight: 700; }
.seal .seal-tag { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 2px; }
.seal.safe .seal-pct, .seal.safe .seal-tag { color: var(--emerald-bright); }
.seal.flag .seal-pct, .seal.flag .seal-tag { color: var(--oxblood-bright); }

.verdict-title { font-family: 'Cormorant Garamond', serif; font-size: 1.9rem; font-weight: 700; margin-bottom: 2px; }
.verdict-title.safe { color: var(--emerald-bright); }
.verdict-title.flag { color: var(--oxblood-bright); }
.verdict-desc { color: var(--text-mid); font-size: 0.92rem; max-width: 440px; }

/* ---------- Badges / pills ---------- */
.pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid var(--line);
    color: var(--gold-bright);
    background: rgba(201,162,39,0.08);
}

/* ---------- Divider ---------- */
.gold-rule { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); margin: 1.6rem 0; }

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: var(--bg-panel);
    border: 1px solid var(--line-soft);
    border-radius: 8px 8px 0 0;
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
}
.stTabs [aria-selected="true"] {
    color: var(--gold-bright) !important;
    border-color: var(--gold) !important;
}

/* ---------- Dataframe ---------- */
[data-testid="stDataFrame"] { border: 1px solid var(--line-soft); border-radius: 8px; overflow: hidden; }

/* ---------- Footer ---------- */
.footer-note {
    text-align: center;
    color: var(--text-low);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--line-soft);
}
</style>
"""


def inject(st):
    st.markdown(CSS, unsafe_allow_html=True)
