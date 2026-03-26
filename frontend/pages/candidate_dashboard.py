import streamlit as st
import requests
from styles import inject_premium_css

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Nukhba | Candidate Portal", page_icon="💎", layout="wide")
inject_premium_css()

if 'user' not in st.session_state or st.session_state['user'] is None or st.session_state['user']['role'] != 'Candidate':
    st.warning("Please login as Candidate from the main app.")
    st.stop()
    
user = st.session_state['user']

st.markdown("<h1 class='nukhba-logo' style='font-size: 2.5rem;'>NUKHBA</h1>", unsafe_allow_html=True)
st.title("👤 Candidate Portal")

tab1, tab2 = st.tabs(["🚀 Explore Opportunities", "📤 My Submissions"])

with tab1:
    st.subheader("Ready for your next challenge?")
    
    try:
        jobs_res = requests.get(f"{API_URL}/jobs")
        if jobs_res.status_code == 200:
            jobs = jobs_res.json()
            open_jobs = [j for j in jobs if j['status'] == 'Open']
            
            if not open_jobs:
                st.info("Check back soon for new openings!")
            else:
                for job in open_jobs:
                    st.markdown(f"""
                    <div class='job-card'>
                        <h3 style='margin-bottom: 5px;'>{job['title']}</h3>
                        <p style='color: #818cf8; font-size: 0.8rem; font-weight: 600;'>ELITE MATCH</p>
                        <p>{job['description'][:150]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("Show Requirements & Apply"):
                        st.write("**Core Requirements:**")
                        st.write(job['requirements'])
                        
                        resume = st.text_area("Paste your Resume / Professional Summary to apply:", key=f"res_{job['id']}", height=150)
                        
                        if st.button("Submit Application", key=f"apply_{job['id']}", use_container_width=True):
                            if len(resume) < 50:
                                st.warning("Please provide a more detailed resume for AI matching.")
                            else:
                                apply_res = requests.post(
                                    f"{API_URL}/applications?candidate_id={user['id']}", 
                                    json={"job_id": job['id'], "resume_text": resume}
                                )
                                if apply_res.status_code == 200:
                                    st.success("Your application has been submitted and AI-screened!")
                                else:
                                    st.error("You have already applied to this role.")
        else:
            st.error("Failed to fetch jobs.")
    except:
        st.error("Backend is offline. Please start the server.")

with tab2:
    st.subheader("Application Tracking")
    
    try:
        my_apps_res = requests.get(f"{API_URL}/applications/candidate/{user['id']}")
        if my_apps_res.status_code == 200:
            apps = my_apps_res.json()
            if not apps:
                st.info("You haven't submitted any applications yet.")
            else:
                for app in apps:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Role: {app['job_id']}**")
                        st.text(f"Applied on: {app['created_at'].split('T')[0]}")
                    with col2:
                        st.button(app['status'], key=f"status_btn_{app['id']}", disabled=True)
                    st.divider()
    except:
        st.error("Backend is offline.")
