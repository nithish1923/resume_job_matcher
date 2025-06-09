import streamlit as st
from resume_parser import parse_resume
from job_matcher import match_jobs
from keyword_enhancer import suggest_keywords
import os

# Set OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def fetch_jobs(keyword, location=None, limit=20):
    mock_jobs = [
        {
            "title": "AI Engineer",
            "company_name": "OpenAI",
            "candidate_required_location": "Remote",
            "description": "Work on cutting-edge AI projects involving large language models and computer vision.",
            "url": "https://openai.com/careers"
        },
        {
            "title": "Machine Learning Engineer",
            "company_name": "Tech Corp",
            "candidate_required_location": "Noida, India",
            "description": "Develop ML models for production systems, focusing on scalability and performance.",
            "url": "https://techcorp.com/jobs/123"
        },
        {
            "title": "Data Scientist",
            "company_name": "Data Insights",
            "candidate_required_location": "New York, USA",
            "description": "Analyze large datasets and build predictive models to support business decisions.",
            "url": "https://datainsights.com/careers/456"
        },
        {
            "title": "NLP Researcher",
            "company_name": "InnovateAI",
            "candidate_required_location": "San Francisco, USA",
            "description": "Research and develop new natural language processing algorithms for conversational AI.",
            "url": "https://innovateai.com/jobs/789"
        },
        {
            "title": "Software Engineer",
            "company_name": "Global Tech",
            "candidate_required_location": "Remote",
            "description": "Build and maintain scalable backend services and APIs.",
            "url": "https://globaltech.com/careers/101"
        },
        {
            "title": "Cloud Engineer",
            "company_name": "CloudWorks",
            "candidate_required_location": "Bangalore, India",
            "description": "Manage and optimize cloud infrastructure for enterprise clients.",
            "url": "https://cloudworks.com/jobs/202"
        },
        {
            "title": "AI Product Manager",
            "company_name": "NextGen AI",
            "candidate_required_location": "Remote",
            "description": "Lead product development for AI-driven platforms.",
            "url": "https://nextgenai.com/careers/303"
        },
        {
            "title": "Computer Vision Engineer",
            "company_name": "Visionary Labs",
            "candidate_required_location": "Berlin, Germany",
            "description": "Design computer vision models for real-time video analysis.",
            "url": "https://visionarylabs.com/jobs/404"
        },
        # You can add more mock jobs here
    ]

    keyword_lower = keyword.lower()
    location_lower = location.lower() if location else ""

    filtered_jobs = []
    for job in mock_jobs:
        title_match = keyword_lower in job["title"].lower()
        location_match = location_lower in job["candidate_required_location"].lower() if location_lower else True
        if title_match and location_match:
            filtered_jobs.append(job)

    # If no match, show some jobs anyway so user sees results
    if not filtered_jobs:
        filtered_jobs = mock_jobs[:limit]

    return filtered_jobs[:limit]


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
                st.markdown(f"[Apply Here]({job['url']})")
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
                    st.markdown(f"[Apply Here]({job['url']})")
                    st.markdown("---")

else:
    st.info("Please upload a resume to get started.")
