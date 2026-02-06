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
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_augmented_journalist_wp_toolkit/ia_mistral_ocr

# launch the file
python 002_grab_content_mistral_ocr.py


"""
from mistralai import Mistral
from dotenv import load_dotenv
import datauri
import os


load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)



ocr_response = client.ocr.process(
  model="mistral-ocr-latest",
  document={
    "type": "document_url",
    "document_url": "https://arxiv.org/pdf/2501.00663",
  },
)
print(ocr_response)






