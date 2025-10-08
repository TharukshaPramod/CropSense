# ui/simple_auth.py - FALLBACK AUTH FOR STREAMLIT CLOUD
import streamlit as st
import os

def is_authenticated():
    """Check if user is authenticated - fallback version"""
    return st.session_state.get("auth_user") is not None

def current_user():
    """Get current authenticated user - fallback version"""
    return st.session_state.get("auth_user")

def current_role():
    """Get current user role - fallback version"""
    return st.session_state.get("auth_role", "user")

def login(username: str, password: str) -> tuple[bool, str]:
    """Login user - fallback version"""
    # Simple demo authentication
    if username == "admin" and password == "admin":
        st.session_state["auth_user"] = username
        st.session_state["auth_role"] = "admin"
        return True, "Login successful"
    elif username == "user" and password == "user":
        st.session_state["auth_user"] = username
        st.session_state["auth_role"] = "user"
        return True, "Login successful"
    else:
        return False, "Invalid credentials"

def signup(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    """Signup user - fallback version"""
    # Simple demo signup
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    # In a real app, you'd store this in a database
    return True, "Account created successfully"

def logout():
    """Clear authentication session - fallback version"""
    for k in ["auth_user", "auth_role"]:
        if k in st.session_state:
            del st.session_state[k]