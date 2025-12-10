from .text_cleaner import TextCleaner
from .jd_parser import JDParser

def parse_jd_pipeline(jd_text: str) -> dict:
    """Complete job description parsing pipeline."""

    # Step 1: Clean text
    clean_text = TextCleaner.clean(jd_text)

    # Step 2: LLM-structured JD extraction
    parser = JDParser(clean_text)
    structured_data = parser.parse()

    return structured_data
