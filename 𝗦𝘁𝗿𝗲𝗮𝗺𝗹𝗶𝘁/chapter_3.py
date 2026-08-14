import streamlit as st 

#goal : To learn how to learn layouts using streamlit
st.header("Hello")
st.title("Chai Taste Poll")
col_1 , col_2 = st.columns(2)

with col_1:
    st.header("Masala Chai")
    vote1 = st.button("Vote for Masala Chai ")
with col_2:
    st.header("Milk Chai")
    vote2 = st.button("Vote for Milk Chai ")
    st.image(r"C:\Users\shobh\OneDrive\Attachments\Pictures\Screenshots 1\Screenshot 2026-08-14 110615.png",width = 600)
    
if vote1:
    st.success("Thanks for voting Masala Chai")
if vote2:
    st.success("Thanks for voting Milk Chai")