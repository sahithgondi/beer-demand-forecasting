import sys
import os
import glob
import pandas as pd
import streamlit as st

# thsi will allow imports from src/ no matter where streamlit is launched from
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features.build_features import build_all_features
from src.models.predict import load_model, predict

# page config
st.set_page_config(page_title="Beer Ordering Prediction", layout="wide")
st.title("Beer Ordering Prediction")

# data loading
@st.cache_data
def load_data():
    # try running from project root first streamlit run app/app.py
    for path in ["data/processed/weekly_orders_clean.csv", "../data/processed/weekly_orders_clean.csv"]:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["date"] = pd.to_datetime(df["date"])
            return build_all_features(df)
    raise FileNotFoundError("Could not find weekly_orders_clean.csv. Run the pipeline first.")

def find_latest_model():
    # finds the most recently saved pkl inside models/
    for base in ["models", "../models"]:
        pkls = glob.glob(os.path.join(base, "linear_regression_*.pkl"))
        if pkls:
            return max(pkls, key=os.path.getmtime)
    return None

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ {e}")
    st.stop()

FEATURES = ["lag_1", "lag_2", "lag_4", "rolling_mean_4", "rolling_std_4", "week", "month", "quarter"]

# load model
model_path = find_latest_model()
if model_path:
    model = load_model(model_path)
else:
    st.warning("No trained model found. Run `python src/pipeline/run_pipeline.py` first.")
    model = None

# tabs
tab_owner, tab_analytics = st.tabs(["Weekly Order Guide", "Analytics"])

# tab 1 owner view - ordering table
with tab_owner:
    st.header("Weekly Order Recommendations")
    st.markdown("The table below shows what to order this week for each beer SKU based on the latest model run.")

    if model:
        # get the latest available row per SKU (most recent week)
        latest_rows = df.sort_values("date").groupby("item_name").tail(1).reset_index(drop=True)

        X_latest = latest_rows[FEATURES]
        preds = predict(model, X_latest)

        order_table = pd.DataFrame({
            "Beer": latest_rows["item_name"].values,
            "Last Week's Orders (cases)": latest_rows["quantity_clean"].values.astype(int),
            "Recommended Order (cases)": preds.round(0).astype(int),
        })

        # sort by recommended order desc so high volume SKUs bubble to the top
        order_table = order_table.sort_values("Recommended Order (cases)", ascending=False).reset_index(drop=True)

        st.dataframe(order_table, use_container_width=True)

        st.info(f"Predictions made using model: `{os.path.basename(model_path)}`")
    else:
        st.error("No model loaded — cannot generate recommendations.")


# tab 2 analytics view
with tab_analytics:
    st.header("SKU Demand Explorer")
    st.markdown("Coming soon: Time-series charts and prediction overlays per individual SKU.")
