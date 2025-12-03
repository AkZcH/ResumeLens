import json
from parser_pipeline import parse_resume_pipeline

# Test the complete pipeline
try:
    result = parse_resume_pipeline("../docs/resume1.pdf")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
    print("Make sure to set GEMINI_API_KEY in your .env file")