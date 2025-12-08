from parsers.llm_structurizer import LLMStructurizer

class MockResponse:
    text = '{"contact": {"name": "John"}, "skills": {"technical": []}, "experience": [], "projects": [], "education": []}'

class MockModel:
    def generate_content(self, prompt):
        return MockResponse()

def test_llm_structurizer_basic(monkeypatch):
    struct = LLMStructurizer()

    # replace real LLM with mock
    monkeypatch.setattr(struct, "model", MockModel())

    result = struct.structure_resume("dummy text")

    assert result["contact"]["name"] == "John"
