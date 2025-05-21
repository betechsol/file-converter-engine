import os
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
from typing import Optional

class FileConverter:
    @staticmethod
    def pdf_to_txt(input_path: str, output_path: str) -> Optional[str]:
        try:
            with open(input_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                text = "\n".join([page.extract_text() for page in reader.pages])
            
            with open(output_path, 'w') as txt_file:
                txt_file.write(text)
            return output_path
        except Exception as e:
            print(f"PDF Error: {str(e)}")
            return None

    @staticmethod
    def docx_to_txt(input_path: str, output_path: str) -> Optional[str]:
        try:
            doc = Document(input_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            
            with open(output_path, 'w') as txt_file:
                txt_file.write(text)
            return output_path
        except Exception as e:
            print(f"DOCX Error: {str(e)}")
            return None

    @staticmethod
    def image_to_txt(input_path: str, output_path: str) -> Optional[str]:
        try:
            text = pytesseract.image_to_string(Image.open(input_path))
            with open(output_path, 'w') as txt_file:
                txt_file.write(text)
            return output_path
        except Exception as e:
            print(f"Image Error: {str(e)}")
            return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert files to TXT")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output TXT file path")
    args = parser.parse_args()

    converter = FileConverter()
    if args.input.endswith('.pdf'):
        converter.pdf_to_txt(args.input, args.output)
    elif args.input.endswith('.docx'):
        converter.docx_to_txt(args.input, args.output)
    elif args.input.lower().endswith(('.png', '.jpg', '.jpeg')):
        converter.image_to_txt(args.input, args.output)
    else:
        print("Unsupported file format")
