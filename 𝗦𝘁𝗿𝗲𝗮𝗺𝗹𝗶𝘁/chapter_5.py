import streamlit as st

st.header("hello")

#goal : how to work with api's and handle requests

import requests

st.title("Live currency converter")
amount = st. number_input("Enter the amount in INR",min_value=1)
st.write(f"You selected INR {amount}")

target_currency = st.selectbox("Convert to:", ["USD", "EUR","GBP", "JPY"])

st.write(f"Converting INR {amount} into {target_currency}")


if st.button("Convert"):
    url  = r"https://api.exchangerate-api.com/v4/latest/INR"
    res = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        rate = data["rates"][target_currency]
        converted = rate*amount
        
        st.success(f"{amount} INR = {converted} {target_currency}")
        
    else:
        st.error("Failed to fetch conversion rate")
        
    

#completed
        
#streamlit completed
        