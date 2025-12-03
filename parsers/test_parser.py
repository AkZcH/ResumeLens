import json
from resume_parser import ResumeParser

# Test the parser with existing PDF
parser = ResumeParser("../docs/resume1.pdf")
result = parser.parse()

# Format output by sections
formatted_output = {
    "contact_info": {
        "email": result['email'],
        "phone": result['phone']
    },
    "skills": result['skills'],
    "experience": result['sections'].get('experience', []),
    "education": result['sections'].get('education', []),
    "projects": result['sections'].get('projects', []),
    "certifications": result['sections'].get('certifications', []),
    "summary": result['sections'].get('summary', [])
}

print(json.dumps(formatted_output, indent=2, ensure_ascii=False))