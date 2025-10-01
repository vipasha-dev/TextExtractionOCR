📄 DocumentProcessor – Intelligent PDF/DOCX Text Extraction & OCR Tool






🔹 Overview

The DocumentProcessor is a Python-based utility for extracting, processing, and structuring text from PDF and DOCX documents.
It supports digitally generated PDFs, scanned image-based PDFs, and tables, making it a powerful tool for document digitization, regulatory compliance, and NLP pipelines.

✨ Features

📝 DOCX → PDF conversion using docx2pdf.

📄 Text extraction from PDFs using PyMuPDF + LangChain’s PyMuPDF4LLMLoader.

🔍 OCR support for scanned PDFs using Tesseract (pytesseract + pdf2image).

📊 Table-aware extraction with pdfplumber.

⚡ Smart page-wise processing → detects if a page has images and applies OCR automatically.

💾 Save to .txt or return as string for downstream ML/NLP tasks.

🛠️ Tech Stack

Python 3.8+

Libraries:

fitz (PyMuPDF)

langchain-pymupdf4llm

pytesseract

pdf2image

pdfplumber

docx2pdf

🚀 Installation
# Clone the repository
git clone https://github.com/yourusername/DocumentProcessor.git
cd DocumentProcessor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make sure Tesseract is installed and added to PATH
# Example (Windows): C:\Program Files\Tesseract-OCR\tesseract.exe

📌 Usage
from document_processor import DocumentProcessor

# Load file (DOCX or PDF)
file_path = "Centralized Monitoring Plan.docx"
processor = DocumentProcessor(file_path)

# Process with table-aware extraction
text = processor.process_file(use_table_aware=True, save_to_file=True)

print("Extracted Text:")
print(text[:500])   # print first 500 chars

📂 Example Output
--- Page 1 ---
This is extracted text from page 1...

--- Table Extracted (Page 2) ---
Column1 | Column2 | Column3
Value1  | Value2  | Value3

💡 Use Cases

📑 Regulatory Document Analysis (SOPs, FDA/EMA guidelines).

📝 Business Document Digitization (contracts, reports).

📊 Structured Data Extraction from financial/lab reports.

🔍 Deviation/Comparison Analysis in compliance workflows.

📜 License

This project is licensed under the MIT License.

🙌 Acknowledgements

PyMuPDF

LangChain

Tesseract OCR

pdfplumber
