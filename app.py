import streamlit as st
from resume_parser import parse_resume
from job_fetcher import fetch_jobs
from job_matcher import match_jobs
from keyword_enhancer import suggest_keywords
import os

# Set OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="📄 Resume & Job Match Agent", layout="wide")

def similarity_color(sim):
    if sim > 0.8:
        return "🟢"
    elif sim > 0.5:
        return "🟡"
    else:
        return "🔴"

with st.sidebar:
    st.header("💡 Tips")
    st.write("""
    - Upload your updated resume (PDF) for best matches  
    - Use specific job titles (e.g., AI Engineer, Data Scientist)  
    - Location 'Remote' returns broader results  
    - Look for jobs with 🟢 high match badges first  
    - Scroll down for suggested keywords to improve your resume
    """)

st.title("📄 Resume & Job Match Agent")

resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if resume:
    with st.spinner("Parsing Resume..."):
        resume_text = parse_resume(resume)

    st.subheader("📝 Parsed Resume Text")
    st.write(resume_text[:500] + "...")

    job_query = st.text_input("Enter Job Role (e.g., AI Engineer)", value="AI Engineer")
    location = st.text_input("Enter Job Location (e.g., Remote)", value="Remote")

    if job_query:
        with st.spinner("Fetching job listings..."):
            jobs = fetch_jobs(job_query, location, limit=20)

        with st.spinner("Matching jobs with resume..."):
            matched_jobs = match_jobs(resume_text, jobs)

        if matched_jobs:
            st.subheader(f"🔎 Top {len(matched_jobs)} Job Matches for Your Resume")
            for job in matched_jobs:
                sim = job['similarity']
                badge = similarity_color(sim)
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {job['title']} at {job['company_name']} {badge}")
                    st.markdown(f"📍 {job['candidate_required_location']}")
                    st.write(job['description'][:300] + "...")
                with col2:
                    st.markdown(f"**Match:** {sim*100:.1f}%")
                    st.markdown(f"[Apply Here]({job.get('url', '#')})")
                st.markdown("---")

            with st.spinner("Generating keyword suggestions..."):
                keywords = suggest_keywords(resume_text, matched_jobs)
                st.subheader("📌 Suggested Keywords to Enhance Your Resume")
                st.markdown(keywords)

        else:
            st.warning("No strong matches found for your resume.")
            if jobs:
                st.subheader("🔍 Similar Job Openings")
                for job in jobs[:5]:
                    st.markdown(f"### {job['title']} at {job['company_name']}")
                    st.markdown(f"📍 {job['candidate_required_location']}")
                    st.write(job['description'][:300] + "...")
                    st.markdown(f"[Apply Here]({job.get('url', '#')})")
                    st.markdown("---")

else:
    st.info("Please upload a resume to get started.")
