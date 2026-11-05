
import streamlit as st
from langchain_ollama import ChatOllama

# Page configuration
st.set_page_config(
    page_title="Qwen AI Chatbot",
    page_icon="🤖"
)

st.title("Qwen AI Chatbot")
st.caption("Powered by Ollama + Qwen3 0.6B")

# Initialize local LLM
llm = ChatOllama(
    model="qwen3:0.6b",
    temperature=0.7
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask anything..."):

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(
                st.session_state.messages
            )
            answer = response.content
            st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
