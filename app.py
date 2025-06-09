import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from job_matcher import match_jobs
from keyword_enhancer import suggest_keywords

st.title("📄 Resume & Job Match Agent")

resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_query = st.text_input("Enter Job Title (e.g., GenAI Developer)")
location = st.text_input("Enter Location (e.g., Remote)", value="Remote")

if resume and job_query:
    with st.spinner("Parsing Resume..."):
        resume_text = parse_resume(resume)

    with st.spinner("Fetching Job Descriptions..."):
        jobs = fetch_jobs(job_query, location)

    with st.spinner("Matching Jobs..."):
        top_matches = match_jobs(resume_text, jobs)

    st.subheader("Top Job Matches")
    for job in top_matches:
        st.markdown(f"### {job['title']} at {job['company']}")
        st.markdown(f"📍 {job['location']}")
        st.write(job['description'][:300] + "...")
        st.markdown("---")

    with st.spinner("Suggesting Keywords..."):
        keywords = suggest_keywords(resume_text, top_matches)
        st.subheader("📌 Keyword Suggestions")
        st.markdown(keywords)