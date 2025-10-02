"""
CropSense Dashboard - Main overview page
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    check_service_health, collect_data, preprocess_data, train_model,
    predict_yield, explain_prediction, create_metrics_dashboard,
    create_feature_importance_chart, create_yield_distribution_chart
)

st.set_page_config(
    page_title="CropSense Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 CropSense Dashboard")
st.markdown("Welcome to your AI-powered crop yield prediction system!")

# Sidebar for quick actions
with st.sidebar:
    st.header("🚀 Quick Actions")
    
    if st.button("🔄 Refresh All Services", type="primary"):
        st.rerun()
    
    if st.button("📊 Run Full Pipeline"):
        with st.spinner("Running full pipeline..."):
            # Collect data
            success, msg = collect_data()
            if success:
                st.success("✅ Data collected")
                # Preprocess
                success, msg = preprocess_data()
                if success:
                    st.success("✅ Data preprocessed")
                    # Train model
                    success, metrics = train_model()
                    if success:
                        st.success("✅ Model trained")
                        st.session_state.training_metrics = metrics
                    else:
                        st.error(f"❌ Training failed: {metrics.get('error', 'Unknown error')}")
                else:
                    st.error(f"❌ Preprocessing failed: {msg}")
            else:
                st.error(f"❌ Collection failed: {msg}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 System Overview")
    
    # Service health status
    st.subheader("🔧 Service Status")
    health_status = check_service_health()
    
    health_cols = st.columns(len(health_status))
    for i, (service, status) in enumerate(health_status.items()):
        with health_cols[i]:
            if status:
                st.success(f"✅ {service}")
            else:
                st.error(f"❌ {service}")
    
    # Pipeline status
    st.subheader("🔄 Pipeline Status")
    
    pipeline_cols = st.columns(4)
    with pipeline_cols[0]:
        st.metric("Data Collection", "Ready", "✅")
    with pipeline_cols[1]:
        st.metric("Preprocessing", "Ready", "✅")
    with pipeline_cols[2]:
        st.metric("Model Training", "Ready", "✅")
    with pipeline_cols[3]:
        st.metric("Prediction", "Ready", "✅")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    # Sample activity data
    activity_data = pd.DataFrame({
        "Time": [datetime.now() - timedelta(hours=i) for i in range(5, 0, -1)],
        "Activity": ["Model Training", "Data Collection", "Prediction", "Data Preprocessing", "System Startup"],
        "Status": ["Success", "Success", "Success", "Success", "Success"]
    })
    
    st.dataframe(activity_data, use_container_width=True)

with col2:
    st.header("🎯 Quick Predict")
    
    # Simple prediction form
    with st.form("quick_predict"):
        st.subheader("Enter Parameters")
        
        region = st.selectbox("Region", ["West", "East", "North", "South"])
        soil_type = st.selectbox("Soil Type", ["Sandy", "Loam", "Clay", "Silt"])
        crop = st.selectbox("Crop", ["Wheat", "Rice", "Soybean", "Barley"])
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=2000.0, value=800.0)
        temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
        fertilizer = st.checkbox("Fertilizer Used", value=True)
        irrigation = st.checkbox("Irrigation Used", value=True)
        weather = st.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy", "Stormy"])
        days_to_harvest = st.number_input("Days to Harvest", min_value=30, max_value=365, value=120)
        
        submitted = st.form_submit_button("🔮 Predict Yield", type="primary")
        
        if submitted:
            payload = {
                "Region": region,
                "Soil_Type": soil_type,
                "Crop": crop,
                "Rainfall_mm": rainfall,
                "Temperature_Celsius": temperature,
                "Fertilizer_Used": fertilizer,
                "Irrigation_Used": irrigation,
                "Weather_Condition": weather,
                "Days_to_Harvest": days_to_harvest
            }
            
            with st.spinner("Making prediction..."):
                success, result = predict_yield(payload)
                if success:
                    predicted_yield = result.get("predicted_yield", 0)
                    st.success(f"🎯 Predicted Yield: {predicted_yield:.2f} tons/hectare")
                    
                    # Get explanation
                    exp_success, explanation = explain_prediction(payload)
                    if exp_success:
                        st.info(f"💡 {explanation.get('summary', 'No explanation available')}")
                    
                    # Store in session state for history
                    if "prediction_history" not in st.session_state:
                        st.session_state.prediction_history = []
                    
                    st.session_state.prediction_history.append({
                        "timestamp": datetime.now(),
                        "prediction": predicted_yield,
                        "payload": payload
                    })
                else:
                    st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")

# Training metrics if available
if "training_metrics" in st.session_state:
    st.header("📊 Model Performance")
    create_metrics_dashboard(st.session_state.training_metrics)

# Prediction history
if "prediction_history" in st.session_state and st.session_state.prediction_history:
    st.header("📈 Recent Predictions")
    
    history_df = pd.DataFrame(st.session_state.prediction_history)
    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
    
    # Create yield trend chart
    fig = px.line(
        history_df, 
        x="timestamp", 
        y="prediction",
        title="Yield Prediction Trend",
        labels={"prediction": "Predicted Yield (tons/hectare)", "timestamp": "Time"}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show recent predictions table
    st.subheader("Recent Predictions")
    display_df = history_df[["timestamp", "prediction"]].copy()
    display_df["timestamp"] = display_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    display_df.columns = ["Time", "Predicted Yield (tons/hectare)"]
    st.dataframe(display_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🌾 **CropSense** - AI-powered crop yield prediction system")
st.markdown("Built with ❤️ using Streamlit, FastAPI, and Machine Learning")
