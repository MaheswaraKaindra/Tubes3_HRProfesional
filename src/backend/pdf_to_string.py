# src/backend/pdf_to_string.py

import os
import pdfplumber
import re

# Opening ONE file at a time and returns its content as ONE string (REGEX version)
def pdf_to_string(pdf_path: str) -> str:

    # Initial checking
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return ""
    
    return_value = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    return_value.append(page_text)
            return "".join(return_value)
        
    except Exception as e:
        print(f"Error processing PDF file {pdf_path}: {e}")
        return ""
    
# Non-regex version for matching text
def normalize_text(text:str) -> str:
    lowered_text = text.lower()
    no_newlines_text = lowered_text.replace('\n', ' ').replace('\r', ' ')
    normalized_text = re.sub(r'\s+', ' ', no_newlines_text).strip()
    return normalized_text
    
# Just for testing
if __name__ == "__main__":
    pdf_path = "10276858.pdf"
    text = pdf_to_string(pdf_path)

    if text:
        print("Extracted text from PDF:")
        print(text)
    normalized_text = normalize_text(text)

    if normalized_text:
        print("Normalized text:")
        print(normalized_text)
        
    else:
        print("No text extracted from the PDF.")