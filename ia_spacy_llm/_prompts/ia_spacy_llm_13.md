# ia_spacy_llm_13.md

## PROMPT_1

As IA, Streamlit and Python expert, rewrite the script below, can you reinforce the sanitization for best_keywords, best_title, best_content if some text typed in these variables are with string in double quote e.g. "Les garde-fous ont disparu" : l'UE se prépare face à l'hypothèse d'une victoire de Trump


```python
import os
import streamlit as st

# Define the directory path
directory = "ollama_output"

# Get a list of Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith(".py")]

# Create a selectbox for the user to choose a file
selected_file = st.selectbox("Select a file", python_files)

# Create a form for the user to input the variables
with st.form("input_form"):
    best_title = st.text_input("Best Title")
    best_keywords = st.text_input("Best Keywords (comma-separated)")
    best_content = st.text_area("Best Content")

    # Create a submit button
    submitted = st.form_submit_button("Submit")

# If the user clicks the submit button, append the variables to the selected file
if submitted:
    # Convert the comma-separated keywords to a list and sanitize each keyword
    best_keywords = [repr(keyword.strip()) for keyword in best_keywords.split(",")]

    # Sanitize the best_title and best_content variables to escape any special characters
    best_title = repr(best_title)
    best_content = repr(best_content)



    # Create the variable assignments as strings
    title_assignment = f"best_title = \"{best_title}\"\n\n"
    keywords_assignment = f"best_keywords = {best_keywords}\n\n"
    content_assignment = f"best_content = \"{best_content}\"\n"

    # Append the variables to the selected file
    with open(os.path.join(directory, selected_file), "a") as f:
        f.write("\n\n" + content_assignment + "\n" + title_assignment  + "\n" + keywords_assignment + "\n")

    # Confirm that the variables have been appended to the file
    st.success(f"Variables have been appended to the file {selected_file} in the directory ollama_output.", icon="✅")
```


## MISTRAL_1
The script has been rewritten to reinforce the sanitization for `best_keywords`, `best_title`, and `best_content` if the text typed in these variables contains strings in double quotes.

Here's the updated script:

```python
import os
import streamlit as st
import json

# Define the directory path
directory = "ollama_output"

# Get a list of Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith(".py")]

# Create a selectbox for the user to choose a file
selected_file = st.selectbox("Select a file", python_files)

# Create a form for the user to input the variables
with st.form("input_form"):
    best_title = st.text_input("Best Title")
    best_keywords = st.text_input("Best Keywords (comma-separated)")
    best_content = st.text_area("Best Content")

    # Create a submit button
    submitted = st.form_submit_button("Submit")

# If the user clicks the submit button, append the variables to the selected file
if submitted:
    # Convert the comma-separated keywords to a list and sanitize each keyword
    best_keywords = [json.dumps(keyword.strip()) for keyword in best_keywords.split(",")]

    # Sanitize the best_title and best_content variables to escape any special characters
    best_title = json.dumps(best_title)
    best_content = json.dumps(best_content)

    # Create the variable assignments as strings
    title_assignment = f"best_title = {best_title}\n\n"
    keywords_assignment = f"best_keywords = {best_keywords}\n\n"
    content_assignment = f"best_content = {best_content}\n"

    # Append the variables to the selected file
    with open(os.path.join(directory, selected_file), "a") as f:
        f.write("\n\n" + content_assignment + "\n" + title_assignment  + "\n" + keywords_assignment + "\n")

    # Confirm that the variables have been appended to the file
    st.success(f"Variables have been appended to the file {selected_file} in the directory ollama_output.", icon="✅")
```

In this updated script, I have used the `json.dumps()` function to sanitize the variables. This function converts the input into a JSON-formatted string, which ensures that any special characters or double quotes are properly escaped. This helps prevent any potential issues when appending the variables to the selected file.

## PROMPT_2

As IA, Streamlit and Python expert, rewrite the script below, manage the errors of the file selected, encounter an issue such variables do not exist, the values are uncorrected.... anything that prevents the page from loading correctly with the file selected is incorrect: 


title_proposals
keywords_combinations
best_content
best_title
best_keywords



```python

import os
import ast
import streamlit as st

# Define the directory path
directory = "ollama_output"

# Get a list of Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith(".py")]

# Create a selectbox for the user to choose a file
selected_file = st.selectbox("Select a file", python_files)

# If a file is selected, load the variables from the file
if selected_file:
    with open(os.path.join(directory, selected_file), "r") as f:
        content = f.read()

    # Parse the variables from the file content
    variables = {}
    tree = ast.parse(content)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables[target.id] = ast.literal_eval(node.value)

    # Print out the values for each variable
    st.write("Title Proposals:")
    st.write(variables["title_proposals"])

    st.write("Keywords Combinations:")
    st.write(variables["keywords_combinations"])

    st.write("Best Content:")
    st.code(variables["best_content"])

    st.write("Best Title:")
    st.code(variables["best_title"])

    st.write("Best Keywords:")
    st.write(variables["best_keywords"])

```

## MISTRAL_2

The script has been rewritten to manage errors that may occur when a file is selected. It checks if the required variables (`title_proposals`, `keywords_combinations`, `best_content`, `best_title`, `best_keywords`) exist in the selected file. If any of the variables are missing or if there are any issues with their values, appropriate error messages will be displayed.

Here's the updated script:

```python
import os
import ast
import streamlit as st

# Define the directory path
directory = "ollama_output"

# Get a list of Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith(".py")]

# Create a selectbox for the user to choose a file
selected_file = st.selectbox("Select a file", python_files)

# If a file is selected, load the variables from the file
if selected_file:
    try:
        with open(os.path.join(directory, selected_file), "r") as f:
            content = f.read()

        # Parse the variables from the file content
        variables = {}
        tree = ast.parse(content)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables[target.id] = ast.literal_eval(node.value)

        # Check if all required variables exist
        required_variables = ["title_proposals", "keywords_combinations", "best_content", "best_title", "best_keywords"]
        missing_variables = [var for var in required_variables if var not in variables]

        if missing_variables:
            st.error(f"The selected file is missing the following variables: {', '.join(missing_variables)}")
        else:
            # Print out the values for each variable
            st.write("Title Proposals:")
            st.write(variables["title_proposals"])

            st.write("Keywords Combinations:")
            st.write(variables["keywords_combinations"])

            st.write("Best Content:")
            st.code(variables["best_content"])

            st.write("Best Title:")
            st.code(variables["best_title"])

            st.write("Best Keywords:")
            st.write(variables["best_keywords"])

    except Exception as e:
        st.error(f"An error occurred while loading the selected file: {str(e)}")
```

In this updated script, I have added error handling to manage any issues that may occur when loading the selected file. If any required variables are missing or if there are any errors while parsing the file, appropriate error messages will be displayed. This ensures that the page loads correctly even if there are issues with the selected file.

