from parsers.pdf_extractor import PDFExtractor
from parsers.text_cleaner import TextCleaner
from parsers.regex_extractors import RegexExtractors
from parsers.skill_extractor import SkillExtractor
from parsers.section_classifier import SectionClassifier
from parsers.llm_structurizer import LLMStructurizer


def parse_resume_pipeline(file_path: str) -> dict:
    """Complete resume parsing pipeline."""
    
    # Step 1: Extract text from PDF
    raw_text = PDFExtractor.extract_text(file_path)
    
    # Step 2: Clean and normalize text
    clean_text = TextCleaner.clean(raw_text)
    
    # Step 3: Extract basic info with regex
    email = RegexExtractors.extract_email(clean_text)
    phone = RegexExtractors.extract_phone(clean_text)
    
    # Step 4: Classify sections
    sections = SectionClassifier.classify_sections(clean_text)
    
    # Step 5: Extract skills
    skills = SkillExtractor.extract_skills(clean_text)
    
    # Step 6: Structure with LLM
    llm_structurizer = LLMStructurizer()
    structured_data = llm_structurizer.structure_resume(clean_text)
    
    return structured_data