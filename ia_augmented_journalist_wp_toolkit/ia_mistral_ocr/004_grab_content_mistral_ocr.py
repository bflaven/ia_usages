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
python 004_grab_content_mistral_ocr.py


"""

from dotenv import load_dotenv
from mistralai import Mistral
import base64
import os

# PUT YOUR OWN FILES
# PDF_PATH = "source/Generative-AI-and-LLMs-for-Dummies.pdf"
# OUTPUT_MD = "destination/Generative-AI-and-LLMs-for-Dummies.md"


# PDF_PATH = "source/005_Alliance_for_facts_IA_journalisme_FR_compressed_0.pdf"
# OUTPUT_MD = "destination/005_Alliance_for_facts_IA_journalisme_FR_compressed_0.md"


PDF_PATH = "source/fake_mistral_ocr.pdf"
OUTPUT_MD = "destination/fake_mistral_ocr.md"


load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

# Read the local PDF and build a data: URL
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

b64 = base64.b64encode(pdf_bytes).decode("ascii")
data_url = f"data:application/pdf;base64,{b64}"

# Run OCR
ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": data_url,
    },
    # optional extras:
    # table_format="markdown",  # or "html" / None
)

# Concatenate all pages' markdown
full_markdown = "\n\n".join(page.markdown for page in ocr_response.pages)

# Write to a Markdown file
os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(full_markdown)

print(f"Markdown exported to: {OUTPUT_MD}")





