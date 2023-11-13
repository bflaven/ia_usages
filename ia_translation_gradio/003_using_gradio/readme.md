# 003_using_gradio


<h2>Using gradio</h2>
--- Source: https://www.gradio.app/guides/quickstart

<pre>
# go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_translation/


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
</pre>

<b>Cut and paste the following code into the file touch 001_gradio_app.py</b>
<pre>
# cut and paste the code below for 001_gradio_app.py
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    
if __name__ == "__main__":
    demo.launch(show_api=False)   
</pre>