# 003_using_gradio


**Using Gradio with some concepts. Plus again for translation extracted from https://huggingface.co/spaces/Geonmo/nllb-translation-demo**

An some other source to understand Gradio. See https://www.gradio.app/guides/quickstart


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
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# install gradio
pip install gradio
pip install sacremoses
conda install -c conda-forge gradio

conda install -c conda-forge sentencepiece
# https://pypi.org/project/sentencepiece/

conda install -c conda-forge sacremoses
# https://pypi.org/project/sentencepiece/


# Model: https://www.gradio.app/guides/using-hugging-face-integrations

# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/003_using_gradio/

# launch the file
python 007_gradio_app_translate.py


# check
# The demo pop in a browser on 
# http://localhost:7860 
# or 
# http://127.0.0.1:7860


# More examples
# https://www.gradio.app/guides/using-hugging-face-integrations
```



```bash
# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/003_using_gradio


# make dir
mkdir 003_using_gradio

# go to the new dir
cd 003_using_gradio

# show env and activate the env
conda info --envs
source activate ia_translation_facebook_nllb
# deactivate if needed
conda deactivate

# install gradio using pip or conda
pip install gradio
# or via https://anaconda.org/conda-forge/gradio
conda install -c conda-forge gradio

# create a file named "001_gradio_app.py"
touch 001_gradio_app.py
```

**Cut and paste the following code into the file touch 001_gradio_app.py**
```python
# cut and paste the code below for 001_gradio_app.py
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    
if __name__ == "__main__":
    demo.launch(show_api=False)   
```


