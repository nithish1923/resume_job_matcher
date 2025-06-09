import streamlit as st
import requests

def fetch_jobs_remotive(keyword):
    url = f"https://remotive.io/api/remote-jobs?search={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("jobs", [])
    else:
        st.error("Failed to fetch jobs from Remotive API")
        return []

st.title("🚀 Job Search with Remotive API (Free & No Credit Card)")

keyword = st.text_input("Enter Job Keyword (e.g., AI Engineer)", value="AI Engineer")

if keyword:
    with st.spinner("Fetching jobs..."):
        jobs = fetch_jobs_remotive(keyword)

    if jobs:
        st.subheader(f"Found {len(jobs)} jobs for '{keyword}'")
        for job in jobs[:10]:  # show top 10 jobs
            st.markdown(f"### [{job['title']}]({job['url']})")
            st.markdown(f"**Company:** {job['company_name']}  |  **Location:** {job['candidate_required_location']}")
            st.write(job['description'][:300] + "...")
            st.markdown("---")
    else:
        st.warning(f"No jobs found for '{keyword}'")
