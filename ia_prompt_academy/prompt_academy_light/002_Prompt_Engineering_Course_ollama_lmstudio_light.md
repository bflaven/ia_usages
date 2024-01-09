# 002_Prompt_Engineering_Course_ollama_lmstudio_light.md

**Loading LLM with ollama.ai or lmstudio.ai**

2 great tools to query LLMs confidentially and securely. The only remark the only remark that this calls for is that lmstudio is much more UX friendly than ollama.

- [ollama.ai](https://ollama.ai/)
- [lmstudio.ai](https://lmstudio.ai/)


## lmstudio.ai
**You can download for MAC, PC, LINUX on the official website.**


Step 1: Downloading LM Studio on Mac M2
1. Open your web browser and navigate to lmstudio.ai.
2. Click on the "Download" section and choose the Mac M2 version.
3. Once the download is complete, locate the downloaded file in your Downloads folder.
4. Double-click on the file to start the installation process.
5. Follow the on-screen instructions to complete the installation.

Step 2: Installing LLM Mistral-7B-Instruct-v0.1 by Mistral AI
1. Visit the Mistral AI website to find the LLM Mistral-7B-Instruct-v0.1 model.
2. Download the model file to your computer.
3. Open LM Studio and navigate to the "Models" section.
4. Click on "Import Model" and select the Mistral-7B-Instruct-v0.1 file.
5. Wait for the model to be imported and verified by LM Studio.

Step 3: Using LM Studio for Daily Tasks
1. Demonstrate how to initiate prompts in LM Studio using Mistral AI's model.
2. Perform a prompt to convert a UAT testing file created with Cypress into a Gherkin file.
3. Show how LM Studio can be used to generate Python code for specific tasks.
4. Highlight the versatility of Mistral AI's model in assisting with various daily tasks.

Step 4: Creating a Python File with AI Assistance
1. Open a text editor and create a new Python file.
2. Demonstrate how to use LM Studio to generate Python code snippets for specific functionalities.
3. Discuss the time-saving aspect of using AI to assist in coding tasks.

## ollama.ai
**Using other LLM**

You can use in the terminal any of these LLM
`llama2`, `mistral`, `orca-mini`

- Check https://ollama.ai/library


Step 1: Downloading Ollama from Ollama.ai
- Open your web browser and navigate to [Ollama.ai](https://ollama.ai/).
- Find the "Download" section and choose the Mac M2 version.
- Once downloaded, locate the file in your Downloads folder.

Step 2: Installing LMM "orca-mini" by Microsoft
- Open the Terminal on your Mac M2.
- Navigate to https://ollama.ai/ and download Ollama.
- Install LMM "orca-mini" using the following command.
```bash   
ollama run orca-mini
```
 
Step 3: Running Ollama Commands in the Terminal
- In the Terminal, use the provided Ollama commands.
```bash 
ollama run llama2
ollama run llama2-uncensored
ollama run orca-mini
```  

Step 4: Using Ollama Commands in the Model
- Inside the model, execute commands like:
```bash 
/?
/list
/set verbose
```  

Step 5: Removing Models and Listing Models
- Use the following commands to remove or list models.
```bash 
ollama rm llama2
ollama rm orca-mini
ollama list
```  

Step 6: Performing Prompts on the Terminal
- Directly in the Terminal, issue prompts:
```bash  
# Example prompts
Tell me 5 facts about Roman history:
Tell me 3 facts about Ludwig Wittgenstein:
Give me a short geographical description with a maximum of 10 lines of the country Argentina:
```

Step 7: Using Langchain for Prompts
- Utilize Langchain for prompts in the Terminal.

```python
  llm("Tell me 5 facts about Roman history:")
  llm("Tell me 3 facts about Ludwig Wittgenstein:")
  llm("Give me a short geographical description with a maximum of 10 lines of the country Argentina:")
```
**Using codellama**

You can use `codellama` to help you coding. A large language model that can use text prompts to generate and discuss code.

Code Llama is a model for generating and discussing code, built on top of Llama 2. It’s designed to make workflows faster and efficient for developers and make it easier for people to learn how to code. It can generate both code and natural language about code. Code Llama supports many of the most popular programming languages used today, including Python, C++, Java, PHP, Typescript (Javascript), C#, Bash and more.


**Ollama commands reminder**

```bash
# To run and chat with Llama 2
ollama run llama2
ollama run codellama:7b



# To run and chat with orca-mini
ollama run orca-mini
ollama pull orca-mini
ollama run codellama:7b

# remove a model
ollama rm llama2
ollama rm orca-mini
ollama rm codellama:7b
ollama rm codellama:7b-python


# list the model
ollama list


# when you are in the model you can use
>>> /?
>>> /list
>>> /set verbose

# to get out from the model
/exit
```




