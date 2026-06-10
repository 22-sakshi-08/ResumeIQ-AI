import re
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.ml.feature_engineering import (
    FeatureExtractor, 
    compute_skill_overlap_score, 
    compute_keyword_coverage_score
)

class ATSPredictor:
    def __init__(self):
        pass

    def predict_ats_score(self, resume_text: str, jd_text: str = None, required_skills: list = None) -> dict:
        """Calculates ATS score out of 100 with explainable breakdown."""
        # 1. Clean inputs
        resume_text_lower = resume_text.lower() if isinstance(resume_text, str) else ""
        
        # 2. Extract stats using FeatureExtractor
        stats = FeatureExtractor.extract_stats(resume_text)
        
        # --- A. SKILL SCORE (Max 40 points) ---
        if required_skills:
            # Check overlap against job description specific skills
            # Extract skills present in resume text
            detected_skills = []
            from src.ml.feature_engineering import MASTER_SKILLS
            for skill in MASTER_SKILLS:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, resume_text_lower):
                    detected_skills.append(skill)
            
            overlap_ratio = compute_skill_overlap_score(detected_skills, required_skills)
            skill_score = round(overlap_ratio * 40, 1)
            skill_details = f"Matched {sum(1 for s in required_skills if s.lower() in [ds.lower() for ds in detected_skills])} of {len(required_skills)} required skills."
        else:
            # Baseline scoring on resume total skills count (cap at 12 skills for full points)
            skill_count = stats["skill_count"]
            skill_score = min(40.0, round((skill_count / 12) * 40, 1))
            skill_details = f"Detected {skill_count} relevant technical skills in candidate profile."

        # --- B. EXPERIENCE SCORE (Max 25 points) ---
        # Look for experience keywords ("led", "managed", "designed", "optimized", "scale", "architected")
        exp_keywords = ["led", "managed", "designed", "optimized", "scale", "architected", "senior", "director", "coordinator", "team"]
        exp_keyword_count = sum(1 for kw in exp_keywords if re.search(r'\b' + re.escape(kw) + r'\b', resume_text_lower))
        
        # Extract years of experience if possible
        # Check patterns like "5 years", "3+ years", "10 years"
        years_matches = re.findall(r'(\d+)\+?\s*years?', resume_text_lower)
        years_exp = 0
        if years_matches:
            years_exp = max([int(y) for y in years_matches])
            
        # Experience scoring breakdown:
        # Years score: 15 max (3 points per year up to 5 years)
        years_score = min(15.0, years_exp * 3.0)
        # Keyword/leadership score: 10 max (2 points per unique leadership keyword matched)
        keyword_score = min(10.0, exp_keyword_count * 2.0)
        
        experience_score = round(years_score + keyword_score, 1)
        experience_details = f"Detected ~{years_exp} years of experience and {exp_keyword_count} leadership/impact terms."

        # --- C. PROJECTS SCORE (Max 20 points) ---
        # Based on presence of projects section, github links, and project keywords
        proj_score = 0.0
        # Check for projects section keyword
        if "projects" in resume_text_lower or "key projects" in resume_text_lower:
            proj_score += 8.0
        # Check for github link
        if "github.com" in resume_text_lower or "git" in resume_text_lower:
            proj_score += 4.0
        # Count project keywords ("build", "implement", "deploy", "create")
        proj_keywords = ["build", "implement", "deploy", "create", "developed", "engineered"]
        proj_keyword_count = sum(1 for kw in proj_keywords if re.search(r'\b' + re.escape(kw) + r'\b', resume_text_lower))
        
        proj_score += min(8.0, proj_keyword_count * 2.0)
        projects_score = round(proj_score, 1)
        projects_details = f"Detected projects indicators and {proj_keyword_count} execution terms."

        # --- D. EDUCATION & CERTIFICATION SCORE (Max 15 points) ---
        # Education degree base points (Max 10)
        edu_score = 5.0  # default baseline
        if "phd" in resume_text_lower or "doctorate" in resume_text_lower:
            edu_score = 10.0
        elif "master" in resume_text_lower or "ms" in resume_text_lower or "msc" in resume_text_lower or "mtech" in resume_text_lower:
            edu_score = 9.0
        elif "bachelor" in resume_text_lower or "bs" in resume_text_lower or "btech" in resume_text_lower or "degree" in resume_text_lower:
            edu_score = 8.0
            
        # Certifications booster points (Max 5)
        # 2.5 points per certification matched (cap at 5)
        cert_count = stats["certification_keyword_count"]
        cert_score = min(5.0, cert_count * 2.5)
        
        education_score = round(edu_score + cert_score, 1)
        education_details = f"Education degree base score: {edu_score}/10, Certifications booster: {cert_score}/5."

        # --- FINAL ATS SCORE (Max 100 points) ---
        final_ats_score = round(skill_score + experience_score + projects_score + education_score, 1)
        final_ats_score = min(100.0, final_ats_score)
        
        return {
            "ats_score": final_ats_score,
            "breakdown": {
                "skill_score": skill_score,
                "experience_score": experience_score,
                "projects_score": projects_score,
                "education_score": education_score
            },
            "explanations": {
                "skills": skill_details,
                "experience": experience_details,
                "projects": projects_details,
                "education": education_details
            }
        }

if __name__ == "__main__":
    predictor = ATSPredictor()
    sample_text = """
    Jane Smith
    jane.smith@gmail.com | github.com/janesmith
    
    SUMMARY
    Machine learning engineer with 6 years of experience building scalable AI systems.
    
    TECHNICAL SKILLS
    Python, C++, PyTorch, Docker, Kubernetes, AWS, SQL.
    
    PROFESSIONAL EXPERIENCE
    Senior ML Engineer | Google | 2020 - Present
    - Led team of 3 developers to optimize model latency by 40%.
    - Designed and implemented real-time inference microservices.
    
    KEY PROJECTS
    Distributed Inference App: Engineered high-throughput deployment pipeline on AWS EKS.
    
    EDUCATION
    Master of Science in Computer Science, Stanford University, 2020
    
    CERTIFICATIONS
    - AWS Certified Solutions Architect
    - TensorFlow Developer Certificate
    """
    
    res = predictor.predict_ats_score(sample_text, required_skills=["Python", "PyTorch", "AWS"])
    print(f"ATS Score: {res['ats_score']}/100")
    print("Breakdown:", res["breakdown"])
    print("Explanations:", res["explanations"])
