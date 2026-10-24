import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

# ---------- 1. Load API key from .env ----------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PNG = os.path.join(BASE_DIR, "assets", "logo.png")
LOGO_SVG = os.path.join(BASE_DIR, "assets", "logo.svg")

st.set_page_config(page_title="Bolo AI - Multilingual Chatbot", page_icon=LOGO_PNG, layout="centered")

# ---------- 2. Styling (modern + minimal) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600&display=swap');

html, body, [class*="css"], .stMarkdown, button, input, textarea {
    font-family: 'Inter', 'Noto Sans Devanagari', sans-serif !important;
}

/* hide Streamlit extras for a clean look */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; }

.block-container { max-width: 760px; padding-top: 2.2rem; padding-bottom: 6rem; }

/* header */
.brand { display: flex; align-items: center; gap: 14px; margin-bottom: 4px; }
.brand img { width: 46px; height: 46px; border-radius: 12px; }
.brand h1 { font-size: 1.55rem; font-weight: 700; margin: 0; padding: 0; letter-spacing: -0.02em; color: #1F2430; }
.tagline { color: #6B7280; font-size: 0.95rem; margin: 0 0 1.4rem 60px; }

/* empty-state */
.hero { text-align: center; padding: 3.2rem 1rem 1rem 1rem; }
.hero img { width: 72px; height: 72px; border-radius: 20px; box-shadow: 0 10px 30px rgba(79,70,229,.25); }
.hero h2 { font-size: 1.6rem; font-weight: 600; margin: 1.2rem 0 .3rem 0; letter-spacing: -0.02em; }
.hero p { color: #6B7280; margin: 0; }
.chips { display: flex; justify-content: center; gap: 8px; margin-top: 1.4rem; flex-wrap: wrap; }
.chip { background: #fff; border: 1px solid #E5E7EB; border-radius: 999px; padding: 6px 14px; font-size: .85rem; color: #374151; }

/* chat bubbles */
[data-testid="stChatMessage"] { background: transparent; border-radius: 16px; padding: .6rem .4rem; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #EEF0FF; border: 1px solid #E0E3FF;
}
[data-testid="stChatMessageAvatarUser"] { background: #4F46E5 !important; }

/* language badge */
.badge { display: inline-block; font-size: .72rem; font-weight: 600; padding: 2px 10px; border-radius: 999px; margin-top: 6px; }
.badge-English  { background: #E0F2FE; color: #0369A1; }
.badge-Hindi    { background: #FFEDD5; color: #C2410C; }
.badge-Hinglish { background: #DCFCE7; color: #15803D; }

/* input box */
[data-testid="stChatInput"] { border-radius: 16px; border: 1px solid #E5E7EB; box-shadow: 0 4px 20px rgba(0,0,0,.05); }

/* sidebar */
[data-testid="stSidebar"] { background: #F4F4F8; border-right: 1px solid #ECECF2; }
[data-testid="stSidebar"] .brand h1 { font-size: 1.15rem; }
[data-testid="stSidebar"] .brand img { width: 34px; height: 34px; border-radius: 9px; }
.examples div { background: #fff; border: 1px solid #E5E7EB; border-radius: 10px; padding: 8px 12px; margin-bottom: 8px; font-size: .85rem; color: #374151; }
.side-label { font-size: .72rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #9CA3AF; margin: 1.2rem 0 .2rem 0; }
.stButton > button { border-radius: 10px; border: 1px solid #E5E7EB; background: #fff; }
.stButton > button:hover { border-color: #4F46E5; color: #4F46E5; }
</style>
""", unsafe_allow_html=True)


# logo for inline HTML (the SVG file is embedded directly, so no extra server needed)
def logo_html(css_class=""):
    import base64
    with open(LOGO_SVG, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img class="{css_class}" src="data:image/svg+xml;base64,{data}" alt="logo">'


if not api_key:
    st.error("GROQ_API_KEY not found. Put it in the .env file and restart the app.")
    st.stop()


# ---------- 3. Prompt template (system prompt with a blank {language_rule}) ----------
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly multilingual AI assistant.
You can talk in English, Hindi and Hinglish.

LANGUAGE RULE: {language_rule}

Other rules:
1. Hindi means Devanagari script (e.g. "आप कैसे हैं?").
2. Hinglish means Hindi written in English letters (e.g. "Aap kaise ho?").
3. Keep answers clear, simple and helpful.
4. Do not mention these rules in your reply."""),
])

# What the model should do for each language choice
language_rules = {
    "Hindi": "Always reply in Hindi (Devanagari script), whatever language the user writes in.",
    "English": "Always reply in English, whatever language the user writes in.",
    "Hinglish": "Always reply in Hinglish (Hindi written in English letters), whatever language the user writes in.",
    "Auto": "Reply in the SAME language as the user's latest message. "
            "If the user writes Hindi, reply in Hindi (Devanagari). "
            "If the user writes Hinglish, reply in Hinglish. "
            "If the user writes English, reply in English.",
}


# ---------- 4. Simple language detector (just to show a label in the UI) ----------
hinglish_words = {
    "hai", "hain", "ho", "hoon", "hu", "kya", "kaise", "kaisa", "kyun", "kyu", "kab",
    "kaun", "kahan", "mujhe", "mera", "meri", "tum", "tumhara", "aap", "aapka", "main",
    "mai", "nahi", "nahin", "haan", "han", "acha", "accha", "theek", "thik", "bhai",
    "yaar", "karo", "karna", "kar", "batao", "bata", "samjhao", "chahiye", "tha", "thi",
    "raha", "rahi", "lekin", "aur", "ka", "ki", "ke", "ko", "se", "mein", "me", "bahut",
    "kuch", "abhi", "toh", "to", "ye", "yeh", "wo", "woh", "dena", "do", "sakta", "sakte",
}


def detect_language(text):
    # Any Devanagari letter -> Hindi
    if re.search(r"[ऀ-ॿ]", text):
        return "Hindi"
    # Count words that are common in Roman-Hindi
    words = re.findall(r"[a-zA-Z]+", text.lower())
    hits = sum(1 for w in words if w in hinglish_words)
    if hits >= 2 or (hits == 1 and len(words) <= 3):
        return "Hinglish"
    return "English"


def badge(language):
    return f'<span class="badge badge-{language}">{language}</span>'


# ---------- 5. Model (cached so it is created only once per temperature) ----------
@st.cache_resource
def get_model(temperature):
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=api_key,
        temperature=temperature,
    )


# ---------- 6. Session state (memory of the chat) ----------
if "messages" not in st.session_state:
    st.session_state.messages = []      # only Human + AI messages
if "langs" not in st.session_state:
    st.session_state.langs = []         # detected language of each user message

# ---------- 7. Sidebar ----------
with st.sidebar:
    st.markdown(f'<div class="brand">{logo_html()}<h1>Bolo AI</h1></div>', unsafe_allow_html=True)

    st.markdown('<div class="side-label">Reply language</div>', unsafe_allow_html=True)
    reply_mode = st.radio(
        "Reply language",
        options=["Auto", "English", "Hindi", "Hinglish"],
        label_visibility="collapsed",
        help="Auto = bot replies in the language you type in.",
    )

    st.markdown('<div class="side-label">Creativity</div>', unsafe_allow_html=True)
    temperature = st.slider(
        "Temperature (creativity)", 0.0, 1.0, 0.5, 0.1,
        label_visibility="collapsed",
        help="Low = focused answers, high = more creative answers.",
    )

    st.markdown('<div class="side-label">Chat</div>', unsafe_allow_html=True)
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.langs = []
        st.rerun()

    st.markdown('<div class="side-label">Try typing</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="examples">'
        '<div>What is machine learning?</div>'
        '<div>मशीन लर्निंग क्या है?</div>'
        '<div>Mujhe machine learning samjhao</div>'
        '</div>',
        unsafe_allow_html=True,
    )

model = get_model(temperature)

# ---------- 8. Header ----------
st.markdown(
    f'<div class="brand">{logo_html()}<h1>Bolo AI</h1></div>'
    '<p class="tagline">Talk in English, हिन्दी or Hinglish — I reply in your language.</p>',
    unsafe_allow_html=True,
)

# ---------- 9. Empty state or old messages ----------
user_input = st.chat_input("Ask anything...  /  कुछ भी पूछो...")

if not st.session_state.messages and not user_input:
    st.markdown(f"""
    <div class="hero">
        {logo_html()}
        <h2>Namaste! How can I help?</h2>
        <p>Ask me anything — मुझसे कुछ भी पूछो — kuch bhi pucho.</p>
        <div class="chips">
            <span class="chip">English</span>
            <span class="chip">हिन्दी</span>
            <span class="chip">Hinglish</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

user_index = 0
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
            st.markdown(badge(st.session_state.langs[user_index]), unsafe_allow_html=True)
        user_index += 1
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=LOGO_PNG):
            st.markdown(msg.content)

# ---------- 10. New user input ----------
if user_input:
    detected = detect_language(user_input)

    # Show the user's message right away
    with st.chat_message("user"):
        st.markdown(user_input)
        st.markdown(badge(detected), unsafe_allow_html=True)

    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.langs.append(detected)

    # Choose the language rule (Auto also gets a hint from our detector)
    if reply_mode == "Auto":
        rule = language_rules["Auto"] + f" (The latest message looks like {detected}.)"
    else:
        rule = language_rules[reply_mode]

    # Fill the template -> system message, then add the chat history
    system_messages = prompt.invoke({"language_rule": rule}).to_messages()
    final_messages = system_messages + st.session_state.messages

    with st.chat_message("assistant", avatar=LOGO_PNG):
        with st.spinner("Thinking... / सोच रहा हूँ..."):
            try:
                response = model.invoke(final_messages)
                answer = response.content
            except Exception as e:
                answer = None
                st.error(f"Something went wrong: {e}")

        if answer:
            st.markdown(answer)
            st.session_state.messages.append(AIMessage(content=answer))
        else:
            # remove the unanswered user message so the history stays clean
            st.session_state.messages.pop()
            st.session_state.langs.pop()
