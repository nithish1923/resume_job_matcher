import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from job_matcher import match_jobs
from keyword_enhancer import suggest_keywords
import os

# Set OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

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
                st.markdown(f"### {job['title']} at {job['company']}")
                st.markdown(f"📍 {job['location']}")
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
                    st.markdown(f"### {job['title']} at {job['company']}")
                    st.markdown(f"📍 {job['location']}")
                    st.write(job['description'][:300] + "...")
                    st.markdown("---")

else:
    st.info("Please upload a resume to get started.")
