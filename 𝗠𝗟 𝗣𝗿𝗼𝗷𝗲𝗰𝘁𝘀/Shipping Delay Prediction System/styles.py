"""
styles.py
----------
Design system for the Shipment Delay Intelligence application.

Palette (named tokens):
    --bg-0        #070B14   deep space navy background
    --bg-1        #0D1220   panel background
    --bg-2        #131a2b   card surface
    --bg-3        #1a2238   raised / hover surface
    --line        rgba(255,255,255,0.08)   hairline borders
    --ink-0       #EDEFF7   primary text
    --ink-1       #9AA3B8   secondary text
    --ink-2       #616B84   tertiary / caption text
    --brand       #6C63FF   electric indigo -- primary accent
    --brand-2     #2DD4BF   transit teal -- motion / "in progress" accent
    --amber       #F5A524   caution / delay-risk accent
    --danger      #F5455C   high risk / error
    --success     #33D17A   on-time / success

Typography:
    Display / headings : "Space Grotesk"
    Body                : "Inter"
    Data / labels / mono: "JetBrains Mono"

Signature element: the "route line" -- a dashed horizontal path with a
travelling dot, used as a section divider and inside the prediction
result card as a shipment-progress motif.
"""

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>

:root{
    --bg-0:#070B14;
    --bg-1:#0D1220;
    --bg-2:#131a2b;
    --bg-3:#1a2238;
    --line: rgba(255,255,255,0.08);
    --ink-0:#EDEFF7;
    --ink-1:#9AA3B8;
    --ink-2:#616B84;
    --brand:#6C63FF;
    --brand-soft: rgba(108,99,255,0.14);
    --brand-2:#2DD4BF;
    --amber:#F5A524;
    --danger:#F5455C;
    --success:#33D17A;
}

/* ---------- base resets ---------- */
html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
    color: var(--ink-0);
}

.stApp{
    background:
        radial-gradient(1200px 600px at 85% -10%, rgba(108,99,255,0.16), transparent 60%),
        radial-gradient(900px 500px at -10% 110%, rgba(45,212,191,0.10), transparent 55%),
        var(--bg-0);
}

h1, h2, h3, h4, .display{
    font-family:'Space Grotesk', sans-serif !important;
    letter-spacing:-0.01em;
    color: var(--ink-0);
}

p, span, li, label, div{
    font-family:'Inter', sans-serif;
}

.mono{
    font-family:'JetBrains Mono', monospace !important;
    letter-spacing:0.02em;
}

::-webkit-scrollbar{ width:8px; height:8px; }
::-webkit-scrollbar-thumb{ background: var(--bg-3); border-radius:8px; }
::-webkit-scrollbar-track{ background: transparent; }

/* ---------- hide default chrome ---------- */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #0A0E19 0%, #090D17 100%);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container{
    padding-top: 1.4rem;
}

/* ---------- generic containers ---------- */
.block-container{
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1180px;
}

/* ---------- eyebrow ---------- */
.eyebrow{
    display:inline-flex;
    align-items:center;
    gap:8px;
    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color: var(--brand-2);
    background: rgba(45,212,191,0.08);
    border:1px solid rgba(45,212,191,0.25);
    padding:6px 14px;
    border-radius:999px;
    margin-bottom:14px;
}
.eyebrow .dot{
    width:6px;height:6px;border-radius:50%;
    background: var(--brand-2);
    box-shadow: 0 0 8px var(--brand-2);
    animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse{
    0%,100%{ opacity:1; transform:scale(1);}
    50%{ opacity:0.4; transform:scale(0.7);}
}

/* ---------- hero ---------- */
.hero-title{
    font-size: clamp(2.4rem, 5vw, 3.7rem);
    font-weight:700;
    line-height:1.05;
    margin-bottom:18px;
    background: linear-gradient(100deg, #FFFFFF 20%, #B9B4FF 55%, #2DD4BF 100%);
    -webkit-background-clip:text;
    background-clip:text;
    -webkit-text-fill-color:transparent;
}
.hero-sub{
    font-size:1.08rem;
    color: var(--ink-1);
    max-width:620px;
    line-height:1.65;
    margin-bottom: 28px;
}

/* ---------- route line signature element ---------- */
.route{
    position:relative;
    height:64px;
    margin: 8px 0 34px 0;
    display:flex;
    align-items:center;
}
.route::before{
    content:"";
    position:absolute;
    left:0; right:0; top:50%;
    height:2px;
    background: repeating-linear-gradient(90deg, var(--line) 0 10px, transparent 10px 18px);
}
.route .node{
    position:relative;
    z-index:2;
    width:11px; height:11px; border-radius:50%;
    background: var(--bg-2);
    border:2px solid var(--brand-2);
}
.route .node.origin{ border-color: var(--brand); }
.route .node.dest{ border-color: var(--brand-2); margin-left:auto; }
.route .truck{
    position:absolute;
    top:50%;
    left:0;
    transform: translate(-50%, -50%);
    font-size:1.15rem;
    animation: travel 4.5s ease-in-out infinite;
    filter: drop-shadow(0 0 6px rgba(108,99,255,0.6));
}
@keyframes travel{
    0%{ left:2%; }
    50%{ left:96%; }
    100%{ left:2%; }
}

/* ---------- glass card ---------- */
.card{
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01));
    border:1px solid var(--line);
    border-radius:18px;
    padding:26px 26px;
    backdrop-filter: blur(14px);
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    height:100%;
}
.card:hover{
    transform: translateY(-4px);
    border-color: rgba(108,99,255,0.4);
    box-shadow: 0 18px 40px -20px rgba(108,99,255,0.45);
}
.card h3{ margin-top:0; margin-bottom:8px; font-size:1.05rem;}
.card p{ color:var(--ink-1); font-size:0.92rem; line-height:1.55; margin:0;}
.card .icon{
    font-size:1.6rem;
    display:inline-flex;
    width:46px; height:46px;
    align-items:center; justify-content:center;
    border-radius:12px;
    background: var(--brand-soft);
    margin-bottom:14px;
}

/* ---------- metric card ---------- */
.metric{
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.008));
    border:1px solid var(--line);
    border-radius:16px;
    padding:20px 22px;
    transition: all .2s ease;
}
.metric:hover{ border-color: rgba(45,212,191,0.35); transform: translateY(-2px);}
.metric .label{
    font-family:'JetBrains Mono', monospace;
    font-size:0.7rem;
    letter-spacing:0.1em;
    text-transform:uppercase;
    color: var(--ink-2);
    margin-bottom:6px;
}
.metric .value{
    font-family:'Space Grotesk', sans-serif;
    font-size:1.9rem;
    font-weight:700;
    color: var(--ink-0);
}
.metric .delta{
    font-family:'JetBrains Mono', monospace;
    font-size:0.78rem;
    color: var(--brand-2);
    margin-top:4px;
}

/* ---------- section heading ---------- */
.section-head{
    display:flex;
    align-items:baseline;
    justify-content:space-between;
    margin: 42px 0 18px 0;
    border-bottom:1px solid var(--line);
    padding-bottom:14px;
}
.section-head h2{ margin:0; font-size:1.55rem; }
.section-head .tag{
    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    color: var(--ink-2);
    letter-spacing:0.08em;
}

/* ---------- pill / badge ---------- */
.badge{
    display:inline-block;
    padding:4px 12px;
    border-radius:999px;
    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    letter-spacing:0.05em;
    border:1px solid var(--line);
    color: var(--ink-1);
}
.badge.brand{ color: var(--brand); border-color: rgba(108,99,255,0.4); background: var(--brand-soft);}
.badge.teal{ color: var(--brand-2); border-color: rgba(45,212,191,0.35); background: rgba(45,212,191,0.08);}

/* ---------- result cards ---------- */
.result{
    border-radius:20px;
    padding:32px;
    border:1px solid var(--line);
    position:relative;
    overflow:hidden;
}
.result.ontime{
    background: linear-gradient(135deg, rgba(51,209,122,0.14), rgba(51,209,122,0.02));
    border-color: rgba(51,209,122,0.4);
}
.result.delay{
    background: linear-gradient(135deg, rgba(245,69,92,0.14), rgba(245,69,92,0.02));
    border-color: rgba(245,69,92,0.4);
}
.result .headline{
    font-family:'Space Grotesk', sans-serif;
    font-size:1.7rem;
    font-weight:700;
    margin-bottom:6px;
}
.result .sub{ color: var(--ink-1); font-size:0.95rem; }

/* ---------- workflow step ---------- */
.step{
    display:flex;
    gap:16px;
    padding:16px 4px;
    border-bottom:1px dashed var(--line);
}
.step:last-child{ border-bottom:none; }
.step .n{
    font-family:'JetBrains Mono', monospace;
    color: var(--brand-2);
    font-size:0.85rem;
    min-width:34px;
}
.step .t{ font-weight:600; color:var(--ink-0); margin-bottom:2px;}
.step .d{ color:var(--ink-1); font-size:0.88rem; }

/* ---------- footer ---------- */
.foot{
    margin-top:60px;
    padding-top:22px;
    border-top:1px solid var(--line);
    color: var(--ink-2);
    font-size:0.82rem;
    display:flex;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:10px;
}

/* ---------- streamlit widget overrides ---------- */
div[data-testid="stMetric"]{
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.008));
    border:1px solid var(--line);
    border-radius:16px;
    padding:16px 18px;
}
.stButton>button{
    background: linear-gradient(100deg, var(--brand), #8B5CF6);
    color:white;
    border:none;
    border-radius:12px;
    padding:0.65rem 1.6rem;
    font-weight:600;
    letter-spacing:0.01em;
    transition: transform .18s ease, box-shadow .18s ease;
    box-shadow: 0 10px 24px -12px rgba(108,99,255,0.7);
}
.stButton>button:hover{
    transform: translateY(-2px);
    box-shadow: 0 14px 30px -12px rgba(108,99,255,0.85);
}
.stTabs [data-baseweb="tab-list"]{ gap: 6px; }
.stTabs [data-baseweb="tab"]{
    background: var(--bg-2);
    border-radius: 10px 10px 0 0;
    color: var(--ink-1);
}
.stTabs [aria-selected="true"]{
    color: var(--ink-0) !important;
    background: var(--bg-3) !important;
}

hr{ border-color: var(--line); }

</style>
"""


def inject(st):
    """Injects the global CSS block into a Streamlit app."""
    st.markdown(CSS, unsafe_allow_html=True)


def route_divider(origin_label="WAREHOUSE", dest_label="CUSTOMER"):
    """Returns HTML for the animated dashed 'route' signature element."""
    return f"""
    <div class="route">
        <div class="node origin"></div>
        <div class="truck">📦</div>
        <div class="node dest"></div>
    </div>
    """


def section_head(title, tag=""):
    return f"""
    <div class="section-head">
        <h2>{title}</h2>
        <span class="tag">{tag}</span>
    </div>
    """
