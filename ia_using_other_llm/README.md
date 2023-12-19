# ia_using_other_llm


**How to load LLM (falcon, llama2, mistral, mixtral, orca-mini...etc) on a local machine e.g Mac, PC with LM Studio and Ollama**



[Read more on flaven.fr: https://flaven.fr/2023/12/empower-your-workflow-harnessing-the-power-of-lm-studio-and-ollama-for-seamless-local-llm-execution/](https://flaven.fr/2023/12/empower-your-workflow-harnessing-the-power-of-lm-studio-and-ollama-for-seamless-local-llm-execution/)




## EXPLANATIONS
- Modelfile_advanced_llama2: Prompt Model for Ollama
- Modelfile_llama2: Prompt Model for Ollama
- Modelfile_orca-mini: Prompt Model for Ollama
- README.md: This readme
- lm_studio_try_1.png: Below a screen capture from a prompt made in LM Studio 
- math_problem_arthur.py: Python conversion from a basic mathematical problem made with Mistral
- prompts_mistral_public.md: Some prompts made on Mistral both for teenagers problems and professional issues.
- samwit_basic.py: extract from https://github.com/samwit/langchain-tutorials/tree/382e8db4dc5e01fc400bee8d4146cb1a2e9c3150/ollama by Sam Witteveen
- samwit_basic_chain.py: ditto
- samwit_rag.py: ditto

**Convert a UAT made with Cypress into a gherkin to enable migration to another testing framework e.g PlayWright (https://playwright.dev) or simply the Q/A workchain**

![Convert a UAT made with Cypress into a gherkin to enable migration to another testing framework e.g PlayWright (https://playwright.dev) or simply the Q/A workchain](lm_studio_try_1.png "Convert a UAT made with Cypress into a gherkin to enable migration to another testing framework e.g PlayWright (https://playwright.dev) or simply the Q/A workchain")


### commands for Ollama

You can find other info at <a href="https://github.com/jmorganca/ollama" target="_blank" rel="noopener">https://github.com/jmorganca/ollama</a>



```bash
# COMMANDS

# To run and chat with Llama 2
ollama run llama2
ollama run orca-mini
ollama run mistral:text
ollama run falcon:7b


# To run and chat with orca-mini
ollama pull llama2
ollama pull orca-mini

# remove a model
ollama rm llama2
ollama rm orca-mini
ollama rm mistral
ollama rm falcon:7b
ollama rm mistral:text
ollama rm orca-mini:latest



# list the model
ollama list


# when you are in the model you can use
>>> /?
>>> /list
>>> /set verbose

# to get out from the model
/exit

# create a custom prompt
# you need to create a file for your model named "hotwater". It look like a file
ollama create hotwater - ./hotwater

# ollama create [modelFileName] - ./[modelFileName]

```

## VIDEOS

Coming soon
