import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep

#many llm call

# Load environment variables
load_dotenv()

# Read API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found!")

# Create Groq client
client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

JD = """
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME = """
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using FastAPI and MySQL.

Deployed an application using Docker.
"""

def ask_llm(system_prompt, user_prompt):

    sys_msg = {
        "role": "system",
        "content": system_prompt
    }

    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    answer = response.choices[0].message.content
    return answer


def step1_resume_extract():
    #extract skills from resume

    system_prompt = """
You are a professional HR assistant.

Extract only the skills from the candidate resume.

Return only the skills.

Do not invent any skills.
"""

    user_prompt = f"""
Extract the skills from this resume.

Resume:

{RESUME}
"""

    return ask_llm(system_prompt, user_prompt)


def step2_match(candidate, jd):

    system_prompt = """
You are a professional HR assistant.

Compare the candidate skills with the job description.

Give:

1. Matching skills
2. Missing skills
3. Match score between 1 and 100
4. Short recommendation whether the candidate is a good fit.
"""

    user_prompt = f"""
Compare and match the skills.

JD:

{jd}

Candidate Skills:

{candidate}
"""

    return ask_llm(system_prompt, user_prompt)


# Main Prompt Chain

candidate_skills = step1_resume_extract()

print("========== Extracted Skills ==========")
print(candidate_skills)

sleep(2)

print("\n========== Final Matching ==========")

result = step2_match(candidate_skills, JD)

print(result)