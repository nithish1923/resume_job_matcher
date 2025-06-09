import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def suggest_keywords(resume_text, top_jobs):
    job_descriptions = "\n".join([job["description"] for job in top_jobs])
    prompt = f"""Given the resume below:
{resume_text}

And the following job descriptions:
{job_descriptions}

What keywords should be added to the resume to improve ATS score?
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
