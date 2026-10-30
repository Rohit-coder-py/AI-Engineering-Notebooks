import re
import requests
import streamlit as st

# Config

DEFAULT_API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Fake Job Posting Detector",
    page_icon="🛡️",
    layout="wide",
)

# ------------------------------------------------------------------
# Styling (dark, premium, multi-colour, high-contrast)
# ------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;500;600&display=swap');

:root{
  --bg:#0b0e14; --panel:#131824; --panel2:#171d2c; --line:#27304a;
  --text:#f1f4fb; --muted:#aab3c9;
  --gold:#d9b45a; --emerald:#2fd4a0; --oxblood:#ff5b6e; --sapphire:#5b8cff; --amethyst:#b07cff; --amber:#ffb454;
}
html, body, [class*="css"], .stApp { font-family:'Inter',sans-serif; color:var(--text); }
.stApp { background: radial-gradient(1200px 600px at 10% -10%, #1a2140 0%, transparent 60%),
                     radial-gradient(900px 500px at 100% 0%, #2a1530 0%, transparent 55%), var(--bg); }
header[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:2rem; max-width:1250px; }

h1.hero{ font-family:'Cormorant Garamond',serif; font-weight:700; font-size:3.1rem; margin:0; line-height:1.05;
  background:linear-gradient(90deg,var(--gold),#fff 45%,var(--sapphire)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.sub{ color:var(--muted); font-size:1.05rem; margin:.4rem 0 1.4rem 0; }
.tag{ font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:.14em; text-transform:uppercase; color:var(--gold); }

.card{ background:linear-gradient(180deg,var(--panel2),var(--panel)); border:1px solid var(--line); border-radius:16px; padding:1.2rem 1.3rem; }
.card h3{ font-family:'Cormorant Garamond',serif; font-size:1.5rem; margin:.1rem 0 .6rem 0; color:var(--text); }

/* inputs */
label, .stTextInput label, .stTextArea label, .stCheckbox label, .stToggle label { color:var(--text) !important; font-weight:500; }
.stTextInput input, .stTextArea textarea{
  background:#0e1320 !important; color:var(--text) !important; border:1px solid var(--line) !important; border-radius:10px !important; }
.stTextInput input:focus, .stTextArea textarea:focus{ border-color:var(--sapphire) !important; box-shadow:0 0 0 2px rgba(91,140,255,.25) !important; }
::placeholder{ color:#6f7a95 !important; }

/* buttons */
.stButton > button, .stFormSubmitButton > button{
  border-radius:10px; border:1px solid var(--line); background:var(--panel2); color:var(--text); font-weight:600; }
.stButton > button:hover{ border-color:var(--gold); color:var(--gold); }
.stFormSubmitButton > button{ background:linear-gradient(90deg,var(--sapphire),var(--amethyst)); border:none; color:#fff; padding:.7rem 1rem; font-size:1.05rem; }
.stFormSubmitButton > button:hover{ filter:brightness(1.12); color:#fff; }

/* toggles: emerald when ON */
label:has(input[role="switch"]:checked) > div:first-of-type{ background-color:var(--emerald) !important; }

/* result */
.verdict{ border-radius:16px; padding:1.1rem 1.3rem; border:1px solid; }
.verdict.bad{ background:rgba(255,91,110,.10); border-color:var(--oxblood); }
.verdict.good{ background:rgba(47,212,160,.10); border-color:var(--emerald); }
.verdict .big{ font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:700; line-height:1.1; }
.verdict.bad .big{ color:var(--oxblood); } .verdict.good .big{ color:var(--emerald); }
.verdict .small{ color:var(--muted); font-size:.95rem; margin-top:.3rem; }

.pill{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.78rem; padding:.2rem .6rem; border-radius:999px; margin:.15rem .25rem .15rem 0; border:1px solid; }
.pill.r{ color:var(--oxblood); border-color:var(--oxblood); background:rgba(255,91,110,.08); }
.pill.a{ color:var(--amber);   border-color:var(--amber);   background:rgba(255,180,84,.08); }
.pill.g{ color:var(--emerald); border-color:var(--emerald); background:rgba(47,212,160,.08); }

.metric{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:.7rem .9rem; }
.metric .k{ font-family:'JetBrains Mono',monospace; font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }
.metric .v{ font-size:1.5rem; font-weight:600; }

.note{ color:var(--muted); font-size:.85rem; border-left:3px solid var(--gold); padding:.2rem .8rem; margin-top:1rem; }
section[data-testid="stSidebar"]{ background:#0d111b; border-right:1px solid var(--line); }
section[data-testid="stSidebar"] *{ color:var(--text); }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Sample postings (so you can demo quickly)
# ------------------------------------------------------------------
SAMPLES = {
    "suspicious": dict(
        title="Work From Home Data Entry - Earn $5000 Weekly",
        company_profile="",
        description="No experience needed! Earn money from home. Send your bank details and a registration fee to get started immediately.",
        requirements="",
        benefits="",
        salary_range="",
        telecommuting=True,
        has_company_logo=False,
        has_questions=False,
    ),
    "genuine": dict(
        title="Senior Data Analyst",
        company_profile="We are a 200-person analytics consultancy founded in 2010, helping retail and healthcare clients make better decisions with data. Our teams work across Pune, Bengaluru and Singapore.",
        description="You will own the reporting layer for our retail clients: build dashboards in Power BI, write SQL against our warehouse, and present findings to client stakeholders each month. You will mentor two junior analysts and work closely with the data engineering team.",
        requirements="4+ years of experience in analytics. Strong SQL and Python. Experience with Power BI or Tableau. Bachelor's degree in a quantitative field.",
        benefits="Health insurance, 24 days paid leave, learning budget, hybrid work policy.",
        salary_range="12-18 LPA",
        telecommuting=False,
        has_company_logo=True,
        has_questions=True,
    ),
}
FIELDS = list(SAMPLES["suspicious"].keys())

# initialise widget state once
for f in FIELDS:
    if f not in st.session_state:
        st.session_state[f] = "" if isinstance(SAMPLES["suspicious"][f], str) else False


def load_sample(name):
    for f in FIELDS:
        st.session_state[f] = SAMPLES[name][f]
    st.session_state.pop("result", None)


def clear_form():
    for f in FIELDS:
        st.session_state[f] = "" if isinstance(SAMPLES["suspicious"][f], str) else False
    st.session_state.pop("result", None)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
SCAM_PHRASES = [
    "registration fee", "bank details", "bank account", "western union", "money order",
    "processing fee", "security deposit", "no experience needed", "no experience required",
    "earn $", "per week", "weekly pay", "whatsapp", "telegram", "gift card", "wire transfer",
    "send your", "act now", "limited slots", "guaranteed income", "work from home and earn",
]


def red_flags(p):
    """Simple, explainable checks on what the user typed (separate from the ML score)."""
    full = " ".join([p["title"], p["company_profile"], p["description"], p["requirements"], p["benefits"]]).lower()
    flags = []
    hits = [ph for ph in SCAM_PHRASES if ph in full]
    if hits:
        flags.append(("r", "Scam-style wording: " + ", ".join(f'"{h}"' for h in hits[:4])))
    if re.search(r"\$\s?\d{4,}|\d{4,}\s?(usd|dollars)", full):
        flags.append(("a", "Very high pay figure quoted in the text"))
    if not p["company_profile"].strip():
        flags.append(("a", "No company profile given"))
    if not p["has_company_logo"]:
        flags.append(("a", "No company logo on the posting"))
    if not p["has_questions"]:
        flags.append(("a", "No screening questions"))
    if not p["salary_range"].strip():
        flags.append(("a", "Salary not mentioned"))
    if not p["requirements"].strip():
        flags.append(("a", "No requirements listed"))
    if len(p["description"].split()) < 25:
        flags.append(("a", "Very short job description"))
    if re.search(r"https?://|www\.", full):
        flags.append(("a", "Contains an external link - check it before clicking"))
    if not flags:
        flags.append(("g", "No obvious red flags in the details you entered"))
    return flags


def gauge_svg(pct):
    """Half-circle meter, green -> amber -> red."""
    import math
    pct = max(0.0, min(100.0, pct))
    ang = math.pi * (1 - pct / 100)            # pi (left) -> 0 (right)
    cx, cy, r = 150, 150, 110
    nx, ny = cx + (r - 18) * math.cos(ang), cy - (r - 18) * math.sin(ang)
    color = "#2fd4a0" if pct < 35 else ("#ffb454" if pct < 65 else "#ff5b6e")
    return f"""
<svg viewBox="0 0 300 190" width="100%" style="max-width:360px;display:block;margin:auto">
  <defs><linearGradient id="g" x1="0" x2="1">
    <stop offset="0" stop-color="#2fd4a0"/><stop offset=".5" stop-color="#ffb454"/><stop offset="1" stop-color="#ff5b6e"/>
  </linearGradient></defs>
  <path d="M40 150 A110 110 0 0 1 260 150" fill="none" stroke="#27304a" stroke-width="22" stroke-linecap="round"/>
  <path d="M40 150 A110 110 0 0 1 260 150" fill="none" stroke="url(#g)" stroke-width="22" stroke-linecap="round" opacity=".95"/>
  <line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#f1f4fb" stroke-width="4" stroke-linecap="round"/>
  <circle cx="{cx}" cy="{cy}" r="9" fill="#f1f4fb"/>
  <text x="{cx}" y="182" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="26" font-weight="600" fill="{color}">{pct:.1f}%</text>
  <text x="38" y="172" font-family="JetBrains Mono, monospace" font-size="11" fill="#aab3c9">0</text>
  <text x="248" y="172" font-family="JetBrains Mono, monospace" font-size="11" fill="#aab3c9">100</text>
</svg>"""


def call_api(base_url, p):
    payload = {
        "title": p["title"].strip(),
        "company_profile": p["company_profile"].strip(),
        "description": p["description"].strip(),
        "requirements": p["requirements"].strip(),
        "benefits": p["benefits"].strip(),
        "salary_range": p["salary_range"].strip(),
        "telecommuting": int(p["telecommuting"]),
        "has_company_logo": int(p["has_company_logo"]),
        "has_questions": int(p["has_questions"]),
    }
    r = requests.post(base_url.rstrip("/") + "/predict", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="tag">Backend</div>', unsafe_allow_html=True)
    api_url = st.text_input("FastAPI URL", value=DEFAULT_API_URL, help="Where `uvicorn app:app` is running")

    try:
        h = requests.get(api_url.rstrip("/") + "/health", timeout=3).json()
        ok = h.get("model_loaded") and h.get("vectorizer_loaded")
        st.markdown(
            f'<span class="pill {"g" if ok else "a"}">{"● API online · model loaded" if ok else "● API online · model missing"}</span>',
            unsafe_allow_html=True,
        )
    except Exception:
        st.markdown('<span class="pill r">● API offline</span>', unsafe_allow_html=True)
        st.caption("Start it with:  `uvicorn app:app --reload`")

    st.markdown("---")
    st.markdown('<div class="tag">Quick demo</div>', unsafe_allow_html=True)
    st.button("⚠️ Load suspicious sample", on_click=load_sample, args=("suspicious",), use_container_width=True)
    st.button("✅ Load genuine sample", on_click=load_sample, args=("genuine",), use_container_width=True)
    st.button("🧹 Clear form", on_click=clear_form, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="tag">About</div>', unsafe_allow_html=True)
    st.caption(
        "TF-IDF text features + 8 structured signals → Random Forest. "
        "Trained on the EMSCAD fake job postings dataset (~5% fraud), so recall on the fraud class matters more than accuracy."
    )

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown('<div class="tag">ML · FastAPI · Streamlit</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero">Fake Job Posting Detector</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub">Paste a job ad, get a fraud-risk score before you apply or share any personal details.</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 1], gap="large")

# ------------------------------------------------------------------
# Form
# ------------------------------------------------------------------
with left:
    with st.form("job_form"):
        st.markdown("### Job details")
        st.text_input("Job title *", key="title", placeholder="e.g. Senior Data Analyst")
        st.text_area("Job description *", key="description", height=150, placeholder="What will the person do day to day?")
        c1, c2 = st.columns(2)
        with c1:
            st.text_area("Company profile", key="company_profile", height=110, placeholder="About the company (optional)")
            st.text_area("Benefits", key="benefits", height=90, placeholder="Insurance, leave, etc. (optional)")
        with c2:
            st.text_area("Requirements", key="requirements", height=110, placeholder="Skills, experience, education (optional)")
            st.text_input("Salary range", key="salary_range", placeholder="e.g. 12-18 LPA (optional)")

        st.markdown("##### Posting signals")
        t1, t2, t3 = st.columns(3)
        t1.toggle("Remote job", key="telecommuting")
        t2.toggle("Has logo", key="has_company_logo")
        t3.toggle("Has questions", key="has_questions")

        submitted = st.form_submit_button("🔍 Analyse posting", use_container_width=True)

if submitted:
    p = {f: st.session_state[f] for f in FIELDS}
    if len(p["title"].strip()) < 3:
        st.session_state["result"] = {"error": "Job title must be at least 3 characters."}
    elif len(p["description"].strip()) < 10:
        st.session_state["result"] = {"error": "Job description must be at least 10 characters."}
    else:
        try:
            with st.spinner("Asking the model..."):
                res = call_api(api_url, p)
            st.session_state["result"] = {"data": res, "flags": red_flags(p), "words": len(p["description"].split())}
        except requests.exceptions.ConnectionError:
            st.session_state["result"] = {"error": f"Can't reach the API at {api_url}. Is `uvicorn app:app --reload` running?"}
        except requests.exceptions.HTTPError as e:
            st.session_state["result"] = {"error": f"API returned an error: {e.response.text}"}
        except Exception as e:
            st.session_state["result"] = {"error": str(e)}

# ------------------------------------------------------------------
# Result
# ------------------------------------------------------------------
with right:
    res = st.session_state.get("result")
    if not res:
        st.markdown(
            """<div class="card"><h3>Result appears here</h3>
            <p style="color:var(--muted)">Fill in the form on the left (or load a sample from the sidebar) and press <b>Analyse posting</b>.</p>
            <span class="pill g">Title + description are required</span>
            <span class="pill a">More details = better prediction</span></div>""",
            unsafe_allow_html=True,
        )
    elif "error" in res:
        st.error(res["error"])
    else:
        d = res["data"]
        pct = d["fraud_percentage"]
        is_fraud = d["prediction"].startswith("Fraud")
        cls = "bad" if is_fraud else "good"
        icon = "🚨" if is_fraud else "✅"
        msg = (
            "The model sees patterns typical of scam postings. Do not pay any fee or share ID / bank details."
            if is_fraud
            else "The model sees patterns typical of genuine postings. Still verify the employer independently."
        )
        st.markdown(
            f'<div class="verdict {cls}"><div class="big">{icon} {d["prediction"]}</div><div class="small">{msg}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(gauge_svg(pct), unsafe_allow_html=True)

        risk = "Low" if pct < 35 else ("Medium" if pct < 65 else "High")
        rc = "#2fd4a0" if risk == "Low" else ("#ffb454" if risk == "Medium" else "#ff5b6e")
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric"><div class="k">Fraud prob.</div><div class="v" style="color:{rc}">{d["fraud_probability"]:.3f}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric"><div class="k">Risk level</div><div class="v" style="color:{rc}">{risk}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric"><div class="k">Desc. words</div><div class="v" style="color:#5b8cff">{res["words"]}</div></div>', unsafe_allow_html=True)

        st.markdown("#### Red-flag checklist")
        st.markdown("".join(f'<span class="pill {c}">{t}</span>' for c, t in res["flags"]), unsafe_allow_html=True)
        st.caption("The checklist is a simple rule-based check on your inputs. It is separate from the ML score.")

        st.markdown(
            '<div class="note">This is only a prediction. Always verify the employer (official website, LinkedIn, reviews) '
            "and never pay money to get a job.</div>",
            unsafe_allow_html=True,
        )
