import re

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

class TextResumeParser:
    def __init__(self, text: str):
        self.raw_text = text

    def extract_email(self):
        match = re.search(EMAIL_REGEX, self.raw_text)
        return match.group(0) if match else None

    def extract_phone(self):
        phone_regex = r"(\+?\d[\d -]{8,}\d)"
        match = re.search(phone_regex, self.raw_text)
        return match.group(0) if match else None

    def extract_skills(self, skills_list):
        found = []
        text_lower = self.raw_text.lower()
        for skill in skills_list:
            if skill.lower() in text_lower:
                found.append(skill)
        return found

    def extract_sections(self):
        sections = {}
        current_sec = "general"
        lines = self.raw_text.split("\n")

        for line in lines:
            line_clean = line.strip().lower()

            if "experience" in line_clean:
                current_sec = "experience"
            elif "education" in line_clean:
                current_sec = "education"
            elif "projects" in line_clean:
                current_sec = "projects"
            elif "skills" in line_clean:
                current_sec = "skills"

            sections.setdefault(current_sec, []).append(line)

        return sections

    def parse(self):
        return {
            "email": self.extract_email(),
            "phone": self.extract_phone(),
            "sections": self.extract_sections(),
            "raw_text": self.raw_text
        }