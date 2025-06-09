import re

def clean_text(text):
    # Lowercase and remove non-alphanumeric characters for simple matching
    return re.sub(r'[^a-z0-9\s]', '', text.lower())

def match_jobs(resume_text, jobs):
    """
    Match jobs to resume by simple keyword overlap.
    Returns jobs sorted by overlap score descending.
    Each job dict will have 'similarity' (0 to 1).
    """
    resume_words = set(clean_text(resume_text).split())

    matched_jobs = []
    for job in jobs:
        job_text = f"{job.get('title', '')} {job.get('description', '')}"
        job_words = set(clean_text(job_text).split())

        # Calculate Jaccard similarity: intersection / union
        intersection = resume_words.intersection(job_words)
        union = resume_words.union(job_words)
        similarity = len(intersection) / len(union) if union else 0

        job['similarity'] = similarity
        matched_jobs.append(job)

    # Sort jobs by similarity descending
    matched_jobs.sort(key=lambda x: x['similarity'], reverse=True)
    return matched_jobs
