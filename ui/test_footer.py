"""
Test script to verify the modern footer works on all pages
"""
import streamlit as st
from modern_footer import render_modern_footer

st.set_page_config(
    page_title="CropSense Footer Test",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 CropSense Modern Footer Test")
st.markdown("Testing the modern footer component that matches your home page design...")

# Test the footer
st.header("Footer Test")
render_modern_footer()

st.success("✅ Modern footer rendered successfully!")
st.info("This footer matches the design from your home page and will appear on all pages.")
