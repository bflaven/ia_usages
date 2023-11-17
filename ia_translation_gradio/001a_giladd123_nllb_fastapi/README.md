# 001a_giladd123_nllb_fastapi

**This POC uses `facebook/nllb-200-distilled-600M` for translation and everything is integrated into an API propelled by FastAPI. It is an attempt using No Language Left Behind (for instance nllb-200-distilled-600M) aka nllb and FastAPI to offer an endpoint for translation**


You need to create an environment like for instance mine with `Anaconda` named `ia_translation_facebook_nllb`.

```bash
source activate ia_translation_facebook_nllb

# The minimum to install is transformers
# The env required install transformers
conda install -c huggingface transformers 
# See https://github.com/huggingface/transformers

conda install -c conda-forge fastapi
# https://anaconda.org/conda-forge/fastapi


# Or you can install via the requirements file
pip install -r requirements.txt
```

```bash
[env]
# Conda ia_translation_facebook_nllb
conda create --name ia_translation_facebook_nllb python=3.9.13
conda info --envs
source activate ia_translation_facebook_nllb
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_translation_facebook_nllb

# update conda
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/001a_giladd123_nllb_fastapi/

# case_1
uvicorn webserver:app --reload

# get the docs
http://127.0.0.1:8000/docs

# required
pip install srsly
```

Source: https://github.com/giladd123/nllb-fastapi


## Original readme nllb-fastapi

This is a simple implementation of an api server that uses nllb and ctranslate2 to translate text to different languages

## Prerequisites

This was written in python-3.10 and might not work with older versions of python.

## Setting up the server

1. Install python requirements `pip install -r requirements.txt`
2. Change model to ct2 format `ct2-transformers-converter --model <model_dir> --output_dir=<output_dir>`
3. Start the server by running `python webserver.py --tokenizer-dir <tokenizer_dir> --model-dir <ct2_model_dir>`

Notice that the tokenizer dir is the regular model directory (as gotten from huggingface), left only with the tokenizer files (model files can be left in but are heavy):

```
config.json
special_tokens_map.json
tokenizer_config.json
tokenizer.json
```
