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
    
if vote1:
    print("shio")