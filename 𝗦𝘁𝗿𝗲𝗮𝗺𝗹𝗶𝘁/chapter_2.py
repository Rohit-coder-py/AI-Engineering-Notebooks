import streamlit as st

st.title("Chai Maker App")

if st.button("Make Chai"):
    st.success("Your chai is being brewed ☕")

add_masala = st.checkbox("Add Masala")
add_milk = st.checkbox("Add Milk")
add_sugar = st.checkbox("Add Sugar")

if add_masala:
    st.success("🌿 Masala added to your chai.")

if add_milk:
    st.success("🥛 Milk added to your chai.")

if add_sugar:
    st.success("🍬 Sugar added to your chai.")
    
    
    
#radio button
    
    
tea_type = st.radio("Choose your chai base ingredients :",['Milk','Tea Leaves','Sugar'])


st.write(f"Select base {tea_type}")


flavour = st. selectbox("Choose flavour: ", ["Adrak","Kesar", "Tulsi"])



sugar_level = st.slider("Sugar level", 0,5,10)



#inputs


chai_cups = st.number_input("How many cups", min_value=1 , max_value=10,step = 1)
st.write(f"Selected cups {chai_cups}")




name = st.text_input("Enter your name")
if name:
    st.write(f"Welcome, {name} ! Your chai is on the way")
    
    
    
    
dob = st.date_input("Select your DOB:")
st.write(f"Welcome, {name} ! Your dob is {dob}")


# completed
