import requests

def fetch_jobs_remotive(keyword):
    url = f"https://remotive.io/api/remote-jobs?search={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("jobs", [])
    else:
        print("Failed to fetch jobs")
        return []

# Example usage:
jobs = fetch_jobs_remotive("AI Engineer")
for job in jobs[:5]:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company_name']}")
    print(f"Location: {job['candidate_required_location']}")
    print(f"URL: {job['url']}")
    print("-" * 40)
