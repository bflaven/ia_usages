# 002_streamlit_no_reruns.md

## PROMPT_1
As an advanced programmer in Python, using Streamlit, can you write a script that load a json file into a variable named "transcript"



## CHATGPT_1


Sure! Here's a simple Streamlit app script that loads a JSON file into a variable named `transcript`.

1. First, make sure you have Streamlit installed. If not, you can install it using:
   ```sh
   pip install streamlit
   ```

2. Create a Python script, for example `app.py`, with the following content:

```python
import streamlit as st
import json

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

st.title("JSON File Loader")

uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Load the JSON file into the transcript variable
    transcript = json.load(uploaded_file)
    
    # Display the loaded JSON data
    st.write(transcript)
    st.success("JSON file loaded successfully!")

# You can also display the transcript variable for debugging purposes
if 'transcript' in locals():
    st.write("Transcript variable contents:", transcript)
```

3. Run the Streamlit app with the following command:
   ```sh
   streamlit run app.py
   ```

This script sets up a simple Streamlit app that allows you to upload a JSON file. The uploaded file is then loaded into the `transcript` variable and displayed on the web app interface. You can further customize this script based on your needs.