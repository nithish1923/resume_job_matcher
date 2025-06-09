def fetch_jobs(keyword, location=None, limit=20):
    url = f"https://remotive.io/api/remote-jobs?search={keyword}"
    response = requests.get(url)
    print("Remotive API status:", response.status_code)
    print("Response content:", response.text[:500])  # first 500 chars
    if response.status_code == 200:
        data = response.json()
        jobs = data.get("jobs", [])
        if location:
            filtered_jobs = [job for job in jobs if location.lower() in job.get("candidate_required_location", "").lower()]
        else:
            filtered_jobs = jobs
        return filtered_jobs[:limit]
    else:
        return []
