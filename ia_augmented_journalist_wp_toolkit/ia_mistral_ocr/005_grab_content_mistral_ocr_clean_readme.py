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
python 005_grab_content_mistral_ocr_clean_readme.py


"""

import re
from typing import List

def clean_readme(input_path: str, output_path: str, patterns: List[str]) -> None:
    """
    Cleans a README file by removing lines or matches defined by regex patterns.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    for pattern in patterns:
        content = re.sub(pattern, "", content, flags=re.MULTILINE)

    # Clean up leftover blank lines
    content = re.sub(r"\n\s*\n+", "\n\n", content).strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ README cleaned and saved to {output_path}")


if __name__ == "__main__":
    # === CONFIGURATION SECTION ===
    # Externalized file paths — easy to change without touching logic
    

    # PUT YOUR OWN FILES
    # input_filename = "destination/EN_Generative-AI-and-LLMs-for-Dummies_002.md"
    # output_filename = "destination/EN_Generative-AI-and-LLMs-for-Dummies_002_CLEANED.md"

    input_filename = "destination/fake_mistral_ocr_001.md"
    output_filename = "destination/fake_mistral_ocr_002_CLEANED.md"




    # Regex patterns to remove specific content (images, etc.)
    patterns_to_remove = [
        r"!\[.*?\]\(.*?\)",   # Markdown image syntax
        r"<img\s+.*?>"        # HTML image tags
    ]
    # ==============================

    clean_readme(input_filename, output_filename, patterns_to_remove)


# Remove linked images like [![...]](...)
## r"\[!\[.*?\]\(.*?\)\]\(.*?\)"  
# Remove blockquotes
## r"^>.*"                        
# Remove header lines
## r"^#.*"                        





