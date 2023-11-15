# 004_pyyush_maskedlanguagemodeling


**This POC uses `xlm-roberta-base`, `xlm-roberta-large` for Masked language modeling with FastAPI and Roberta**

You need to create an environment like for instance mine with `Anaconda` named `ia_translation_facebook_nllb`.

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
pip freeze > requirements_full.txt

# to install
pip install -r requirements.txt

# install gradio
pip install gradio
conda install -c conda-forge gradio



# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/004_pyyush_maskedlanguagemodeling/

# launch the api
uvicorn main:app --reload



# launch the Gradio.py
python ui.py


conda install -c anaconda rich
pip install rich

# check
The demo pop in a browser on 
http://localhost:7860 
or 
http://127.0.0.1:7860
```

## Masked Language Modeling


## Setup
Before running the code, please ensure that you have installed the required dependencies mentioned in the requirements.txt file. You can do this by running the following command in your terminal:
```bash
pip3 install -r requirements.txt
```

# FastAPI
To run the FastAPI web server, you can use the following command in your terminal:
``` bash
uvicorn fastAPI:app 
```
Once the server is up and running, you can access the Swagger documentation for the API at <ins>http://127.0.0.1:8000/docs</ins> \
Alternatively, you can use the curl command to test the API as shown below:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hello <mask>",
  "model": "xlm-roberta-base"
}'
```

# Gradio
To run the Gradio web application, you can use the following command in your terminal:
``` bash
python Gradio.py
```
Once the server is up and running, you can access the web application at <ins>http://127.0.0.1:7860</ins>