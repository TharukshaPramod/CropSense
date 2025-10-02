"""
Utility functions for CropSense UI
"""
import os
import requests
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Service URLs (work both in Docker and locally via env overrides)
COLLECTOR_URL = os.environ.get("COLLECTOR_URL", "http://collector:8001")
PREPROCESSOR_URL = os.environ.get("PREPROCESSOR_URL", "http://preprocessor:8002")
PREDICTOR_URL = os.environ.get("PREDICTOR_URL", "http://predictor:8003")
INTERPRETER_URL = os.environ.get("INTERPRETER_URL", "http://interpreter:8004")
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

def check_service_health() -> Dict[str, bool]:
    """Check health of all services"""
    services = {
        "Collector": f"{COLLECTOR_URL}/health",
        "Preprocessor": f"{PREPROCESSOR_URL}/health",
        "Predictor": f"{PREDICTOR_URL}/health",
        "Interpreter": f"{INTERPRETER_URL}/health",
        "Ollama": f"{OLLAMA_URL}/api/tags"
    }
    
    health_status = {}
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=3)
            health_status[name] = response.status_code == 200
        except Exception:
            health_status[name] = False
    
    return health_status

def collect_data() -> Tuple[bool, str]:
    """Collect data from source"""
    try:
        response = requests.post(f"{COLLECTOR_URL}/collect", 
                               json={"source": "local"}, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            return True, result.get("path", "Data collected successfully")
        else:
            return False, f"Collection failed: {response.text}"
    except Exception as e:
        return False, f"Collection error: {e}"

def preprocess_data() -> Tuple[bool, str]:
    """Preprocess collected data"""
    try:
        response = requests.post(f"{PREPROCESSOR_URL}/preprocess", 
                               json={}, 
                               timeout=180)
        if response.status_code == 200:
            result = response.json()
            return True, result.get("features_path", "Preprocessing completed")
        else:
            return False, f"Preprocessing failed: {response.text}"
    except Exception as e:
        return False, f"Preprocessing error: {e}"

def train_model() -> Tuple[bool, Dict]:
    """Train the ML model"""
    try:
        response = requests.post(f"{PREDICTOR_URL}/train", 
                               json={}, 
                               timeout=600)
        if response.status_code == 200:
            result = response.json()
            return True, result
        else:
            return False, {"error": f"Training failed: {response.text}"}
    except Exception as e:
        return False, {"error": f"Training error: {e}"}

def predict_yield(payload: Dict) -> Tuple[bool, Dict]:
    """Predict crop yield"""
    try:
        response = requests.post(f"{PREDICTOR_URL}/predict", 
                               json=payload, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            return True, result
        else:
            return False, {"error": f"Prediction failed: {response.text}"}
    except Exception as e:
        return False, {"error": f"Prediction error: {e}"}

def explain_prediction(payload: Dict) -> Tuple[bool, Dict]:
    """Get prediction explanation"""
    try:
        response = requests.post(f"{INTERPRETER_URL}/explain", 
                               json=payload, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            return True, result
        else:
            return False, {"error": f"Explanation failed: {response.text}"}
    except Exception as e:
        return False, {"error": f"Explanation error: {e}"}

def create_feature_importance_chart(features: List[Tuple[str, float]]) -> go.Figure:
    """Create feature importance chart"""
    if not features:
        return go.Figure()
    
    feature_names, importance_values = zip(*features)
    
    fig = go.Figure(data=[
        go.Bar(
            x=importance_values,
            y=feature_names,
            orientation='h',
            marker_color=['#FF6B6B' if x < 0 else '#4ECDC4' for x in importance_values],
            text=[f"{x:.3f}" for x in importance_values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Feature Importance Analysis",
        xaxis_title="Impact on Yield",
        yaxis_title="Features",
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def create_yield_distribution_chart(predictions: List[float]) -> go.Figure:
    """Create yield distribution chart"""
    fig = go.Figure(data=[
        go.Histogram(
            x=predictions,
            nbinsx=20,
            marker_color='#4ECDC4',
            opacity=0.7
        )
    ])
    
    fig.update_layout(
        title="Yield Prediction Distribution",
        xaxis_title="Predicted Yield (tons/hectare)",
        yaxis_title="Frequency",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def create_metrics_dashboard(metrics: Dict) -> None:
    """Create metrics dashboard"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Mean Absolute Error",
            value=f"{metrics.get('mae', 0):.4f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Root Mean Square Error",
            value=f"{metrics.get('rmse', 0):.4f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="R² Score",
            value=f"{metrics.get('r2', 0):.4f}",
            delta=None
        )

def generate_prediction_report(predictions: List[Dict], explanations: List[Dict]) -> str:
    """Generate a comprehensive prediction report"""
    report = f"""
# CropSense Prediction Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
Total Predictions: {len(predictions)}

## Predictions
"""
    
    for i, (pred, exp) in enumerate(zip(predictions, explanations), 1):
        report += f"""
### Prediction {i}
- **Predicted Yield**: {pred.get('predicted_yield', 'N/A'):.2f} tons/hectare
- **Input Parameters**:
  - Region: {pred.get('Region', 'N/A')}
  - Soil Type: {pred.get('Soil_Type', 'N/A')}
  - Crop: {pred.get('Crop', 'N/A')}
  - Rainfall: {pred.get('Rainfall_mm', 'N/A')} mm
  - Temperature: {pred.get('Temperature_Celsius', 'N/A')}°C
  - Fertilizer Used: {pred.get('Fertilizer_Used', 'N/A')}
  - Irrigation Used: {pred.get('Irrigation_Used', 'N/A')}

### Key Insights
{exp.get('summary', 'No explanation available')}

---
"""
    
    return report

def save_predictions_to_csv(predictions: List[Dict], filename: str = None) -> str:
    """Save predictions to CSV"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cropsense_predictions_{timestamp}.csv"
    
    df = pd.DataFrame(predictions)
    df.to_csv(filename, index=False)
    return filename

def load_sample_data() -> pd.DataFrame:
    """Load sample data for demonstration"""
    return pd.DataFrame({
        "Region": ["West", "East", "North", "South"] * 5,
        "Soil_Type": ["Sandy", "Loam", "Clay", "Silt"] * 5,
        "Crop": ["Wheat", "Rice", "Soybean", "Barley"] * 5,
        "Rainfall_mm": [800, 1200, 600, 900] * 5,
        "Temperature_Celsius": [25, 28, 22, 26] * 5,
        "Fertilizer_Used": [True, True, False, True] * 5,
        "Irrigation_Used": [True, False, True, True] * 5,
        "Weather_Condition": ["Sunny", "Cloudy", "Rainy", "Sunny"] * 5,
        "Days_to_Harvest": [120, 140, 110, 130] * 5,
    })
