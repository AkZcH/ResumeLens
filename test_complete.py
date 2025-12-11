from parsers.text_parser import TextResumeParser
from parsers.jd_parser import JDParser

# Sample resume text
sample_resume = """
John Doe
Software Engineer
john.doe@email.com
+1-555-123-4567

EXPERIENCE
Senior Software Engineer at TechCorp (2020-2023)
• Developed web applications using Python and React
• Led a team of 5 developers
• Improved system performance by 40%

Software Developer at StartupXYZ (2018-2020)
• Built REST APIs using FastAPI
• Worked with PostgreSQL databases
• Implemented CI/CD pipelines

EDUCATION
Bachelor of Science in Computer Science
University of Technology (2014-2018)

SKILLS
Python, JavaScript, React, FastAPI, PostgreSQL, Docker, AWS

PROJECTS
E-commerce Platform
• Built using Python, React, and PostgreSQL
• Handles 10,000+ daily transactions
"""

# Sample job description
sample_jd = """
Senior Python Developer

Requirements:
• 5+ years of Python experience
• Experience with React and JavaScript
• Knowledge of PostgreSQL databases
• AWS cloud experience
• Strong leadership skills

Responsibilities:
• Lead development team
• Design scalable applications
• Mentor junior developers
"""

# Test resume parser
print("=== RESUME PARSER TEST ===")
resume_parser = TextResumeParser(sample_resume)
resume_result = resume_parser.parse()

print(f"Email: {resume_result['email']}")
print(f"Phone: {resume_result['phone']}")
print(f"Sections: {list(resume_result['sections'].keys())}")

skills_list = ["Python", "JavaScript", "React", "FastAPI", "PostgreSQL", "Docker", "AWS", "Java", "C++"]
found_skills = resume_parser.extract_skills(skills_list)
print(f"Found Skills: {found_skills}")

# Test JD parser
print("\n=== JD PARSER TEST ===")
jd_parser = JDParser(sample_jd)
jd_result = jd_parser.parse()
jd_skills = jd_parser.extract_skills(skills_list)

print(f"JD Requirements: {jd_result['requirements']}")
print(f"JD Skills: {jd_skills}")

# Gap analysis
print("\n=== GAP ANALYSIS ===")
missing_skills = [skill for skill in jd_skills if skill not in found_skills]
print(f"Missing Skills: {missing_skills}")
print(f"Matching Skills: {[skill for skill in jd_skills if skill in found_skills]}")