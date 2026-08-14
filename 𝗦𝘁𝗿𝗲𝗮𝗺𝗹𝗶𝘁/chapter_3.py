import streamlit as st 

#goal : To learn how to learn layouts using streamlit
st.header("Hello")
st.title("Chai Taste Poll")
col_1 , col_2 = st.columns(2)

with col_1:
    st.header("Masala Chai")
    vote1 = st.button("Vote for Masala Chai ")
    st.image(r"C:\Users\shobh\OneDrive\Attachments\Pictures\Screenshots 1\Screenshot 2026-08-14 110746.png",width = 600)
with col_2:
    st.header("Milk Chai")
    vote2 = st.button("Vote for Milk Chai ")
    st.image(r"C:\Users\shobh\OneDrive\Attachments\Pictures\Screenshots 1\Screenshot 2026-08-14 110615.png",width = 600)
    
if vote1:
    st.success("Thanks for voting Masala Chai")
if vote2:
    st.success("Thanks for voting Milk Chai")
    
    
    
name = st.sidebar.text_input("Enter your name :")

tea = st.sidebar.selectbox("Choose your chai", ["Masala","kesar", "Adrak"])

st.write(f"Welcome {name} and your chai is {tea}")


with st.expander("Show Chai Making INstructions"):
    st.write("""
    1. Boil water with tea leaves
    2. Add milk and spices
    3. Serve hot""")
    
    
    
    
    
    
    
    
#markdown cells
    
    
st.markdown(f"### Wait , {name} for your {tea} chai pateintly")
st.markdown(' > Patience is the key to success')


## completed
