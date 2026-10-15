import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

modes = {
    1: ("Professional", "You are a professional, friendly, and helpful AI assistant. Answer questions clearly, accurately, and respectfully. Use simple language and examples when helpful. Be polite, patient, and solution-oriented. Admit when you don't know something. Never insult or criticize the user."),
    2: ("Angry", "You are an angry AI agent. Respond aggressively and impatiently, but do not threaten or genuinely abuse the user."),
    3: ("Funny", "You are a very funny AI agent. Respond with humor, jokes, and witty remarks whenever appropriate."),
    4: ("Sad", "You are a sad AI agent. Respond in a melancholic, emotional, and thoughtful tone."),
    5: ("Motivational", "You are a motivational AI agent. Inspire the user with positive energy, encouragement, and practical advice."),
    6: ("Friendly", "You are a warm, friendly AI companion. Speak casually and make the user feel comfortable."),
    7: ("Teacher", "You are an expert teacher. Explain concepts step by step using simple language, examples, and clear explanations."),
    8: ("Coder", "You are an expert programming assistant. Write clean, correct, efficient code and explain errors and solutions clearly."),
    9: ("Scientist", "You are a scientific assistant. Explain topics using evidence, logical reasoning, and accurate scientific concepts."),
    10: ("Formal", "You are a formal AI assistant. Use professional language, structured answers, and a respectful tone."),
    11: ("Sarcastic", "You are a sarcastic AI agent. Use clever, playful sarcasm without being genuinely cruel or insulting."),
    12: ("Philosopher", "You are a philosophical AI assistant. Explore ideas deeply, ask thoughtful questions, and explain different perspectives."),
}


@st.cache_resource
def get_model():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
    )


model = get_model()

# ---------- Session state ----------
if "choice" not in st.session_state:
    st.session_state.choice = 1
    st.session_state.messages = [SystemMessage(content=modes[1][1])]
if "ended" not in st.session_state:
    st.session_state.ended = False
if "notice" not in st.session_state:
    st.session_state.notice = None

# ---------- Sidebar: mode selection ----------
with st.sidebar:
    st.header("Choose your AI mode")
    selected = st.radio(
        "Mode",
        options=list(modes.keys()),
        index=list(modes.keys()).index(st.session_state.choice),
        format_func=lambda n: f"{n}. {modes[n][0]}",
        label_visibility="collapsed",
        disabled=st.session_state.ended,
    )

    # Same behaviour as original: switching mode starts a fresh message list
    if selected != st.session_state.choice:
        st.session_state.choice = selected
        st.session_state.messages = [SystemMessage(content=modes[selected][1])]
        st.session_state.notice = f"{modes[selected][0]} mode activated!"
        st.rerun()

mode_name = modes[st.session_state.choice][0]

# ---------- Header ----------
st.title("🤖 AI Chatbot")
st.caption(f"{mode_name} mode  •  Type 'mode' to change mode or 'exit' to stop")

if st.session_state.notice:
    st.success(st.session_state.notice)
    st.session_state.notice = None

# ---------- Chat history ----------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content.replace("*", ""))

# ---------- Input ----------
if st.session_state.ended:
    st.info("Chat ended. Refresh the page to start a new chat.")
    st.chat_input("Chat ended", disabled=True)
else:
    user_input = st.chat_input("You: ")

    if user_input:
        if user_input.lower() == "exit":
            st.session_state.ended = True
            print(st.session_state.messages)
            st.rerun()

        elif user_input.lower() == "mode":
            st.session_state.notice = "Pick a mode from the sidebar on the left."
            st.rerun()

        else:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = model.invoke(st.session_state.messages)
                st.markdown(response.content.replace("*", ""))

            st.session_state.messages.append(AIMessage(content=response.content))