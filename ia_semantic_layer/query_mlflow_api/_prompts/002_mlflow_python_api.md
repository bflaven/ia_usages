## PROMPT
As a Python and MLflow expert, write a python script that will fullfill  this objective: create inside an experiment with the help of python MLfow API, here are the steps for the script .


1. The mlflow that I want to query is this one `[site]/mlflow/#/experiments`. The url is protected by an .htaccess

```python
# Configuration - Set your credentials here
MLFLOW_TRACKING_URI = "[site]/mlflow"
USERNAME = "[username]"
PASSWORD = "[password]"
```
2. Select in the experiments list, the experiment named  `gold_dataset`. Make this selected experiment a variable that I can be easily change e.g. add it to configuration `# Configuration - Set your credentials here`
3. Follow the steps below and make all the values for each variables easily changeable so I can set different type of run.
	- Pass the prompt to the variable `Prompt Template` e.g. `I have an online store selling {{ stock_type }}. Write a one-sentence advertisement for use in social media.`
	- Define the variables used within the prompt e.g `{{ stock_type }}` which is replaced by the value `books`.
	- Select the model from `Served LLM model` e.g. `mistral-ollama`.
	- Define the value for `Temperature` e.g. `0.2`.
	- Define the value for `Max tokens` e.g. `20000`.
	- Define the value for `New run name` e.g. `bf-auto-[timestamp]`. Can you make the run name include a timestamp and the pattern above?
	- Output the result to a JSON file named after the run defined above, e.g. `bf-auto-[timestamp].json`





## OUTPUT
See 0003_mlflow_python_api.py








