# match_jobs.py
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_jobs(resume_text, jobs):
    """
    Matches jobs to resume text using cosine similarity of embeddings.
    Returns jobs sorted by similarity descending, each with 'similarity' key.
    """
    # Encode resume once
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    matched_jobs = []
    for job in jobs:
        # Combine title + description to represent job text
        job_text = f"{job.get('title', '')} {job.get('description', '')}"

        # Encode job text
        job_embedding = model.encode(job_text, convert_to_tensor=True)

        # Compute cosine similarity (value between 0 and 1)
        similarity = util.pytorch_cos_sim(resume_embedding, job_embedding).item()

        # Add similarity score to job dict
        job['similarity'] = similarity
        matched_jobs.append(job)

    # Sort jobs by similarity descending (best matches first)
    matched_jobs.sort(key=lambda x: x['similarity'], reverse=True)

    return matched_jobs
