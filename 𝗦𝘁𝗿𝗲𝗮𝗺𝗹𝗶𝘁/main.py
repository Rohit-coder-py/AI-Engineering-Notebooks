import streamlit as st

st.title("First Streamlit app")


st.title("Hello Chai App")
st.subheader("Brewed with streamlit")
st.text("Welcome to your first interative app")
st.write("Chooose your fav. variety of chai")

chai = st.selectbox("Your fav chai: ", ["Masala chai","Lemon Tea", "Adrak Chai", "Kesar Chai"])


st.write("You selected",chai)


st.success(f"Your {chai} has been already brewed")