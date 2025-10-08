# ui/pages/06_👑_Admin.py - FIXED ADMIN PANEL
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_utils import is_authenticated, current_user, current_role
from modern_footer import render_modern_footer

st.set_page_config(
    page_title="CropSense Admin",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIXED ADMIN CSS
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid;
        margin: 0.5rem;
        text-align: center;
    }
    
    .metric-card-warning { border-left-color: #ff9800; }
    .metric-card-success { border-left-color: #4CAF50; }
    .metric-card-info { border-left-color: #2196F3; }
    .metric-card-danger { border-left-color: #f44336; }
    
    .user-table {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .system-health {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .admin-action-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .admin-action-card:hover {
        transform: translateY(-5px);
        border-color: #667eea;
    }
    
    .action-card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .action-card-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    
    .action-card-description {
        font-size: 0.9rem;
        color: #666;
        line-height: 1.4;
    }
    
    /* Ensure proper text wrapping */
    .metric-card h3 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# AUTHENTICATION AND PERMISSION CHECK
if not is_authenticated():
    st.error("🔐 Authentication required. Please log in to access the admin panel.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/00_🔐_Login.py")
    st.stop()

if current_role() != "admin":
    st.error("🚫 Access Denied. Administrator privileges required.")
    st.info("You need to be an administrator to access this page.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/01_Dashboard.py")
    st.stop()

# SAMPLE DATA GENERATION
def generate_sample_data():
    """Generate sample data for the admin panel"""
    # Sample users data
    users_data = {
        'user_id': range(1, 51),
        'username': [f'user{i}@example.com' for i in range(1, 51)],
        'role': ['user'] * 45 + ['admin'] * 5,
        'status': ['active'] * 40 + ['inactive'] * 8 + ['suspended'] * 2,
        'registration_date': [datetime.now() - timedelta(days=x) for x in range(50, 0, -1)],
        'last_login': [datetime.now() - timedelta(hours=x*12) for x in range(50)],
        'predictions_made': [x * 3 for x in range(50, 0, -1)]
    }
    
    # System metrics
    system_metrics = {
        'total_users': 50,
        'active_users': 40,
        'predictions_today': 127,
        'system_uptime': '99.8%',
        'avg_response_time': '245ms',
        'storage_used': '2.3GB/10GB',
        'api_requests': '12,457',
        'error_rate': '0.2%'
    }
    
    return pd.DataFrame(users_data), system_metrics

# Load sample data
users_df, system_metrics = generate_sample_data()

# ADMIN HEADER
st.markdown(f"""
<div class="admin-header">
    <h1>👑 CropSense Admin Panel</h1>
    <p>Welcome, Administrator {current_user()}! Manage your AI agriculture platform</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">👑</div>
        <h3 style="margin: 0; color: #2E8B57;">Admin Console</h3>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">CropSense Administration</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("🔄 Refresh All Data", use_container_width=True):
        st.rerun()
    
    if st.button("📊 Generate Reports", use_container_width=True):
        st.success("📈 Reports generated successfully!")
    
    if st.button("🔧 System Check", use_container_width=True):
        st.info("🛠️ System check completed!")
    
    st.markdown("---")
    
    st.markdown("### 📈 Real-time Stats")
    st.metric("Active Users", "40", "5")
    st.metric("Predictions Today", "127", "12")
    st.metric("System Load", "45%", "-3%")
    
    st.markdown("---")
    
    st.markdown("### 👤 Admin Info")
    st.write(f"**User:** {current_user()}")
    st.write(f"**Role:** Administrator")
    st.write(f"**Last Access:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    if st.button("🚪 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/01_Dashboard.py")

# MAIN ADMIN CONTENT
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 User Management", "⚙️ System Settings", "📈 Analytics"])

with tab1:
    st.markdown("### 🏠 Admin Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-success">
            <h3>{system_metrics['total_users']}</h3>
            <p>Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-info">
            <h3>{system_metrics['active_users']}</h3>
            <p>Active Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-warning">
            <h3>{system_metrics['predictions_today']}</h3>
            <p>Predictions Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card metric-card-danger">
            <h3>{system_metrics['error_rate']}</h3>
            <p>Error Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        # User registration trend
        st.subheader("📈 User Registration Trend")
        registration_trend = users_df.groupby(
            users_df['registration_date'].dt.date
        ).size().reset_index(name='count')
        
        fig_reg = px.line(
            registration_trend, 
            x='registration_date', 
            y='count',
            title="Daily User Registrations",
            labels={'registration_date': 'Date', 'count': 'New Users'}
        )
        st.plotly_chart(fig_reg, use_container_width=True)
    
    with col2:
        # User status distribution
        st.subheader("📊 User Status Distribution")
        status_counts = users_df['status'].value_counts()
        
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="User Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Quick Actions - FIXED LAYOUT
    st.markdown("### ⚡ Quick Admin Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        st.markdown("""
        <div class="admin-action-card">
            <div class="action-card-icon">👥</div>
            <div class="action-card-title">User Management</div>
            <div class="action-card-description">Manage users and permissions</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Users", key="manage_users", use_container_width=True):
            st.info("Navigating to User Management...")
    
    with action_col2:
        st.markdown("""
        <div class="admin-action-card">
            <div class="action-card-icon">📊</div>
            <div class="action-card-title">Analytics</div>
            <div class="action-card-description">View system analytics and reports</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Analytics", key="view_analytics", use_container_width=True):
            st.info("Navigating to Analytics...")
    
    with action_col3:
        st.markdown("""
        <div class="admin-action-card">
            <div class="action-card-icon">⚙️</div>
            <div class="action-card-title">Settings</div>
            <div class="action-card-description">System configuration and setup</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Configure", key="configure", use_container_width=True):
            st.info("Navigating to Settings...")
    
    with action_col4:
        st.markdown("""
        <div class="admin-action-card">
            <div class="action-card-icon">🔒</div>
            <div class="action-card-title">Security</div>
            <div class="action-card-description">Security and access controls</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Security", key="security", use_container_width=True):
            st.info("Navigating to Security...")

with tab2:
    st.markdown("### 👥 User Management")
    
    # User search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search Users", placeholder="Enter username or email")
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "active", "inactive", "suspended"])
    
    with col3:
        role_filter = st.selectbox("Filter by Role", ["All", "user", "admin"])
    
    # Filter users
    filtered_users = users_df.copy()
    if search_query:
        filtered_users = filtered_users[filtered_users['username'].str.contains(search_query, case=False)]
    if status_filter != "All":
        filtered_users = filtered_users[filtered_users['status'] == status_filter]
    if role_filter != "All":
        filtered_users = filtered_users[filtered_users['role'] == role_filter]
    
    # User table
    st.markdown("#### 📋 User List")
    
    # Display user table
    display_df = filtered_users[['username', 'role', 'status', 'registration_date', 'last_login', 'predictions_made']].copy()
    display_df['registration_date'] = display_df['registration_date'].dt.strftime('%Y-%m-%d')
    display_df['last_login'] = display_df['last_login'].dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # User actions
    st.markdown("#### 🛠️ User Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_user = st.selectbox("Select User", filtered_users['username'].tolist())
        user_role = filtered_users[filtered_users['username'] == selected_user]['role'].iloc[0]
        user_status = filtered_users[filtered_users['username'] == selected_user]['status'].iloc[0]
    
    with col2:
        st.write(f"**Current Role:** {user_role}")
        st.write(f"**Current Status:** {user_status}")
    
    with col3:
        if st.button("🔄 Toggle Role", use_container_width=True):
            st.success(f"Role toggled for {selected_user}")
        
        if st.button("🚫 Suspend User", use_container_width=True):
            st.warning(f"User {selected_user} suspended")
        
        if st.button("🗑️ Delete User", use_container_width=True, type="secondary"):
            st.error(f"User {selected_user} deleted")

with tab3:
    st.markdown("### ⚙️ System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 General Settings")
        
        st.text_input("System Name", value="CropSense AI")
        st.text_area("System Description", value="AI-Powered Crop Yield Prediction System")
        st.number_input("Session Timeout (minutes)", min_value=5, max_value=480, value=30)
        st.selectbox("Default Language", ["English", "Spanish", "French", "German"])
        
        if st.button("💾 Save General Settings", use_container_width=True):
            st.success("General settings saved!")
    
    with col2:
        st.markdown("#### 🔒 Security Settings")
        
        st.number_input("Password Minimum Length", min_value=6, max_value=20, value=8)
        st.checkbox("Require Special Characters", value=True)
        st.checkbox("Enable Two-Factor Authentication", value=False)
        st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
        
        if st.button("🔐 Save Security Settings", use_container_width=True):
            st.success("Security settings saved!")
    
    st.markdown("#### 🗃️ Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Backup Database", use_container_width=True):
            st.info("Database backup initiated...")
    
    with col2:
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.info("Cache cleared successfully!")
    
    with col3:
        if st.button("📊 Reset Analytics", use_container_width=True):
            st.warning("Analytics data reset!")

with tab4:
    st.markdown("### 📈 Advanced Analytics")
    
    # Performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 System Performance")
        
        # CPU Usage
        st.metric("CPU Usage", "45%", "-2%")
        st.progress(45)
        
        # Memory Usage
        st.metric("Memory Usage", "68%", "5%")
        st.progress(68)
        
        # Disk Usage
        st.metric("Disk Usage", "23%", "1%")
        st.progress(23)
    
    with col2:
        st.subheader("📊 Prediction Analytics")
        
        # Prediction success rate
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 98.7,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Prediction Accuracy"},
            delta = {'reference': 97.5},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 90], 'color': "lightgray"},
                    {'range': [90, 100], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 99}}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # API Usage
    st.subheader("🌐 API Usage Statistics")
    
    # Sample API data
    api_data = pd.DataFrame({
        'endpoint': ['/predict', '/weather', '/soil', '/crops', '/analytics'],
        'requests': [1250, 890, 670, 450, 320],
        'avg_response_time': [245, 120, 180, 200, 350],
        'error_rate': [0.2, 0.1, 0.3, 0.4, 0.5]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_api = px.bar(
            api_data, 
            x='endpoint', 
            y='requests',
            title="API Requests by Endpoint",
            color='requests',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_api, use_container_width=True)
    
    with col2:
        fig_response = px.bar(
            api_data, 
            x='endpoint', 
            y='avg_response_time',
            title="Average Response Time (ms)",
            color='avg_response_time',
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_response, use_container_width=True)

# Render modern footer
render_modern_footer()

# Add some sample data export functionality
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📤 Data Export")
    
    if st.button("📄 Export User Data", use_container_width=True):
        st.success("User data exported successfully!")
    
    if st.button("📊 Export Analytics", use_container_width=True):
        st.success("Analytics data exported successfully!")