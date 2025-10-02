"""
CropSense Predictions - Advanced prediction interface
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    predict_yield, explain_prediction, create_feature_importance_chart,
    create_yield_distribution_chart, save_predictions_to_csv, load_sample_data
)

st.set_page_config(
    page_title="CropSense Predictions",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Advanced Predictions")
st.markdown("Make single predictions or batch process multiple scenarios")

# Initialize session state
if "predictions" not in st.session_state:
    st.session_state.predictions = []
if "explanations" not in st.session_state:
    st.session_state.explanations = []

# Sidebar for prediction options
with st.sidebar:
    st.header("🎯 Prediction Options")
    
    prediction_mode = st.radio(
        "Choose prediction mode:",
        ["Single Prediction", "Batch Upload", "Scenario Analysis"]
    )
    
    st.markdown("---")
    
    if st.button("🗑️ Clear All Predictions"):
        st.session_state.predictions = []
        st.session_state.explanations = []
        st.rerun()
    
    if st.button("📊 Download Results"):
        if st.session_state.predictions:
            filename = save_predictions_to_csv(st.session_state.predictions)
            with open(filename, "rb") as f:
                st.download_button(
                    label="📥 Download CSV",
                    data=f.read(),
                    file_name=filename,
                    mime="text/csv"
                )

# Main content based on prediction mode
if prediction_mode == "Single Prediction":
    st.header("🎯 Single Prediction")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        with st.form("single_prediction"):
            # Basic parameters
            region = st.selectbox("Region", ["West", "East", "North", "South"], key="single_region")
            soil_type = st.selectbox("Soil Type", ["Sandy", "Loam", "Clay", "Silt"], key="single_soil")
            crop = st.selectbox("Crop", ["Wheat", "Rice", "Soybean", "Barley", "Corn", "Cotton"], key="single_crop")
            
            # Environmental parameters
            st.subheader("Environmental Conditions")
            rainfall = st.slider("Rainfall (mm)", 0, 2000, 800, 50)
            temperature = st.slider("Temperature (°C)", -10, 50, 25, 1)
            weather = st.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy", "Stormy"], key="single_weather")
            
            # Agricultural practices
            st.subheader("Agricultural Practices")
            fertilizer = st.checkbox("Fertilizer Used", value=True, key="single_fertilizer")
            irrigation = st.checkbox("Irrigation Used", value=True, key="single_irrigation")
            days_to_harvest = st.slider("Days to Harvest", 30, 365, 120, 10)
            
            # Advanced parameters
            with st.expander("🔧 Advanced Parameters"):
                area = st.number_input("Area (hectares)", min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
                planting_density = st.number_input("Planting Density (plants/m²)", min_value=1, max_value=100, value=20)
                soil_ph = st.slider("Soil pH", 4.0, 9.0, 6.5, 0.1)
                organic_matter = st.slider("Organic Matter (%)", 0.0, 10.0, 2.5, 0.1)
            
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
                    # Make prediction
                    success, result = predict_yield(payload)
                    if success:
                        predicted_yield = result.get("predicted_yield", 0)
                        st.success(f"🎯 Predicted Yield: {predicted_yield:.2f} tons/hectare")
                        
                        # Get explanation
                        exp_success, explanation = explain_prediction(payload)
                        
                        # Store results
                        st.session_state.predictions.append({
                            "timestamp": datetime.now(),
                            "predicted_yield": predicted_yield,
                            "payload": payload
                        })
                        
                        if exp_success:
                            st.session_state.explanations.append(explanation)
                        else:
                            st.session_state.explanations.append({"summary": "No explanation available"})
                        
                        st.rerun()
                    else:
                        st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
    
    with col2:
        st.subheader("Prediction Results")
        
        if st.session_state.predictions:
            latest_pred = st.session_state.predictions[-1]
            latest_exp = st.session_state.explanations[-1] if st.session_state.explanations else {}
            
            # Display latest prediction
            st.metric(
                "Latest Prediction",
                f"{latest_pred['predicted_yield']:.2f} tons/hectare",
                delta=None
            )
            
            # Display explanation
            st.subheader("💡 Explanation")
            st.info(latest_exp.get("summary", "No explanation available"))
            
            # Feature importance if available
            if "top_features" in latest_exp:
                st.subheader("📊 Feature Importance")
                fig = create_feature_importance_chart(latest_exp["top_features"])
                st.plotly_chart(fig, use_container_width=True)

elif prediction_mode == "Batch Upload":
    st.header("📊 Batch Prediction")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload CSV File")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Upload a CSV file with columns: Region, Soil_Type, Crop, Rainfall_mm, Temperature_Celsius, Fertilizer_Used, Irrigation_Used, Weather_Condition, Days_to_Harvest"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File uploaded successfully! {len(df)} rows found.")
                
                # Display sample data
                st.subheader("📋 Sample Data")
                st.dataframe(df.head(), use_container_width=True)
                
                # Validate required columns
                required_columns = [
                    "Region", "Soil_Type", "Crop", "Rainfall_mm", 
                    "Temperature_Celsius", "Fertilizer_Used", 
                    "Irrigation_Used", "Weather_Condition", "Days_to_Harvest"
                ]
                
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                else:
                    if st.button("🔮 Process Batch Predictions", type="primary"):
                        with st.spinner("Processing batch predictions..."):
                            batch_predictions = []
                            batch_explanations = []
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            for i, row in df.iterrows():
                                status_text.text(f"Processing row {i+1}/{len(df)}")
                                progress_bar.progress((i+1) / len(df))
                                
                                payload = row.to_dict()
                                
                                # Make prediction
                                success, result = predict_yield(payload)
                                if success:
                                    predicted_yield = result.get("predicted_yield", 0)
                                    batch_predictions.append({
                                        "timestamp": datetime.now(),
                                        "predicted_yield": predicted_yield,
                                        "payload": payload
                                    })
                                    
                                    # Get explanation (optional for batch)
                                    exp_success, explanation = explain_prediction(payload)
                                    if exp_success:
                                        batch_explanations.append(explanation)
                                    else:
                                        batch_explanations.append({"summary": "No explanation available"})
                            
                            # Store results
                            st.session_state.predictions.extend(batch_predictions)
                            st.session_state.explanations.extend(batch_explanations)
                            
                            st.success(f"✅ Batch processing complete! {len(batch_predictions)} predictions made.")
                            st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
        
        # Sample data download
        st.subheader("📥 Download Sample Template")
        sample_data = load_sample_data()
        csv = sample_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=csv,
            file_name="cropsense_sample.csv",
            mime="text/csv"
        )
    
    with col2:
        st.subheader("Batch Results")
        
        if st.session_state.predictions:
            # Create results dataframe
            results_df = pd.DataFrame([
                {
                    "Timestamp": pred["timestamp"],
                    "Region": pred["payload"]["Region"],
                    "Crop": pred["payload"]["Crop"],
                    "Predicted Yield": pred["predicted_yield"]
                }
                for pred in st.session_state.predictions
            ])
            
            st.dataframe(results_df, use_container_width=True)
            
            # Summary statistics
            st.subheader("📊 Summary Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Predictions", len(results_df))
            with col2:
                st.metric("Average Yield", f"{results_df['Predicted Yield'].mean():.2f} t/ha")
            with col3:
                st.metric("Max Yield", f"{results_df['Predicted Yield'].max():.2f} t/ha")

elif prediction_mode == "Scenario Analysis":
    st.header("🎭 Scenario Analysis")
    
    st.markdown("Compare different scenarios to understand the impact of various factors on crop yield.")
    
    # Scenario comparison
    scenarios = st.multiselect(
        "Select scenarios to compare:",
        ["Baseline", "High Rainfall", "Low Temperature", "No Fertilizer", "Optimal Conditions"],
        default=["Baseline", "Optimal Conditions"]
    )
    
    if scenarios:
        # Define scenario parameters
        scenario_params = {
            "Baseline": {
                "Region": "West", "Soil_Type": "Sandy", "Crop": "Wheat",
                "Rainfall_mm": 800, "Temperature_Celsius": 25,
                "Fertilizer_Used": True, "Irrigation_Used": True,
                "Weather_Condition": "Sunny", "Days_to_Harvest": 120
            },
            "High Rainfall": {
                "Region": "West", "Soil_Type": "Sandy", "Crop": "Wheat",
                "Rainfall_mm": 1500, "Temperature_Celsius": 25,
                "Fertilizer_Used": True, "Irrigation_Used": True,
                "Weather_Condition": "Rainy", "Days_to_Harvest": 120
            },
            "Low Temperature": {
                "Region": "West", "Soil_Type": "Sandy", "Crop": "Wheat",
                "Rainfall_mm": 800, "Temperature_Celsius": 15,
                "Fertilizer_Used": True, "Irrigation_Used": True,
                "Weather_Condition": "Cloudy", "Days_to_Harvest": 120
            },
            "No Fertilizer": {
                "Region": "West", "Soil_Type": "Sandy", "Crop": "Wheat",
                "Rainfall_mm": 800, "Temperature_Celsius": 25,
                "Fertilizer_Used": False, "Irrigation_Used": True,
                "Weather_Condition": "Sunny", "Days_to_Harvest": 120
            },
            "Optimal Conditions": {
                "Region": "East", "Soil_Type": "Loam", "Crop": "Wheat",
                "Rainfall_mm": 1000, "Temperature_Celsius": 28,
                "Fertilizer_Used": True, "Irrigation_Used": True,
                "Weather_Condition": "Sunny", "Days_to_Harvest": 110
            }
        }
        
        if st.button("🔮 Run Scenario Analysis", type="primary"):
            with st.spinner("Running scenario analysis..."):
                scenario_results = []
                
                for scenario in scenarios:
                    payload = scenario_params[scenario]
                    success, result = predict_yield(payload)
                    
                    if success:
                        predicted_yield = result.get("predicted_yield", 0)
                        scenario_results.append({
                            "Scenario": scenario,
                            "Predicted Yield": predicted_yield,
                            "Parameters": payload
                        })
                
                if scenario_results:
                    # Create comparison chart
                    results_df = pd.DataFrame(scenario_results)
                    
                    fig = px.bar(
                        results_df,
                        x="Scenario",
                        y="Predicted Yield",
                        title="Scenario Comparison",
                        color="Predicted Yield",
                        color_continuous_scale="Viridis"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display results table
                    st.subheader("📊 Scenario Results")
                    st.dataframe(results_df[["Scenario", "Predicted Yield"]], use_container_width=True)
                    
                    # Store in session state
                    for result in scenario_results:
                        st.session_state.predictions.append({
                            "timestamp": datetime.now(),
                            "predicted_yield": result["Predicted Yield"],
                            "payload": result["Parameters"]
                        })

# Results section (always visible if there are predictions)
if st.session_state.predictions:
    st.header("📈 All Predictions")
    
    # Create yield distribution chart
    yields = [pred["predicted_yield"] for pred in st.session_state.predictions]
    fig = create_yield_distribution_chart(yields)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed results table
    st.subheader("📋 Detailed Results")
    
    results_data = []
    for i, (pred, exp) in enumerate(zip(st.session_state.predictions, st.session_state.explanations)):
        results_data.append({
            "ID": i+1,
            "Timestamp": pred["timestamp"].strftime("%Y-%m-%d %H:%M"),
            "Region": pred["payload"]["Region"],
            "Crop": pred["payload"]["Crop"],
            "Predicted Yield": f"{pred['predicted_yield']:.2f} t/ha",
            "Rainfall": f"{pred['payload']['Rainfall_mm']} mm",
            "Temperature": f"{pred['payload']['Temperature_Celsius']}°C"
        })
    
    results_df = pd.DataFrame(results_data)
    st.dataframe(results_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🌾 **CropSense Predictions** - Advanced prediction interface")
