import json
from parsers.parser_pipeline import parse_resume_pipeline

try:
    result = parse_resume_pipeline("docs/image_resume.pdf")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
    print("Make sure to set GEMINI_API_KEY in your .env file")
