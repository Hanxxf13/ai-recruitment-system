import streamlit as st
import requests
import pandas as pd
import time
import json

# ─── CONFIG & STYLE ───────────────────────────────────────────────────────────
# Use Streamlit Secrets for Cloud Deployment
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="NUKHBA | Elite Selection 🥂", layout="wide")

# Cyber-Luxury Design System: Obsidian & Gold
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,900;1,400&family=Inter:wght@100;300;500;900&family=Amiri:wght@400;700&display=swap');
    
    :root {
        --gold: #D4AF37;
        --gold-glow: rgba(212, 175, 55, 0.4);
        --obsidian: #0A0A0B;
        --charcoal: #1A1A1C;
        --glass: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(212, 175, 55, 0.15);
    }
    
    .stApp {
        background: url("app/static/nukhba_bg.png") no-gradient;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Overlay to ensure readability */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 10, 11, 0.85);
        z-index: -1;
    }
    
    /* Elegant Heading */
    .hero-text {
        font-family: 'Playfair Display', serif;
        color: var(--gold);
        font-size: 4rem;
        line-height: 1;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    
    .sub-hero {
        font-family: 'Inter', sans-serif;
        color: #888;
        font-weight: 100;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-size: 0.9rem;
    }

    /* Glassmorphic Card */
    .glass-card {
        background: var(--glass);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Minimalist Inputs */
    .stTextInput>div>div>input {
        background: transparent !important;
        border: 0px !important;
        border-bottom: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 0px !important;
        padding-left: 0px !important;
        font-weight: 300;
    }
    .stTextInput>div>div>input:focus {
        border-bottom: 1px solid var(--gold) !important;
        box-shadow: none !important;
    }

    /* "Enter the Vault" Button */
    .stButton>button {
        background: linear-gradient(135deg, #B8860B 0%, #D4AF37 50%, #FFD700 100%) !important;
        color: black !important;
        border: none !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        padding: 12px 40px !important;
        border-radius: 50px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 0 20px var(--gold-glow) !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px var(--gold-glow) !important;
    }

    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "user" not in st.session_state: st.session_state.user = None
if "page" not in st.session_state: st.session_state.page = "Auth"

# ─── AUTH PAGE ───────────────────────────────────────────────────────────────
def show_auth():
    # Subtle top spacing
    st.write("##")
    
    col1, padding, col2 = st.columns([1.2, 0.2, 1])
    
    with col1:
        st.markdown('<div style="margin-top: 100px;">', unsafe_allow_html=True)
        st.markdown('<p class="sub-hero">Distinguished Talent Ecosystem</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-text">NUKHBA</h1>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-family: \'Playfair Display\', serif; font-weight: 100; color: white; font-size: 2rem;">The Bridge of Excellence.</h2>', unsafe_allow_html=True)
        st.write("---")
        st.markdown('<p style="color: #666; font-size: 1.1rem; max-width: 80%;">An exclusive sanctuary for elite professionals and visionary recruiters. Secure entry required.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-family: \'Amiri\', serif; font-size: 2.5rem; color: var(--gold); margin-bottom: -15px;">نخبة</p>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: var(--gold); letter-spacing: 2px; font-weight: 300; margin-top: 0px;">ELITE SELECTION</h3>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Registration"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            pwd   = st.text_input("Password", type="password", key="login_pwd")
            if st.button("Login"):
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
        st.markdown('</div>', unsafe_allow_html=True)

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
