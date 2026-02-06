"""
[env]
# Conda Environment
conda create --name mistral_ocr python=3.9.13
conda info --envs
source activate mistral_ocr
conda deactivate


# BURN AFTER READING
source activate mistral_ocr



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n mistral_ocr

# BURN AFTER READING
conda env remove -n mistral_ocr


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install mistralai python-dotenv datauri

python -m pip install mistralai python-dotenv datauri


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_augmented_journalist_wp_toolkit/ia_mistral_ocr

# launch the file
python 001_grab_content_mistral_ocr.py


"""

import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()

# Define a class to manage PDF files
class PDFManager:
    """
    A simple class to manage a list of PDF files.
    You can add or remove files as needed.
    """

    def __init__(self, initial_files: List[str] = None):
        """
        Initialize the PDFManager with a list of PDF files.
        :param initial_files: List of PDF file paths.
        """
        self.pdf_files = initial_files if initial_files else []

    def add_pdf(self, file_path: str) -> None:
        """
        Add a PDF file to the list.
        :param file_path: Path to the PDF file.
        """
        if file_path not in self.pdf_files:
            self.pdf_files.append(file_path)
            print(f"Added: {file_path}")
        else:
            print(f"File already exists: {file_path}")

    def remove_pdf(self, file_path: str) -> None:
        """
        Remove a PDF file from the list.
        :param file_path: Path to the PDF file.
        """
        if file_path in self.pdf_files:
            self.pdf_files.remove(file_path)
            print(f"Removed: {file_path}")
        else:
            print(f"File not found: {file_path}")

    def list_pdfs(self) -> None:
        """Print the list of PDF files."""
        print("Current PDF files:")
        for pdf in self.pdf_files:
            print(f"- {pdf}")


# Initialize the PDFManager with your files
pdf_manager = PDFManager([
    # PUT YOUR OWN FILES
    # "Generative-AI-and-LLMs-for-Dummies.pdf",
    # "005_Alliance_for_facts_IA_journalisme_FR_compressed_0.pdf",
    "fake_mistral_ocr.pdf"
])

# Example usage
if __name__ == "__main__":
    # List current PDFs
    pdf_manager.list_pdfs()

    # Add a new PDF (example)
    # pdf_manager.add_pdf("new_file.pdf")

    # Remove a PDF (example)
    pdf_manager.remove_pdf("Generative-AI-and-LLMs-for-Dummies.pdf")

    # List PDFs again
    pdf_manager.list_pdfs()

    # Access the Mistral API key from .env
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if mistral_api_key:
        print(f"Mistral API Key loaded successfully.")
    else:
        print("Mistral API Key not found in .env file.")







