#01_basics


import streamlit as st

st.title("My AI Application")

st.sidebar.title("Settings")
st.sidebar.write("Configure your app here.")

name = st.sidebar.text_input("Enter your name")

if name:
    st.write(f"Welcome, {name}!")



#02_Add different widgets
    

import streamlit as st

st.title("AI Model Configuration")

st.sidebar.header("Model Settings")

model = st.sidebar.selectbox(
    "Choose an LLM",
    ["Llama", "GPT", "Gemini"]
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7
)

debug_mode = st.sidebar.checkbox("Enable debug mode")

st.subheader("Current Configuration")

st.write("Selected model:", model)
st.write("Temperature:", temperature)
st.write("Debug mode:", debug_mode)



# 03_ Build a navigation sidebar
import streamlit as st

st.sidebar.title("AI Dashboard")

page = st.sidebar.radio("Navigate",["Home", "Chatbot", "Documents", "Settings"])

if page == "Home":
    st.title("Home")
    st.write("Welcome to your AI dashboard.")

elif page == "Chatbot":
    st.title("AI Chatbot")
    st.write("Chat with your AI model here.")

elif page == "Documents":
    st.title("Document Manager")
    st.write("Upload and manage your documents.")

elif page == "Settings":
    st.title("Settings")
    st.write("Configure your application.")
