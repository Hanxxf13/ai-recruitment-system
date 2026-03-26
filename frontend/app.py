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
        <div style='text-align: center; margin-top: 50px;'>
            <h2>Welcome to Nukhba, {user['name']}!</h2>
            <p>Your elite AI-powered recruitment journey starts here.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("👈 **HR Managers**: Use the sidebar to access 'HR Dashboard' to post jobs and review AI-screened candidates.")
    with c2:
        st.info("👈 **Candidates**: Use the sidebar to access 'Candidate Dashboard' to find jobs and track your applications.")
