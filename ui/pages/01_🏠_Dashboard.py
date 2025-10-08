"""
CropSense Dashboard - Modern Advanced Overview
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
from auth_utils import is_authenticated, current_user, current_role
from modern_footer import render_modern_footer

st.set_page_config(
    page_title="CropSense Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MODERN CSS FOR DASHBOARD
st.markdown("""
<style>
    /* Modern Dashboard Styles */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .service-status {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: 600;
        text-align: center;
    }
    
    .status-healthy {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white;
    }
    
    .status-error {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .glass-panel {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .user-welcome {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    /* Sidebar improvements */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
</style>
""", unsafe_allow_html=True)

# AUTHENTICATION CHECK
if not is_authenticated():
    st.error("🔐 Authentication required. Please log in to access the dashboard.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/00_🔐_Login.py")
    st.stop()

# USER WELCOME SECTION
user_role = current_role()
st.markdown(f"""
<div class="user-welcome">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h2 style="margin: 0; font-size: 1.8rem;">Welcome back, {current_user()}! 👋</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                {'👑 Administrator' if user_role == 'admin' else '👨‍🌾 Farmer'} • {datetime.now().strftime('%A, %B %d, %Y')}
            </p>
        </div>
        <div style="font-size: 3rem;">🌾</div>
    </div>
</div>
""", unsafe_allow_html=True)

# MODERN SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 15px;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🌾</div>
        <h3 style="margin: 0; color: white;">CropSense</h3>
        <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">AI Agriculture Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Section
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🔄 Refresh Data", use_container_width=True, help="Refresh all dashboard data"):
        st.rerun()
    
    if st.button("📊 Run Analysis", use_container_width=True, help="Run crop analysis"):
        st.info("🔍 Starting crop analysis...")
    
    if st.button("🌤️ Weather Update", use_container_width=True, help="Update weather data"):
        st.info("⏳ Fetching latest weather data...")
    
    st.markdown("---")
    
    # System Status
    st.markdown("### 📊 System Status")
    
    # Mock service health - replace with actual check_service_health() if available
    health_status = {
        "Data Collector": True,
        "AI Predictor": True,
        "Weather API": True,
        "Database": True
    }
    
    for service, status in health_status.items():
        status_icon = "✅" if status else "❌"
        status_text = "Healthy" if status else "Offline"
        st.write(f"{status_icon} **{service}**: {status_text}")
    
    st.markdown("---")
    
    # User Info
    st.markdown("### 👤 User Info")
    st.write(f"**Role:** {user_role.title()}")
    st.write(f"**Status:** 🟢 Active")
    st.write(f"**Last Login:** Today")
    
    if st.button("🚪 Logout", use_container_width=True):
        from auth_utils import logout
        logout()
        st.success("Logged out successfully!")
        st.rerun()

# MAIN DASHBOARD CONTENT
# Top Metrics Row
st.markdown("### 📈 Real-time Overview")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; text-align: center;">🌾</div>
        <div style="text-align: center; font-size: 1.8rem; font-weight: bold; color: #2E8B57;">15.2K</div>
        <div style="text-align: center; color: #666;">Active Farms</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; text-align: center;">🎯</div>
        <div style="text-align: center; font-size: 1.8rem; font-weight: bold; color: #FF6B6B;">98.7%</div>
        <div style="text-align: center; color: #666;">Prediction Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; text-align: center;">📊</div>
        <div style="text-align: center; font-size: 1.8rem; font-weight: bold; color: #4ECDC4;">2.4M</div>
        <div style="text-align: center; color: #666;">Acres Monitored</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col4:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; text-align: center;">🚀</div>
        <div style="text-align: center; font-size: 1.8rem; font-weight: bold; color: #45B7D1;">45%</div>
        <div style="text-align: center; color: #666;">Avg Yield Increase</div>
    </div>
    """, unsafe_allow_html=True)

# Main Content Columns
col1, col2 = st.columns([2, 1])

with col1:
    # System Overview
    st.markdown("### 🔧 System Overview")
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        
        # Service Health in a modern layout
        st.subheader("🛠️ Service Health Status")
        health_cols = st.columns(len(health_status))
        for i, (service, status) in enumerate(health_status.items()):
            with health_cols[i]:
                status_class = "status-healthy" if status else "status-error"
                st.markdown(f'<div class="service-status {status_class}">{service}<br>{"✅ Healthy" if status else "❌ Offline"}</div>', unsafe_allow_html=True)
        
        # Pipeline Status
        st.subheader("🔄 AI Pipeline Status")
        pipeline_stages = [
            ("Data Collection", "Ready", "✅"),
            ("Preprocessing", "Ready", "✅"), 
            ("Model Training", "Ready", "✅"),
            ("Prediction", "Ready", "✅")
        ]
        
        for stage, status, icon in pipeline_stages:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{stage}**")
            with col_b:
                if status == "Ready":
                    st.success(f"{icon} {status}")
                else:
                    st.warning(f"{icon} {status}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("### 📈 Recent Activity")
    
    # Sample activity data
    activity_data = pd.DataFrame({
        "Time": [datetime.now() - timedelta(hours=i) for i in range(6, 0, -1)],
        "Activity": [
            "AI Model Retraining Completed", 
            "Weather Data Sync", 
            "Yield Prediction Generated", 
            "Soil Analysis Updated",
            "System Health Check",
            "User Login"
        ],
        "Status": ["Success", "Success", "Success", "Warning", "Success", "Success"],
        "Duration": ["2m 34s", "45s", "3.2s", "1m 12s", "15s", "N/A"]
    })
    
    # Style the dataframe
    st.dataframe(
        activity_data,
        use_container_width=True,
        column_config={
            "Time": st.column_config.DatetimeColumn("Timestamp", format="HH:mm"),
            "Activity": "Activity",
            "Status": st.column_config.TextColumn("Status"),
            "Duration": "Duration"
        },
        hide_index=True
    )

with col2:
    # Quick Prediction Panel
    st.markdown("### 🎯 Quick Prediction")
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        
        with st.form("quick_predict"):
            st.subheader("🌱 Crop Parameters")
            
            # Organized form layout
            col_a, col_b = st.columns(2)
            
            with col_a:
                region = st.selectbox("📍 Region", ["North", "South", "East", "West", "Central"])
                soil_type = st.selectbox("🌱 Soil Type", ["Loam", "Clay", "Sandy", "Silt", "Peaty"])
                crop = st.selectbox("🌾 Crop Type", ["Wheat", "Rice", "Corn", "Soybean", "Barley", "Cotton"])
            
            with col_b:
                rainfall = st.slider("💧 Rainfall (mm)", 0.0, 2000.0, 800.0, 50.0)
                temperature = st.slider("🌡️ Temperature (°C)", -10.0, 50.0, 25.0, 1.0)
                days_to_harvest = st.slider("📅 Days to Harvest", 30, 365, 120, 10)
            
            # Advanced options
            with st.expander("⚙️ Advanced Options"):
                fertilizer = st.checkbox("🧪 Fertilizer Used", value=True)
                irrigation = st.checkbox("💦 Irrigation Used", value=True)
                weather = st.selectbox("☁️ Weather Condition", ["Sunny", "Cloudy", "Rainy", "Stormy", "Windy"])
            
            submitted = st.form_submit_button("🔮 Predict Yield", type="primary", use_container_width=True)
            
            if submitted:
                # Mock prediction - replace with actual predict_yield() if available
                predicted_yield = round(3.5 + (rainfall / 500) + (temperature / 10) + (0.5 if fertilizer else 0) + (0.3 if irrigation else 0), 2)
                
                # Enhanced result display
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="text-align: center;">
                        <h2 style="margin: 0; font-size: 2.5rem;">{predicted_yield}</h2>
                        <p style="margin: 0; opacity: 0.9;">tons/hectare</p>
                        <div style="margin-top: 1rem; font-size: 0.9rem;">
                            📍 {region} • 🌱 {soil_type} • 🌾 {crop}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AI Insights
                with st.expander("💡 AI Insights"):
                    st.info(f"Based on your inputs, the predicted yield is **{predicted_yield} tons/hectare**. Optimal conditions detected for {crop.lower()} cultivation in the {region.lower()} region.")
                
                # Store prediction history
                if "prediction_history" not in st.session_state:
                    st.session_state.prediction_history = []
                
                st.session_state.prediction_history.append({
                    "timestamp": datetime.now(),
                    "prediction": predicted_yield,
                    "region": region,
                    "crop": crop,
                    "rainfall": rainfall,
                    "temperature": temperature
                })
        
        st.markdown('</div>', unsafe_allow_html=True)

# PREDICTION HISTORY WITH VISUALIZATIONS
if "prediction_history" in st.session_state and st.session_state.prediction_history:
    st.markdown("### 📊 Prediction Analytics")
    
    history_df = pd.DataFrame(st.session_state.prediction_history)
    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
    
    # Create interactive charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Yield trend chart
        fig_trend = px.line(
            history_df, 
            x="timestamp", 
            y="prediction",
            title="📈 Yield Prediction Trend",
            labels={"prediction": "Predicted Yield (tons/hectare)", "timestamp": "Time"},
            color_discrete_sequence=['#2E8B57']
        )
        fig_trend.update_layout(
            height=300,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Crop distribution chart
        if len(history_df) > 1:
            fig_crop = px.pie(
                history_df,
                names='crop',
                title='🌾 Crop Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_crop.update_layout(height=300, showlegend=True)
            st.plotly_chart(fig_crop, use_container_width=True)
    
    # Recent predictions table
    st.markdown("#### 📋 Recent Predictions")
    display_df = history_df[["timestamp", "prediction", "region", "crop"]].copy()
    display_df["timestamp"] = display_df["timestamp"].dt.strftime("%m/%d %H:%M")
    display_df["prediction"] = display_df["prediction"].round(2)
    display_df.columns = ["Time", "Yield (t/ha)", "Region", "Crop"]
    
    st.dataframe(
        display_df.sort_values("Time", ascending=False).head(10),
        use_container_width=True,
        hide_index=True
    )

# FEATURE HIGHLIGHTS
st.markdown("### ✨ Today's Highlights")
highlight_col1, highlight_col2, highlight_col3 = st.columns(3)

with highlight_col1:
    st.markdown("""
    <div class="feature-highlight">
        <h4>🚀 Peak Performance</h4>
        <p>AI models running at 98.7% accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with highlight_col2:
    st.markdown("""
    <div class="feature-highlight">
        <h4>🌧️ Weather Alert</h4>
        <p>Optimal conditions for wheat cultivation</p>
    </div>
    """, unsafe_allow_html=True)

with highlight_col3:
    st.markdown("""
    <div class="feature-highlight">
        <h4>📈 Growth Trend</h4>
        <p>15% increase in predictions today</p>
    </div>
    """, unsafe_allow_html=True)

# Render modern footer
render_modern_footer()