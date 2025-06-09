import requests

def fetch_jobs(query, location="Remote", limit=10):
    url = "https://jobs.indianapi.in/jobs"
    params = {
        "title": query,
        "location": location,
        "limit": limit
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []
