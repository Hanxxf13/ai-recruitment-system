import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Recruitment Platform", page_icon="🚀", layout="wide")

st.title("🌟 AI Talent Intelligence Platform")
st.markdown("---")

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            # Mock login call against register/login endpoint 
            # (Note: proper Auth would use OAuth2 Password Bearer)
            try:
                # We use the login endpoint we made
                resp = requests.post(f"{API_URL}/users/login", json={
                    "name": "", "email": email, "password": password, "role": ""
                })
                if resp.status_code == 200:
                    st.session_state['user'] = resp.json()
                    st.success(f"Welcome back, {st.session_state['user']['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            except Exception as e:
                st.error("Backend Server is not running. Please start the API.")
                
    with tab2:
        st.subheader("Create an Account")
        name_reg = st.text_input("Full Name")
        email_reg = st.text_input("Email Address")
        pass_reg = st.text_input("Password", type="password")
        role_reg = st.selectbox("Role", ["Candidate", "HR", "Admin"])
        
        if st.button("Register"):
            resp = requests.post(f"{API_URL}/users/register", json={
                "name": name_reg,
                "email": email_reg,
                "password": pass_reg,
                "role": role_reg
            })
            if resp.status_code == 200:
                st.success("Account created successfully! Please login.")
            else:
                st.error(resp.json().get("detail", "Error creating account"))
else:
    user = st.session_state['user']
    st.sidebar.title(f"Welcome, {user['name']}")
    st.sidebar.text(f"Role: {user['role']}")
    
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.rerun()
        
    st.markdown("### Please select your dashboard from the sidebar menu to the left.")
    st.info("👈 Navigate to 'candidate_dashboard' or 'hr_dashboard' based on your role.")
