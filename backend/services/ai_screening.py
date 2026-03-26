import re

def calculate_fit_score(resume_text: str, job_requirements: str) -> dict:
    """
    A simplified AI Screening module simulating NLP extraction and matching.
    In a full production environment, this would use Spacy/Transformers.
    For this MVP, it uses keyword frequency matching to ensure no heavy ML models
    need to be downloaded just to run the application.
    """
    # Normalize text
    resume_lower = resume_text.lower()
    req_lower = job_requirements.lower()
    
    # Extract simple words as "skills" (excluding common stop words roughly)
    words = re.findall(r'\b[a-z]{3,}\b', req_lower)
    skills = set(words)
    
    if not skills:
        return {"score": 50.0, "feedback": "Job has no specific requirements listed."}
        
    matched = [skill for skill in skills if skill in resume_lower]
    
    score = round(float(len(matched) / len(skills)) * 100, 2)
    
    feedback = f"Matched {len(matched)} out of {len(skills)} inferred key requirements. "
    if score > 80:
        feedback += "Excellent fit!"
    elif score > 50:
        feedback += "Good potential, but missing some key skills."
    else:
        feedback += "Does not meet many core requirements."
        
    return {"score": score, "feedback": feedback}
