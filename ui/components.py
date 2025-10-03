"""
CropSense UI Components - FIXED VERSION
Beautiful, modern components for the CropSense application
"""
import streamlit as st
from datetime import datetime
import os

def inject_all_css():
    """Inject ALL CSS at once at the beginning"""
    css = """
    <style>
    /* Hero Section Styles */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .hero-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: white;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        line-height: 1.5;
    }
    .feature-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        height: 100%;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        opacity: 0.8;
        line-height: 1.4;
    }
    
    /* Footer Section Styles */
    .footer-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        margin-top: 3rem;
        border-radius: 15px;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
    }
    .footer-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: white;
    }
    .footer-text {
        color: rgba(255,255,255,0.9);
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    .footer-stats {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .stat-item {
        text-align: center;
        margin: 0.5rem;
    }
    .stat-number {
        font-size: 1.2rem;
        font-weight: bold;
        color: #f0f8ff;
    }
    .stat-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    .footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.2);
        margin-top: 1rem;
        padding-top: 1rem;
        text-align: center;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Showcase Section Styles */
    .showcase-container {
        padding: 2rem 0;
        margin: 2rem 0;
    }
    .showcase-title {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #2E8B57;
        margin-bottom: 1rem;
    }
    .showcase-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    .feature-item {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #4ECDC4;
        height: 100%;
    }
    .showcase-feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .showcase-feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2E8B57;
        margin-bottom: 0.5rem;
    }
    .showcase-feature-desc {
        color: #666;
        line-height: 1.6;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_hero_section():
    """Render a beautiful hero section"""
    # Inject ALL CSS at the beginning
    inject_all_css()
    
    # Hero section
    with st.container():
        st.markdown("""
        <div class="hero-container">
            <div class="hero-logo">🌾</div>
            <h1 class="hero-title">CropSense</h1>
            <p class="hero-subtitle">AI-Powered Crop Yield Prediction System<br>Transform your farming with intelligent insights and data-driven decisions</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔮</div>
                <div class="feature-title">Smart Predictions</div>
                <div class="feature-desc">Advanced ML models for accurate yield forecasting</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌱</div>
                <div class="feature-title">Sustainable Farming</div>
                <div class="feature-desc">Optimize resources for better environmental impact</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Real-time Analysis</div>
                <div class="feature-desc">Live monitoring and comprehensive data insights</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Performance Tracking</div>
                <div class="feature-desc">Monitor trends and improve your farming strategies</div>
            </div>
            """, unsafe_allow_html=True)
        
        # CTA buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 Get Started", key="hero_get_started", use_container_width=True):
                st.info("Navigate to Dashboard to get started!")
        with col2:
            if st.button("🔮 Make Predictions", key="hero_predictions", use_container_width=True):
                st.info("Navigate to Predictions page to make predictions!")
        with col3:
            if st.button("📊 View Analysis", key="hero_analysis", use_container_width=True):
                st.info("Navigate to Analysis page to view insights!")

def render_feature_showcase():
    """Render a feature showcase section"""
    # CSS is already injected by hero section
    
    with st.container():
        st.markdown("""
        <div class="showcase-container">
            <h2 class="showcase-title">Why Choose CropSense?</h2>
            <p class="showcase-subtitle">Our cutting-edge AI technology combines machine learning, weather data, and agricultural expertise to deliver unparalleled crop yield predictions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature items
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-item">
                <div class="showcase-feature-icon">🤖</div>
                <div class="showcase-feature-title">Advanced AI Models</div>
                <div class="showcase-feature-desc">State-of-the-art machine learning algorithms trained on extensive agricultural datasets to provide the most accurate predictions.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-item">
                <div class="showcase-feature-icon">📱</div>
                <div class="showcase-feature-title">User-Friendly Interface</div>
                <div class="showcase-feature-desc">Intuitive dashboard designed for farmers of all technical levels, making advanced AI accessible to everyone.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-item">
                <div class="showcase-feature-icon">📊</div>
                <div class="showcase-feature-title">Comprehensive Analytics</div>
                <div class="showcase-feature-desc">Detailed reports and visualizations help you understand the factors influencing your crop yields and optimize accordingly.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-item">
                <div class="showcase-feature-icon">🌤️</div>
                <div class="showcase-feature-title">Real-time Weather Integration</div>
                <div class="showcase-feature-desc">Seamlessly integrated weather APIs provide up-to-date environmental data for more precise yield forecasting.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-item">
                <div class="showcase-feature-icon">🔒</div>
                <div class="showcase-feature-title">Secure & Reliable</div>
                <div class="showcase-feature-desc">Enterprise-grade security with 99.9% uptime guarantee, ensuring your data is safe and the system is always available.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-item">
                <div class="showcase-feature-icon">🌍</div>
                <div class="showcase-feature-title">Global Coverage</div>
                <div class="showcase-feature-desc">Support for multiple crops, regions, and farming practices worldwide, making it suitable for diverse agricultural needs.</div>
            </div>
            """, unsafe_allow_html=True)

def render_modern_footer():
    """Render a beautiful, modern footer"""
    # CSS is already injected by hero section
    
    current_year = datetime.now().year
    environment = "Docker" if os.path.exists('/.dockerenv') else "Local"
    
    with st.container():
        st.markdown('<div class="footer-container">', unsafe_allow_html=True)
        
        # Brand section
        st.markdown('<div class="footer-title">🌾 CropSense</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-text">Revolutionizing agriculture with AI-powered crop yield prediction. Our advanced machine learning models help farmers optimize their harvests and make data-driven decisions for sustainable farming.</div>', unsafe_allow_html=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="stat-item"><div class="stat-number">99.2%</div><div class="stat-label">Accuracy</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-item"><div class="stat-number">10K+</div><div class="stat-label">Predictions</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stat-item"><div class="stat-number">500+</div><div class="stat-label">Farmers</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="stat-item"><div class="stat-number">24/7</div><div class="stat-label">Support</div></div>', unsafe_allow_html=True)
        
        # Footer bottom
        st.markdown(f'<div class="footer-bottom">© {current_year} CropSense. All rights reserved. | Built with ❤️ using Streamlit, FastAPI, and Machine Learning | Environment: {environment}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)