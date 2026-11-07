import streamlit as st

count = 0

if st.button("Click Me"):
    count += 1

st.write(count)