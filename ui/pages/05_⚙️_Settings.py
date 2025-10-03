"""
CropSense Settings - Configuration and system management
"""
import streamlit as st
import os
import sys
from datetime import datetime
import json

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import check_service_health
from auth_utils import is_authenticated, current_role
from modern_footer import render_modern_footer

st.set_page_config(
    page_title="CropSense Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings & Configuration")
st.markdown("Configure your CropSense system and manage preferences")

# Admin-only access
if not is_authenticated() or current_role() != "admin":
    st.warning("Settings are restricted to admin. Please login with an admin account.")
    st.stop()

# Initialize session state for settings
if "settings" not in st.session_state:
    st.session_state.settings = {
        "theme": "light",
        "default_crop": "Wheat",
        "default_region": "West",
        "auto_refresh": False,
        "notifications": True,
        "data_retention_days": 30,
        "model_preference": "lightgbm",
        "ollama_model": "llama3"
    }

# Sidebar for navigation
with st.sidebar:
    st.header("🔧 Settings Categories")
    
    setting_category = st.radio(
        "Select category:",
        ["General", "Model Configuration", "API Settings", "System Status", "Data Management"]
    )

# Main content based on selected category
if setting_category == "General":
    st.header("🌐 General Settings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎨 Appearance")
        
        # Theme selection
        theme = st.selectbox(
            "Theme",
            ["light", "dark"],
            index=0 if st.session_state.settings["theme"] == "light" else 1
        )
        st.session_state.settings["theme"] = theme
        
        # Default values
        st.subheader("🎯 Default Values")
        
        default_crop = st.selectbox(
            "Default Crop",
            ["Wheat", "Rice", "Soybean", "Barley", "Corn", "Cotton"],
            index=["Wheat", "Rice", "Soybean", "Barley", "Corn", "Cotton"].index(st.session_state.settings["default_crop"])
        )
        st.session_state.settings["default_crop"] = default_crop
        
        default_region = st.selectbox(
            "Default Region",
            ["West", "East", "North", "South"],
            index=["West", "East", "North", "South"].index(st.session_state.settings["default_region"])
        )
        st.session_state.settings["default_region"] = default_region
        
        # User preferences
        st.subheader("👤 User Preferences")
        
        auto_refresh = st.checkbox(
            "Auto-refresh data",
            value=st.session_state.settings["auto_refresh"]
        )
        st.session_state.settings["auto_refresh"] = auto_refresh
        
        notifications = st.checkbox(
            "Enable notifications",
            value=st.session_state.settings["notifications"]
        )
        st.session_state.settings["notifications"] = notifications
        
        data_retention = st.slider(
            "Data retention (days)",
            min_value=1,
            max_value=365,
            value=st.session_state.settings["data_retention_days"]
        )
        st.session_state.settings["data_retention_days"] = data_retention
    
    with col2:
        st.subheader("💾 Save Settings")
        
        if st.button("💾 Save Configuration", type="primary"):
            # Save settings to session state (in real app, save to file/database)
            st.success("✅ Settings saved successfully!")
        
        if st.button("🔄 Reset to Defaults"):
            st.session_state.settings = {
                "theme": "light",
                "default_crop": "Wheat",
                "default_region": "West",
                "auto_refresh": False,
                "notifications": True,
                "data_retention_days": 30,
                "model_preference": "lightgbm",
                "ollama_model": "llama3"
            }
            st.success("✅ Settings reset to defaults!")
            st.rerun()
        
        # Export/Import settings
        st.subheader("📤 Export/Import")
        
        # Export settings
        settings_json = json.dumps(st.session_state.settings, indent=2)
        st.download_button(
            label="📥 Export Settings",
            data=settings_json,
            file_name=f"cropsense_settings_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
        
        # Import settings
        uploaded_file = st.file_uploader(
            "📤 Import Settings",
            type="json",
            help="Upload a settings JSON file"
        )
        
        if uploaded_file is not None:
            try:
                imported_settings = json.load(uploaded_file)
                st.session_state.settings.update(imported_settings)
                st.success("✅ Settings imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error importing settings: {e}")

elif setting_category == "Model Configuration":
    st.header("🤖 Model Configuration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Model Preferences")
        
        # Model selection
        model_preference = st.selectbox(
            "Preferred Model",
            ["lightgbm", "random_forest", "xgboost"],
            index=["lightgbm", "random_forest", "xgboost"].index(st.session_state.settings["model_preference"])
        )
        st.session_state.settings["model_preference"] = model_preference
        
        # Model parameters
        st.subheader("🔧 Model Parameters")
        
        with st.expander("LightGBM Parameters"):
            n_estimators = st.slider("Number of Estimators", 100, 2000, 1000)
            learning_rate = st.slider("Learning Rate", 0.01, 0.3, 0.05, 0.01)
            max_depth = st.slider("Max Depth", 3, 15, 6)
            subsample = st.slider("Subsample", 0.5, 1.0, 0.8, 0.1)
        
        with st.expander("Random Forest Parameters"):
            rf_n_estimators = st.slider("Number of Trees", 50, 500, 200)
            rf_max_depth = st.slider("Max Depth", 3, 20, 10)
            rf_min_samples_split = st.slider("Min Samples Split", 2, 20, 2)
    
    with col2:
        st.subheader("🧠 AI/LLM Configuration")
        
        # Ollama model selection
        ollama_model = st.selectbox(
            "Ollama Model",
            ["llama3", "llama2", "flan-t5", "mistral"],
            index=["llama3", "llama2", "flan-t5", "mistral"].index(st.session_state.settings["ollama_model"])
        )
        st.session_state.settings["ollama_model"] = ollama_model
        
        # LLM parameters
        st.subheader("🔧 LLM Parameters")
        
        max_tokens = st.slider("Max Tokens", 50, 500, 200)
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1)
        
        # Model testing
        st.subheader("🧪 Model Testing")
        
        if st.button("🔬 Test Model Connection"):
            with st.spinner("Testing model connection..."):
                # Test model connection
                health_status = check_service_health()
                if health_status.get("Predictor", False):
                    st.success("✅ Model service is running")
                else:
                    st.error("❌ Model service is not available")
        
        if st.button("🎯 Test Prediction"):
            with st.spinner("Testing prediction..."):
                # Test prediction with default values
                test_payload = {
                    "Region": "West",
                    "Soil_Type": "Sandy",
                    "Crop": "Wheat",
                    "Rainfall_mm": 800,
                    "Temperature_Celsius": 25,
                    "Fertilizer_Used": True,
                    "Irrigation_Used": True,
                    "Weather_Condition": "Sunny",
                    "Days_to_Harvest": 120
                }
                
                try:
                    from utils import predict_yield
                    success, result = predict_yield(test_payload)
                    if success:
                        st.success(f"✅ Test prediction successful: {result.get('predicted_yield', 0):.2f} t/ha")
                    else:
                        st.error(f"❌ Test prediction failed: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Test prediction error: {e}")

elif setting_category == "API Settings":
    st.header("🔌 API Configuration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🌐 Service URLs")
        
        # Service URL configuration
        collector_url = st.text_input(
            "Collector URL",
            value=os.environ.get("COLLECTOR_URL", "http://collector:8001"),
            help="URL for the data collector service"
        )
        
        preprocessor_url = st.text_input(
            "Preprocessor URL",
            value=os.environ.get("PREPROCESSOR_URL", "http://preprocessor:8002"),
            help="URL for the data preprocessor service"
        )
        
        predictor_url = st.text_input(
            "Predictor URL",
            value=os.environ.get("PREDICTOR_URL", "http://predictor:8003"),
            help="URL for the prediction service"
        )
        
        interpreter_url = st.text_input(
            "Interpreter URL",
            value=os.environ.get("INTERPRETER_URL", "http://interpreter:8004"),
            help="URL for the explanation service"
        )
        
        ollama_url = st.text_input(
            "Ollama URL",
            value=os.environ.get("OLLAMA_HOST", "http://ollama:11434"),
            help="URL for the Ollama LLM service"
        )
    
    with col2:
        st.subheader("🔧 API Settings")
        
        # Timeout settings
        st.subheader("⏱️ Timeout Settings")
        
        request_timeout = st.slider("Request Timeout (seconds)", 5, 300, 30)
        training_timeout = st.slider("Training Timeout (seconds)", 60, 1800, 600)
        prediction_timeout = st.slider("Prediction Timeout (seconds)", 5, 120, 30)
        
        # Retry settings
        st.subheader("🔄 Retry Settings")
        
        max_retries = st.slider("Max Retries", 1, 5, 3)
        retry_delay = st.slider("Retry Delay (seconds)", 1, 10, 2)
        
        # Connection testing
        st.subheader("🧪 Connection Testing")
        
        if st.button("🔍 Test All Connections"):
            with st.spinner("Testing connections..."):
                health_status = check_service_health()
                
                for service, status in health_status.items():
                    if status:
                        st.success(f"✅ {service}")
                    else:
                        st.error(f"❌ {service}")
        
        if st.button("🔄 Refresh Service Status"):
            st.rerun()

elif setting_category == "System Status":
    st.header("📊 System Status")
    
    # Service health check
    st.subheader("🔧 Service Health")
    
    health_status = check_service_health()
    
    # Create status grid
    status_cols = st.columns(len(health_status))
    for i, (service, status) in enumerate(health_status.items()):
        with status_cols[i]:
            if status:
                st.success(f"✅ {service}")
            else:
                st.error(f"❌ {service}")
    
    # System information
    st.subheader("💻 System Information")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.metric("Python Version", sys.version.split()[0])
        st.metric("Streamlit Version", st.__version__)
        st.metric("Current Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with info_col2:
        st.metric("Environment", "Docker" if os.path.exists("/.dockerenv") else "Local")
        st.metric("Working Directory", os.getcwd())
        st.metric("User", os.environ.get("USER", "Unknown"))
    
    # Resource usage (simulated)
    st.subheader("📈 Resource Usage")
    
    resource_col1, resource_col2, resource_col3 = st.columns(3)
    
    with resource_col1:
        st.metric("CPU Usage", "45%", "5%")
    
    with resource_col2:
        st.metric("Memory Usage", "2.1 GB", "0.3 GB")
    
    with resource_col3:
        st.metric("Disk Usage", "15.2 GB", "1.2 GB")
    
    # Logs section
    st.subheader("📋 System Logs")
    
    log_level = st.selectbox("Log Level", ["INFO", "WARNING", "ERROR", "DEBUG"])
    
    if st.button("📥 Download Logs"):
        # Simulate log download
        log_content = f"""
CropSense System Logs
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Log Level: {log_level}

[INFO] System started successfully
[INFO] All services are running
[INFO] Model loaded successfully
[WARNING] High memory usage detected
[INFO] Prediction completed successfully
"""
        
        st.download_button(
            label="📥 Download Logs",
            data=log_content,
            file_name=f"cropsense_logs_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

elif setting_category == "Data Management":
    st.header("💾 Data Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗂️ Data Storage")
        
        # Data directories
        st.write("**Data Directories:**")
        st.write(f"- Raw Data: `data/raw/`")
        st.write(f"- Processed Data: `data/processed/`")
        st.write(f"- Models: `predictor/models/`")
        st.write(f"- Common Models: `common/models/`")
        
        # Data statistics
        st.subheader("📊 Data Statistics")
        
        # Simulate data statistics
        st.metric("Raw Data Files", "5")
        st.metric("Processed Files", "3")
        st.metric("Model Files", "2")
        st.metric("Total Size", "45.2 MB")
        
        # Data cleanup
        st.subheader("🧹 Data Cleanup")
        
        if st.button("🗑️ Clean Old Data"):
            st.info("This would clean data older than the retention period")
        
        if st.button("🔄 Reset All Data"):
            st.warning("This would delete all data and reset the system")
    
    with col2:
        st.subheader("📤 Data Export")
        
        # Export options
        export_type = st.selectbox(
            "Export Type",
            ["All Data", "Raw Data Only", "Processed Data Only", "Models Only"]
        )
        
        export_format = st.selectbox(
            "Export Format",
            ["ZIP", "TAR", "Individual Files"]
        )
        
        if st.button("📥 Export Data"):
            st.info(f"Exporting {export_type} in {export_format} format...")
        
        # Backup options
        st.subheader("💾 Backup Options")
        
        backup_frequency = st.selectbox(
            "Backup Frequency",
            ["Daily", "Weekly", "Monthly", "Manual"]
        )
        
        backup_location = st.text_input(
            "Backup Location",
            value="/backups/cropsense/",
            help="Directory to store backups"
        )
        
        if st.button("💾 Create Backup"):
            st.info("Creating backup...")
        
        # Restore options
        st.subheader("🔄 Restore Options")
        
        uploaded_backup = st.file_uploader(
            "Upload Backup File",
            type=["zip", "tar"],
            help="Upload a backup file to restore"
        )
        
        if uploaded_backup is not None:
            if st.button("🔄 Restore from Backup"):
                st.warning("This would restore data from the uploaded backup file")

# Render modern footer
render_modern_footer()
