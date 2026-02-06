
# 001_mistral_ocr.md

## PROMPT_1 

As a Python and Mistral OCR, can you write a script in Python that merge SCRIPT_1 into SCRIPT_2

- SCRIPT_2
```python
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
    # "Generative-AI-and-LLMs-for-Dummies.pdf",
    # "005_Alliance_for_facts_IA_journalisme_FR_compressed_0.pdf",
    "analyse_projet_ia_den_fmm_v1_241125.pdf"
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
```

- SCRIPT_1
```python
import os
import base64
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.ocr import OcrResponse

# Load environment variables from .env file
load_dotenv()

# Initialize the Mistral client
client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

def read_file_as_data_uri(file_path: str) -> str:
    """
    Read a local file and return its content as a data URI.
    :param file_path: Path to the local file.
    :return: Data URI string.
    """
    with open(file_path, "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
        return f"data:application/pdf;base64,{base64_encoded}"

def process_local_pdf(file_path: str) -> OcrResponse:
    """
    Process a local PDF file using Mistral OCR.
    :param file_path: Path to the local PDF file.
    :return: OCR response from Mistral API.
    """
    data_uri = read_file_as_data_uri(file_path)
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "data_uri",
            "data_uri": data_uri,
        },
    )
    return ocr_response

# Example usage
if __name__ == "__main__":
    # Replace with the path to your local PDF file
    local_pdf_path = "Generative-AI-and-LLMs-for-Dummies.pdf"

    # Process the local PDF
    response = process_local_pdf(local_pdf_path)
    print(response)
```











