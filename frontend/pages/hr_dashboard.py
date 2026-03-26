import streamlit as st
import requests
import pandas as pd
from styles import inject_premium_css

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="HR Command Center", layout="wide")
inject_premium_css()

if 'user' not in st.session_state or st.session_state['user'] is None or st.session_state['user']['role'] != 'HR':
    st.warning("Please login as HR from the main app.")
    st.stop()
    
user = st.session_state['user']

st.title("💼 HR Command Center")

tab1, tab2 = st.tabs(["➕ Post a Job", "🔍 AI Application Review"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Draft New Listing")
        title = st.text_input("Exact Job Title", placeholder="e.g. Lead Fullstack Engineer")
        description = st.text_area("Detailed Description", height=200)
    with col2:
        st.subheader("AI Search Parameters")
        requirements = st.text_area("Key Requirements (Comma-separated for AI)", height=200, placeholder="Python, AWS, React, Project Management")
        
        if st.button("Deploy Listing", use_container_width=True):
            res = requests.post(f"{API_URL}/jobs?hr_id={user['id']}", json={
                "title": title, "description": description, "requirements": requirements
            })
            if res.status_code == 200:
                st.success("Listing is now LIVE on TalentSpark!")
            else:
                st.error("Failed to post.")

with tab2:
    st.subheader("Intelligent Screening Queue")
    
    jobs_res = requests.get(f"{API_URL}/jobs")
    if jobs_res.status_code == 200:
        jobs = jobs_res.json()
        my_jobs = [j for j in jobs if j['hr_id'] == user['id']]
        
        if not my_jobs:
            st.info("No active listings found.")
        else:
            job_titles = {j['title']: j['id'] for j in my_jobs}
            selected_job = st.selectbox("Select Active Role:", list(job_titles.keys()))
            
            if selected_job:
                job_id = job_titles[selected_job]
                apps_res = requests.get(f"{API_URL}/applications/{job_id}")
                
                if apps_res.status_code == 200:
                    apps = apps_res.json()
                    if not apps:
                        st.info("Waiting for first applicant...")
                    else:
                        for app in apps:
                            score_color = "green" if app['ai_score'] > 75 else "orange" if app['ai_score'] > 40 else "red"
                            with st.expander(f"Applicant #{app['id']} | Match Score: {app['ai_score']}%"):
                                st.markdown(f"#### Fit Profile: <span style='color:{score_color}'>{app['ai_score']}%</span>", unsafe_allow_html=True)
                                st.info(f"**AI Insight:** {app['ai_feedback']}")
                                
                                st.write("**Resume Highlights:**")
                                st.code(app['resume_text'][:500] + "...")
                                
                                st.divider()
                                s1, s2 = st.columns([2, 1])
                                with s1:
                                    new_status = st.selectbox("Pipeline Status", ["Screened", "Interviewing", "Rejected", "Hired"], key=f"status_{app['id']}")
                                with s2:
                                    if st.button("Update", key=f"btn_{app['id']}", use_container_width=True):
                                        res = requests.put(f"{API_URL}/applications/{app['id']}/status?status={new_status}")
                                        if res.status_code == 200:
                                            st.success("Done!")
                                            st.rerun()
                else:
                    st.error("Error retrieving queue.")
