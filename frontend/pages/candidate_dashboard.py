import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Candidate Dashboard", layout="wide")

if 'user' not in st.session_state or st.session_state['user'] is None or st.session_state['user']['role'] != 'Candidate':
    st.warning("Please login as Candidate from the main app.")
    st.stop()
    
user = st.session_state['user']

st.title("👤 Candidate Dashboard")

tab1, tab2 = st.tabs(["Browse Jobs", "My Applications"])

with tab1:
    st.header("Available Job Openings")
    
    jobs_res = requests.get(f"{API_URL}/jobs")
    if jobs_res.status_code == 200:
        jobs = jobs_res.json()
        open_jobs = [j for j in jobs if j['status'] == 'Open']
        
        if not open_jobs:
            st.info("No open jobs available at the moment.")
        else:
            for job in open_jobs:
                with st.expander(f"{job['title']} (ID: {job['id']})"):
                    st.write("**Description:**")
                    st.write(job['description'])
                    st.write("**Requirements:**")
                    st.write(job['requirements'])
                    
                    resume = st.text_area("Paste your Resume (Text) here to apply:", key=f"res_{job['id']}")
                    
                    if st.button("Apply Now", key=f"apply_{job['id']}"):
                        if len(resume) < 20:
                            st.warning("Please provide a proper resume text.")
                        else:
                            apply_res = requests.post(
                                f"{API_URL}/applications?candidate_id={user['id']}", 
                                json={"job_id": job['id'], "resume_text": resume}
                            )
                            if apply_res.status_code == 200:
                                st.success("Application submitted successfully!")
                            else:
                                st.error(f"Failed: {apply_res.json().get('detail', 'Error')}")

with tab2:
    st.header("Track My Applications")
    
    my_apps_res = requests.get(f"{API_URL}/applications/candidate/{user['id']}")
    if my_apps_res.status_code == 200:
        apps = my_apps_res.json()
        if not apps:
            st.info("You haven't applied to any jobs yet.")
        else:
            for app in apps:
                st.markdown("---")
                st.subheader(f"Application for Job ID: {app['job_id']}")
                st.write(f"**Status:** {app['status']}")
                st.write(f"**Applied On:** {app['created_at'].split('T')[0]}")
                # We intentionally don't show internal AI match score to the candidate, only the recruitment team sees it.
                # Just show the status and application details.
                st.info("Your application is currently being reviewed.")
