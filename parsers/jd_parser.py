from .llm_structurizer import LLMStructurizer
from .text_cleaner import TextCleaner


class JDParser:
    """
    LLM-powered Job Description parser.
    Uses Groq model + strict JSON extraction prompt.
    """

    def __init__(self, jd_text: str, model="llama-3.3-70b-versatile"):
        self.raw_text = jd_text
        self.clean_text = TextCleaner.clean(jd_text)
        self.model = model

    def parse(self):
        """
        Build prompt → Send to LLM → Return clean JSON.
        """
        llm = LLMStructurizer(model=self.model)

        prompt = llm.build_jd_prompt(self.clean_text)

        data = llm.generate_json(prompt)

        # Add raw text for debugging/traceability
        data["raw_text"] = self.raw_text

        return data

