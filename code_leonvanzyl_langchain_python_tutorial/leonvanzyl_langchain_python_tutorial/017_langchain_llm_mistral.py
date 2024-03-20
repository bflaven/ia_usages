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
python -m pip install BeautifulSoup4

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_using_flowiseai/

# LAUNCH the file
python 017_langchain_llm_mistral.py


https://python.langchain.com/docs/integrations/llms/ollama
https://www.youtube.com/watch?v=hVs8MVydN3A&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=2
https://github.com/leonvanzyl/langchain-python-tutorial/blob/lesson-1/llm.py

https://python.langchain.com/docs/get_started/introduction

- illustration
https://python.langchain.com/docs/modules/data_connection/

https://github.com/kimtth/azure-openai-llm-vector-langchain/blob/8e9cf8fb82b6463c9283ba9c183e6964b111b7ad/code/langchain-%40practical-ai/langchain_2_(%EB%AF%B9%EC%8A%A4%EC%9D%98_%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5).py

- russian stuff
https://github.com/ai-forever/gigachain/tree/f97b4cf1796bd4a05c9e4062e98c8f794930d9c7/libs/langchain

- korean stuff
https://github.com/kimtth/azure-openai-llm-vector-langchain/blob/8e9cf8fb82b6463c9283ba9c183e6964b111b7ad/code/langchain-%40practical-ai/langchain_2_(%EB%AF%B9%EC%8A%A4%EC%9D%98_%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5).py


https://github.com/ohdoking/ollama-with-rag

https://github.com/samwit/langchain-tutorials/blob/382e8db4dc5e01fc400bee8d4146cb1a2e9c3150/ollama/rag.py

https://github.com/aakinlalu/GenerativeAI/blob/0deb8877e55f06bbf42b744dddc53545c44e8cab/notebooks/10_Ollama_with_rag_using_chroma.ipynb#L24

https://www.youtube.com/watch?v=-Ueh5XBpcoY&list=PL4HikwTaYE0GEs7lvlYJQcvKhq0QZGRVn&index=5

"""
# from langchain import StrOutputParser, Ollama, ChatPromptTemplate
# from langchain.prompts import ChatPromptTemplate

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
# from langchain.chains.combine_documents import create_combine_documents_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader



# disable for the moment deprecated message
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def get_documents_from_web(url):

    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents


# print(get_documents_from_web("https://en.wikipedia.org/wiki/Barack_Obama"))

docs = get_documents_from_web(
    "https://en.wikipedia.org/wiki/Barack_Obama")

llm_model = "mistral:latest"
prompt = ChatPromptTemplate.from_template("""
Answer the user's question:
Question: {input}
Context: {context}
""")
llm = Ollama(model=llm_model)
chain = create_stuff_documents_chain(llm, prompt)

docA = Document("Bruno Flaven has been a Project Manager in a wide variety of Internet (Mobile, Website) for 20 years now. Since 2023, Bruno Flaven is working mainly on AI.")

# Invoke the chain
result = chain.invoke({
    "input": "Who is Barack Obama?",
    "context": docs
})

print('\n–-- RESULT')
print(result)



    # llm_model = "mistral:latest"
    # prompt = ChatPromptTemplate.from_template("""
    # Answer the user's question:
    # Question: {input}
    # Context: {context}
    # """)
    # llm = Ollama(model=llm_model)
    # chain = create_stuff_documents_chain(llm, prompt)

"""
docA = Document("Bruno Flaven has been a Project Manager in a wide variety of Internet (Mobile, Website) for 20 years now. Since 2023, Bruno Flaven is working mainly on AI.")
            
# Invoke the chain
result = chain.invoke({
    "input": "Who is Bruno Flaven?",
    "context": [docA]
})

# print('\n–-- RESULT')
# print(result)
"""


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

# print('\n–-- RESULT')
# print(result)





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