"""
CropSense - AI-powered Crop Yield Prediction System
Main Streamlit Application
"""
import streamlit as st
import os
import sys
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure page
st.set_page_config(
    page_title="CropSense - AI Crop Yield Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #4ECDC4;
        margin-bottom: 3rem;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4ECDC4;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    .stButton > button {
        background-color: #4ECDC4;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #45B7B8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🌾 CropSense</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered Crop Yield Prediction System</p>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    
    # Page selection
    page = st.selectbox(
        "Select a page:",
        [
            "🏠 Dashboard",
            "🔮 Predictions", 
            "📊 Analysis",
            "📄 Reports",
            "⚙️ Settings"
        ]
    )
    
    st.markdown("---")
    
    # Quick status check
    st.markdown("## 🔧 System Status")
    
    try:
        from utils import check_service_health
        health_status = check_service_health()
        
        for service, status in health_status.items():
            if status:
                st.success(f"✅ {service}")
            else:
                st.error(f"❌ {service}")
    except Exception as e:
        st.error("❌ Status check failed")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    if st.button("🔄 Refresh Status"):
        st.rerun()
    
    if st.button("📊 Run Pipeline"):
        st.info("Navigate to Dashboard to run the full pipeline")
    
    st.markdown("---")
    
    # System info
    st.markdown("## ℹ️ System Info")
    st.markdown(f"**Version:** 1.0.0")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")
    st.markdown(f"**Environment:** {'Docker' if os.path.exists('/.dockerenv') else 'Local'}")

# Main content based on page selection
if page == "🏠 Dashboard":
    st.info("🌐 **Dashboard Page** - Navigate to the Dashboard page in the sidebar to access the main dashboard features.")
    st.markdown("""
    ### 🎯 Available Features:
    - **System Overview**: Service health and status monitoring
    - **Quick Predict**: Simple prediction form
    - **Pipeline Management**: Run data collection, preprocessing, and training
    - **Recent Activity**: Track system usage and predictions
    
    ### 🚀 Quick Start:
    1. Use the sidebar to navigate to different pages
    2. Check service status in the sidebar
    3. Run the full pipeline from the Dashboard
    4. Make predictions and analyze results
    """)

elif page == "🔮 Predictions":
    st.info("🔮 **Predictions Page** - Navigate to the Predictions page in the sidebar to access advanced prediction features.")
    st.markdown("""
    ### 🎯 Available Features:
    - **Single Prediction**: Make individual yield predictions
    - **Batch Upload**: Process CSV files with multiple scenarios
    - **Scenario Analysis**: Compare different farming conditions
    - **Feature Importance**: Understand what drives predictions
    
    ### 📊 Prediction Types:
    - **Real-time Predictions**: Get instant yield estimates
    - **Batch Processing**: Upload CSV files for bulk predictions
    - **Scenario Comparison**: Test different farming strategies
    """)

elif page == "📊 Analysis":
    st.info("📊 **Analysis Page** - Navigate to the Analysis page in the sidebar to access data analysis features.")
    st.markdown("""
    ### 🔍 Analysis Features:
    - **Feature Analysis**: Understand which factors affect yield most
    - **Yield Trends**: Analyze yield patterns and distributions
    - **Correlation Matrix**: Explore relationships between variables
    - **Sensitivity Analysis**: See how input changes affect outputs
    - **Model Performance**: Evaluate prediction accuracy
    
    ### 📈 Visualization Tools:
    - Interactive charts and graphs
    - Statistical analysis
    - Performance metrics
    - Data exploration tools
    """)

elif page == "📄 Reports":
    st.info("📄 **Reports Page** - Navigate to the Reports page in the sidebar to access reporting features.")
    st.markdown("""
    ### 📋 Report Types:
    - **Prediction Summary**: Overview of all predictions
    - **Detailed Analysis**: Comprehensive feature analysis
    - **Custom Reports**: Build reports with selected sections
    - **Data Export**: Download results in multiple formats
    
    ### 📥 Export Options:
    - **CSV**: Raw data and processed results
    - **JSON**: Structured data format
    - **Markdown**: Formatted reports
    - **HTML**: Web-ready reports
    """)

elif page == "⚙️ Settings":
    st.info("⚙️ **Settings Page** - Navigate to the Settings page in the sidebar to access configuration options.")
    st.markdown("""
    ### 🔧 Configuration Areas:
    - **General Settings**: Theme, defaults, preferences
    - **Model Configuration**: ML model parameters and testing
    - **API Settings**: Service URLs and connection testing
    - **System Status**: Health monitoring and resource usage
    - **Data Management**: Backup, restore, cleanup options
    
    ### 🛠️ System Management:
    - Service health monitoring
    - Configuration backup/restore
    - Performance tuning
    - Data management tools
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>🌾 CropSense</strong> - AI-powered crop yield prediction system</p>
    <p>Built with ❤️ using Streamlit, FastAPI, and Machine Learning</p>
    <p>© 2024 CropSense. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)