import streamlit as st
import requests
import pandas as pd
import time
import json

# ─── CONFIG & STYLE ───────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"

st.set_page_config(page_title="NUKHBA | Elite Selection 🥂", layout="wide")

# Obsidian & Gold Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;500;900&display=swap');
    
    :root {
        --gold: #D4AF37;
        --obsidian: #0A0A0B;
        --glass: rgba(255, 255, 255, 0.03);
    }
    
    .main { background-color: var(--obsidian); color: white; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        background: linear-gradient(135deg, var(--gold), #B8860B); 
        color: black; border: none; font-weight: 900; 
        border-radius: 4px; padding: 10px 24px;
    }
    h1, h2, h3 { font-family: 'Amiri', serif; color: var(--gold); }
    .card { background: var(--glass); border: 1px solid rgba(212, 175, 55, 0.2); padding: 20px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "user" not in st.session_state: st.session_state.user = None
if "page" not in st.session_state: st.session_state.page = "Auth"

# ─── AUTH PAGE ───────────────────────────────────────────────────────────────
def show_auth():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("ELITE • SELECTION")
        st.subheader("NUKHBA")
        st.write("Welcome to the bridge of distinguished talent.")
        
    with col2:
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            pwd   = st.text_input("Password", type="password", key="login_pwd")
            if st.button("✨ Enter the Vault"):
                try:
                    res = requests.post(f"{API_URL}/users/login", json={"email":email, "password":pwd, "name":"", "role":""})
                    if res.status_code == 200:
                        st.session_state.user = res.json()
                        st.success(f"Welcome back, {st.session_state.user['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else: st.error("Invalid credentials")
                except: st.error("Backend not reachable")
                
        with tab2:
            st.info("Registration is currently direct (Email + Password only).")
            reg_name = st.text_input("Full Name")
            reg_role = st.selectbox("Role", ["Candidate", "HR", "Admin"])
            reg_email = st.text_input("Email Address")
            reg_pwd = st.text_input("Choose Password", type="password")
            
            if st.button("💎 Join the Elite"):
                if not reg_name or not reg_email or not reg_pwd:
                    st.warning("Please fill all fields")
                else:
                    try:
                        res = requests.post(f"{API_URL}/users/register", 
                                            json={"name":reg_name, "email":reg_email, "password":reg_pwd, "role":reg_role})
                        if res.status_code == 200:
                            st.success("Account created! Signing you in...")
                            st.session_state.user = res.json()
                            time.sleep(1)
                            st.rerun()
                        else: st.error(res.json().get("detail", "Registration failed"))
                    except Exception as e: st.error(f"Error: {e}")

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
def show_dashboard():
    u = st.session_state.user
    st.sidebar.title(f"👑 {u['name']}")
    st.sidebar.write(f"Role: {u['role']}")
    if st.sidebar.button("Logout"): 
        st.session_state.user = None
        st.rerun()
        
    if u['role'] in ['HR', 'Admin']:
        st.title("HR Command Center")
        st.markdown('<div class="card">Manage candidates and job openings.</div>', unsafe_allow_html=True)
        # Dashboard logic...
    else:
        st.title("Candidate Career Portal")
        st.markdown('<div class="card">Track your applications and elite opportunities.</div>', unsafe_allow_html=True)

# ─── MAIN ────────────────────────────────────────────────────────────────────
if st.session_state.user is None:
    show_auth()
else:
    show_dashboard()
