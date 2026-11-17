import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


# ==========================
# Resume Screening Function
# ==========================
def analyze_resume(text):

    # Remove invalid unicode characters
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = ''.join(
        c for c in text
        if ord(c) < 0xD800 or ord(c) > 0xDFFF
    )

    prompt = f"""
    You are an expert ATS Resume Screening System.

    Analyze the following resume and provide:

    1. ATS Score (0-100)
    2. Candidate Summary
    3. Skills Detected
    4. Experience Level
    5. Strengths
    6. Weaknesses
    7. Suggested Job Roles
    8. Missing Skills
    9. Resume Improvement Suggestions
    10. Final Recommendation
        (Hire / Maybe / Reject)

    Resume:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text


# ==========================
# HR Recruitment Assistant
# ==========================
def hr_assistant(name, skills, experience):

    prompt = f"""
    You are an HR Recruitment Expert.

    Candidate Name:
    {name}

    Skills:
    {skills}

    Experience:
    {experience}

    Generate:

    1. Candidate Summary
    2. Technical Skill Evaluation
    3. Communication Assessment
    4. Strengths
    5. Weaknesses
    6. 10 Interview Questions
    7. Hiring Recommendation
       (Hire / Maybe / Reject)
    8. Expected Job Roles
    9. Salary Range Suggestion

    Give the output in a professional format.
    """

    response = model.generate_content(prompt)

    return response.text


# ==========================
# Interview Question Generator
# ==========================
def generate_questions(skill):

    prompt = f"""
    Generate 15 interview questions for:

    {skill}

    Divide them into:
    - Beginner
    - Intermediate
    - Advanced
    """

    response = model.generate_content(prompt)

    return response.text


# ==========================
# Job Recommendation
# ==========================
def recommend_job(skills):

    prompt = f"""
    Based on the following skills:

    {skills}

    Suggest:
    1. Suitable Job Roles
    2. Career Path
    3. Required Certifications
    4. Missing Skills
    5. Learning Roadmap
    """

    response = model.generate_content(prompt)

    return response.text