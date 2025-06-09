import re

def clean_text(text):
    return re.sub(r'[^a-z0-9\s]', '', text.lower())

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

def match_jobs(resume_text, jobs):
    resume_words = set(clean_text(resume_text).split())

    matched_jobs = []
    for job in jobs:
        job_title = job.get('title', '')
        job_desc = job.get('description', '')

        job_title_words = set(clean_text(job_title).split())
        job_desc_words = set(clean_text(job_desc).split())

        title_score = jaccard_similarity(resume_words, job_title_words)
        desc_score = jaccard_similarity(resume_words, job_desc_words)

        similarity = 0.7 * title_score + 0.3 * desc_score

        job['similarity'] = similarity
        matched_jobs.append(job)

    matched_jobs.sort(key=lambda x: x['similarity'], reverse=True)
    return matched_jobs
