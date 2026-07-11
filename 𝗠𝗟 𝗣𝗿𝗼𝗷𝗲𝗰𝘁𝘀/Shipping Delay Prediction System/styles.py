"""
styles.py
----------
Design system for the Shipment Delay Intelligence application.

v2 -- "Control Tower" direction.
Same public API as before (inject / route_divider / section_head) and the
same CSS class names, so nothing in app.py needs to change. Only the look
has been rebuilt.

Palette (named tokens):
    --bg-0        #0A0B0F   graphite black background
    --bg-1        #0F1116   panel background
    --bg-2        #15171F   card surface
    --bg-3        #1C1F29   raised / hover surface
    --line        rgba(255,255,255,0.07)   hairline borders
    --ink-0       #F4F5F7   primary text
    --ink-1       #979CA8   secondary text
    --ink-2       #5A5F6C   tertiary / caption text
    --brand       #4C8EFF   signal blue -- primary accent ("in transit")
    --brand-2     #34D399   arrival green -- motion / confirm accent
    --amber       #FFB020   caution / delay-risk accent
    --danger      #FF5C72   high risk / error
    --success     #34D399   on-time / success

Typography:
    Display / headings : "Outfit"        -- geometric, technical, quiet confidence
    Body                : "Inter"
    Data / labels / mono: "IBM Plex Mono"

Signature element: the "manifest line" -- a hairline route rail with a
single glowing signal ping that sweeps between two waypoint nodes. No
emoji, no clutter -- the motion itself carries the "shipment in progress"
idea. Used as a section divider and inside the prediction result card.
"""

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>

:root{
    --bg-0:#0A0B0F;
    --bg-1:#0F1116;
    --bg-2:#15171F;
    --bg-3:#1C1F29;
    --line: rgba(255,255,255,0.07);
    --ink-0:#F4F5F7;
    --ink-1:#979CA8;
    --ink-2:#5A5F6C;
    --brand:#4C8EFF;
    --brand-soft: rgba(76,142,255,0.12);
    --brand-2:#34D399;
    --amber:#FFB020;
    --danger:#FF5C72;
    --success:#34D399;
}

/* ---------- base resets ---------- */
html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
    color: var(--ink-0);
}

.stApp{
    background:
        linear-gradient(180deg, rgba(76,142,255,0.05) 0%, transparent 22%),
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,255,255,0.025) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.02) 40px),
        var(--bg-0);
}

h1, h2, h3, h4, .display{
    font-family:'Outfit', sans-serif !important;
    letter-spacing:-0.015em;
    color: var(--ink-0);
}

p, span, li, label, div{
    font-family:'Inter', sans-serif;
}

/* ---------- force-override Streamlit's own (light-mode) text colors ----------
   Streamlit ships its own default text-color rules scoped to data-testid
   containers (e.g. stMarkdownContainer, stSidebarNav). Those selectors are
   more specific than plain element selectors above, so without !important
   here they win and text renders in Streamlit's default dark-gray -- which
   is invisible on our dark background. This block guarantees our palette
   always wins, everywhere Streamlit renders text. */
.stApp, .stApp p, .stApp span, .stApp label, .stApp li,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stText"],
[data-testid="stCaptionContainer"]{
    color: var(--ink-0) !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
.stApp h1, .stApp h2, .stApp h3, .stApp h4{
    font-family:'Outfit', sans-serif !important;
    color: var(--ink-0) !important;
}

/* muted / secondary text that should stay dimmer than ink-0 */
[data-testid="stCaptionContainer"],
.stApp small{
    color: var(--ink-1) !important;
}

/* ---------- sidebar page navigation ---------- */
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span,
[data-testid="stSidebarNav"] a *,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{
    color: var(--ink-1) !important;
    font-family:'Inter', sans-serif !important;
}
[data-testid="stSidebarNav"] a:hover span,
[data-testid="stSidebarNav"] a:hover *,
[data-testid="stSidebarNav"] a[aria-current="page"] span,
[data-testid="stSidebarNav"] a[aria-current="page"] *{
    color: var(--ink-0) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"]{
    background: var(--bg-3) !important;
    border-radius: 8px;
}

/* generic widget labels (selectbox, slider, radio, etc.) */
.stApp [data-testid="stWidgetLabel"] p{
    color: var(--ink-1) !important;
}

.mono{
    font-family:'IBM Plex Mono', monospace !important;
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
    background: linear-gradient(180deg, #0B0C11 0%, #08090C 100%);
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
    font-family:'IBM Plex Mono', monospace;
    font-size:0.72rem;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color: var(--brand);
    background: rgba(76,142,255,0.08);
    border:1px solid rgba(76,142,255,0.28);
    padding:6px 14px;
    border-radius:6px;
    margin-bottom:14px;
}
.eyebrow .dot{
    width:6px;height:6px;border-radius:50%;
    background: var(--brand);
    box-shadow: 0 0 8px var(--brand);
    animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse{
    0%,100%{ opacity:1; transform:scale(1);}
    50%{ opacity:0.35; transform:scale(0.7);}
}

/* ---------- hero ---------- */
.hero-title{
    font-size: clamp(2.4rem, 5vw, 3.7rem);
    font-weight:700;
    line-height:1.05;
    margin-bottom:18px;
    color: var(--ink-0);
}
.hero-title em{
    font-style:normal;
    background: linear-gradient(100deg, var(--brand) 0%, var(--brand-2) 100%);
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

/* ---------- route line signature element ("manifest line") ---------- */
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
    height:1px;
    background: var(--line);
}
.route .node{
    position:relative;
    z-index:2;
    width:9px; height:9px; border-radius:2px;
    background: var(--bg-2);
    border:2px solid var(--brand-2);
    transform: rotate(45deg);
}
.route .node.origin{ border-color: var(--brand); }
.route .node.dest{ border-color: var(--brand-2); margin-left:auto; }
.route .truck{
    position:absolute;
    top:50%;
    left:0;
    width:8px; height:8px;
    border-radius:50%;
    background: var(--brand);
    box-shadow: 0 0 0 4px rgba(76,142,255,0.15), 0 0 16px 2px rgba(76,142,255,0.8);
    transform: translate(-50%, -50%);
    animation: travel 4.5s ease-in-out infinite;
}
.route .truck::after{
    content:"";
    position:absolute;
    top:50%; right:100%;
    width:46px; height:1px;
    transform: translateY(-50%);
    background: linear-gradient(90deg, transparent, rgba(76,142,255,0.6));
}
@keyframes travel{
    0%{ left:2%; }
    50%{ left:96%; }
    100%{ left:2%; }
}

/* ---------- glass card ---------- */
.card{
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008));
    border:1px solid var(--line);
    border-radius:14px;
    padding:26px 26px;
    position:relative;
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    height:100%;
}
.card::before{
    content:"";
    position:absolute;
    top:-1px; left:14px; right:14px; height:1px;
    background: linear-gradient(90deg, transparent, rgba(76,142,255,0.5), transparent);
    opacity:0;
    transition: opacity .25s ease;
}
.card:hover{
    transform: translateY(-4px);
    border-color: rgba(76,142,255,0.35);
    box-shadow: 0 18px 40px -22px rgba(76,142,255,0.5);
}
.card:hover::before{ opacity:1; }
.card h3{ margin-top:0; margin-bottom:8px; font-size:1.05rem;}
.card p{ color:var(--ink-1); font-size:0.92rem; line-height:1.55; margin:0;}
.card .icon{
    font-size:1.4rem;
    display:inline-flex;
    width:44px; height:44px;
    align-items:center; justify-content:center;
    border-radius:10px;
    background: var(--brand-soft);
    border:1px solid rgba(76,142,255,0.2);
    margin-bottom:14px;
}

/* ---------- metric card ---------- */
.metric{
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.006));
    border:1px solid var(--line);
    border-radius:12px;
    padding:20px 22px;
    transition: all .2s ease;
}
.metric:hover{ border-color: rgba(52,211,153,0.3); transform: translateY(-2px);}
.metric .label{
    font-family:'IBM Plex Mono', monospace;
    font-size:0.7rem;
    letter-spacing:0.1em;
    text-transform:uppercase;
    color: var(--ink-2);
    margin-bottom:6px;
}
.metric .value{
    font-family:'Outfit', sans-serif;
    font-size:1.9rem;
    font-weight:700;
    color: var(--ink-0);
}
.metric .delta{
    font-family:'IBM Plex Mono', monospace;
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
    font-family:'IBM Plex Mono', monospace;
    font-size:0.72rem;
    color: var(--ink-2);
    letter-spacing:0.08em;
}

/* ---------- pill / badge ---------- */
.badge{
    display:inline-block;
    padding:4px 12px;
    border-radius:6px;
    font-family:'IBM Plex Mono', monospace;
    font-size:0.72rem;
    letter-spacing:0.05em;
    border:1px solid var(--line);
    color: var(--ink-1);
}
.badge.brand{ color: var(--brand); border-color: rgba(76,142,255,0.4); background: var(--brand-soft);}
.badge.teal{ color: var(--brand-2); border-color: rgba(52,211,153,0.35); background: rgba(52,211,153,0.08);}

/* ---------- result cards ---------- */
.result{
    border-radius:16px;
    padding:32px;
    border:1px solid var(--line);
    position:relative;
    overflow:hidden;
}
.result::before{
    content:"";
    position:absolute;
    top:0; left:0; bottom:0; width:3px;
}
.result.ontime{
    background: linear-gradient(135deg, rgba(52,211,153,0.12), rgba(52,211,153,0.015));
    border-color: rgba(52,211,153,0.35);
}
.result.ontime::before{ background: var(--success); }
.result.delay{
    background: linear-gradient(135deg, rgba(255,92,114,0.12), rgba(255,92,114,0.015));
    border-color: rgba(255,92,114,0.35);
}
.result.delay::before{ background: var(--danger); }
.result .headline{
    font-family:'Outfit', sans-serif;
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
    font-family:'IBM Plex Mono', monospace;
    color: var(--brand);
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
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.006));
    border:1px solid var(--line);
    border-radius:12px;
    padding:16px 18px;
}
.stButton>button{
    background: var(--brand);
    color:#08090C;
    border:none;
    border-radius:9px;
    padding:0.65rem 1.6rem;
    font-weight:600;
    letter-spacing:0.01em;
    transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    box-shadow: 0 10px 24px -14px rgba(76,142,255,0.8);
}
.stButton>button:hover{
    transform: translateY(-2px);
    background: #6BA1FF;
    box-shadow: 0 14px 30px -14px rgba(76,142,255,0.9);
}
.stTabs [data-baseweb="tab-list"]{ gap: 6px; }
.stTabs [data-baseweb="tab"]{
    background: var(--bg-2);
    border-radius: 8px 8px 0 0;
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
    """Returns HTML for the animated 'manifest line' signature element."""
    return f"""
    <div class="route">
        <div class="node origin"></div>
        <div class="truck"></div>
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