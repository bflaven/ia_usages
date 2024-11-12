# ia_spacy_llm_7.md




## PROMPT_1
As IA and Python expert, write a script that enable to pass a prompt to Ollama, installed locally on mac, with the model "mistral:latest" and get the answer.


## MISTRAL (codestral)

Sure, I can help you with that. Here's a simple Python script that uses the `subprocess` module to interact with Ollama. This script assumes that Ollama is installed and running locally on your Mac.

```python
import subprocess

def get_ollama_response(prompt, model="mistral:latest"):
    command = f"ollama run {model} -f json"
    process = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = process.communicate(input=prompt)

    if err:
        print(f"Error: {err}")
        return None

    response = out.strip().split('\n')[-1]  # Extract the last line which should contain the JSON response
    response_json = json.loads(response)
    return response_json["response"]

prompt = "Your prompt here"
response = get_ollama_response(prompt)
print(response)
```

This script defines a function `get_ollama_response` that takes a prompt and a model name as input. It then constructs a command to run Ollama with the specified model and the `-f json` flag to format the output as JSON. The prompt is sent to the standard input of the Ollama process, and the output is captured. The function then extracts the response from the JSON output and returns it.

Please replace `"Your prompt here"` with your actual prompt. Also, make sure you have the `json` module imported if you're using Python 3.5 or higher. If you're using an earlier version of Python, you'll need to install the `simplejson` package and replace `json` with `simplejson` in the script.

## PROMPT_2
As IA and Python expert, rewrite this script in `code_example` so it enables to pass a sophisticated prompt to Ollama like the one below in `prompt_example`


- `prompt_example`
```text
Return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes. 


Title Proposals:
1. Trump's Resurgence: US Election Reveals Cracks in Anti-Trump Coalition
2. The Fragmented Democratic Coalition: Kamala Harris Falters as Trump Wins US Election
3. Republican Surge: Class, Race, and Age Factors in Trump's US Presidential Victory
4. Democratic Divides: US Election Results Expose Cracks in the Anti-Trump Alliance
5. US Election 2024: Kamala Harris Struggles Amidst Shifts in American Voter Base
6. The Coalition Cracks: Trump's Comeback and the Fissures in Democratic Support
7. US Presidential Election Aftermath: Examining the Democratic Coalition's Vulnerabilities
8. The New Political Landscape: Trump Capitalizes on Shifts in Class, Race, and Age
9. Kamala Harris' Struggles: Understanding the Cracks in the Anti-Trump Coalition
10. The Evolving American Voter Base: Insights from the 2024 US Presidential Election

Keywords:
1. Republican Party, USA 2024, Democratic Party, Donald Trump, Kamala Harris, US presidential election, coalition, 
class, race, age.
2. US Election, Donald Trump, Political Shifts, Democratic Coalition, Class, Race, Age, Kamala Harris.
3. Anti-Trump Coalition, Cracks, US Election Results, Republican Surge, Class, Race, Age.
4. Kamala Harris, Democratic Divides, US Election 2024, Political Landscape, Trump, Shifts.
5. Democratic Party, Coalition, US Presidential Election, Voter Base, Class, Race, Age, Trump.
6. Republican Comeback, Democratic Vulnerabilities, Class, Race, Age, Trump, Kamala Harris.
7. Political Landscape, US Election 2024, Coalition, Trump, Kamala Harris, Class, Race, Age.
8. Anti-Trump Alliance, Cracks, US Presidential Election, Democratic Party, Republican Surge, Voter Base.
9. Voter Base, Democratic Coalition, US Election Results, Class, Race, Age, Trump.
10. Class, Race, Age, Political Shifts, Kamala Harris, Trump, Democratic Party, US Election 2024.
```

- `code_example`
```python
import ollama
response = ollama.chat(model='mistral:latest', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
```

## MISTRAL (codestral)

Here is the rewritten script in Python that enables you to pass a sophisticated prompt to Ollama:

```python
import ollama

prompt = """
Return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes.

Title Proposals:
1. Trump's Resurgence: US Election Reveals Cracks in Anti-Trump Coalition
2. The Fragmented Democratic Coalition: Kamala Harris Falters as Trump Wins US Election
3. Republican Surge: Class, Race, and Age Factors in Trump's US Presidential Victory
4. Democratic Divides: US Election Results Expose Cracks in the Anti-Trump Alliance
5. US Election 2024: Kamala Harris Struggles Amidst Shifts in American Voter Base
6. The Coalition Cracks: Trump's Comeback and the Fissures in Democratic Support
7. US Presidential Election Aftermath: Examining the Democratic Coalition's Vulnerabilities
8. The New Political Landscape: Trump Capitalizes on Shifts in Class, Race, and Age
9. Kamala Harris' Struggles: Understanding the Cracks in the Anti-Trump Coalition
10. The Evolving American Voter Base: Insights from the 2024 US Presidential Election

Keywords:
1. Republican Party, USA 2024, Democratic Party, Donald Trump, Kamala Harris, US presidential election, coalition, class, race, age.
2. US Election, Donald Trump, Political Shifts, Democratic Coalition, Class, Race, Age, Kamala Harris.
3. Anti-Trump Coalition, Cracks, US Election Results, Republican Surge, Class, Race, Age.
4. Kamala Harris, Democratic Divides, US Election 2024, Political Landscape, Trump, Shifts.
5. Democratic Party, Coalition, US Presidential Election, Voter Base, Class, Race, Age, Trump.
6. Republican Comeback, Democratic Vulnerabilities, Class, Race, Age, Trump, Kamala Harris.
7. Political Landscape, US Election 2024, Coalition, Trump, Kamala Harris, Class, Race, Age.
8. Anti-Trump Alliance, Cracks, US Presidential Election, Democratic Party, Republican Surge, Voter Base.
9. Voter Base, Democratic Coalition, US Election Results, Class, Race, Age, Trump.
10. Class, Race, Age, Political Shifts, Kamala Harris, Trump, Democratic Party, US Election 2024.
"""

response = ollama.chat(model='mistral:latest', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

print(response['message']['content'])
```

This script will send the prompt to the Ollama model and print the response.

## PROMPT

Change the script so the output goes to a readme file named ia_ollama_{datetime}.md where datetime is a pyhton datetime.


## MISTRAL (codestral)
Here is the revised script that writes the output to a markdown file named `ia_ollama_{datetime}.md` where `datetime` is the current date and time:

```python
import ollama
from datetime import datetime

prompt = """
Return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes.

Title Proposals:
1. Trump's Resurgence: US Election Reveals Cracks in Anti-Trump Coalition
2. The Fragmented Democratic Coalition: Kamala Harris Falters as Trump Wins US Election
3. Republican Surge: Class, Race, and Age Factors in Trump's US Presidential Victory
4. Democratic Divides: US Election Results Expose Cracks in the Anti-Trump Alliance
5. US Election 2024: Kamala Harris Struggles Amidst Shifts in American Voter Base
6. The Coalition Cracks: Trump's Comeback and the Fissures in Democratic Support
7. US Presidential Election Aftermath: Examining the Democratic Coalition's Vulnerabilities
8. The New Political Landscape: Trump Capitalizes on Shifts in Class, Race, and Age
9. Kamala Harris' Struggles: Understanding the Cracks in the Anti-Trump Coalition
10. The Evolving American Voter Base: Insights from the 2024 US Presidential Election

Keywords:
1. Republican Party, USA 2024, Democratic Party, Donald Trump, Kamala Harris, US presidential election, coalition, class, race, age.
2. US Election, Donald Trump, Political Shifts, Democratic Coalition, Class, Race, Age, Kamala Harris.
3. Anti-Trump Coalition, Cracks, US Election Results, Republican Surge, Class, Race, Age.
4. Kamala Harris, Democratic Divides, US Election 2024, Political Landscape, Trump, Shifts.
5. Democratic Party, Coalition, US Presidential Election, Voter Base, Class, Race, Age, Trump.
6. Republican Comeback, Democratic Vulnerabilities, Class, Race, Age, Trump, Kamala Harris.
7. Political Landscape, US Election 2024, Coalition, Trump, Kamala Harris, Class, Race, Age.
8. Anti-Trump Alliance, Cracks, US Presidential Election, Democratic Party, Republican Surge, Voter Base.
9. Voter Base, Democratic Coalition, US Election Results, Class, Race, Age, Trump.
10. Class, Race, Age, Political Shifts, Kamala Harris, Trump, Democratic Party, US Election 2024.
"""

response = ollama.chat(model='mistral:latest', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

# Get the current date and time
now = datetime.now()

# Format the date and time as a string
datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create the filename
filename = f"ia_ollama_{datetime_str}.md"

# Write the response to the file
with open(filename, "w") as f:
    f.write(response['message']['content'])
```

This script will write the response to a markdown file named `ia_ollama_{datetime}.md` where `datetime` is the current date and time in the format `YYYY-MM-DD_HH-MM-SS`.



# PROMPT
write the file in directory named "ollama_output"

## MISTRAL (codestral)
Here is the revised script that writes the output to a markdown file named `ia_ollama_{datetime}.md` in a directory named `ollama_output`:

```python
import ollama
from datetime import datetime
import os

prompt = """
Return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes.

Title Proposals:
1. Trump's Resurgence: US Election Reveals Cracks in Anti-Trump Coalition
2. The Fragmented Democratic Coalition: Kamala Harris Falters as Trump Wins US Election
3. Republican Surge: Class, Race, and Age Factors in Trump's US Presidential Victory
4. Democratic Divides: US Election Results Expose Cracks in the Anti-Trump Alliance
5. US Election 2024: Kamala Harris Struggles Amidst Shifts in American Voter Base
6. The Coalition Cracks: Trump's Comeback and the Fissures in Democratic Support
7. US Presidential Election Aftermath: Examining the Democratic Coalition's Vulnerabilities
8. The New Political Landscape: Trump Capitalizes on Shifts in Class, Race, and Age
9. Kamala Harris' Struggles: Understanding the Cracks in the Anti-Trump Coalition
10. The Evolving American Voter Base: Insights from the 2024 US Presidential Election

Keywords:
1. Republican Party, USA 2024, Democratic Party, Donald Trump, Kamala Harris, US presidential election, coalition, class, race, age.
2. US Election, Donald Trump, Political Shifts, Democratic Coalition, Class, Race, Age, Kamala Harris.
3. Anti-Trump Coalition, Cracks, US Election Results, Republican Surge, Class, Race, Age.
4. Kamala Harris, Democratic Divides, US Election 2024, Political Landscape, Trump, Shifts.
5. Democratic Party, Coalition, US Presidential Election, Voter Base, Class, Race, Age, Trump.
6. Republican Comeback, Democratic Vulnerabilities, Class, Race, Age, Trump, Kamala Harris.
7. Political Landscape, US Election 2024, Coalition, Trump, Kamala Harris, Class, Race, Age.
8. Anti-Trump Alliance, Cracks, US Presidential Election, Democratic Party, Republican Surge, Voter Base.
9. Voter Base, Democratic Coalition, US Election Results, Class, Race, Age, Trump.
10. Class, Race, Age, Political Shifts, Kamala Harris, Trump, Democratic Party, US Election 2024.
"""

response = ollama.chat(model='mistral:latest', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

# Get the current date and time
now = datetime.now()

# Format the date and time as a string
datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create the filename
filename = f"ia_ollama_{datetime_str}.md"

# Create the directory if it doesn't exist
os.makedirs("ollama_output", exist_ok=True)

# Write the response to the file in the directory
with open(os.path.join("ollama_output", filename), "w") as f:
    f.write(response['message']['content'])
```

This script will write the response to a markdown file named `ia_ollama_{datetime}.md` in a directory named `ollama_output`. If the directory doesn't exist, it will be created.