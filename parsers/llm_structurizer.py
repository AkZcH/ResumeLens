import json
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class LLMStructurizer:
    """
    Groq-powered LLM helper for structured JSON extraction.
    Used by JDParser and can be extended for resume parser later.
    """

    def __init__(self, model="llama-3.3-70b-versatile"):
        self.model = model
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

        self.client = Groq(api_key=api_key)

    def build_jd_prompt(self, jd_text: str):
        """
        Strict, expert-level JD parsing template.
        Generates a prompt that forces the model to produce structured JSON.
        """

        return f"""
You are an expert job description analysis engine.

Your job is to transform noisy, raw JD text into a precise,
strictly factual, structured JSON job description representation.

Follow these rules with ZERO exceptions:

STRICT RULES:
1. Do NOT fabricate or infer ANY skills, responsibilities, company details,
   experience levels, metrics, or technologies beyond what the raw text explicitly contains.
2. If information is partially present, extract only that part.
3. Do NOT expand or assume skills not explicitly mentioned.
4. Keep responsibilities, requirements, preferred skills, and details separate.
5. Rewrite responsibility bullets concisely using action verbs, but DO NOT invent new claims.
6. All extracted keywords must be STRICTLY grounded in the JD.
7. Output pure JSON. No commentary, no markdown.

YOUR OBJECTIVE:
Given the RAW_JD_TEXT, produce a structured JSON breakdown with:
- job title
- company
- location
- responsibilities
- required skills
- preferred skills
- experience required
- education required
- technologies/tools/domains mentioned
- concise summary
- clean normalized keyword list

INPUT (RAW_JD_TEXT):
{jd_text}

REQUIRED JSON SCHEMA:
{{
  "job_title": "",
  "company": "",
  "location": "",
  "employment_type": "",
  "experience_required": "",
  "education_required": "",
  "required_skills": [],
  "preferred_skills": [],
  "responsibilities": [],
  "tools_and_tech": [],
  "domains": [],
  "summary": "",
  "keywords": []
}}

ADDITIONAL REQUIREMENTS:
- Extract tools/tech exactly as mentioned (Python, SQL, AWS, React, etc.).
- Extract domain skills (e.g., NLP, Computer Vision, Microservices, DevOps).
- Extract measurable expectations (if present).
- Responsibilities must be 1-line action-driven bullets.
- The 'keywords' array must include ALL unique nouns/skills/tech/tools found (max 30).
- If ANY section is missing, return an empty list or empty string.

OUTPUT:
Return ONLY valid JSON.
"""

    def generate_json(self, prompt: str):
        """
        Sends the prompt to Groq LLM and forces JSON output.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content

        # Attempt to parse JSON
        try:
            return json.loads(output)
        except Exception:
            # If the LLM fails to produce valid JSON, return raw output
            return {"raw_output": output}
