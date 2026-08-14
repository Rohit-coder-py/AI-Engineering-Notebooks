import streamlit as st

st.title("First Streamlit app")


st.title("Hello Chai App")
st.subheader("Brewed with streamlit")
st.text("Welcome to your first interactive app")
st.write("Chooose your fav. variety of chai")

chai = st.selectbox("Your fav chai: ", ["Masala chai","Lemon Tea", "Adrak Chai", "Kesar Chai",'Milk Tea'])


st.write("You selected",chai)


st.success(f"Your {chai} has been already brewed")


st.info("Chai is getting ready ")