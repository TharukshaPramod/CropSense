# ui/pages/00_🔐_Login.py - LOGIN PAGE ONLY
import streamlit as st
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_utils import login, signup, is_authenticated, logout, current_user
from modern_footer import render_modern_footer
import re

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide")

st.title("🔐 Login / Signup")

tab_login, tab_signup = st.tabs(["Login", "Sign up"])

with tab_login:
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Email / Username").strip()
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary")
        if submitted:
            ok, msg = login(username, password)
            if ok:
                st.success("✅ Logged in")
                st.rerun()
            else:
                st.error(f"❌ {msg}")

with tab_signup:
    st.subheader("Create Account")
    with st.form("signup_form"):
        username_s = st.text_input("Email", key="signup_user").strip()
        password_s = st.text_input("Password", type="password", key="signup_pw")
        password_s2 = st.text_input("Confirm Password", type="password", key="signup_pw2")
        admin_code = st.text_input("Admin invite code (optional)", type="password")
        submitted_s = st.form_submit_button("Sign up", type="primary")
        if submitted_s:
            # Validations
            if not username_s:
                st.error("❌ Email is required")
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", username_s):
                st.error("❌ Enter a valid email address")
            elif len(password_s) < 8:
                st.error("❌ Password must be at least 8 characters")
            elif len(password_s) > 64:
                st.error("❌ Password must be at most 64 characters")
            elif password_s != password_s2:
                st.error("❌ Passwords do not match")
            elif not re.search(r"[A-Za-z]", password_s) or not re.search(r"\d", password_s):
                st.error("❌ Password must include letters and numbers")
            else:
                # Ensure bcrypt-safe length on client side as well (truncate >72 bytes)
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
                        st.success("✅ Admin account created. You can log in now.")
                    else:
                        st.success("✅ Account created. You can log in now.")
                else:
                    st.error(f"❌ {msg}")

st.markdown("---")
if is_authenticated():
    st.info(f"Logged in as: {current_user()}")
    if st.button("Logout"):
        logout()
        st.success("Logged out")
        st.rerun()

# Render modern footer
render_modern_footer()