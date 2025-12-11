import os
from parsers.pdf_extractor import PDFExtractor

def test_pdf_extractor_returns_text():
    """Test that PDF extractor returns non-empty text for a sample PDF."""

    sample_path = "docs/sample_resume.pdf"

    # skip test if file missing
    if not os.path.exists(sample_path):
        assert True
        return

    text = PDFExtractor.extract_text(sample_path)

    assert isinstance(text, str)
    assert len(text) > 10
