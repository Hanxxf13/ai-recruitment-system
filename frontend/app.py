import streamlit as st
import requests
from styles import inject_premium_css

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title=" Elite Selection", page_icon="💎", layout="wide")
inject_premium_css()

# Header Section
st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 class='nukhba-logo'>نخبة</h1>
        <p class='nukhba-subtitle'>ELITE • SELECTION</p>
    </div>
""", unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    # Use 2 columns to mimic the split screen image
    pane_left, pane_right = st.columns([1.5, 1], gap="large")
    
    with pane_left:
        # Side image with testimonial
        st.markdown(f"""
            <div class='side-pane' style='background-image: url("https://raw.githubusercontent.com/Hanxxf13/ai-recruitment-system/main/frontend/nukhba_bg.png"); min-height: 850px; border-radius: 30px;'>
                <div class='quote-box'>
                    "Nukhba is where precision meets talent. We found our elite engineering team in a matter of days."
                    <br><br>
                    <span style='font-size: 1.1rem; opacity: 0.8; font-weight: 400;'>Sarah Al-Mulla<br>VP of Engineering</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Demo Credentials**: `hr@example.com` / `password123`")
        
    with pane_right:
        st.markdown("<div style='padding: 20px 40px;'>", unsafe_allow_html=True)
        # Nukhba Logo (Black on White for this screen)
        st.markdown("<h1 style='font-family: Amiri; font-size: 3.5rem; color: #000; margin-bottom: 40px;'>نخبة</h1>", unsafe_allow_html=True)
        
        # Tab Selection logic
        tab_choice = st.radio("Select Action", ["Sign In", "Create Account"], horizontal=True, label_visibility="collapsed")
        
        if tab_choice == "Sign In":
            st.markdown("<h2 style='font-size: 2.2rem; font-weight: 800; color: #1a1a1a;'>Welcome Back</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 1rem; margin-top: -10px;'>Enter your elite login details.</p>", unsafe_allow_html=True)
            
            email = st.text_input("Email address", placeholder="hr@example.com", key="login_email_final")
            password = st.text_input("Password", type="password", key="login_pass_final")
            
            if st.button("Login", use_container_width=True):
                try:
                    resp = requests.post(f"{API_URL}/users/login", json={
                        "name": "", "email": email, "password": password, "role": ""
                    }, timeout=10)
                    if resp.status_code == 200:
                        st.session_state['user'] = resp.json()
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please use: hr@example.com / password123")
                except:
                    st.error("Connection failed.")
        
        else:
            st.markdown("<h2 style='font-size: 2.2rem; font-weight: 800; color: #1a1a1a;'>Let's join with us</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 1rem; margin-top: -10px;'>Start your elite recruitment journey.</p>", unsafe_allow_html=True)
            
            # Registration State Machine
            if 'reg_step' not in st.session_state:
                st.session_state['reg_step'] = 1
                
            if st.session_state['reg_step'] == 1:
                col_n, col_r = st.columns(2)
                with col_n: name = st.text_input("Full Name", placeholder="Jane Doe")
                with col_r: role = st.selectbox("Role", ["Candidate", "HR", "Admin"])
                
                email_reg = st.text_input("Email Address", placeholder="jane@example.com")
                pass_reg = st.text_input("Password", type="password")
                
                countries = {
                    "United Arab Emirates": "+971 🇦🇪",
                    "Saudi Arabia": "+966 🇸🇦",
                    "Qatar": "+974 🇶🇦",
                    "Oman": "+968 🇴🇲",
                    "Kuwait": "+965 🇰🇼",
                    "Bahrain": "+973 🇧🇭",
                    "United States": "+1 🇺🇸",
                    "United Kingdom": "+44 🇬🇧",
                    "India": "+91 🇮🇳"
                }
                
                c_col, p_col = st.columns([1, 1.5])
                with c_col:
                    country_name = st.selectbox("Country", list(countries.keys()))
                    c_code = countries[country_name]
                with p_col:
                    phone_no = st.text_input(f"Phone Number ({c_code})", placeholder="50 123 4567")
                
                if st.button("Request OTP", use_container_width=True):
                    if email_reg and phone_no:
                        try:
                            resp = requests.post(f"{API_URL}/users/request-otp", params={"email": email_reg, "phone": phone_no})
                            if resp.status_code == 200:
                                st.session_state['sent_otp'] = resp.json()['otp']
                                st.session_state['reg_data'] = {
                                    "name": name, "email": email_reg, "password": pass_reg, 
                                    "role": role, "country": f"{country_name} {c_code}", "phone": phone_no
                                }
                                st.session_state['reg_step'] = 2
                                st.rerun()
                        except:
                            st.error("Failed to fetch OTP.")
                    else:
                        st.warning("Please fill email and phone.")
            
            else:
                st.info(f"✨ OTP sent to {st.session_state['reg_data']['phone']} (Demo OTP: **{st.session_state['sent_otp']}**)")
                otp_input = st.text_input("Enter 4-digit OTP", placeholder="0000")
                if st.button("Verify & Complete Registration", use_container_width=True):
                    if otp_input == st.session_state['sent_otp']:
                        try:
                            resp = requests.post(f"{API_URL}/users/register", json=st.session_state['reg_data'])
                            if resp.status_code == 200:
                                st.success("🎉 Registration Elite Complete! Please Sign In.")
                                st.session_state['reg_step'] = 1
                            else:
                                st.error(resp.json().get("detail", "Error"))
                        except:
                            st.error("Registration failed.")
                    else:
                        st.error("Invalid OTP. Try again.")
                if st.button("Go Back", key="back_btn"):
                    st.session_state['reg_step'] = 1
                    st.rerun()

        st.markdown("<p style='text-align: center; color: #999; margin-top: 40px; font-size: 0.8rem;'>Need help? Contact support</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
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
