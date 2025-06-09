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
        # Add more diverse mock jobs here to cover more roles & locations
    ]

    # Simple filtering based on keyword and location (case insensitive)
    filtered_jobs = []
    keyword_lower = keyword.lower()
    location_lower = location.lower() if location else ""

    for job in mock_jobs:
        title_match = keyword_lower in job["title"].lower()
        location_match = location_lower in job["candidate_required_location"].lower() if location_lower else True
        if title_match and location_match:
            filtered_jobs.append(job)

    # If no filtered jobs, return some default jobs to ensure at least one result
    if not filtered_jobs:
        filtered_jobs = mock_jobs[:limit]

    return filtered_jobs[:limit]
