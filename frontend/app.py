import streamlit as st
import requests
from styles import inject_premium_css

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Nukhba | Elite Selection", page_icon="💎", layout="wide")
inject_premium_css()

# Header Section
st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 class='nukhba-logo'>نخبة</h1>
        <p class='nukhba-subtitle'>NUKHBA • ELITE SELECTION</p>
    </div>
""", unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Native Streamlit container for the login flow
        with st.container(border=True):
            tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
            
            with tab1:
                st.markdown("### Welcome Back")
                email = st.text_input("Email", placeholder="hr@example.com", key="login_email")
                password = st.text_input("Password", type="password", key="login_pass")
                if st.button("Access Dashboard", use_container_width=True):
                    try:
                        resp = requests.post(f"{API_URL}/users/login", json={
                            "name": "", "email": email, "password": password, "role": ""
                        }, timeout=10)
                        if resp.status_code == 200:
                            st.session_state['user'] = resp.json()
                            st.success(f"Log-in successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please use: hr@example.com / password123")
                    except requests.exceptions.ConnectionError:
                        st.error(f"⚠️ Connection Failed: Backend at {API_URL} is unreachable.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                
                # Forgot Password Section
                with st.expander("🔑 Forgot Password?"):
                    st.write("Reset your elite credentials")
                    reset_email = st.text_input("Your Registered Email", key="reset_email")
                    new_password = st.text_input("New Password", type="password", key="reset_pass")
                    if st.button("Reset Password", use_container_width=True):
                        try:
                            resp = requests.put(f"{API_URL}/users/reset-password", json={
                                "name": "any", "email": reset_email, "password": new_password, "role": "any"
                            })
                            if resp.status_code == 200:
                                st.success("🚀 Password updated! You can now sign in.")
                            else:
                                st.error("Account not found. Please check the email.")
                        except:
                            st.error("Backend offline.")
                
                # Hidden connection health check
                with st.expander("🔍 System Connection Debug"):
                    st.write(f"Testing connectivity to: `{API_URL}`")
                    if st.button("Run Diagnostic"):
                        try:
                            health = requests.get(f"{API_URL}/", timeout=5)
                            st.write(f"✅ Status Code: {health.status_code}")
                            st.success("Backend is reachable!")
                        except Exception as e:
                            st.error(f"❌ Failed: {str(e)}")
                        
            with tab2:
                st.markdown("### Join TalentSpark")
                name_reg = st.text_input("Full Name", placeholder="Jane Doe")
                email_reg = st.text_input("Email", placeholder="jane@example.com")
                pass_reg = st.text_input("Password", type="password", key="reg_pass")
                role_reg = st.selectbox("Account Type", ["Candidate", "HR", "Admin"])
                
                if st.button("Start My Journey", use_container_width=True):
                    try:
                        resp = requests.post(f"{API_URL}/users/register", json={
                            "name": name_reg, "email": email_reg, "password": pass_reg, "role": role_reg
                        }, timeout=5)
                        if resp.status_code == 200:
                            st.success("✨ Welcome aboard! You can now log in.")
                        else:
                            st.error(resp.json().get("detail", "Registration failed."))
                    except:
                        st.error("⚠️ Backend connection failed.")
else:
    user = st.session_state['user']
    st.sidebar.markdown(f"### ✨ {user['name']}")
    st.sidebar.info(f"Role: {user['role']}")
    
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state['user'] = None
        st.rerun()
        
    st.markdown(f"""
        <div style='text-align: center; margin-top: 50px; padding: 40px; background: rgba(255,255,255,0.03); border-radius: 25px;'>
            <h1 style='font-weight: 800; font-size: 3rem;'>Welcome to Nukhba Elite, {user['name']}!</h1>
            <p style='font-size: 1.3rem; opacity: 0.7;'>The future of AI-powered talent intelligence is now in your hands.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Elite Jobs", "154", "12 new")
    with m2:
        st.metric("Top Candidates", "2.8k", "24 screened")
    with m3:
        st.metric("AI Accuracy", "98.4%", "↑ 1.2%")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Quick Navigation")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='elite-card'>
            <h4>🏢 For HR Managers</h4>
            <p>Access your dashboard to post elite roles and review AI screenings.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Recruit Master Dashboard", key="hr_btn"):
            st.switch_page("pages/hr_dashboard.py")
            
    with c2:
        st.markdown("""
        <div class='elite-card'>
            <h4>🚀 For Top Talent</h4>
            <p>Explore opportunities matched specifically to your unique skill profile.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Elite Career Portal", key="cand_btn"):
            st.switch_page("pages/candidate_dashboard.py")
