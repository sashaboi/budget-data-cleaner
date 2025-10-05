#!/usr/bin/env python3
"""
Simple PDF text extractor using PyPDF2
"""

from PyPDF2 import PdfReader
import sys

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        print(f"📄 Reading PDF: {pdf_path}")
        print(f"📊 Total pages: {len(reader.pages)}")
        print("=" * 50)
        
        for i, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            text += f"\n--- Page {i} ---\n"
            text += page_text
            text += "\n"
        
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_reader.py <pdf_file_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    
    if text:
        print(text)
    else:
        print("Failed to extract text from PDF")
