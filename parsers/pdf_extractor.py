from pypdf import PdfReader

class PDFExtractor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract all text from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")