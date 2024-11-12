# ia_spacy_llm_9.md

## PROMPT_1
As IA, Streamlit and Python expert, write a script that add that has three tabs. For each tab, create a value with st.input, a refresh button and a submit button. If the user click on the submit button, it will st.write the value typed by the user.
For the script, do not forget to code these three things addtionnaly:

Define a title with an icon
Load the page with a full width 
Here are the labels for the tabs: Send to LLM, Similarity score, Explanations



## MISTRAL_1

You're right, I apologize for the oversight. I'll modify the script to include unique keys for each text input widget. Here's the corrected version:

```python
import streamlit as st

# Define a title with an icon
st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")

# Create three tabs
tab1, tab2, tab3 = st.tabs(["Send to LLM", "Similarity score", "Explanations"])

# Tab 1: Send to LLM
with tab1:
    user_input1 = st.text_input("Enter your text:", key="tab1_input")
    if st.button("Refresh1"):
        user_input1 = ""
    if st.button("Submit1"):
        st.write("You entered: ", user_input1)

# Tab 2: Similarity score
with tab2:
    user_input2 = st.text_input("Enter your text:", key="tab2_input")
    if st.button("Refresh2"):
        user_input2 = ""
    if st.button("Submit2"):
        st.write("You entered: ", user_input2)

# Tab 3: Explanations
with tab3:
    user_input3 = st.text_input("Enter your text:", key="tab3_input")
    if st.button("Refresh3"):
        user_input3 = ""
    if st.button("Submit3"):
        st.write("You entered: ", user_input3)
```

In this version, each text input widget has a unique key, which prevents the DuplicateWidgetID error.

## PROMPT_2
As IA, Streamlit and Python expert, write a script that list only the python files inside a directory named "ollama_output", the user can select a file by the filename. He can fill up a form with threed variables three variables: best_title, best_keywords, best_content. If the user click on a submit button, it will append the variables: best_title, best_keywords, best_content as python variables inside the file selected without empty it.

Below, here are examples of the value and the way it has to inserted into the file selected.

```python
best_title = "Kylian Mbappé left out of France squad for Israel and Italy games"

best_keywords = ["Republican Party", "USA 2024", "Donald Trump", "Kamala Harris", "US presidential election", "Democratic Party"]


best_content = "Struggling to make an impact at Real Madrid, star striker Kylian Mbappé has been left out of the France squad for their upcoming matches against Israel and Italy for the UEFA Nations League."
```

## MISTRAL_2

Here's a Python script using Streamlit that fulfills your requirements:

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
    # Convert the comma-separated keywords to a list
    best_keywords = [keyword.strip() for keyword in best_keywords.split(",")]

    # Create the variable assignments as strings
    title_assignment = f"best_title = \"{best_title}\"\n\n"
    keywords_assignment = f"best_keywords = {best_keywords}\n\n"
    content_assignment = f"best_content = \"{best_content}\"\n"

    # Append the variables to the selected file
    with open(os.path.join(directory, selected_file), "a") as f:
        f.write("\n" + title_assignment + keywords_assignment + content_assignment)

    # Confirm that the variables have been appended to the file
    st.success("Variables have been appended to the file.")
```

This script creates a Streamlit app that lists all the Python files in the "ollama_output" directory. The user can select a file from the dropdown menu. They can then fill out a form with three variables: `best_title`, `best_keywords`, and `best_content`. When the user clicks the submit button, the script appends the variables to the selected file as Python variables without emptying it. The `best_keywords` variable is converted from a comma-separated string to a list.


## PROMPT

Modify the prompt below so the result given by the LLM are in the same language as the elements given in the variables. If needed, you add the language as a variable in the prompt such as {language}


``` python
prompt = f"""
    Make 10 proposals for a similar title based on this title_model, 10 keywords based on on the keywords_model and this content_source.

    - title_model
    ```text
    {title_model}
    ```

    - keywords_model
    ```text
    {keywords_model}
    ```

    ```text
    {content_source}
    ```

    Just return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes.
    """
```