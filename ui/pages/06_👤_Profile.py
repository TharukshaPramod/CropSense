import streamlit as st
import os, sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_utils import is_authenticated, current_user, current_role, load_profile, save_profile, logout
from modern_footer import render_modern_footer

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

# Custom CSS for enhanced profile page
st.markdown("""
<style>
.profile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
}

.profile-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
    border-left: 5px solid #667eea;
}

.stats-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    margin: 0.5rem;
}

.stats-number {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.stats-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

.avatar-large {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid white;
    margin: 0 auto 1rem auto;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    color: white;
}

.profile-section {
    margin-bottom: 2rem;
}

.section-title {
    color: #2c3e50;
    border-bottom: 2px solid #667eea;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    font-size: 1.5rem;
}

.activity-item {
    padding: 1rem;
    border-left: 3px solid #667eea;
    background: #f8f9fa;
    margin-bottom: 0.5rem;
    border-radius: 0 8px 8px 0;
}

.activity-time {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

def get_user_avatar(name):
    """Generate avatar based on user name"""
    if not name:
        return "👤"
    return name[0].upper()

def get_user_stats(username):
    """Get user statistics - you can expand this with real data"""
    return {
        "farms_managed": 3,
        "total_acres": 1250,
        "predictions_made": 47,
        "data_uploads": 12
    }

def get_recent_activity(username):
    """Get recent user activity"""
    return [
        {"action": "Updated farm data", "time": "2 hours ago"},
        {"action": "Ran yield prediction", "time": "1 day ago"},
        {"action": "Viewed analytics", "time": "2 days ago"},
        {"action": "Updated profile", "time": "1 week ago"}
    ]

def main():
    if not is_authenticated():
        st.warning("🔐 Please login from the Login page to access your profile.")
        st.stop()

    username = current_user()
    role = current_role()
    
    # Load profile data
    profile = load_profile(username) or {}
    
    # Profile Header
    st.markdown(f"""
    <div class="profile-header">
        <div class="avatar-large">
            {get_user_avatar(profile.get('full_name', username))}
        </div>
        <h1 style="margin-bottom: 0.5rem;">{profile.get('full_name', username)}</h1>
        <p style="opacity: 0.9; margin-bottom: 0.5rem;">{profile.get('organization', 'Agricultural Professional')}</p>
        <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; display: inline-block;">
            <strong>Role:</strong> {role} | <strong>Username:</strong> {username}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Profile Information Section
        st.markdown('<div class="section-title">📝 Profile Information</div>', unsafe_allow_html=True)
        
        with st.form("profile_form", clear_on_submit=False):
            st.subheader("Personal Details")
            
            col1a, col1b = st.columns(2)
            with col1a:
                full_name = st.text_input(
                    "Full Name *", 
                    value=profile.get("full_name", ""),
                    placeholder="Enter your full name"
                )
                
            with col1b:
                organization = st.text_input(
                    "Organization",
                    value=profile.get("organization", ""),
                    placeholder="Your farm or company name"
                )
            
            st.subheader("Agricultural Preferences")
            col2a, col2b = st.columns(2)
            with col2a:
                # Default region selection
                region_options = ["Select region", "West", "East", "North", "South", "Midwest", "Southwest"]
                current_region = profile.get("default_region", "")
                region_index = region_options.index(current_region) if current_region in region_options else 0
                default_region = st.selectbox("Default Region *", region_options, index=region_index)
                
            with col2b:
                # Default crop selection
                crop_options = ["Select crop", "Wheat", "Rice", "Soybean", "Barley", "Corn", "Cotton", "Other"]
                current_crop = profile.get("default_crop", "")
                crop_index = crop_options.index(current_crop) if current_crop in crop_options else 0
                default_crop = st.selectbox("Primary Crop *", crop_options, index=crop_index)
            
            # Display additional info (read-only since they're not in save_profile)
            st.subheader("Account Information")
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.text_input("Username", value=username, disabled=True)
                st.text_input("Role", value=role, disabled=True)
            with info_col2:
                # Show email (username is email in your system)
                st.text_input("Email", value=username, disabled=True)
                st.text_input("Member Since", value="2024", disabled=True)
            
            # Form submission
            submitted = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)
            
            if submitted:
                # Basic validation
                if not full_name:
                    st.error("❌ Please fill in your full name")
                elif default_region == "Select region" or default_crop == "Select crop":
                    st.error("❌ Please select a valid region and primary crop")
                else:
                    # Extract values from dropdowns (remove "Select" options)
                    region_value = default_region if default_region != "Select region" else ""
                    crop_value = default_crop if default_crop != "Select crop" else ""
                    
                    # Call save_profile with only the supported parameters
                    save_profile(
                        username=username,
                        full_name=full_name,
                        organization=organization,
                        default_region=region_value,
                        default_crop=crop_value
                    )
                    st.success("✅ Profile saved successfully!")
                    st.rerun()
    
    with col2:
        # User Statistics
        st.markdown('<div class="section-title">📊 Your Statistics</div>', unsafe_allow_html=True)
        
        stats = get_user_stats(username)
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{stats['farms_managed']}</div>
                <div class="stats-label">Farms Managed</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{stats['total_acres']}</div>
                <div class="stats-label">Total Acres</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{stats['predictions_made']}</div>
                <div class="stats-label">Predictions</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{stats['data_uploads']}</div>
                <div class="stats-label">Data Uploads</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent Activity
        st.markdown('<div class="section-title">📈 Recent Activity</div>', unsafe_allow_html=True)
        
        activities = get_recent_activity(username)
        for activity in activities:
            st.markdown(f"""
            <div class="activity-item">
                <div>{activity['action']}</div>
                <div class="activity-time">{activity['time']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Update Farm Data", use_container_width=True):
            st.info("Navigate to Farm Management to update your data")
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Navigate to Analytics dashboard")
        
        if st.button("🌤️ Check Weather", use_container_width=True):
            st.info("Navigate to Weather Insights")
    
    # Account Management Section
    st.markdown("---")
    st.markdown('<div class="section-title">⚙️ Account Management</div>', unsafe_allow_html=True)
    
    acc_col1, acc_col2, acc_col3 = st.columns(3)
    
    with acc_col1:
        if st.button("🔐 Change Password", use_container_width=True):
            st.info("Password change functionality coming soon!")
    
    with acc_col2:
        if st.button("📧 Contact Support", use_container_width=True):
            st.info("Email: support@cropsense.ai")
    
    with acc_col3:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.success("👋 Logged out successfully!")
            st.rerun()
    
    # Display current profile data for debugging (optional)
    with st.expander("🔍 Debug: View Raw Profile Data"):
        st.json(profile)

if __name__ == "__main__":
    main()
    render_modern_footer()