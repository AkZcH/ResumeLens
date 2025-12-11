from parsers.helpers.section_headers import SECTION_HEADERS

class SectionClassifier:
    @staticmethod
    def classify_sections(text: str) -> dict:
        sections = {}
        current_sec = "general"
        lines = text.split("\n")

        for line in lines:
            line_clean = line.strip().lower()
            
            # Check for section headers
            for section, headers in SECTION_HEADERS.items():
                if any(header in line_clean for header in headers):
                    current_sec = section
                    break

            sections.setdefault(current_sec, []).append(line)

        return sections