import streamlit as st

# Initialize
if "count" not in st.session_state:
    st.session_state.count = 0

# Increment
if st.button("Increase"):
    st.session_state.count += 1

# Decrement
if st.button("Decrease"):
    st.session_state.count -= 1

# Reset
if st.button("Reset"):
    st.session_state.count = 0

# Display
st.write("Current Count:", st.session_state.count)