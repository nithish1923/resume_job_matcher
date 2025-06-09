from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, job_list):
    if not job_list:
        return []

    descriptions = [job["description"] for job in job_list]
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text] + descriptions)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    top_indices = similarities.argsort()[-3:][::-1]

    return [job_list[i] for i in top_indices]