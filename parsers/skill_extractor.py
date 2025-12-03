from helpers.skill_dictionary import SKILL_KEYWORDS

class SkillExtractor:
    @staticmethod
    def extract_skills(text: str) -> list:
        found = []
        text_lower = text.lower()
        
        for skill, variants in SKILL_KEYWORDS.items():
            for variant in variants:
                if variant in text_lower:
                    found.append(skill)
                    break
        return found