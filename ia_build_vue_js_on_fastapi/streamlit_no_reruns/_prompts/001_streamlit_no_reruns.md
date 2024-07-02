# 001_streamlit_no_reruns.md

## PROMPT_1
As an advanced programmer in Python, using Streamlit, can you write a script that load plotly express, pandas. The script has as header "Fruits List", create a dictionary named \_dic that has Name and Quantity, load this dataframe inside a panda dataframe, create a load with st.button
If load is on write the \_df, add below opt with a st.radio that loads Plot type, Bar or Pie, if opt is equal to Bar load px.bar name and quantity else it will Pie Chart.



## CHATGPT_1

Sure! Below is a script using Streamlit, Plotly Express, and Pandas that follows your requirements:

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# Header
st.title("Fruits List")

# Create a dictionary
_dic = {
    "Name": ["Apple", "Banana", "Cherry", "Date", "Elderberry"],
    "Quantity": [10, 15, 7, 25, 5]
}

# Load dictionary into a pandas dataframe
_df = pd.DataFrame(_dic)

# Create a button to load the dataframe
if st.button('Load'):
    st.write(_df)
    
    # Add radio options for plot type
    opt = st.radio('Plot type', ['Bar', 'Pie'])

    # Display the appropriate plot
    if opt == 'Bar':
        fig = px.bar(_df, x='Name', y='Quantity', title='Bar Plot of Fruits')
        st.plotly_chart(fig)
    elif opt == 'Pie':
        fig = px.pie(_df, names='Name', values='Quantity', title='Pie Chart of Fruits')
        st.plotly_chart(fig)
```

### Explanation:
1. **Importing Libraries**: Import necessary libraries - Streamlit (`st`), Pandas (`pd`), and Plotly Express (`px`).
2. **Header**: Use `st.title("Fruits List")` to create the header.
3. **Dictionary Creation**: Create a dictionary named `_dic` containing fruit names and their quantities.
4. **Load Dictionary into DataFrame**: Convert the dictionary into a pandas DataFrame.
5. **Button for Loading DataFrame**: Use `st.button('Load')` to create a button. When this button is pressed, the DataFrame is displayed using `st.write(_df)`.
6. **Radio Button for Plot Type**: Use `st.radio` to create radio buttons for selecting the plot type ('Bar' or 'Pie').
7. **Conditional Plot Display**: Depending on the selected option, use Plotly Express to generate and display either a bar chart or a pie chart.

To run this script, save it as `app.py` and run it using the command:
```bash
streamlit run app.py
```

This script will create a web interface where users can load a DataFrame and choose to display it as either a bar chart or a pie chart.
