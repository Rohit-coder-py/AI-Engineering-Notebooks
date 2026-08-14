import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("#####  Social Media Addiction Dashboard")

st.subheader("File Upload")
#goal : To learn how to work with Datasets

file = st. file_uploader("UPload your csv file", type=["csv"])

if file:
    df = pd. read_csv(file)
    st.subheader("Data Preview")
    st.dataframe(df)

if file:
    st.subheader("Summary Stats")
    st.write(df.describe())

if file:
    name = df["Name"].unique()
    selected_name = st.selectbox("Filter by names", name)
    filtered_data = df[df["Name"] == selected_name]
    st.dataframe(filtered_data)


#we can also plot graphs using matplotlib
    
#completed