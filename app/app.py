import streamlit as st
from run_pipeline import your_function  # reuse your pipeline

st.title("Beer Demand Forecast")

if st.button("Run Prediction"):
    result = your_function()
    st.write(result)

