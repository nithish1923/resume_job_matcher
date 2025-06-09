import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from job_matcher import match_jobs
from keyword_enhancer import suggest_keywords

st.title("📄 Resume & Job Match Agent")

resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if resume:
    with st.spinner("Parsing Resume..."):
        resume_text = parse_resume(resume)

    st.subheader("Parsed Resume Text")
    st.write(resume_text[:500] + "...")

    # Extract broad job query from resume text - For demo, let's take top nouns or just ask user
    job_query = st.text_input("Enter Job Role / Title to search jobs for (e.g., AI Engineer)")
    location = st.text_input("Enter Location (e.g., Remote)", value="Remote")

    if job_query:
        with st.spinner("Fetching job listings matching your resume..."):
            jobs = fetch_jobs(job_query, location, limit=20)

        with st.spinner("Matching jobs to your resume..."):
            matched_jobs = match_jobs(resume_text, jobs)

        st.subheader(f"Top {len(matched_jobs)} Jobs Matching Your Resume")

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
            st.info("No closely matching jobs found. Try adjusting the job role or location.")

else:
    st.info("Please upload your resume to begin.")
