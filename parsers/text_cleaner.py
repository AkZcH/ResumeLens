import re

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        """Clean and normalize raw text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize bullet points
        text = re.sub(r'[•·▪▫‣⁃]', '•', text)
        # Remove weird unicode
        text = text.encode('ascii', 'ignore').decode('ascii')
        return text.strip()