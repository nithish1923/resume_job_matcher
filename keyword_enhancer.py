import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def suggest_keywords(resume_text, top_jobs):
    job_descriptions = "\n".join([job["description"] for job in top_jobs])
    prompt = f"Given the resume below:\n{resume_text}\n\nAnd the following job descriptions:\n{job_descriptions}\n\nWhat keywords should be added to the resume to improve ATS score?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]