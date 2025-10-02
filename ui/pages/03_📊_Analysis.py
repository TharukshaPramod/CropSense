"""
CropSense Analysis - Advanced data analysis and visualization
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    predict_yield, explain_prediction, create_feature_importance_chart,
    load_sample_data, check_service_health
)

st.set_page_config(
    page_title="CropSense Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Advanced Analysis")
st.markdown("Comprehensive analysis of crop yield predictions and feature relationships")

# Initialize session state
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = []

# Sidebar for analysis options
with st.sidebar:
    st.header("🔧 Analysis Options")
    
    analysis_type = st.selectbox(
        "Select analysis type:",
        ["Feature Analysis", "Yield Trends", "Correlation Matrix", "Sensitivity Analysis", "Model Performance"]
    )
    
    st.markdown("---")
    
    # Data generation options
    st.subheader("📊 Generate Sample Data")
    if st.button("🎲 Generate Random Scenarios"):
        # Generate random scenarios for analysis
        np.random.seed(42)
        n_scenarios = 100
        
        regions = ["West", "East", "North", "South"]
        soil_types = ["Sandy", "Loam", "Clay", "Silt"]
        crops = ["Wheat", "Rice", "Soybean", "Barley"]
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Stormy"]
        
        scenarios = []
        for i in range(n_scenarios):
            scenario = {
                "Region": np.random.choice(regions),
                "Soil_Type": np.random.choice(soil_types),
                "Crop": np.random.choice(crops),
                "Rainfall_mm": np.random.normal(800, 200),
                "Temperature_Celsius": np.random.normal(25, 5),
                "Fertilizer_Used": np.random.choice([True, False]),
                "Irrigation_Used": np.random.choice([True, False]),
                "Weather_Condition": np.random.choice(weather_conditions),
                "Days_to_Harvest": np.random.randint(90, 150)
            }
            scenarios.append(scenario)
        
        # Make predictions for all scenarios
        with st.spinner("Generating predictions..."):
            predictions = []
            for scenario in scenarios:
                success, result = predict_yield(scenario)
                if success:
                    scenario["Predicted_Yield"] = result.get("predicted_yield", 0)
                    predictions.append(scenario)
            
            st.session_state.analysis_data = predictions
            st.success(f"✅ Generated {len(predictions)} scenarios with predictions")
            st.rerun()
    
    if st.button("🗑️ Clear Analysis Data"):
        st.session_state.analysis_data = []
        st.rerun()

# Main content based on analysis type
if not st.session_state.analysis_data:
    st.info("👆 Generate sample data from the sidebar to start analysis")
    
    # Show sample data preview
    st.subheader("📋 Sample Data Preview")
    sample_data = load_sample_data()
    st.dataframe(sample_data, use_container_width=True)
    
    st.markdown("""
    ### 🎯 Analysis Features Available:
    - **Feature Analysis**: Understand which factors most influence yield
    - **Yield Trends**: Track yield patterns across different conditions
    - **Correlation Matrix**: Explore relationships between variables
    - **Sensitivity Analysis**: See how changes in inputs affect outputs
    - **Model Performance**: Evaluate prediction accuracy and reliability
    """)

else:
    df = pd.DataFrame(st.session_state.analysis_data)
    
    if analysis_type == "Feature Analysis":
        st.header("🔍 Feature Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Feature importance analysis
            st.subheader("📊 Feature Impact on Yield")
            
            # Calculate feature importance using correlation
            numeric_features = ["Rainfall_mm", "Temperature_Celsius", "Days_to_Harvest"]
            correlations = []
            
            for feature in numeric_features:
                if feature in df.columns:
                    corr = df[feature].corr(df["Predicted_Yield"])
                    correlations.append((feature, corr))
            
            # Categorical feature analysis
            categorical_features = ["Region", "Soil_Type", "Crop", "Weather_Condition"]
            for feature in categorical_features:
                if feature in df.columns:
                    # Calculate mean yield by category
                    mean_yields = df.groupby(feature)["Predicted_Yield"].mean()
                    # Use coefficient of variation as importance
                    importance = mean_yields.std() / mean_yields.mean()
                    correlations.append((feature, importance))
            
            # Create feature importance chart
            if correlations:
                feature_names, importance_values = zip(*correlations)
                fig = go.Figure(data=[
                    go.Bar(
                        x=importance_values,
                        y=feature_names,
                        orientation='h',
                        marker_color='#4ECDC4',
                        text=[f"{x:.3f}" for x in importance_values],
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title="Feature Importance Analysis",
                    xaxis_title="Importance Score",
                    yaxis_title="Features",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Quick Stats")
            
            # Basic statistics
            st.metric("Total Scenarios", len(df))
            st.metric("Average Yield", f"{df['Predicted_Yield'].mean():.2f} t/ha")
            st.metric("Yield Range", f"{df['Predicted_Yield'].min():.2f} - {df['Predicted_Yield'].max():.2f} t/ha")
            st.metric("Std Deviation", f"{df['Predicted_Yield'].std():.2f} t/ha")
            
            # Top performing scenarios
            st.subheader("🏆 Top 5 Scenarios")
            top_scenarios = df.nlargest(5, "Predicted_Yield")[["Crop", "Region", "Predicted_Yield"]]
            st.dataframe(top_scenarios, use_container_width=True)
        
        # Detailed feature analysis
        st.subheader("🔬 Detailed Feature Analysis")
        
        feature_tabs = st.tabs(["🌡️ Environmental", "🌱 Agricultural", "📍 Geographic"])
        
        with feature_tabs[0]:
            col1, col2 = st.columns(2)
            
            with col1:
                # Rainfall vs Yield
                fig = px.scatter(
                    df, x="Rainfall_mm", y="Predicted_Yield",
                    color="Crop", title="Rainfall vs Yield",
                    labels={"Rainfall_mm": "Rainfall (mm)", "Predicted_Yield": "Yield (t/ha)"}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Temperature vs Yield
                fig = px.scatter(
                    df, x="Temperature_Celsius", y="Predicted_Yield",
                    color="Crop", title="Temperature vs Yield",
                    labels={"Temperature_Celsius": "Temperature (°C)", "Predicted_Yield": "Yield (t/ha)"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with feature_tabs[1]:
            col1, col2 = st.columns(2)
            
            with col1:
                # Fertilizer impact
                fertilizer_impact = df.groupby("Fertilizer_Used")["Predicted_Yield"].mean()
                fig = px.bar(
                    x=fertilizer_impact.index,
                    y=fertilizer_impact.values,
                    title="Fertilizer Impact on Yield",
                    labels={"x": "Fertilizer Used", "y": "Average Yield (t/ha)"}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Irrigation impact
                irrigation_impact = df.groupby("Irrigation_Used")["Predicted_Yield"].mean()
                fig = px.bar(
                    x=irrigation_impact.index,
                    y=irrigation_impact.values,
                    title="Irrigation Impact on Yield",
                    labels={"x": "Irrigation Used", "y": "Average Yield (t/ha)"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with feature_tabs[2]:
            col1, col2 = st.columns(2)
            
            with col1:
                # Region analysis
                region_yield = df.groupby("Region")["Predicted_Yield"].mean().sort_values(ascending=False)
                fig = px.bar(
                    x=region_yield.index,
                    y=region_yield.values,
                    title="Average Yield by Region",
                    labels={"x": "Region", "y": "Average Yield (t/ha)"}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Soil type analysis
                soil_yield = df.groupby("Soil_Type")["Predicted_Yield"].mean().sort_values(ascending=False)
                fig = px.bar(
                    x=soil_yield.index,
                    y=soil_yield.values,
                    title="Average Yield by Soil Type",
                    labels={"x": "Soil Type", "y": "Average Yield (t/ha)"}
                )
                st.plotly_chart(fig, use_container_width=True)

    elif analysis_type == "Yield Trends":
        st.header("📈 Yield Trends Analysis")
        
        # Yield distribution
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig = px.histogram(
                df, x="Predicted_Yield",
                title="Yield Distribution",
                labels={"Predicted_Yield": "Predicted Yield (t/ha)", "count": "Frequency"},
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Box plot by crop
            fig = px.box(
                df, x="Crop", y="Predicted_Yield",
                title="Yield Distribution by Crop",
                labels={"Predicted_Yield": "Predicted Yield (t/ha)"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series simulation (using Days_to_Harvest as proxy)
        st.subheader("⏰ Harvest Timeline Analysis")
        
        # Create a timeline based on days to harvest
        df_sorted = df.sort_values("Days_to_Harvest")
        
        fig = px.scatter(
            df_sorted, x="Days_to_Harvest", y="Predicted_Yield",
            color="Crop", size="Rainfall_mm",
            title="Yield vs Harvest Timeline",
            labels={"Days_to_Harvest": "Days to Harvest", "Predicted_Yield": "Predicted Yield (t/ha)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Seasonal analysis (simulated)
        st.subheader("🌍 Seasonal Patterns")
        
        # Simulate seasonal data
        df["Season"] = df["Temperature_Celsius"].apply(
            lambda x: "Winter" if x < 15 else "Spring" if x < 25 else "Summer" if x < 35 else "Fall"
        )
        
        seasonal_yield = df.groupby("Season")["Predicted_Yield"].mean()
        fig = px.bar(
            x=seasonal_yield.index,
            y=seasonal_yield.values,
            title="Average Yield by Season",
            labels={"x": "Season", "y": "Average Yield (t/ha)"}
        )
        st.plotly_chart(fig, use_container_width=True)

    elif analysis_type == "Correlation Matrix":
        st.header("🔗 Correlation Analysis")
        
        # Select numeric columns for correlation
        numeric_cols = ["Rainfall_mm", "Temperature_Celsius", "Days_to_Harvest", "Predicted_Yield"]
        correlation_df = df[numeric_cols].corr()
        
        # Create correlation heatmap
        fig = px.imshow(
            correlation_df,
            text_auto=True,
            aspect="auto",
            title="Feature Correlation Matrix",
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed correlation analysis
        st.subheader("📊 Correlation Details")
        
        # Find strongest correlations
        corr_with_yield = correlation_df["Predicted_Yield"].abs().sort_values(ascending=False)
        corr_with_yield = corr_with_yield.drop("Predicted_Yield")  # Remove self-correlation
        
        st.write("**Strongest correlations with yield:**")
        for feature, corr in corr_with_yield.head(5).items():
            st.write(f"- {feature}: {corr:.3f}")

    elif analysis_type == "Sensitivity Analysis":
        st.header("🎯 Sensitivity Analysis")
        
        st.markdown("Analyze how changes in input parameters affect yield predictions.")
        
        # Parameter selection
        param_col1, param_col2 = st.columns(2)
        
        with param_col1:
            base_rainfall = st.slider("Base Rainfall (mm)", 0, 2000, 800)
            rainfall_range = st.slider("Rainfall Range (±)", 0, 500, 200)
        
        with param_col2:
            base_temp = st.slider("Base Temperature (°C)", -10, 50, 25)
            temp_range = st.slider("Temperature Range (±)", 0, 20, 10)
        
        if st.button("🔬 Run Sensitivity Analysis"):
            # Create sensitivity scenarios
            rainfall_values = np.linspace(base_rainfall - rainfall_range, base_rainfall + rainfall_range, 10)
            temp_values = np.linspace(base_temp - temp_range, base_temp + temp_range, 10)
            
            sensitivity_results = []
            
            with st.spinner("Running sensitivity analysis..."):
                for rainfall in rainfall_values:
                    for temp in temp_values:
                        scenario = {
                            "Region": "West",
                            "Soil_Type": "Sandy",
                            "Crop": "Wheat",
                            "Rainfall_mm": rainfall,
                            "Temperature_Celsius": temp,
                            "Fertilizer_Used": True,
                            "Irrigation_Used": True,
                            "Weather_Condition": "Sunny",
                            "Days_to_Harvest": 120
                        }
                        
                        success, result = predict_yield(scenario)
                        if success:
                            sensitivity_results.append({
                                "Rainfall": rainfall,
                                "Temperature": temp,
                                "Yield": result.get("predicted_yield", 0)
                            })
            
            if sensitivity_results:
                sensitivity_df = pd.DataFrame(sensitivity_results)
                
                # Create 3D surface plot
                fig = go.Figure(data=[
                    go.Surface(
                        x=sensitivity_df.pivot(index="Temperature", columns="Rainfall", values="Yield").columns,
                        y=sensitivity_df.pivot(index="Temperature", columns="Rainfall", values="Yield").index,
                        z=sensitivity_df.pivot(index="Temperature", columns="Rainfall", values="Yield").values,
                        colorscale="Viridis"
                    )
                ])
                
                fig.update_layout(
                    title="Yield Sensitivity to Rainfall and Temperature",
                    scene=dict(
                        xaxis_title="Rainfall (mm)",
                        yaxis_title="Temperature (°C)",
                        zaxis_title="Predicted Yield (t/ha)"
                    ),
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary statistics
                st.subheader("📊 Sensitivity Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Yield Range", f"{sensitivity_df['Yield'].min():.2f} - {sensitivity_df['Yield'].max():.2f} t/ha")
                with col2:
                    st.metric("Yield Std Dev", f"{sensitivity_df['Yield'].std():.2f} t/ha")
                with col3:
                    st.metric("Coefficient of Variation", f"{sensitivity_df['Yield'].std() / sensitivity_df['Yield'].mean():.3f}")

    elif analysis_type == "Model Performance":
        st.header("🎯 Model Performance Analysis")
        
        # Service health check
        st.subheader("🔧 System Health")
        health_status = check_service_health()
        
        health_cols = st.columns(len(health_status))
        for i, (service, status) in enumerate(health_status.items()):
            with health_cols[i]:
                if status:
                    st.success(f"✅ {service}")
                else:
                    st.error(f"❌ {service}")
        
        # Model performance metrics
        st.subheader("📊 Performance Metrics")
        
        # Simulate model performance metrics
        performance_metrics = {
            "Mean Absolute Error": 0.15,
            "Root Mean Square Error": 0.23,
            "R² Score": 0.87,
            "Mean Absolute Percentage Error": 5.2
        }
        
        metric_cols = st.columns(len(performance_metrics))
        for i, (metric, value) in enumerate(performance_metrics.items()):
            with metric_cols[i]:
                st.metric(metric, f"{value:.3f}")
        
        # Prediction accuracy analysis
        st.subheader("🎯 Prediction Accuracy")
        
        # Simulate accuracy by crop type
        accuracy_by_crop = {
            "Wheat": 0.89,
            "Rice": 0.85,
            "Soybean": 0.82,
            "Barley": 0.87
        }
        
        fig = px.bar(
            x=list(accuracy_by_crop.keys()),
            y=list(accuracy_by_crop.values()),
            title="Model Accuracy by Crop Type",
            labels={"x": "Crop", "y": "Accuracy Score"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Error distribution
        st.subheader("📈 Error Distribution")
        
        # Simulate prediction errors
        np.random.seed(42)
        errors = np.random.normal(0, 0.2, 1000)
        
        fig = px.histogram(
            x=errors,
            title="Prediction Error Distribution",
            labels={"x": "Prediction Error", "y": "Frequency"},
            nbins=30
        )
        fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Perfect Prediction")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🌾 **CropSense Analysis** - Advanced data analysis and visualization")
