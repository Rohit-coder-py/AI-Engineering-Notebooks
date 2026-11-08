# import streamlit as st
# 
# count = 0
# 
# if st.button("Click Me"):
#     count += 1
# 
# st.write(count)


import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Click Me"):
    st.session_state.count += 1

st.write(st.session_state.count)



###

# Initialize a variable
st.session_state.name = "Rohit"

# Access a variable
print(st.session_state.name)

# Update a variable
st.session_state.name = "Harsh"

# Dictionary-style access
st.session_state["name"]

# Check whether a variable exists
if "name" not in st.session_state:
    st.session_state.name = "Rohit"
    
    
    
# #===================Chat

import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])