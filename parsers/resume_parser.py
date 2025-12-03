import re
from pdf_extractor import PDFExtractor
from text_cleaner import TextCleaner
from helpers.regex_patterns import EMAIL_REGEX, PHONE_REGEX
from helpers.skill_dictionary import SKILL_KEYWORDS, get_all_skills
from helpers.section_headers import SECTION_HEADERS

class ResumeParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_text = PDFExtractor.extract_text(file_path)
        self.clean_text = TextCleaner.clean(self.raw_text)

    def extract_email(self):
        match = re.search(EMAIL_REGEX, self.clean_text)
        return match.group(0) if match else None

    def extract_phone(self):
        match = re.search(PHONE_REGEX, self.clean_text)
        return match.group(0) if match else None

    def extract_skills(self):
        """Extract skills using dictionary matching."""
        found = []
        text_lower = self.clean_text.lower()
        
        for skill, variants in SKILL_KEYWORDS.items():
            for variant in variants:
                if variant in text_lower:
                    found.append(skill)
                    break
        return found

    def extract_sections(self):
        """Extract sections using header mapping."""
        sections = {}
        current_sec = "general"
        lines = self.clean_text.split("\n")

        for line in lines:
            line_clean = line.strip().lower()
            
            # Check for section headers
            for section, headers in SECTION_HEADERS.items():
                if any(header in line_clean for header in headers):
                    current_sec = section
                    break

            sections.setdefault(current_sec, []).append(line)

        return sections

    def parse(self):
        """Main parse function."""
        return {
            "email": self.extract_email(),
            "phone": self.extract_phone(),
            "skills": self.extract_skills(),
            "sections": self.extract_sections(),
            "raw_text": self.raw_text
        }
