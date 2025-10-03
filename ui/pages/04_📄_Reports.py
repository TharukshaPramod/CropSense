"""
CropSense Reports - Generate comprehensive reports and exports
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
import json
import base64
from io import BytesIO

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    generate_prediction_report, save_predictions_to_csv,
    create_feature_importance_chart, create_yield_distribution_chart
)

st.set_page_config(
    page_title="CropSense Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Reports & Exports")
st.markdown("Generate comprehensive reports and export your prediction data")

# Initialize session state
if "report_data" not in st.session_state:
    st.session_state.report_data = []

# Sidebar for report options
with st.sidebar:
    st.header("📊 Report Options")
    
    report_type = st.selectbox(
        "Select report type:",
        ["Prediction Summary", "Detailed Analysis", "Custom Report", "Data Export"]
    )
    
    st.markdown("---")
    
    # Report customization
    st.subheader("🎨 Customization")
    
    include_charts = st.checkbox("Include Charts", value=True)
    include_explanations = st.checkbox("Include Explanations", value=True)
    include_statistics = st.checkbox("Include Statistics", value=True)
    
    # Date range selection
    st.subheader("📅 Date Range")
    date_range = st.date_input(
        "Select date range:",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        max_value=datetime.now()
    )

# Main content based on report type
if report_type == "Prediction Summary":
    st.header("📋 Prediction Summary Report")
    
    # Sample data for demonstration
    if not st.session_state.report_data:
        st.info("No prediction data available. Generate some predictions first!")
        
        # Create sample data for demonstration
        if st.button("🎲 Generate Sample Data"):
            sample_predictions = [
                {
                    "timestamp": datetime.now() - timedelta(days=i),
                    "predicted_yield": 3.2 + (i * 0.1),
                    "payload": {
                        "Region": "West",
                        "Soil_Type": "Sandy",
                        "Crop": "Wheat",
                        "Rainfall_mm": 800 + (i * 50),
                        "Temperature_Celsius": 25 + (i * 0.5),
                        "Fertilizer_Used": True,
                        "Irrigation_Used": True,
                        "Weather_Condition": "Sunny",
                        "Days_to_Harvest": 120
                    }
                }
                for i in range(10)
            ]
            
            sample_explanations = [
                {
                    "summary": f"Sample explanation for prediction {i+1}. Key factors include rainfall and temperature.",
                    "top_features": [
                        ("Rainfall_mm", 0.3 + (i * 0.05)),
                        ("Temperature_Celsius", 0.2 + (i * 0.03)),
                        ("Fertilizer_Used", 0.15),
                        ("Soil_Type", 0.1),
                        ("Region", 0.05)
                    ]
                }
                for i in range(10)
            ]
            
            st.session_state.report_data = {
                "predictions": sample_predictions,
                "explanations": sample_explanations
            }
            st.success("✅ Sample data generated!")
            st.rerun()
    
    if st.session_state.report_data:
        predictions = st.session_state.report_data["predictions"]
        explanations = st.session_state.report_data["explanations"]
        
        # Report preview
        st.subheader("📊 Report Preview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Summary statistics
            yields = [p["predicted_yield"] for p in predictions]
            
            st.metric("Total Predictions", len(predictions))
            st.metric("Average Yield", f"{sum(yields)/len(yields):.2f} t/ha")
            st.metric("Yield Range", f"{min(yields):.2f} - {max(yields):.2f} t/ha")
            
            # Yield distribution chart
            if include_charts:
                fig = create_yield_distribution_chart(yields)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Recent predictions
            st.subheader("📈 Recent Predictions")
            recent_df = pd.DataFrame([
                {
                    "Date": p["timestamp"].strftime("%m/%d"),
                    "Yield": f"{p['predicted_yield']:.2f} t/ha",
                    "Crop": p["payload"]["Crop"]
                }
                for p in predictions[-5:]
            ])
            st.dataframe(recent_df, use_container_width=True)
        
        # Detailed predictions table
        st.subheader("📋 Detailed Predictions")
        
        detailed_df = pd.DataFrame([
            {
                "Date": p["timestamp"].strftime("%Y-%m-%d %H:%M"),
                "Region": p["payload"]["Region"],
                "Crop": p["payload"]["Crop"],
                "Rainfall (mm)": p["payload"]["Rainfall_mm"],
                "Temperature (°C)": p["payload"]["Temperature_Celsius"],
                "Predicted Yield (t/ha)": f"{p['predicted_yield']:.2f}"
            }
            for p in predictions
        ])
        
        st.dataframe(detailed_df, use_container_width=True)
        
        # Export options
        st.subheader("📥 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV export
            csv_data = detailed_df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name=f"cropsense_predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # JSON export
            json_data = json.dumps(predictions, default=str, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_data,
                file_name=f"cropsense_predictions_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        with col3:
            # Markdown report
            markdown_report = generate_prediction_report(predictions, explanations)
            st.download_button(
                label="📝 Download Markdown",
                data=markdown_report,
                file_name=f"cropsense_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

elif report_type == "Detailed Analysis":
    st.header("🔍 Detailed Analysis Report")
    
    if st.session_state.report_data:
        predictions = st.session_state.report_data["predictions"]
        explanations = st.session_state.report_data["explanations"]
        
        # Feature importance analysis
        st.subheader("📊 Feature Importance Analysis")
        
        # Aggregate feature importance
        all_features = {}
        for exp in explanations:
            if "top_features" in exp:
                for feature, importance in exp["top_features"]:
                    if feature not in all_features:
                        all_features[feature] = []
                    all_features[feature].append(abs(importance))
        
        # Calculate average importance
        avg_importance = {feature: sum(values)/len(values) for feature, values in all_features.items()}
        sorted_features = sorted(avg_importance.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_features:
            fig = create_feature_importance_chart(sorted_features)
            st.plotly_chart(fig, use_container_width=True)
        
        # Crop analysis
        st.subheader("🌱 Crop Analysis")
        
        crop_data = {}
        for pred in predictions:
            crop = pred["payload"]["Crop"]
            if crop not in crop_data:
                crop_data[crop] = []
            crop_data[crop].append(pred["predicted_yield"])
        
        crop_stats = pd.DataFrame([
            {
                "Crop": crop,
                "Count": len(yields),
                "Avg Yield": f"{sum(yields)/len(yields):.2f} t/ha",
                "Min Yield": f"{min(yields):.2f} t/ha",
                "Max Yield": f"{max(yields):.2f} t/ha"
            }
            for crop, yields in crop_data.items()
        ])
        
        st.dataframe(crop_stats, use_container_width=True)
        
        # Regional analysis
        st.subheader("🌍 Regional Analysis")
        
        region_data = {}
        for pred in predictions:
            region = pred["payload"]["Region"]
            if region not in region_data:
                region_data[region] = []
            region_data[region].append(pred["predicted_yield"])
        
        region_stats = pd.DataFrame([
            {
                "Region": region,
                "Count": len(yields),
                "Avg Yield": f"{sum(yields)/len(yields):.2f} t/ha",
                "Min Yield": f"{min(yields):.2f} t/ha",
                "Max Yield": f"{max(yields):.2f} t/ha"
            }
            for region, yields in region_data.items()
        ])
        
        st.dataframe(region_stats, use_container_width=True)
        
        # Environmental impact analysis
        st.subheader("🌡️ Environmental Impact Analysis")
        
        # Rainfall vs Yield
        rainfall_data = [(p["payload"]["Rainfall_mm"], p["predicted_yield"]) for p in predictions]
        rainfall_df = pd.DataFrame(rainfall_data, columns=["Rainfall", "Yield"])
        
        fig = px.scatter(
            rainfall_df, x="Rainfall", y="Yield",
            title="Rainfall vs Yield Relationship",
            labels={"Rainfall": "Rainfall (mm)", "Yield": "Predicted Yield (t/ha)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Temperature vs Yield
        temp_data = [(p["payload"]["Temperature_Celsius"], p["predicted_yield"]) for p in predictions]
        temp_df = pd.DataFrame(temp_data, columns=["Temperature", "Yield"])
        
        fig = px.scatter(
            temp_df, x="Temperature", y="Yield",
            title="Temperature vs Yield Relationship",
            labels={"Temperature": "Temperature (°C)", "Yield": "Predicted Yield (t/ha)"}
        )
        st.plotly_chart(fig, use_container_width=True)

elif report_type == "Custom Report":
    st.header("🎨 Custom Report Builder")
    
    st.markdown("Build a custom report with your specific requirements.")
    
    # Report sections
    st.subheader("📋 Report Sections")
    
    sections = st.multiselect(
        "Select sections to include:",
        [
            "Executive Summary",
            "Prediction Overview",
            "Feature Analysis",
            "Crop Performance",
            "Regional Analysis",
            "Environmental Impact",
            "Recommendations",
            "Technical Details"
        ],
        default=["Executive Summary", "Prediction Overview", "Feature Analysis"]
    )
    
    # Report format
    st.subheader("📄 Report Format")
    
    format_col1, format_col2 = st.columns(2)
    
    with format_col1:
        report_format = st.radio(
            "Choose format:",
            ["Markdown", "HTML", "PDF (Coming Soon)"]
        )
    
    with format_col2:
        include_appendix = st.checkbox("Include Appendix", value=True)
        include_charts = st.checkbox("Include Charts", value=True)
    
    # Generate custom report
    if st.button("🔨 Generate Custom Report", type="primary"):
        if st.session_state.report_data:
            predictions = st.session_state.report_data["predictions"]
            explanations = st.session_state.report_data["explanations"]
            
            # Build custom report
            report_content = f"""
# CropSense Custom Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            if "Executive Summary" in sections:
                report_content += """
## Executive Summary

This report provides a comprehensive analysis of crop yield predictions generated by the CropSense AI system. The analysis covers {} predictions across multiple crops and regions, providing insights into yield patterns and key influencing factors.

Key Findings:
- Average predicted yield: {:.2f} tons/hectare
- Yield range: {:.2f} - {:.2f} tons/hectare
- Most influential factors: Rainfall, Temperature, Soil Type

""".format(
                    len(predictions),
                    sum(p["predicted_yield"] for p in predictions) / len(predictions),
                    min(p["predicted_yield"] for p in predictions),
                    max(p["predicted_yield"] for p in predictions)
                )
            
            if "Prediction Overview" in sections:
                report_content += """
## Prediction Overview

The system generated {} predictions with the following distribution:

""".format(len(predictions))
                
                # Add prediction statistics
                yields = [p["predicted_yield"] for p in predictions]
                report_content += f"- Mean yield: {sum(yields)/len(yields):.2f} t/ha\n"
                report_content += f"- Standard deviation: {pd.Series(yields).std():.2f} t/ha\n"
                report_content += f"- Coefficient of variation: {pd.Series(yields).std()/pd.Series(yields).mean():.3f}\n\n"
            
            if "Feature Analysis" in sections:
                report_content += """
## Feature Analysis

The following features were identified as most influential in yield predictions:

"""
                # Add feature importance
                all_features = {}
                for exp in explanations:
                    if "top_features" in exp:
                        for feature, importance in exp["top_features"]:
                            if feature not in all_features:
                                all_features[feature] = []
                            all_features[feature].append(abs(importance))
                
                avg_importance = {feature: sum(values)/len(values) for feature, values in all_features.items()}
                sorted_features = sorted(avg_importance.items(), key=lambda x: x[1], reverse=True)
                
                for i, (feature, importance) in enumerate(sorted_features[:5], 1):
                    report_content += f"{i}. {feature}: {importance:.3f}\n"
                
                report_content += "\n"
            
            if "Recommendations" in sections:
                report_content += """
## Recommendations

Based on the analysis, the following recommendations are made:

1. **Optimize Irrigation**: Ensure adequate water supply during critical growth periods
2. **Soil Management**: Focus on soil health and nutrient balance
3. **Weather Monitoring**: Implement real-time weather monitoring for better predictions
4. **Crop Rotation**: Consider crop rotation strategies for improved yields
5. **Technology Adoption**: Leverage AI predictions for decision-making

"""
            
            # Display report preview
            st.subheader("📄 Report Preview")
            st.markdown(report_content)
            
            # Download options
            st.subheader("📥 Download Report")
            
            if report_format == "Markdown":
                st.download_button(
                    label="📝 Download Markdown Report",
                    data=report_content,
                    file_name=f"cropsense_custom_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
            elif report_format == "HTML":
                # Create HTML content without f-string backslash issues
                html_style = """
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #2E8B57; }
        h2 { color: #4ECDC4; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
"""
                html_body = report_content.replace('#', '<h1>').replace('##', '<h2>').replace('\n', '<br>')
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>CropSense Custom Report</title>
    <style>{html_style}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
                st.download_button(
                    label="🌐 Download HTML Report",
                    data=html_content,
                    file_name=f"cropsense_custom_report_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )
        else:
            st.warning("No data available for report generation. Please generate some predictions first.")

elif report_type == "Data Export":
    st.header("📊 Data Export")
    
    if st.session_state.report_data:
        predictions = st.session_state.report_data["predictions"]
        
        # Export options
        st.subheader("📥 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Raw data export
            st.subheader("📋 Raw Data")
            
            raw_data = []
            for pred in predictions:
                raw_data.append({
                    "timestamp": pred["timestamp"],
                    "predicted_yield": pred["predicted_yield"],
                    **pred["payload"]
                })
            
            raw_df = pd.DataFrame(raw_data)
            
            # CSV export
            csv_data = raw_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Raw CSV",
                data=csv_data,
                file_name=f"cropsense_raw_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # JSON export
            json_data = json.dumps(raw_data, default=str, indent=2)
            st.download_button(
                label="📄 Download Raw JSON",
                data=json_data,
                file_name=f"cropsense_raw_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        with col2:
            # Processed data export
            st.subheader("🔧 Processed Data")
            
            # Summary statistics
            summary_data = {
                "total_predictions": len(predictions),
                "average_yield": sum(p["predicted_yield"] for p in predictions) / len(predictions),
                "min_yield": min(p["predicted_yield"] for p in predictions),
                "max_yield": max(p["predicted_yield"] for p in predictions),
                "std_yield": pd.Series([p["predicted_yield"] for p in predictions]).std(),
                "generated_at": datetime.now().isoformat()
            }
            
            # Summary CSV
            summary_df = pd.DataFrame([summary_data])
            summary_csv = summary_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Summary CSV",
                data=summary_csv,
                file_name=f"cropsense_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Summary JSON
            summary_json = json.dumps(summary_data, indent=2)
            st.download_button(
                label="📄 Download Summary JSON",
                data=summary_json,
                file_name=f"cropsense_summary_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        # Data preview
        st.subheader("👀 Data Preview")
        st.dataframe(raw_df.head(10), use_container_width=True)
        
        # Data quality check
        st.subheader("🔍 Data Quality Check")
        
        quality_metrics = {
            "Total Records": len(raw_df),
            "Missing Values": raw_df.isnull().sum().sum(),
            "Duplicate Records": raw_df.duplicated().sum(),
            "Data Completeness": f"{((len(raw_df) - raw_df.isnull().sum().sum()) / (len(raw_df) * len(raw_df.columns)) * 100):.1f}%"
        }
        
        for metric, value in quality_metrics.items():
            st.metric(metric, value)
    
    else:
        st.info("No data available for export. Please generate some predictions first.")

# Footer
st.markdown("---")
st.markdown("🌾 **CropSense Reports** - Comprehensive reporting and data export")
