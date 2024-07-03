# 001_streamlit_annotated_text.md

## PROMPT_1
As an advanced programmer in Python, using Streamlit, can you write a script using this function "annotated_text" and spacy

```python
with st.echo():
    from annotated_text import annotated_text

    annotated_text(
        "This ",
        ("is", "Verb"),
        " some ",
        ("annotated", "Adj"),
        ("text", "Noun"),
        " for those of ",
        ("you", "Pronoun"),
        " who ",
        ("like", "Verb"),
        " this sort of ",
        ("thing", "Noun"),
        ". ",
        "And here's a ",
        ("word", ""),
        " with a fancy background but no label.",
    )
```

```python
nlp = spacy.load("en_core_web_sm")

sample_text = "I was walking down 5th Avenue yesterday in New York City and I saw Bill Gates!"
doc = nlp(sample_text)
for entity in doc.ents:
    st.write(f"Entity Detected: {entity.text}, of type: {entity.label_}")  
```



## CHATGPT_1
Sure! Here is a Streamlit script that combines `annotated_text` with spaCy to display annotated entities from a sample text:

```python
import streamlit as st
from annotated_text import annotated_text
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample text for analysis
sample_text = "I was walking down 5th Avenue yesterday in New York City and I saw Bill Gates!"

# Process the text with spaCy
doc = nlp(sample_text)

# Create a list to hold annotated text elements
annotated_elements = []

# Iterate over the tokens in the doc and annotate entities
for token in doc:
    if token.ent_type_:
        annotated_elements.append((token.text, token.ent_type_))
    else:
        annotated_elements.append(token.text)

# Display the annotated text using Streamlit
with st.echo():
    annotated_text(*annotated_elements)
```

Here's how this script works:
1. **Imports**: It imports the necessary libraries: `streamlit`, `annotated_text`, and `spacy`.
2. **Load spaCy Model**: It loads the spaCy model `en_core_web_sm`.
3. **Sample Text**: It defines a sample text to be analyzed.
4. **Process Text**: It processes the text with spaCy to obtain entities.
5. **Annotate Text**: It creates a list of elements, annotating entities with their labels.
6. **Display Text**: It uses the `annotated_text` function to display the annotated text in Streamlit.

To run this script, save it as a `.py` file and run it using Streamlit:

```bash
streamlit run your_script_name.py
```

This will start a Streamlit app in your default web browser, displaying the annotated text.

