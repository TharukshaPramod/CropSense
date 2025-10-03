# ui/auth_utils.py - STREAMLIT AUTHENTICATION HELPERS
import streamlit as st
from typing import Optional
import os, sys

# Ensure project root is on path to import `common`
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from common.auth import create_user, authenticate_user, create_access_token, get_profile, upsert_profile, get_user_row

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return bool(st.session_state.get("auth_user"))

def current_user() -> Optional[str]:
    """Get current authenticated user"""
    return st.session_state.get("auth_user")

def current_role() -> str:
    """Get current user role"""
    return st.session_state.get("auth_role", "user")

def login(username: str, password: str) -> tuple[bool, str]:
    """Login user with better error handling"""
    try:
        if authenticate_user(username, password):
            st.session_state["auth_user"] = username
            row = get_user_row(username)
            st.session_state["auth_role"] = row[3] if row else "user"
            st.session_state["auth_token"] = create_access_token(username)
            return True, "Login successful"
        return False, "Invalid username or password"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def signup(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    """Signup user with better error handling"""
    try:
        # Additional client-side validation
        if not username or not password:
            return False, "Username and password are required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Check if username looks like an email (basic validation)
        if '@' not in username:
            return False, "Please use your email as username"
        
        create_user(username, password, role=role)
        return True, "Account created successfully"
        
    except ValueError as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            return False, "Username already exists"
        else:
            return False, error_msg
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def logout():
    """Clear authentication session"""
    for k in ["auth_user", "auth_role", "auth_token"]:
        if k in st.session_state:
            del st.session_state[k]

def load_profile(username: str):
    """Load user profile"""
    return get_profile(username)

def save_profile(username: str, full_name: str | None, organization: str | None, default_region: str | None, default_crop: str | None):
    """Save user profile"""
    upsert_profile(username, full_name, organization, default_region, default_crop)