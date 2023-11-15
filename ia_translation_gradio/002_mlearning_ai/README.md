# 002_mlearning_ai

**This POC uses `facebook/nllb-200-distilled-600M` for translation and everything is integrated into an API propelled by FastAPI. It is using langdetect and again nllb**


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


# install langdetect
pip install langdetect
conda install -c conda-forge langdetect
# See https://pypi.org/project/langdetect/


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