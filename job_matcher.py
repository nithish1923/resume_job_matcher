import random

def match_jobs(resume_text, jobs):
    matched_jobs = []
    for job in jobs:
        # If job title words appear in resume, give a high match score, else random lower
        title_words = set(job.get('title', '').lower().split())
        resume_words = set(resume_text.lower().split())

        if title_words.intersection(resume_words):
            similarity = random.uniform(0.8, 1.0)  # 80% to 100% match
        else:
            similarity = random.uniform(0.3, 0.7)  # lower match score

        job['similarity'] = similarity
        matched_jobs.append(job)

    # Sort descending by similarity
    matched_jobs.sort(key=lambda x: x['similarity'], reverse=True)
    return matched_jobs
