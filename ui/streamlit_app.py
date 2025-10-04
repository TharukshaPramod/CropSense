"""
CropSense - AI-powered Crop Yield Prediction System
MODERN & ADVANCED VERSION
"""
import streamlit as st
import os
import sys
from datetime import datetime
import random

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure page FIRST - CRITICAL
st.set_page_config(
    page_title="CropSense - AI Crop Yield Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MODERN CSS WITH ANIMATIONS AND GRADIENTS
css = """
<style>
/* ===== HIDE DEFAULT FOOTER & STYLING ===== */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* Make the default header blend better */
.stApp [data-testid="stToolbar"] {
    opacity: 0.7;
    color: #2E8B57 !important;
    font-size: 0.9rem;
    transition: opacity 0.3s ease;
}
.stApp [data-testid="stToolbar"]:hover {
    opacity: 1;
}

/* Modern Color Variables */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
    --glass-effect: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
}

/* Hero Section - Modern Design */
.hero-modern {
    background: var(--primary-gradient);
    color: white;
    padding: 4rem 2rem;
    border-radius: 25px;
    margin-bottom: 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.hero-modern::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 50px 50px;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(1deg); }
}

.hero-logo-modern {
    font-size: 5rem;
    margin-bottom: 1.5rem;
    animation: bounce 2s ease-in-out infinite;
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.2));
}

@keyframes bounce {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-10px) scale(1.05); }
}

.hero-title-modern {
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    background: linear-gradient(45deg, #fff, #f0f8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.hero-subtitle-modern {
    font-size: 1.4rem;
    margin-bottom: 3rem;
    opacity: 0.9;
    line-height: 1.6;
    font-weight: 300;
}

/* Glass Morphism Cards */
.glass-card {
    background: var(--glass-effect);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    padding: 2rem;
    border-radius: 20px;
    margin: 1rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s ease;
}

.glass-card:hover::before {
    left: 100%;
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

.feature-icon-modern {
    font-size: 3rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2));
}

.feature-title-modern {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: white;
}

.feature-desc-modern {
    font-size: 1rem;
    opacity: 0.9;
    line-height: 1.5;
}

/* Modern Footer */
.footer-modern {
    background: var(--dark-gradient);
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
    background: var(--success-gradient);
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

/* Animated Stats */
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

/* Showcase Section */
.showcase-modern {
    padding: 4rem 0;
    margin: 3rem 0;
    position: relative;
}

.showcase-title-modern {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #2E8B57, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.showcase-subtitle-modern {
    text-align: center;
    font-size: 1.3rem;
    color: #666;
    margin-bottom: 3rem;
    line-height: 1.6;
}

.feature-card-modern {
    background: white;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 1.5rem 0;
    border-left: 5px solid;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.feature-card-modern::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(78, 205, 196, 0.05), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.feature-card-modern:hover::before {
    opacity: 1;
}

.feature-card-modern:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.feature-icon-showcase {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    filter: drop-shadow(0 5px 10px rgba(0,0,0,0.1));
}

.feature-title-showcase {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.feature-desc-showcase {
    color: #666;
    line-height: 1.7;
    font-size: 1.1rem;
}

/* Gradient Borders */
.gradient-border-1 { border-left-color: #667eea; }
.gradient-border-2 { border-left-color: #f093fb; }
.gradient-border-3 { border-left-color: #4facfe; }
.gradient-border-4 { border-left-color: #43e97b; }
.gradient-border-5 { border-left-color: #fa709a; }
.gradient-border-6 { border-left-color: #ffecd2; }

/* Modern Button Styles */
.stButton > button {
    background: var(--primary-gradient);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 1rem 2rem;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Pulse Animation */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Floating Elements */
.floating {
    animation: floating 3s ease-in-out infinite;
}

@keyframes floating {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title-modern { font-size: 2.5rem; }
    .hero-subtitle-modern { font-size: 1.1rem; }
    .showcase-title-modern { font-size: 2rem; }
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# NOW import other modules
try:
    from auth_utils import is_authenticated
    from utils import check_service_health
except ImportError as e:
    def is_authenticated():
        return False
    def check_service_health():
        return {"Collector": False, "Preprocessor": False, "Predictor": False, "Interpreter": False}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# MODERN HERO SECTION
st.markdown("""
<div class="hero-modern">
    <div class="hero-logo-modern floating">🌾</div>
    <div class="hero-title-modern">CropSense</div>
    <div class="hero-subtitle-modern">
        AI-Powered Precision Agriculture Platform<br>
        Harness the power of machine learning to transform your farming operations
    </div>
</div>
""", unsafe_allow_html=True)

# INTERACTIVE FEATURE CARDS
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Why Farmers Choose CropSense?
    </h2>
    <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;">
        Experience the future of agriculture with our cutting-edge AI solutions
    </p>
</div>
""", unsafe_allow_html=True)

# Feature cards in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div class="feature-icon-modern">🤖</div>
        <div class="feature-title-modern">AI-Powered Insights</div>
        <div class="feature-desc-modern">Advanced machine learning algorithms provide accurate yield predictions and actionable insights</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div class="feature-icon-modern">🌦️</div>
        <div class="feature-title-modern">Smart Weather</div>
        <div class="feature-desc-modern">Real-time weather integration with predictive analytics for optimal planting and harvesting</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <div class="feature-icon-modern">📊</div>
        <div class="feature-title-modern">Data Analytics</div>
        <div class="feature-desc-modern">Comprehensive dashboards and reports to track performance and optimize operations</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="glass-card">
        <div class="feature-icon-modern">🔒</div>
        <div class="feature-title-modern">Secure & Scalable</div>
        <div class="feature-desc-modern">Enterprise-grade security with cloud scalability for farms of all sizes</div>
    </div>
    """, unsafe_allow_html=True)

# CTA SECTION WITH MODERN BUTTONS
st.markdown("""
<div style="text-align: center; margin: 4rem 0;">
    <h3 style="font-size: 2rem; margin-bottom: 2rem; color: #2c3e50;">Ready to Transform Your Farming?</h3>
</div>
""", unsafe_allow_html=True)

cta_col1, cta_col2, cta_col3 = st.columns(3)
with cta_col1:
    if st.button("🚀 Start Free Trial", key="cta_trial", use_container_width=True):
        st.success("🎉 Free trial activated! Explore all features for 14 days.")
with cta_col2:
    if st.button("📞 Book Demo", key="cta_demo", use_container_width=True):
        st.info("📅 Our team will contact you to schedule a personalized demo.")
with cta_col3:
    if st.button("🌾 View Case Studies", key="cta_cases", use_container_width=True):
        st.info("📚 Check out success stories from farmers using CropSense.")

# REAL-TIME METRICS DASHBOARD
st.markdown("""
<div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 2rem; border-radius: 20px; margin: 3rem 0;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3 style="font-size: 2rem; font-weight: 700; color: #2c3e50;">Live System Performance</h3>
        <p style="color: #666;">Real-time metrics from our global farming network</p>
    </div>
""", unsafe_allow_html=True)

# Animated metrics
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.markdown("""
    <div class="stat-card pulse">
        <div class="stat-number">15.2K</div>
        <div class="stat-label">Active Farms</div>
    </div>
    """, unsafe_allow_html=True)

with metrics_col2:
    st.markdown("""
    <div class="stat-card pulse">
        <div class="stat-number">98.7%</div>
        <div class="stat-label">Prediction Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with metrics_col3:
    st.markdown("""
    <div class="stat-card pulse">
        <div class="stat-number">2.4M</div>
        <div class="stat-label">Acres Monitored</div>
    </div>
    """, unsafe_allow_html=True)

with metrics_col4:
    st.markdown("""
    <div class="stat-card pulse">
        <div class="stat-number">45%</div>
        <div class="stat-label">Yield Increase</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌾</div>
        <h3 style="margin: 0; color: #2E8B57;">CropSense</h3>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">AI Agriculture Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CLEAR HOME NAVIGATION BUTTON
    if st.button("🏠 **Return to Home**", use_container_width=True, type="primary"):
        st.rerun()
    
    st.markdown("## 🧭 Navigation")
    
    # Remove "💰 Commercialization" from main app navigation since it's now a separate page
    default_page = "🏠 Dashboard" if is_authenticated() else "🔐 Login"
    page_options = ["🔐 Login", "👤 Profile", "🏠 Dashboard", "🔮 Predictions", "📊 Analysis", "📄 Reports", "⚙️ Settings"]
    
    page = st.selectbox("Select a page:", page_options, index=page_options.index(default_page))
    
    st.markdown("---")
    st.markdown("## 📈 Live Metrics")
    
    # Mini metrics in sidebar
    st.metric("System Health", "Optimal", "2%")
    st.metric("Active Users", "1,247", "34")
    st.metric("Predictions Today", "892", "67")
    
    st.markdown("---")
    st.markdown("## 🔧 Quick Actions")
    
    if st.button("🔄 Refresh Data", key="sidebar_refresh", use_container_width=True):
        st.rerun()
    
    if st.button("📊 Generate Report", key="sidebar_report", use_container_width=True):
        st.info("Report generation started...")
    
    if st.button("🌤️ Weather Update", key="sidebar_weather", use_container_width=True):
        st.info("Fetching latest weather data...")
    
    st.markdown("---")
    st.markdown("## 🏆 Achievements")
    
    st.progress(75)
    st.caption("Profile Completion: 75%")
    
    st.progress(90)
    st.caption("AI Model Accuracy: 90%")
    
    st.progress(60)
    st.caption("Data Coverage: 60%")

# MAIN CONTENT BASED ON PAGE SELECTION
if page == "🔐 Login":
    st.info("Use the Login page in the sidebar (page is separate).")
    
elif page == "👤 Profile":
    st.info("Use the Profile page in the sidebar (page is separate).")
    
elif page == "🏠 Dashboard":
    # ENHANCED SHOWCASE SECTION
    st.markdown("""
    <div class="showcase-modern">
        <div class="showcase-title-modern">Advanced Features</div>
        <div class="showcase-subtitle-modern">
            Discover how CropSense leverages cutting-edge technology to revolutionize agriculture
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card-modern gradient-border-1">
            <div class="feature-icon-showcase">🧠</div>
            <div class="feature-title-showcase">Neural Network Predictions</div>
            <div class="feature-desc-showcase">
                Our deep learning models analyze historical data, weather patterns, and soil conditions 
                to provide accurate yield predictions with 98.7% accuracy.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card-modern gradient-border-3">
            <div class="feature-icon-showcase">🛰️</div>
            <div class="feature-title-showcase">Satellite Imaging</div>
            <div class="feature-desc-showcase">
                High-resolution satellite imagery combined with computer vision algorithms 
                to monitor crop health, growth stages, and potential issues in real-time.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card-modern gradient-border-5">
            <div class="feature-icon-showcase">📱</div>
            <div class="feature-title-showcase">Mobile Integration</div>
            <div class="feature-desc-showcase">
                Access all features on-the-go with our mobile app. Receive alerts, 
                view reports, and make decisions from anywhere in the world.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card-modern gradient-border-2">
            <div class="feature-icon-showcase">🤝</div>
            <div class="feature-title-showcase">Collaborative Farming</div>
            <div class="feature-desc-showcase">
                Connect with other farmers, share insights, and collaborate on best practices 
                through our secure community platform.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card-modern gradient-border-4">
            <div class="feature-icon-showcase">💸</div>
            <div class="feature-title-showcase">Cost Optimization</div>
            <div class="feature-desc-showcase">
                AI-powered recommendations for resource allocation, reducing waste and 
                maximizing ROI while maintaining sustainable practices.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card-modern gradient-border-6">
            <div class="feature-icon-showcase">🌍</div>
            <div class="feature-title-showcase">Global Market Insights</div>
            <div class="feature-desc-showcase">
                Access real-time market prices, demand forecasts, and export opportunities 
                to make informed business decisions.
            </div>
        </div>
        """, unsafe_allow_html=True)

# MODERN FOOTER
current_year = datetime.now().year
environment = "Docker" if os.path.exists('/.dockerenv') else "Local"

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

# ADDITIONAL MODERN ELEMENTS

# Testimonial Section
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem; border-radius: 20px; margin: 3rem 0; text-align: center;">
    <h3 style="font-size: 2rem; margin-bottom: 2rem;">What Farmers Say</h3>
    <div style="font-size: 1.2rem; font-style: italic; margin-bottom: 2rem;">
        "CropSense increased our yield by 45% and reduced water usage by 30%. The AI predictions are incredibly accurate!"
    </div>
    <div style="font-weight: bold;">- Raj Kumar, Farm Owner</div>
</div>
""", unsafe_allow_html=True)

# Newsletter Signup
with st.expander("📰 Stay Updated with CropSense"):
    col1, col2 = st.columns([2, 1])
    with col1:
        email = st.text_input("Enter your email for updates:", placeholder="your.email@example.com")
    with col2:
        if st.button("Subscribe", use_container_width=True):
            if email:
                st.success("🎉 Thank you for subscribing! We'll keep you updated.")
            else:
                st.warning("Please enter your email address.")