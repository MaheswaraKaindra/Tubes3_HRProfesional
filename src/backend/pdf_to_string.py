# src/backend/pdf_to_string.py

import os
import pdfplumber

# Opening ONE file at a time and returns its content as ONE string
def pdf_to_string_regex(pdf_path: str) -> str:

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
    
# Just for testing
if __name__ == "__main__":
    pdf_path = "10276858.pdf"
    text = pdf_to_string_regex(pdf_path)
    if text:
        print("Extracted text from PDF:")
        print(text)
    else:
        print("No text extracted from the PDF.")