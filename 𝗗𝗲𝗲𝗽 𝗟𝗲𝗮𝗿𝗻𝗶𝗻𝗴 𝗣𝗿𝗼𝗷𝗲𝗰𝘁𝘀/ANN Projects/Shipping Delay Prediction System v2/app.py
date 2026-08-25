import streamlit as st
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import joblib

# ---------------------------------------------------------
# 1. LOAD ALL SAVED ARTIFACTS
# These were saved in the notebook after training:
#   - shipsense_model.pth   -> trained model weights
#   - scaler.pkl            -> StandardScaler fitted on training data
#   - encoder.pkl           -> OrdinalEncoder fitted on categorical columns
#   - feature_order.pkl     -> exact column order the model expects
#   - categorical_columns.pkl / numerical_columns.pkl
#   - best_hyperparameters.pkl -> hidden layer sizes found by Optuna
# ---------------------------------------------------------

scaler = joblib.load("models/scaler.pkl")
encoder = joblib.load("models/encoder.pkl")
feature_order = joblib.load("models/feature_order.pkl")
categorical_columns = joblib.load("models/categorical_columns.pkl")
numerical_columns = joblib.load("models/numerical_columns.pkl")
best_params = joblib.load("models/best_hyperparameters.pkl")


# ---------------------------------------------------------
# 2. REBUILD THE MODEL ARCHITECTURE
# We have to define the exact same class used during training,
# then load the saved weights into it. Only the weights (.pth)
# are saved, not the architecture itself.
# ---------------------------------------------------------
class ShipSenseModel(nn.Module):
    def __init__(self, input_features, hidden1, hidden2, hidden3, dropout):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_features, hidden1),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden2, hidden3),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden3, 1)
        )

    def forward(self, x):
        return self.network(x)


model = ShipSenseModel(
    input_features=len(feature_order),
    hidden1=best_params["hidden1"],
    hidden2=best_params["hidden2"],
    hidden3=best_params["hidden3"],
    dropout=best_params["dropout"]
)
model.load_state_dict(torch.load("models/shipsense_model.pth", map_location="cpu"))
model.eval()  # inference mode -> disables dropout


# ---------------------------------------------------------
# 3. GET DROPDOWN OPTIONS DIRECTLY FROM THE ENCODER
# encoder.categories_ stores the exact categories it saw during
# training, in the same order as `categorical_columns`.
# ---------------------------------------------------------
category_options = {
    col: list(cats) for col, cats in zip(categorical_columns, encoder.categories_)
}


# ---------------------------------------------------------
# 4. STREAMLIT UI
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
# 5. PREDICTION LOGIC (runs only after form submit)
# ---------------------------------------------------------
if submitted:

    # Build one-row dataframe with the SAME columns/order the model was trained on
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
    input_df = input_df[feature_order]  # enforce exact training column order

    # Step 1: encode categorical columns with the SAME fitted encoder
    input_df[categorical_columns] = encoder.transform(input_df[categorical_columns])

    # Step 2: scale ALL columns with the SAME fitted scaler
    # (scaler was fit on the full feature set after encoding, not just numeric cols)
    scaled_input = scaler.transform(input_df)

    # Step 3: convert to tensor and run through the model
    input_tensor = torch.tensor(scaled_input, dtype=torch.float32)

    with torch.no_grad():
        logit = model(input_tensor)
        probability = torch.sigmoid(logit).item()

    prediction = "Late Delivery Risk" if probability >= 0.5 else "No Delay Risk"

    st.subheader("Result")
    st.write(f"**Prediction:** {prediction}")
    st.write(f"**Probability of Late Delivery:** {probability:.2%}")
    st.progress(probability)