import os
import fitz  
import pytesseract
from pdf2image import convert_from_path
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from docx2pdf import convert
import pdfplumber

class DocumentProcessor:
    def __init__(self, file_path):
        self.original_path = file_path
        self.file_path = file_path

    def convert_docx_to_pdf(self):
        """
        Converts DOCX to PDF using docx2pdf.
        """
        output_pdf = os.path.splitext(self.file_path)[0] + "_converted.pdf"
        try:
            convert(self.file_path, output_pdf)
            print(f"✅ DOCX converted to PDF: {output_pdf}")
            self.file_path = output_pdf
        except Exception as e:
            print(f"❌ DOCX to PDF conversion failed: {e}")
            self.file_path = None

    def extract_text_from_page(self, page_num):
        """
        Extracts text from a specific page using LangChain's PyMuPDF4LLMLoader.
        """
        loader = PyMuPDF4LLMLoader(self.file_path)
        documents = loader.load()
        for doc in documents:
            if doc.metadata['page'] + 1 == page_num:
                return doc.page_content
        return ""

    def extract_text_from_ocr(self, page_num):
        """
        Enhanced OCR using Tesseract with layout-aware config.
        Attempts sentence-level structure preservation from tables.
        """
        images = convert_from_path(self.file_path, first_page=page_num, last_page=page_num)
        extracted_text = ""
        for image in images:
            text = pytesseract.image_to_string(image, config='--psm 6')
            extracted_text += f"--- OCR Extracted Text (Page {page_num}) ---\n{text.strip()}\n"
        return extracted_text

    def extract_text_with_pdfplumber(self):
        """
        Extracts tables and text from the PDF using pdfplumber.
        Attempts to reconstruct text from tabular data.
        """
        all_text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                tables = page.extract_tables()
                all_text += f"--- Page {page_num} ---\n{text if text else ''}\n"

                for table in tables:
                    table_text = "\n".join([" | ".join(cell if cell else "" for cell in row) for row in table])
                    all_text += f"\n--- Table Extracted (Page {page_num}) ---\n{table_text}\n"
        return all_text

    def process_pdf_pagewise(self):
        """
        Processes PDF page by page: uses OCR for image-heavy pages, else extracts text.
        Returns the entire text from the document.
        """
        all_text = ""
        doc = fitz.open(self.file_path)
        for page_num, page in enumerate(doc, start=1):
            image_list = page.get_images(full=True)
            if image_list:
                print(f"🔍 Page {page_num} contains images. Running OCR...")
                text = self.extract_text_from_ocr(page_num)
            else:
                text = self.extract_text_from_page(page_num)
            all_text += f"--- Page {page_num} ---\n{text}\n"
        return all_text

    def save_text_to_file(self, text, output_path=None):
        """
        Saves the extracted text to a .txt file.
        If no output_path is provided, creates one based on the original file name.
        """
        if not output_path:
            # Create output filename based on original file
            base_name = os.path.splitext(os.path.basename(self.original_path))[0]
            output_path = f"{base_name}_extracted_text.txt"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"💾 Text saved to: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Failed to save text file: {e}")
            return None

    def process_file(self, use_table_aware=False, save_to_file=True, output_path=None):
        """
        Unified entry point: convert DOCX to PDF if needed, then process as PDF.
        Allows optional use of table-aware extraction and saving to file.
        """
        if self.file_path.lower().endswith(".docx"):
            print("📝 Converting DOCX to PDF...")
            self.convert_docx_to_pdf()
            if not self.file_path:
                print("❌ Conversion failed. Exiting.")
                return ""

        if self.file_path.lower().endswith(".pdf"):
            print("📄 Processing PDF file...")
            if use_table_aware:
                extracted_text = self.extract_text_with_pdfplumber()
            else:
                extracted_text = self.process_pdf_pagewise()
            
            # Save to file if requested
            if save_to_file and extracted_text:
                self.save_text_to_file(extracted_text, output_path)
            
            return extracted_text
        else:
            print("❌ Unsupported file format.")
            return ""

if __name__ == "__main__":
    file_path = r"path/to/the/file"
    processor = DocumentProcessor(file_path)

    extracted_text = processor.process_file(use_table_aware=True, save_to_file=False)
    print("EXTRACTED TEXT:")
    print(extracted_text)
