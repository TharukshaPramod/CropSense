# ui/pages/00_🔐_Login.py - FIXED BACKGROUND AND FOOTER
import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_utils import login, signup, is_authenticated, logout, current_user
from modern_footer import render_modern_footer
import re

st.set_page_config(
    page_title="CropSense Login",
    page_icon="🔐", 
    layout="centered"
)

# FIXED CSS - PROPER BACKGROUND AND FOOTER
st.markdown("""
<style>
    /* Fix background for entire page */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh;
    }
    
    /* Center the content but keep footer full width */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 1rem;
        max-width: 500px;
    }
    
    /* Simple white card */
    .login-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 0 auto;
        max-width: 500px;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem auto;
        max-width: 500px;
    }
    
    /* Make footer container full width */
    .main .block-container:last-child {
        max-width: none !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Ensure footer content is centered but container is full width */
    .footer-container {
        width: 100%;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication and redirect
if is_authenticated():
    st.markdown(f"""
    <div class="success-box">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
        <h2>Welcome back, {current_user()}!</h2>
        <p>You are already logged in.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Go to Dashboard", use_container_width=True, type="primary"):
            st.session_state.redirect_to_dashboard = True
            st.rerun()
    
    if st.session_state.get('redirect_to_dashboard'):
        st.session_state.redirect_to_dashboard = False
        st.switch_page("streamlit_app.py")
    
    st.stop()

# Initialize session state
if 'show_redirect_button' not in st.session_state:
    st.session_state.show_redirect_button = False

# MAIN LOGIN CONTENT
st.markdown("""
<div class="login-card">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌾</div>
        <h1 style="color: #2E8B57; margin-bottom: 0.5rem;">CropSense</h1>
        <p style="color: #666; margin-bottom: 0;">AI-Powered Crop Yield Prediction</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["🔐 **Login**", "📝 **Sign Up**"])

with tab1:
    if st.session_state.show_redirect_button:
        st.success("✅ Login successful! Click below to go to your dashboard.")
        if st.button("🚀 Continue to Dashboard", type="primary", use_container_width=True):
            st.session_state.redirect_to_dashboard = True
            st.session_state.show_redirect_button = False
            st.rerun()
    
    with st.form("login_form"):
        st.subheader("Welcome Back 👋")
        
        username = st.text_input(
            "**📧 Email / Username**", 
            placeholder="Enter your email or username"
        ).strip()
        
        password = st.text_input(
            "**🔒 Password**", 
            type="password", 
            placeholder="Enter your password"
        )
        
        submitted = st.form_submit_button(
            "🚀 **Login to Dashboard**", 
            type="primary", 
            use_container_width=True
        )
        
        if submitted:
            if not username or not password:
                st.error("❌ Please fill in all fields")
            else:
                with st.spinner("🔐 Authenticating..."):
                    ok, msg = login(username, password)
                    if ok:
                        st.session_state.show_redirect_button = True
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

with tab2:
    with st.form("signup_form"):
        st.subheader("Create Account 🌟")
        
        username_s = st.text_input(
            "**📧 Email Address**", 
            placeholder="your.email@example.com"
        ).strip()
        
        password_s = st.text_input(
            "**🔒 Password**", 
            type="password", 
            placeholder="Create a strong password (min. 8 characters)"
        )
        
        password_s2 = st.text_input(
            "**🔒 Confirm Password**", 
            type="password", 
            placeholder="Re-enter your password"
        )
        
        admin_code = st.text_input(
            "**👑 Admin Code (Optional)**", 
            type="password",
            placeholder="Enter admin invite code if available"
        )
        
        submitted_s = st.form_submit_button(
            "🌟 **Create Account**", 
            type="primary", 
            use_container_width=True
        )
        
        if submitted_s:
            # Validations
            if not username_s:
                st.error("❌ Email is required")
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", username_s):
                st.error("❌ Please enter a valid email address")
            elif len(password_s) < 8:
                st.error("❌ Password must be at least 8 characters")
            elif len(password_s) > 64:
                st.error("❌ Password must be at most 64 characters")
            elif password_s != password_s2:
                st.error("❌ Passwords do not match")
            elif not re.search(r"[A-Za-z]", password_s) or not re.search(r"\d", password_s):
                st.error("❌ Password must include both letters and numbers")
            else:
                with st.spinner("Creating your account..."):
                    # Ensure bcrypt-safe length
                    pw_bytes = password_s.encode("utf-8")
                    if len(pw_bytes) > 72:
                        password_s = pw_bytes[:72].decode("utf-8", errors="ignore")

                    # Determine role via invite code
                    invite = (admin_code or "").strip()
                    expected = os.environ.get("CROPSENSE_ADMIN_INVITE_CODE", "ADMIN2025")
                    role = "admin" if invite and invite == expected else "user"
                    
                    ok, msg = signup(username_s, password_s, role=role)
                    if ok:
                        if role == "admin":
                            st.success("✅ Admin account created successfully! You can now log in.")
                        else:
                            st.success("✅ Account created successfully! You can now log in.")
                        st.balloons()
                        st.info("💡 Please switch to the Login tab to access your account.")
                    else:
                        st.error(f"❌ {msg}")

# Close login card
st.markdown("</div>", unsafe_allow_html=True)

# Simple footer info
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: white;">
    <p>🔒 Your data is securely encrypted and protected</p>
</div>
""", unsafe_allow_html=True)

# Help section
with st.expander("ℹ️ Need Help?"):
    st.markdown("""
    **Having trouble logging in?**
    
    - Ensure you're using the correct email and password
    - Passwords must be at least 8 characters with letters and numbers
    - Forgot your password? Contact support for assistance
    
    **New to CropSense?**
    
    - Sign up for a free account to get started
    - No credit card required for the trial period
    - Access all basic features immediately
    """)

# Create a container for the footer to ensure full width
st.markdown('<div class="footer-container">', unsafe_allow_html=True)

# Render your existing modern footer
render_modern_footer()

# Close footer container
st.markdown('</div>', unsafe_allow_html=True)

# Handle redirect
if st.session_state.get('redirect_to_dashboard'):
    st.session_state.redirect_to_dashboard = False
    st.session_state.show_redirect_button = False
    st.switch_page("streamlit_app.py")