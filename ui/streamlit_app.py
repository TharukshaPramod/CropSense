# ui/streamlit_app.py
import streamlit as st
import requests, os, json
st.set_page_config(page_title="CropSense Demo", layout="wide")
st.title("CropSense — Crop Yield Prediction")

col1, col2 = st.columns([2,1])

with col1:
    st.header("Upload or select dataset")
    uploaded = st.file_uploader("Upload CSV (optional)", type="csv")
    if st.button("Use sample / collect raw and preprocess"):
        try:
            r = requests.post("http://localhost:8001/collect", json={"source":"local"}, timeout=10)
            st.write("Collector:", r.json())
            r2 = requests.post("http://localhost:8002/preprocess", json={}, timeout=120)
            st.write("Preprocessor:", r2.json())
            st.success("Preprocessing complete")
        except Exception as e:
            st.error("Ensure collector and preprocessor are running. " + str(e))

    st.subheader("Manual single prediction")
    rainfall = st.number_input("Rainfall (mm)", value=800.0)
    temp = st.number_input("Temperature (C)", value=22.0)
    area = st.number_input("Area (ha)", value=100.0)
    fert = st.selectbox("Fertilizer used", [True, False])
    irr = st.selectbox("Irrigation used", [True, False])
    crop = st.selectbox("Crop", ["Wheat", "Rice", "Soybean", "Barley", "Cotton"])
    if st.button("Predict & Explain"):
        payload = {
            "Region": "Demo",
            "Soil_Type": "Sandy",
            "Crop": crop,
            "Rainfall_mm": rainfall,
            "Temperature_Celsius": temp,
            "Fertilizer_Used": fert,
            "Irrigation_Used": irr,
            "Weather_Condition": "Sunny",
            "Days_to_Harvest": 120
        }
        headers = {}
        # If you have login implemented, set token in env or ask user to paste
        token = st.text_input("JWT token (optional)", "")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            pr = requests.post("http://localhost:8003/predict", json=payload, headers=headers, timeout=10)
            if pr.status_code != 200:
                st.error(f"Predict failed: {pr.text}")
            else:
                out = pr.json()
                st.success(f"Predicted yield: {out['predicted_yield']:.3f} t/ha")
                ex = requests.post("http://localhost:8004/explain", json=payload, headers=headers, timeout=20)
                if ex.status_code == 200:
                    e = ex.json()
                    st.subheader("Explanation")
                    st.write(e.get("summary"))
                    st.write("Top features:", e.get("top_features"))
                else:
                    st.warning("Explain failed: " + ex.text)
        except Exception as e:
            st.error("Error calling services: " + str(e))
