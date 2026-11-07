import streamlit as st


st.header("File+Text Uploader :")

user_input = st.chat_input(
    "Ask something or upload a file...",
    accept_file=True
)

if user_input:
    prompt = user_input.text
    files = user_input.files

    st.write("Prompt:", prompt)

    for file in files:
        st.write("Filename:", file.name)