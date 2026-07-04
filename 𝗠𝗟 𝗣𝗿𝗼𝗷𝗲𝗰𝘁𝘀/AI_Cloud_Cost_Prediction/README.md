# AI Cloud Cost Prediction using Machine Learning

Predicts Azure billing cost (`CostInBillingCurrency`) for a given service line item using a Linear Regression model, deployed as a Streamlit app.

## Results

| Metric | Value |
|---|---|
| MAE | 0.1058 |
| RMSE | 0.3068 |
| R² | 0.459 |

(See `notebooks/01_Cloud_Cost_Prediction.ipynb` for full EDA and derivation.)

## Project structure

```
AI Cloud Cost Prediction
│
├── data
│   └── anonymized_costs.csv
│
├── notebooks
│   └── 01_Cloud_Cost_Prediction.ipynb
│
├── models
│   ├── linear_regression_pipeline.pkl   # preprocessing + scaler + encoders + model, bundled
│   ├── feature_schema.pkl               # required input columns, in order
│   └── category_options.pkl             # valid category values (populates the app's dropdowns)
│
├── images                                # exported EDA charts
├── app.py
├── requirements.txt
└── README.md
```

## Design decision: one bundled pipeline instead of separate scaler/encoder files

The original plan called for saving the Linear Regression model and `StandardScaler` separately. Instead, preprocessing (scaling + one-hot encoding + ordinal encoding) and the model are combined into a single `sklearn.pipeline.Pipeline`, saved as one `.pkl`. This removes an entire class of bugs where the app's manual encoding/column-order logic drifts out of sync with what the model was trained on — the app calls `pipeline.predict(df)` and the same transform always runs.

## Feature handling

- **Dropped** (pure identifiers, no predictive signal): `InvoiceSectionName`, `SubscriptionName`, `ResourceGroup`, `ResourceName`
- **One-hot encoded**: `MeterCategory`, `ConsumedService`, `ResourceLocation`
- **Ordinal encoded** (high cardinality — one-hot would explode dimensionality): `MeterSubCategory`, `MeterName`
- **Engineered from `Date`**: `Year`, `Month`, `Day`, `Weekday`

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Known limitation / next step

Cost data is heavily right-skewed and non-linear (a small number of services dominate spend). Linear Regression is a reasonable, interpretable baseline; a v2 would compare Random Forest / Gradient Boosting regressors, which should fit the non-linear cost tail better.
