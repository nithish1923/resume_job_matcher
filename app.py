import streamlit as st
import requests
from resume_parser import parse_resume
from job_matcher import match_jobs
from keyword_enhancer import suggest_keywords
import os

# Set OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def fetch_jobs(keyword, location=None, limit=20):
    """
    Fetch jobs from Remotive API by keyword.
    Since Remotive API doesn't support location filtering,
    we filter jobs client-side by checking location string.
    """
    url = f"https://remotive.io/api/remote-jobs?search={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        jobs = data.get("jobs", [])
        if location:
            # Filter jobs by location substring (case-insensitive)
            filtered_jobs = [job for job in jobs if location.lower() in job.get("candidate_required_location", "").lower()]
        else:
            filtered_jobs = jobs
        return filtered_jobs[:limit]
    else:
        st.error("Failed to fetch jobs from Remotive API")
        return []

st.title("📄 Resume & Job Match Agent")

resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if resume:
    with st.spinner("Parsing Resume..."):
        resume_text = parse_resume(resume)

    st.subheader("Parsed Resume Text")
    st.write(resume_text[:500] + "...")

    job_query = st.text_input("Enter Job Role (e.g., GenAI Developer)", value="AI Engineer")
    location = st.text_input("Enter Job Location (e.g., Remote)", value="Remote")

    if job_query:
        with st.spinner("Fetching job listings..."):
            jobs = fetch_jobs(job_query, location, limit=20)

        with st.spinner("Matching jobs with resume..."):
            matched_jobs = match_jobs(resume_text, jobs)

        st.subheader(f"Top {len(matched_jobs)} Job Matches for Your Resume")

        if matched_jobs:
            for job in matched_jobs:
                similarity_pct = job.get('similarity', 0) * 100
                st.markdown(f"### {job['title']} at {job['company_name']}  (Match: {similarity_pct:.1f}%)")
                st.markdown(f"📍 {job['candidate_required_location']}")
                st.write(job['description'][:300] + "...")
                st.markdown("---")

            with st.spinner("Generating keyword suggestions..."):
                keywords = suggest_keywords(resume_text, matched_jobs)
                st.subheader("📌 Suggested Keywords to Enhance Your Resume")
                st.markdown(keywords)

        else:
            st.warning("No strong matches found for your resume.")
            if jobs:
                st.subheader("🔍 Here are some similar job openings instead:")
                for job in jobs[:5]:
                    st.markdown(f"### {job['title']} at {job['company_name']}")
                    st.markdown(f"📍 {job['candidate_required_location']}")
                    st.write(job['description'][:300] + "...")
                    st.markdown("---")

else:
    st.info("Please upload a resume to get started.")
