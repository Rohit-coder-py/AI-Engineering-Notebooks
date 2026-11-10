import streamlit as st

st.write("Enter a number to generate its multiplication table.")

number = st.number_input("Enter a number:",min_value=1,)

if st.button("Generate Table"):
    st.subheader(f"Multiplication Table of {number}")

    for i in range(1, 11):
        st.write(f"{number} × {i} = {number * i}")
