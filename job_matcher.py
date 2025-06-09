import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_keywords(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]{4,}\b', text)
    common_skills = {"python", "tensorflow", "pytorch", "llm", "gpt", "ai", "ml", "rag", "streamlit", "gcp", "aws", "azure", "langchain"}
    return list(set(words) & common_skills)

def match_jobs(resume_text, job_list, similarity_threshold=0.03):
    if not job_list:
        return []

    resume_keywords = extract_keywords(resume_text)
    if not resume_keywords:
        return []

    descriptions = [job.get("description", "") for job in job_list]
    all_texts = [" ".join(resume_keywords)] + descriptions

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    top_indices = similarities.argsort()[::-1][:5]
    return [job_list[i] for i in top_indices if similarities[i] > similarity_threshold]
