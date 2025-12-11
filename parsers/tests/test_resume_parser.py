from parsers.resume_parser import ResumeParser

def test_resume_parser_extracts_email_phone():
    sample_text = """
    John Doe
    Email: john@example.com
    Phone: +1-555-123-4567
    Skills: Python, SQL
    """

    parser = ResumeParser(file_path=None)
    parser.raw_text = sample_text   # manually setting text

    result = parser.parse()

    assert result["email"] == "john@example.com"
    assert result["phone"] == "+1-555-123-4567"
    assert "Python" in result["skills"]
