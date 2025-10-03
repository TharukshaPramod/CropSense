import streamlit as st
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_utils import is_authenticated, current_user, current_role, load_profile, save_profile, logout
from modern_footer import render_modern_footer

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

st.title("👤 Profile")

if not is_authenticated():
    st.warning("Please login from the 🔐 Login page.")
    st.stop()

username = current_user()
role = current_role()
st.info(f"User: {username} | Role: {role}")

profile = load_profile(username) or {}

with st.form("profile_form"):
    full_name = st.text_input("Full Name", value=profile.get("full_name", ""))
    organization = st.text_input("Organization", value=profile.get("organization", ""))
    default_region = st.selectbox("Default Region", ["West", "East", "North", "South"], index=0 if not profile.get("default_region") else ["West","East","North","South"].index(profile.get("default_region")))
    default_crop = st.selectbox("Default Crop", ["Wheat", "Rice", "Soybean", "Barley", "Corn", "Cotton"], index=0 if not profile.get("default_crop") else ["Wheat","Rice","Soybean","Barley","Corn","Cotton"].index(profile.get("default_crop")))
    submitted = st.form_submit_button("Save", type="primary")
    if submitted:
        save_profile(username, full_name, organization, default_region, default_crop)
        st.success("✅ Profile saved")

st.markdown("---")
if st.button("Logout"):
    logout()
    st.success("Logged out")
    st.rerun()

# Render modern footer
render_modern_footer()





