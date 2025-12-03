from parsers.jd_parser import JDParser

# Test JD Parser with sample text
sample_jd = """
Software Engineer Position

Requirements:
• 3+ years of Python experience
• Experience with React and JavaScript
• Knowledge of SQL databases
• Strong problem-solving skills
• Bachelor's degree in Computer Science

Responsibilities:
• Develop web applications
• Write clean, maintainable code
• Collaborate with cross-functional teams
"""

jd_parser = JDParser(sample_jd)
skills_list = ["Python", "React", "JavaScript", "SQL", "Java", "C++", "Node.js"]

result = jd_parser.parse()
found_skills = jd_parser.extract_skills(skills_list)

print("JD Parser Results:")
print(f"Requirements: {result['requirements']}")
print(f"Found Skills: {found_skills}")