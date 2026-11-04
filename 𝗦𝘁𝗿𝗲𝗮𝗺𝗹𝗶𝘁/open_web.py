import streamlit as st
import webbrowser

if "opened" not in st.session_state:
    webbrowser.open("https://console.groq.com/")
    st.session_state.opened = True

st.title("My AI Application")