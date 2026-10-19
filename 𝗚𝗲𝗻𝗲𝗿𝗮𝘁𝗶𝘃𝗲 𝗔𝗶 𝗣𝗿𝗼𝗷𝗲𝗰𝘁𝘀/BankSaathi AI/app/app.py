
import os
from typing import Optional, List

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

# ---------------------------------------------------------------------------
# 0. Basic settings
# ---------------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "..", "assests", "logo_small.jpg")

MODEL_NAME = "openai/gpt-oss-20b"


MAX_HISTORY_MESSAGES = 12

EXAMPLE_QUESTIONS = [
    "What is UPI and how does it work?",
    "UPI PIN kya hota hai?",
    "NEFT, RTGS aur IMPS me kya difference hai?",
    "Debit card aur credit card me kya fark hai?",
]

st.set_page_config(page_title="BankSaathi AI", page_icon=LOGO_PATH, layout="centered")


# ---------------------------------------------------------------------------
# 1. Models  (same ChatGroq you already use; @st.cache_resource = create once)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_chat_model():
    # temperature 0.3 -> focused answers (good for banking facts)
    return ChatGroq(
        model=MODEL_NAME,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
        max_tokens=2000,
    )


@st.cache_resource
def get_extract_model():
    # temperature 0 -> most predictable output, best for structured JSON
    return ChatGroq(
        model=MODEL_NAME,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        max_tokens=2000,
    )


# ---------------------------------------------------------------------------
# 2. System prompt for the chat (built from the sidebar settings)
# ---------------------------------------------------------------------------
def build_system_prompt(language_choice, level_choice):
    # --- language rules ---
    if language_choice == "Auto (same as my question)":
        language_rules = """
    - If the user asks in Hindi, reply in Hindi.
    - If the user asks in Hinglish, reply in Hinglish.
    - If the user asks in English, reply in English."""
    else:
        language_rules = f"""
    - Always reply in {language_choice}, even if the question is in another language."""

    # --- how detailed should the answer be ---
    if level_choice == "Simple":
        level_rules = """
    - Keep answers short and very easy, like explaining to someone new to banking.
    - Use everyday examples (for example: sending money to a friend)."""
    else:
        level_rules = """
    - Give a more detailed answer with step-by-step points when useful.
    - Still avoid heavy jargon, and explain any banking term you use."""

    return f"""
    You are BankSaathi AI, a multilingual banking assistant for India.

    LANGUAGE RULES:{language_rules}

    ANSWER STYLE:{level_rules}

    RESPONSIBILITIES:
    - Explain UPI, ATM, debit cards, credit cards, bank transfers, NEFT, RTGS,
      IMPS, account statements and other everyday banking concepts in simple language.
    - Provide clear, helpful, step-by-step guidance when appropriate.
    - Only answer banking, payments and money-safety questions. If the question
      is about something else, politely say you can only help with banking topics.

    ACCURACY:
    - Fees, transaction limits, timings and interest rates change and differ
      between banks. Do NOT state exact numbers as facts. Say they vary and
      ask the user to check their bank's official app or website, or RBI/NPCI.
    - If unsure, clearly say so instead of inventing information.

    SAFETY:
    - Never ask for OTPs, UPI PINs, ATM PINs, passwords, CVVs or full card numbers.
    - Never claim to access bank accounts or perform transactions.
    - For account-specific issues, direct users to their bank's official
      app, website, branch, or verified customer support.
    - If the user describes a possible fraud, tell them to contact their bank
      immediately and report it on the National Cyber Crime Helpline 1930
      or cybercrime.gov.in.
    """


# ---------------------------------------------------------------------------
# 3. Privacy guard: stop users from sending secrets to the AI
# ---------------------------------------------------------------------------
SECRET_WORDS = ["otp", "pin", "cvv", "password", "passcode"]


def contains_sensitive_info(text):
    """Return True if the text looks like it contains an OTP / PIN / card number."""
    text_lower = text.lower()

    # Rule 1: a secret word AND a number with 4 or more digits
    # ("my OTP is 482913" -> True, but "UPI PIN kya hota hai?" -> False)
    digit_count = sum(1 for ch in text if ch.isdigit())
    if digit_count >= 4:
        for word in SECRET_WORDS:
            if word in text_lower:
                return True

    # Rule 2: a very long number (card = 16 digits, Aadhaar = 12 digits).
    # Spaces and dashes inside a number do not break it.
    run = 0
    for ch in text:
        if ch.isdigit():
            run += 1
            if run >= 12:
                return True
        elif ch in " -":
            continue
        else:
            run = 0

    return False


SENSITIVE_WARNING = (
    "⚠️ Your message looks like it contains a private detail (OTP, PIN, CVV, "
    "password or a long card/account number). For your safety I did **not** send "
    "it to the AI. Please never share these with anyone - not even a bank "
    "employee. Remove the private part and ask again."
)


# ---------------------------------------------------------------------------
# 4. Structured output models (Pydantic, same idea as EduSage AI v2)
# ---------------------------------------------------------------------------
class BankingTerm(BaseModel):
    is_banking_term: bool = Field(
        description="True only if the input is a banking, payments or money term"
    )
    term: str
    category: Optional[str] = Field(
        default=None,
        description="One of: Payments, Cards, Accounts, Loans, Security, Other",
    )
    simple_meaning: str
    hindi_meaning: Optional[str] = None
    real_life_example: Optional[str] = None
    how_it_works: List[str] = Field(default_factory=list)
    safety_tip: Optional[str] = None
    related_terms: List[str] = Field(default_factory=list)


class ScamCheck(BaseModel):
    risk_level: str = Field(description="Exactly one of: Low, Medium, High")
    scam_type: Optional[str] = None
    red_flags: List[str] = Field(default_factory=list)
    explanation: str
    what_to_do: List[str] = Field(default_factory=list)


term_parser = PydanticOutputParser(pydantic_object=BankingTerm)
scam_parser = PydanticOutputParser(pydantic_object=ScamCheck)

term_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are BankSaathi AI, an assistant that explains Indian banking terms.

Explain the given term according to the provided schema.
Rules:
- If the input is not a banking / payments / money term, set is_banking_term to false
  and keep the other fields short or empty.
- Use very simple language. Write hindi_meaning in simple Hindi (Devanagari).
- Do not state exact fees, limits or interest rates; they vary by bank.
- Do not invent information.

{format_instructions}
"""),
    ("human", "Banking term: {term}")
])

scam_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are BankSaathi AI, an assistant that helps Indian users spot banking scams.

Read the message the user received (SMS, WhatsApp, email or call script) and check it
according to the provided schema.

Things that often signal a scam: urgency or threats ("account will be blocked today"),
requests for OTP / PIN / CVV / password, unknown links, "KYC update" or "reward" offers,
requests to install apps, a stranger asking you to send money, or a "refund" that needs
you to enter your PIN.

Rules:
- risk_level must be exactly Low, Medium or High.
- Explain in simple English and keep every point short.
- You cannot be 100% sure. Never say a message is definitely safe.
- Do not invent phone numbers or websites.
- In what_to_do, always include: do not click links, do not share OTP/PIN, and verify
  through the bank's official app, website or the number printed on the card.

{format_instructions}
"""),
    ("human", "Message to check:\n{message}")
])


def run_structured(model, prompt, parser, variables):
    """Fill the prompt -> call the model -> parse the answer into a Pydantic object."""
    final_prompt = prompt.invoke({
        **variables,
        "format_instructions": parser.get_format_instructions(),
    })
    response = model.invoke(final_prompt)
    return parser.parse(response.content)


# ---------------------------------------------------------------------------
# 5. Session state (Streamlit's memory between reruns)
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    # Only Human + AI messages are stored. The SystemMessage is added fresh
    # on every call, so sidebar changes (language / level) work immediately.
    st.session_state.history = []
if "pending" not in st.session_state:
    st.session_state.pending = None


def set_pending(question):
    st.session_state.pending = question


def clear_chat():
    st.session_state.history = []
    st.session_state.pending = None


# ---------------------------------------------------------------------------
# 6. Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image(LOGO_PATH, width="stretch")

    page = st.radio(
        "What do you want to do?",
        ["💬 Chat with BankSaathi", "📖 Banking Term Explainer", "🛡️ Scam Message Checker"],
    )

    st.divider()
    st.subheader("Chat settings")
    language_choice = st.selectbox(
        "Reply language",
        ["Auto (same as my question)", "Hindi", "Hinglish", "English"],
    )
    level_choice = st.radio("Explanation level", ["Simple", "Detailed"], horizontal=True)
    st.button("🗑️ Clear chat", on_click=clear_chat, width="stretch")

    st.divider()
    st.error(
        "**Never share** your OTP, UPI PIN, ATM PIN, password, CVV or full card "
        "number with anyone - including this chatbot."
    )
    st.caption(
        "BankSaathi AI is a learning project. It gives general information only, "
        "cannot access your bank account, and is not an official service of any bank."
    )



# ---------------------------------------------------------------------------
# 7. PAGE 1 - Chat
# ---------------------------------------------------------------------------
def show_chat_page():
    st.title("BankSaathi AI")
    st.caption("Banking guidance that speaks your language - Hindi, English or Hinglish.")

    # Show old messages
    for msg in st.session_state.history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # Welcome + example questions (only on an empty chat)
    if not st.session_state.history and not st.session_state.pending:
        st.info(
            "Namaste! 🙏 Ask me anything about everyday banking - UPI, ATM, cards, "
            "NEFT/RTGS/IMPS, statements and more."
        )
        st.write("**Try asking:**")
        columns = st.columns(2)
        for i, question in enumerate(EXAMPLE_QUESTIONS):
            columns[i % 2].button(
                question, key=f"example_{i}", on_click=set_pending,
                args=(question,), width="stretch",
            )

    # Get the question: from the chat box or from an example button
    user_input = st.chat_input("Ask your banking question...")
    if not user_input and st.session_state.pending:
        user_input = st.session_state.pending
    st.session_state.pending = None

    if not user_input:
        return

    # Privacy guard first - secrets never reach the model or the history
    if contains_sensitive_info(user_input):
        with st.chat_message("assistant"):
            st.warning(SENSITIVE_WARNING)
        return

    st.session_state.history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # SystemMessage + only the most recent messages (trimming memory)
    messages = [SystemMessage(content=build_system_prompt(language_choice, level_choice))]
    messages += st.session_state.history[-MAX_HISTORY_MESSAGES:]

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = get_chat_model().invoke(messages)
            answer = response.content
            if not answer or not answer.strip():
                raise ValueError("The model returned an empty answer. Please try again.")
        except Exception as e:
            st.session_state.history.pop()  # remove the question that failed
            st.error(f"Something went wrong: {e}")
            return
        st.markdown(answer)

    st.session_state.history.append(AIMessage(content=answer))


# ---------------------------------------------------------------------------
# 8. PAGE 2 - Banking Term Explainer
# ---------------------------------------------------------------------------
def show_term_page():
    st.title("📖 Banking Term Explainer")
    st.caption("Type any banking word and get a simple explanation in English + Hindi.")

    term = st.text_input("Banking term", placeholder="e.g. IFSC code, EMI, KYC, UPI, CIBIL score")

    if not st.button("Explain", type="primary", width="stretch"):
        return
    if not term.strip():
        st.warning("Please type a banking term first.")
        return

    try:
        with st.spinner("Explaining..."):
            data = run_structured(get_extract_model(), term_prompt, term_parser, {"term": term})
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        return

    if not data.is_banking_term:
        st.info("That doesn't look like a banking term. Try words like UPI, NEFT, EMI or KYC.")
        return

    st.divider()
    st.header(data.term)
    if data.category:
        st.caption(f"Category: {data.category}")

    st.subheader("In simple words")
    st.write(data.simple_meaning)

    if data.hindi_meaning:
        st.subheader("हिंदी में")
        st.write(data.hindi_meaning)

    if data.real_life_example:
        st.subheader("Example")
        st.write(data.real_life_example)

    if data.how_it_works:
        st.subheader("How it works")
        for number, step in enumerate(data.how_it_works, start=1):
            st.write(f"{number}. {step}")

    if data.safety_tip:
        st.warning(f"🔒 **Safety tip:** {data.safety_tip}")

    if data.related_terms:
        st.subheader("Related terms")
        st.write(" ".join(f"`{t}`" for t in data.related_terms))

    with st.expander("Raw JSON"):
        st.code(data.model_dump_json(indent=4), language="json")


# ---------------------------------------------------------------------------
# 9. PAGE 3 - Scam Message Checker
# ---------------------------------------------------------------------------
def show_scam_page():
    st.title("🛡️ Scam Message Checker")
    st.caption("Got a suspicious SMS, WhatsApp or email? Paste it here to check for warning signs.")
    st.info(
        "Before pasting, replace any OTP, PIN, card number or account number with XXXX."
    )

    message = st.text_area(
        "Message you received", height=200,
        placeholder="e.g. Dear customer, your account will be blocked today. Update KYC at http://...",
    )

    if not st.button("Check message", type="primary", width="stretch"):
        return
    if not message.strip():
        st.warning("Please paste a message first.")
        return
    if contains_sensitive_info(message):
        st.warning(SENSITIVE_WARNING)
        return

    try:
        with st.spinner("Checking..."):
            data = run_structured(get_extract_model(), scam_prompt, scam_parser, {"message": message})
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        return

    st.divider()
    risk = data.risk_level.strip().lower()
    if risk == "high":
        st.error("🚨 **HIGH RISK** - this looks like a scam. Do not respond.")
    elif risk == "medium":
        st.warning("⚠️ **MEDIUM RISK** - be careful and verify before doing anything.")
    else:
        st.success("🟢 **LOW RISK** - no strong warning signs found, but still stay careful.")

    if data.scam_type:
        st.write(f"**Possible scam type:** {data.scam_type}")

    st.subheader("Why")
    st.write(data.explanation)

    if data.red_flags:
        st.subheader("Red flags")
        for flag in data.red_flags:
            st.write(f"- 🚩 {flag}")

    if data.what_to_do:
        st.subheader("What you should do")
        for action in data.what_to_do:
            st.write(f"- ✅ {action}")

    st.caption(
        "This is an AI estimate, not a guarantee. If you lost money or shared your details, "
        "call your bank immediately and report on the National Cyber Crime Helpline **1930** "
        "or cybercrime.gov.in."
    )


# ---------------------------------------------------------------------------
# 10. Show the selected page
# ---------------------------------------------------------------------------
if page.startswith("💬"):
    show_chat_page()
elif page.startswith("📖"):
    show_term_page()
else:
    show_scam_page()

