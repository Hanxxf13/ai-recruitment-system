import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="HR Dashboard", layout="wide")

if 'user' not in st.session_state or st.session_state['user'] is None or st.session_state['user']['role'] != 'HR':
    st.warning("Please login as HR from the main app.")
    st.stop()
    
user = st.session_state['user']

st.title("💼 HR Manager Dashboard")

tab1, tab2 = st.tabs(["Post a Job", "Review Applications"])

with tab1:
    st.header("Create New Job Posting")
    title = st.text_input("Job Title")
    description = st.text_area("Job Description")
    requirements = st.text_area("Requirements (Keywords, Skills)")
    
    if st.button("Post Job"):
        res = requests.post(f"{API_URL}/jobs?hr_id={user['id']}", json={
            "title": title,
            "description": description,
            "requirements": requirements
        })
        if res.status_code == 200:
            st.success("Job posted successfully!")
            st.code(res.json())
        else:
            st.error("Failed to post job")

with tab2:
    st.header("AI Application Review")
    
    # Get all jobs
    jobs_res = requests.get(f"{API_URL}/jobs")
    if jobs_res.status_code == 200:
        jobs = jobs_res.json()
        my_jobs = [j for j in jobs if j['hr_id'] == user['id']]
        
        if not my_jobs:
            st.info("You haven't posted any jobs yet.")
        else:
            job_titles = {j['title']: j['id'] for j in my_jobs}
            selected_job = st.selectbox("Select Job to review applications", list(job_titles.keys()))
            
            if selected_job:
                job_id = job_titles[selected_job]
                apps_res = requests.get(f"{API_URL}/applications/{job_id}")
                
                if apps_res.status_code == 200:
                    apps = apps_res.json()
                    if not apps:
                        st.info("No applications yet for this job.")
                    else:
                        for app in apps:
                            with st.expander(f"Application ID: {app['id']} - Candidate ID: {app['candidate_id']} | Score: {app['ai_score']}"):
                                st.write("**Resume Snippet:**")
                                st.text(app['resume_text'][:200] + "...")
                                
                                st.metric("AI Match Score", f"{app['ai_score']}%")
                                st.info(f"**AI Explainability:** {app['ai_feedback']}")
                                
                                st.write(f"Current Status: **{app['status']}**")
                                
                                new_status = st.selectbox("Update Status", ["Screened", "Interviewing", "Rejected", "Hired"], key=f"status_{app['id']}")
                                if st.button("Save Status", key=f"btn_{app['id']}"):
                                    res = requests.put(f"{API_URL}/applications/{app['id']}/status?status={new_status}")
                                    if res.status_code == 200:
                                        st.success("Updated successfully.")
                                    else:
                                        st.error("Failed to update.")
                else:
                    st.error("Could not fetch applications.")
