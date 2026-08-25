# ---------------------------------------------------------
# app.py - main


import streamlit as st
import pandas as pd
import torch

from src.preprocessing import scaler, encoder, feature_order, categorical_columns
from src.inference import model


category_options = {}
for col, cats in zip(categorical_columns, encoder.categories_):
    category_options[col] = list(cats)
    
    
print(category_options)


# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.title("ShipSense — Late Delivery Risk Predictor")
st.write("Enter shipment details below to predict the risk of a late delivery.")

with st.form("prediction_form"):
    st.subheader("Order Details")
    Type = st.selectbox("Payment Type", category_options["Type"])
    Shipping_Mode = st.selectbox("Shipping Mode", category_options["Shipping Mode"])
    Days_scheduled = st.slider("Days for Shipment (Scheduled)", 0, 4, 3)
    Order_Item_Quantity = st.slider("Order Item Quantity", 1, 5, 2)

    st.subheader("Product / Category")
    Category_Name = st.selectbox("Category Name", category_options["Category Name"])
    Department_Name = st.selectbox("Department Name", category_options["Department Name"])
    Product_Price = st.number_input("Product Price ($)", value=141.0)
    Order_Item_Product_Price = st.number_input("Order Item Product Price ($)", value=141.0)
    Sales = st.number_input("Sales ($)", value=203.0)

    st.subheader("Discount & Profit")
    Order_Item_Discount = st.number_input("Order Item Discount ($)", value=20.0)
    Order_Item_Discount_Rate = st.slider("Order Item Discount Rate", 0.0, 0.25, 0.10)
    Order_Item_Profit_Ratio = st.number_input("Order Item Profit Ratio", value=0.12)
    Benefit_per_order = st.number_input("Benefit per Order ($)", value=22.0)
    Sales_per_customer = st.number_input("Sales per Customer ($)", value=183.0)
    Order_Item_Total = st.number_input("Order Item Total ($)", value=183.0)
    Order_Profit_Per_Order = st.number_input("Order Profit Per Order ($)", value=22.0)

    st.subheader("Customer Info")
    Customer_Segment = st.selectbox("Customer Segment", category_options["Customer Segment"])
    Customer_Country = st.selectbox("Customer Country", category_options["Customer Country"])
    Customer_State = st.selectbox("Customer State", sorted(category_options["Customer State"]))
    Customer_City = st.selectbox("Customer City", sorted(category_options["Customer City"]))

    st.subheader("Order Location")
    Market = st.selectbox("Market", category_options["Market"])
    Order_Region = st.selectbox("Order Region", category_options["Order Region"])
    Order_Country = st.selectbox("Order Country", sorted(category_options["Order Country"]))
    Order_State = st.selectbox("Order State", sorted(category_options["Order State"]))
    Order_City = st.selectbox("Order City", sorted(category_options["Order City"]))
    Latitude = st.number_input("Latitude", value=29.7, format="%.4f")
    Longitude = st.number_input("Longitude", value=-84.9, format="%.4f")

    submitted = st.form_submit_button("Predict")


# ---------------------------------------------------------
# Runs only after the user clicks Predict. Nothing here is
# wrapped in a function -- it's the same encode -> scale -> predict
# sequence the notebook used, just done for one row instead of
# a whole DataFrame.
# ---------------------------------------------------------
if submitted:

    # Step 0: put the form values into one row, in the exact
    # column order the model was trained on
    input_dict = {
        "Type": Type,
        "Days for shipment (scheduled)": Days_scheduled,
        "Benefit per order": Benefit_per_order,
        "Sales per customer": Sales_per_customer,
        "Category Name": Category_Name,
        "Customer City": Customer_City,
        "Customer Country": Customer_Country,
        "Customer Segment": Customer_Segment,
        "Customer State": Customer_State,
        "Department Name": Department_Name,
        "Latitude": Latitude,
        "Longitude": Longitude,
        "Market": Market,
        "Order City": Order_City,
        "Order Country": Order_Country,
        "Order Item Discount": Order_Item_Discount,
        "Order Item Discount Rate": Order_Item_Discount_Rate,
        "Order Item Product Price": Order_Item_Product_Price,
        "Order Item Profit Ratio": Order_Item_Profit_Ratio,
        "Order Item Quantity": Order_Item_Quantity,
        "Sales": Sales,
        "Order Item Total": Order_Item_Total,
        "Order Profit Per Order": Order_Profit_Per_Order,
        "Order Region": Order_Region,
        "Order State": Order_State,
        "Product Price": Product_Price,
        "Shipping Mode": Shipping_Mode,
    }

    input_df = pd.DataFrame([input_dict])
    input_df = input_df[feature_order]

    # Step 1: encode categorical columns with the already-fitted encoder
    input_df[categorical_columns] = encoder.transform(input_df[categorical_columns])

    # Step 2: scale the full row with the already-fitted scaler
    scaled_input = scaler.transform(input_df)

    # Step 3: tensor + forward pass through the model
    input_tensor = torch.tensor(scaled_input, dtype=torch.float32)

    with torch.no_grad():
        logit = model(input_tensor)
        probability = torch.sigmoid(logit).item()

    prediction = "Late Delivery Risk" if probability >= 0.5 else "No Delay Risk"

    st.subheader("Result")
    st.write(f"**Prediction:** {prediction}")
    st.write(f"**Probability of Late Delivery:** {probability:.2%}")
    st.progress(probability)