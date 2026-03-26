import streamlit as st
import requests
from styles import inject_premium_css

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="TalentSpark AI", page_icon="✨", layout="wide")
inject_premium_css()

# Header Section
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            ✨ TalentSpark AI
        </h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>The Next-Gen Intelligent Recruitment Ecosystem</p>
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
                        }, timeout=5)
                        if resp.status_code == 200:
                            st.session_state['user'] = resp.json()
                            st.success(f"Log-in successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Try: hr@example.com / password123")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Backend is offline. Please start your FastAPI server.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        
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
        <div style='text-align: center; margin-top: 50px;'>
            <h2>Welcome to TalentSpark, {user['name']}!</h2>
            <p>Your AI-powered career journey starts here.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("👈 **HR Managers**: Use the sidebar to access 'HR Dashboard' to post jobs and review AI-screened candidates.")
    with c2:
        st.info("👈 **Candidates**: Use the sidebar to access 'Candidate Dashboard' to find jobs and track your applications.")
