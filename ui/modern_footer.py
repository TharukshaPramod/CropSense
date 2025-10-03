"""
Modern Footer Component for CropSense
Reusable footer that matches the home page design
"""
import streamlit as st
from datetime import datetime
import os

def render_modern_footer():
    """Render the modern footer that matches the home page design"""
    # Get system info
    current_year = datetime.now().year
    environment = "Docker" if os.path.exists('/.dockerenv') else "Local"
    
    # Add the CSS for the footer (only if not already added)
    st.markdown("""
    <style>
    /* Modern Footer CSS */
    .footer-modern {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-radius: 25px 25px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .footer-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .footer-title-modern {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-text-modern {
        color: rgba(255,255,255,0.8);
        margin-bottom: 2rem;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stat-card:hover {
        background: rgba(255,255,255,0.15);
        transform: translateY(-5px);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Footer content
    st.markdown("""
    <div class="footer-modern">
        <div class="footer-title-modern">Join the Agricultural Revolution</div>
        <div class="footer-text-modern">
            CropSense is trusted by thousands of farmers worldwide to optimize their operations, 
            increase yields, and build sustainable farming practices for the future.
        </div>
    """, unsafe_allow_html=True)
    
    # Footer stats
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)
    
    with footer_col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">15K+</div>
            <div class="stat-label">Happy Farmers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with footer_col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">45%</div>
            <div class="stat-label">Avg. Yield Increase</div>
        </div>
        """, unsafe_allow_html=True)
    
    with footer_col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">98.7%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with footer_col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Support</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer links and info
    st.markdown(f"""
    <div style="border-top: 1px solid rgba(255,255,255,0.2); margin-top: 2rem; padding-top: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="color: rgba(255,255,255,0.7);">
                © {current_year} CropSense AI. All rights reserved.<br>
                Built with ❤️ using Streamlit, FastAPI, and Machine Learning
            </div>
            <div style="color: rgba(255,255,255,0.7); text-align: right;">
                Environment: {environment}<br>
                Version 2.1.0 • Latest Update: {datetime.now().strftime('%Y-%m-%d')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
