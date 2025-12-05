# parsers/pdf_extractor.py

import os
import tempfile
from typing import Optional

import pdfplumber
from pypdf import PdfReader
import pytesseract
from PIL import Image


class PDFExtractor:
    @staticmethod
    def extract_with_pdfplumber(file_path: str) -> str:
        """Extract text using pdfplumber (best for modern PDFs)."""
        try:
            text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text.append(page.extract_text() or "")
            return "\n".join(text).strip()
        except:
            return ""

    @staticmethod
    def extract_with_pypdf(file_path: str) -> str:
        """Fallback: Extract text using PyPDF (works for older PDFs)."""
        try:
            reader = PdfReader(file_path)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text).strip()
        except:
            return ""

    @staticmethod
    def extract_with_ocr(file_path: str, dpi: int = 300, lang: Optional[str] = None) -> str:
        """Final fallback: OCR extraction for scanned/image PDFs."""
        try:
            text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Save each page as image temporarily
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                        img_path = tmp.name

                    # Convert PDF page → image
                    page.to_image(resolution=dpi).save(img_path)

                    # Run OCR
                    img = Image.open(img_path)
                    extracted = pytesseract.image_to_string(img, lang=lang) if lang else pytesseract.image_to_string(img)
                    text.append(extracted)

                    # Clean temp file
                    os.remove(img_path)

            return "\n".join(text).strip()
        except:
            return ""

    @staticmethod
    def extract_text(file_path: str, ocr_lang: Optional[str] = None) -> str:
        """
        Master extractor: tries PDFPlumber → PyPDF → OCR.
        Returns best possible text.
        """
        # Try pdfplumber
        text = PDFExtractor.extract_with_pdfplumber(file_path)
        if len(text) > 30:
            print("📄 Extracted using: pdfplumber")  # cooment out later
            return text

        # Try PyPDF
        text = PDFExtractor.extract_with_pypdf(file_path)
        if len(text) > 30:
            print("📄 Extracted using: PyPDF")  # later on comment out
            return text

        # Try OCR
        print("🖼️ Using OCR (Tesseract)...")  # later on comment out
        text = PDFExtractor.extract_with_ocr(file_path, lang=ocr_lang)

        if len(text) > 0:
            print("🔍 Extracted using: OCR")  
        else:
            print("❌ OCR extraction failed")

        return text