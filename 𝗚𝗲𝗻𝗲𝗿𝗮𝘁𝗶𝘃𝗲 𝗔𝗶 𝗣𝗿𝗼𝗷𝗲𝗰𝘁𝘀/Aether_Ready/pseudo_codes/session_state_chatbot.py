
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

st.title("My AI Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask anything...")

if user_input:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Convert stored history into LangChain messages
    chat_history = []

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            chat_history.append(
                HumanMessage(content=msg["content"])
            )

        elif msg["role"] == "assistant":
            chat_history.append(
                AIMessage(content=msg["content"])
            )

    # Generate context-aware AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            response = llm.invoke(chat_history)

        st.write(response.content)

    # Store AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })
