import re

class JDParser:
    def __init__(self, jd_text: str):
        self.text = jd_text.lower()

    def extract_skills(self, skills_list):
        found = []
        for skill in skills_list:
            if skill.lower() in self.text:
                found.append(skill)
        return found

    def extract_requirements(self):
        """Find bullet points / responsibilities."""
        bullets = re.findall(r"[-•*]\s+(.*)", self.text)
        return bullets

    def parse(self):
        return {
            "requirements": self.extract_requirements()
        }
