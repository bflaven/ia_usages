#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name langchain_fastapi_poc python=3.9.13
conda info --envs
source activate langchain_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n langchain_fastapi_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

python -m pip install python-dotenv
python -m pip install langchain-openai

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/

# LAUNCH the file
python 014_langchain_llm_mistral.py


https://python.langchain.com/docs/integrations/llms/ollama
https://www.youtube.com/watch?v=hVs8MVydN3A&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=2
https://github.com/leonvanzyl/langchain-python-tutorial/blob/lesson-1/llm.py

https://python.langchain.com/docs/get_started/introduction

- illustration
https://python.langchain.com/docs/modules/data_connection/

https://github.com/kimtth/azure-openai-llm-vector-langchain/blob/8e9cf8fb82b6463c9283ba9c183e6964b111b7ad/code/langchain-%40practical-ai/langchain_2_(%EB%AF%B9%EC%8A%A4%EC%9D%98_%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5).py

https://github.com/ai-forever/gigachain/tree/f97b4cf1796bd4a05c9e4062e98c8f794930d9c7/libs/langchain

LangChain Tutorial (Python) #4: Chat with Documents using Retrieval Chains
https://www.youtube.com/watch?v=-Ueh5XBpcoY&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=4


"""
# from langchain import StrOutputParser, Ollama, ChatPromptTemplate
# from langchain.prompts import ChatPromptTemplate

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
# from langchain.chains.combine_documents import create_combine_documents_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


llm_model = "mistral:latest"
prompt = ChatPromptTemplate.from_messages(
                [("system", "What are everyone's favorite colors:\\n\\n{context}")]
            )
llm = Ollama(model=llm_model)
chain = create_stuff_documents_chain(llm, prompt)

docs = [
        Document(page_content="Jesse loves red but not yellow"),
        Document(page_content = "Jamal loves green but not as much as he loves orange")
            ]




result = chain.invoke({"context": docs})
print('\n–-- RESULT')
print(result)



# prompt = ChatPromptTemplate.from_template("""
# Answer the user's question:
# Question: {input}
# Context: {context}
#     """)

# # Create a chain for combining documents
# chain = create_stuff_documents_chain(
#     llm=llm_model,
#     prompt=prompt
# )

# # Invoke the chain
# result = chain.invoke({
#     "input": "Who is Bruno Flaven?",
#     "context": [docA]
# })

print('\n–-- RESULT')
print(result)





"""
    prompt = ChatPromptTemplate.from_messages(
                [("system", "What are everyone's favorite colors:\\n\\n{context}")]
            )
            llm = ChatOpenAI(model_name="gpt-3.5-turbo")
            chain = create_stuff_documents_chain(llm, prompt)

            docs = [
                Document(page_content="Jesse loves red but not yellow"),
                Document(page_content = "Jamal loves green but not as much as he loves orange")
            ]

            chain.invoke({"context": docs})
    
"""