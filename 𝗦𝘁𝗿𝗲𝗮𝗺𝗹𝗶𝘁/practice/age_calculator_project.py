import streamlit as st
import math 

st.title("Calculate your age Here")

dob = st.number_input("Please select your Date Of Birth (DOB) here : ", min_value=1 , max_value=10000,step = 1)

st.write(f"You selected {dob}")

cur = st.number_input("Enter current year : ",min_value=1920 , max_value=10000,step = 1)

st.write(f"You selected {cur}")
if cur:
    st.success("Calculating...........")

if cur:
    st.write(f"You are currently {math.trunc(abs(cur-dob))} years old ")

    st.success("Thanks for using our program.")
