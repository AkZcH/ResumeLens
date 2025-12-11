import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

PROMPT_TEMPLATE = """
You are an expert resume analysis engine.

Your job is to transform noisy, raw extracted resume text into a precise,
strictly factual, structured JSON resume representation.

Follow these rules with ZERO exceptions:

STRICT RULES:
1. Do NOT fabricate or infer ANY dates, skills, tools, companies, roles,
   metrics, impact, or technologies beyond what the raw text explicitly contains.
2. If information is partially present, extract only the part that exists.
3. Do NOT over-expand skills. Only extract skills explicitly referenced.
4. Do NOT merge sections. Keep experience, projects, and education separate.
5. For bullets, rewrite them concisely using action verbs + metric/impact,
   but do NOT invent new claims.
6. All extracted keywords must be STRICTLY grounded in the text.
7. Output pure JSON. No commentary, no Markdown.

YOUR OBJECTIVE:
Given the RAW_RESUME_TEXT, produce a structured JSON breakdown with:
- correctly segmented sections
- concise bullets
- extracted metrics
- technologies, tools, domains
- product/technical/other skill categorization
- clean, normalized keywords for each experience/project

INPUT (RAW_RESUME_TEXT):
{{RAW_RESUME_TEXT}}

REQUIRED JSON SCHEMA:
{
  "contact": {
    "name": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "github": ""
  },
  "summary": "",
  "skills": {
    "technical": [],
    "product": [],
    "other": []
  },
  "experience": [
    {
      "company": "",
      "role": "",
      "location": "",
      "start_date": "",
      "end_date": "",
      "bullets": [
        "one-line bullet with metric or impact",
        "another one-line bullet"
      ],
      "keywords": []
    }
  ],
  "projects": [
    {
      "name": "",
      "description": "",
      "impact": "",
      "tech_stack": [],
      "keywords": []
    }
  ],
  "education": [
    {
      "institution": "",
      "degree": "",
      "location": "",
      "start_year": "",
      "end_year": "",
      "cgpa": "",
      "coursework": []
    }
  ]
}

ADDITIONAL REQUIREMENTS:
- Extract metrics exactly as written (e.g., "40%", "250+ registrations", "95% reduction").
- Normalize tools/tech (React, AWS, SQL, Node.js, ML, etc.).
- Extract domain skills (e.g., Product Strategy, 2D–3D Reconstruction, Distributed Systems).
- Extract product skills (e.g., Prioritization, Roadmapping, Stakeholder alignment).
- Extract soft/leadership skills (e.g., Coordination, Mentorship).
- For each experience entry, produce clean keyword lists (max 20).
- If any section is missing, return an empty list/field.

OUTPUT:
Return ONLY valid JSON.
"""

def repair_json(text):
    text = text.strip()
    text = re.sub(r'^[^{]*', '', text)
    text = re.sub(r'[^}]*$', '', text)
    text = re.sub(r',\s*([}\]])', r'\1', text)
    text = text.replace("\n", " ")
    return text

class LLMStructurizer:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def try_parse_json(self, text):
        try:
            return json.loads(text)
        except:
            fixed = repair_json(text)
            return json.loads(fixed)

    def strict_prompt(self, raw_text):
        return (
            "Return ONLY valid JSON. "
            "No explanation. No comments. No markdown.\n\n"
            + raw_text
        )

    def structure_resume(self, raw_text: str) -> dict:
        prompt = PROMPT_TEMPLATE.replace("{{RAW_RESUME_TEXT}}", raw_text)

        try:
            response = self.model.generate_content(prompt)
            cleaned = response.text.strip()

            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            print("Raw LLM Response:")
            print(cleaned[:1000] + "..." if len(cleaned) > 1000 else cleaned)

            return self.try_parse_json(cleaned)

        except Exception:
            strict_response = self.model.generate_content(
                self.strict_prompt(raw_text)
            ).text.strip()

            try:
                return self.try_parse_json(strict_response)
            except:
                return {
                    "contact": {},
                    "summary": "",
                    "skills": {"technical": [], "product": [], "other": []},
                    "experience": [],
                    "projects": [],
                    "education": []
                }
