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
    # Import and run dashboard page
    try:
        exec(open("pages/01_🏠_Dashboard.py").read())
    except FileNotFoundError:
        st.error("Dashboard page not found. Please ensure all page files are present.")
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

elif page == "🔮 Predictions":
    # Import and run predictions page
    try:
        exec(open("pages/02_🔮_Predictions.py").read())
    except FileNotFoundError:
        st.error("Predictions page not found. Please ensure all page files are present.")
    except Exception as e:
        st.error(f"Error loading predictions page: {e}")

elif page == "📊 Analysis":
    # Import and run analysis page
    try:
        exec(open("pages/03_📊_Analysis.py").read())
    except FileNotFoundError:
        st.error("Analysis page not found. Please ensure all page files are present.")
    except Exception as e:
        st.error(f"Error loading analysis page: {e}")

elif page == "📄 Reports":
    # Import and run reports page
    try:
        exec(open("pages/04_📄_Reports.py").read())
    except FileNotFoundError:
        st.error("Reports page not found. Please ensure all page files are present.")
    except Exception as e:
        st.error(f"Error loading reports page: {e}")

elif page == "⚙️ Settings":
    # Import and run settings page
    try:
        exec(open("pages/05_⚙️_Settings.py").read())
    except FileNotFoundError:
        st.error("Settings page not found. Please ensure all page files are present.")
    except Exception as e:
        st.error(f"Error loading settings page: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>🌾 CropSense</strong> - AI-powered crop yield prediction system</p>
    <p>Built with ❤️ using Streamlit, FastAPI, and Machine Learning</p>
    <p>© 2024 CropSense. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)