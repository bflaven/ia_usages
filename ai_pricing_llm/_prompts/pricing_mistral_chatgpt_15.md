
# pricing_mistral_chatgpt_13.md

## prompt_1
As an advanced programmer in Streamlit, write a function that counts the number of caracters in a text stored in a variable named "TEXT_SAMPLE_SUMMARY".



## ChatGPT_1

To count the number of characters in a given text, you can create a Streamlit function that does this and display the result on your Streamlit app. Here's how you'd write a simple function and display the result in a Streamlit application:

```bash
# If Streamlit isn't installed, uncomment the following line
# !pip install streamlit
```

```python
import streamlit as st

# Define the function to count characters
def count_characters(text):
    # Returns the number of characters including spaces
    return len(text)

# Define a sample text
TEXT_SAMPLE_SUMMARY = "Streamlit makes it easy to build and share beautiful apps."

# Create a Streamlit app
def main():
    st.title("Character Count App")

    # Display the text for reference
    st.write("Text:")
    st.text(TEXT_SAMPLE_SUMMARY)

    # Count the number of characters
    character_count = count_characters(TEXT_SAMPLE_SUMMARY)

    # Display the result
    st.write("Number of characters (including spaces):", character_count)

if __name__ == "__main__":
    main()
```

To run the above code:
1. Copy the code to a Python file, say `app.py`.
2. Open a terminal or command prompt.
3. Navigate to the directory containing `app.py`.
4. Run `streamlit run app.py`.
5. This should open a browser or a new tab in an existing browser, where you'll see the text and the character count. 

This simple Streamlit app will display the text stored in `TEXT_SAMPLE_SUMMARY` and show the total number of characters, including spaces.

