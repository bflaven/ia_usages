#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""


[env]
# Conda Environment
conda create --name news_category_analysis python=3.9.13
conda info --envs
source activate news_category_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n news_category_analysis

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


python -m pip install transformers




# [path]
cd /Users/brunoflaven/Documents/02_copy/DERA_Ghislain_USECASES/text-classification/

# LAUNCH the file
python 016_ollama_text_classification.py



# install
python -m pip install langchain faiss-cpu
python -m pip install langchain-community



https://medium.com/scrapehero/building-qa-bot-with-ollama-local-llm-platform-c11d1e1f3035
https://github.com/amalaj7/Tesla-Insights-Ollama/blob/main/main.py

https://github.com/mneedham/LearnDataWithMark/blob/main/few-shot-prompting/notebooks/FewShotPrompting-Tutorial.ipynb



"""
from langchain_community.llms import Ollama

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = Ollama(model="mistral:latest", 
            #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0.9,
             )

pre_prompt = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling, "

brainstorm_template = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling. Please brainstorm and create 10 ideas for a short to medium length blog post around the topic: {topic}?"
brainstorm_prompt = PromptTemplate(
    input_variables=["topic"],
    template=brainstorm_template,
)

brainstorm_chain = LLMChain(llm=llm, 
                 prompt=brainstorm_prompt,
                 verbose=False)

user_input = input("What do you want to write a blog about: ")

# Run the chain only specifying the input variable.
# brainstorm_output = brainstorm_chain.run(user_input)
brainstorm_output = brainstorm_chain.invoke(user_input)

print(brainstorm_output)

pre_prompt_intro = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling, "

introduction_template = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling. Please output only an introduction about idea number {number} from the following list " + brainstorm_output + " Don't respond with any text other than the introduction "

introduction_prompt = PromptTemplate(
    input_variables=["number"],
    template=introduction_template
)

introduction_chain = LLMChain(llm=llm,
                    prompt=introduction_prompt,
                    verbose=False)

choice_input = int(input("\n\nNumber to generate: "))

# introduction_output = introduction_chain.run(choice_input)
introduction_output = introduction_output.invoke(choice_input)


pre_prompt_body = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling, "

body_template = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling. Please read through the following introduction and write the body of the blog post: {intro} don't respond with any text other than the body of the blog "

body_prompt = PromptTemplate(
    input_variables=["intro"],
    template=body_template
)

body_chain = LLMChain(llm=llm,
                    prompt=body_prompt,
                    verbose=False)

# body_output = body_chain.run(introduction_output)
body_output = body_output.invoke(introduction_output)


pre_prompt_end = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling, "

end_template = "You are a respected industry leader in writing and blogs with indepth knowledge of all factors including tone and storytelling. Please read through the following body of a blog post then write a suitable conclussion of the blog post: {intro} {body} don't respond with any text othet than the conclussion of the blog "

end_prompt = PromptTemplate(
    input_variables=["body"],
    template=end_template
)

end_chain = LLMChain(llm=llm,
                    prompt=end_prompt,
                    verbose=False)

# end_output = end_chain.run(introduction_output, body_output)
end_output = end_chain.invoke(introduction_output, body_output)



print("\n\n\nHere is the final blog post: \n\n\n"+ end_output)





