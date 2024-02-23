# fastapi_usecase_1_sentiment_analysis

- usecase_1 comments sentiment analysis (usecase_1_sentiment_analysis)

- **Source :** sentiment_analysis_reviews_0.csv, sample de commentaires (1001).
- **Objective :** Give a sentiment analysis on all of these comments.
- **Negative/positive:**  prediction via ML on the nature of the comment**


**To convert the project into a deployable app**
**Here are the requirements to manipulate locally the file**


```bash

[env]
# Conda Environment
conda create --name sentiment_analysis python=3.9.13
conda info --envs
source activate sentiment_analysis
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [install]
# for ML
python -m pip install transformers
python -m pip install pyarrow
python -m pip install pandas
python -m pip install numpy
python -m pip install tensorflow
python -m pip install sentencepiece
python -m pip install torchvision 

# for API
python -m pip install fastapi uvicorn 
python -m pip install fastapi transformers

# for UX
python -m pip install streamlit requests


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/fastapi_usecase_1_sentiment_analysis/

# LAUNCH THE API
uvicorn app.main:app --reload

# Check http://localhost:8000
# Check http://127.0.0.1:8000

# LAUNCH THE WEBAPP
streamlit run ux.py
# Check http://localhost:8501


```


## HOW-TO

### PROMPT_1
**As a prominent developper, convert the code below into a Python Class and create a file named "model.py". This file "model.py" and the Class has to be imported and declared into a file named "main.py" that will load the model inside an endpoint driven by FastAPI so the user can get a result.**


### RESULT_PROMPT_1
To convert the provided code into a Python class and separate it into files as instructed, follow the steps below.

First, create a file named `model.py` and define a class named `SentimentAnalysisModel` that encapsulates the functionality of sentiment analysis using the given transformer model.

```python
# model.py
from transformers import pipeline

class SentimentAnalysisModel:
    def __init__(self):
        self.model = pipeline(
            task='text-classification',
            model="cmarkea/distilcamembert-base-sentiment",
            tokenizer="cmarkea/distilcamembert-base-sentiment",
            top_k=None
        )

    def analyze_sentiment(self, message):
        result = self.model(message)
        return result
```

Next, create a file named `main.py` where you import the `SentimentAnalysisModel` class and use it to perform sentiment analysis on FastAPI endpoint.

```python
# main.py
from fastapi import FastAPI
from model import SentimentAnalysisModel

app = FastAPI()

# Instantiate the SentimentAnalysisModel
sentiment_model = SentimentAnalysisModel()

@app.get("/sentiment-analysis/")
async def get_sentiment_analysis(message: str):
    """
    Perform sentiment analysis on the given message.
    """
    result = sentiment_model.analyze_sentiment(message)
    return result
```

Make sure you have FastAPI and Transformers installed in your environment. You can install them using pip if you haven't already:

```
pip install fastapi transformers
```

Now, you can run the FastAPI server by executing `uvicorn main:app --reload` in your terminal. This command starts the server, and you can access the sentiment analysis endpoint at `http://127.0.0.1:8000/sentiment-analysis/`.

You can test the endpoint by sending a GET request with a message parameter, like this:

```
http://127.0.0.1:8000/sentiment-analysis/?message=Your%20message%20goes%20here
```

Replace `Your%20message%20goes%20here` with the message you want to analyze. The server will return the sentiment analysis result.


### PROMPT_2
**As a prominent developper, add a streamlit application in a file named "ux.py" that called the endpoint sentiment analysis. The user is able to type inside a field named "comment", click on button submit and get the result into a json array visible that can folded and unfolded with a button named "Hidden result". Here is a an exemple of th JSON provided by the API.**


### RESULT_PROMPT_2


To create a Streamlit application that calls the sentiment analysis endpoint and displays the result in a collapsible JSON format along with the mapped appreciation, you can create a file named `ux.py` with the following code:

```python
import streamlit as st
import requests

# Define the URL of the sentiment analysis endpoint
SENTIMENT_ANALYSIS_URL = "http://127.0.0.1:8000/sentiment-analysis/"

# Mapping of sentiment labels to appreciation
sentiment_mapping = {
    "1 star": "terrible appreciation",
    "2 stars": "bad appreciation",
    "3 stars": "neutral appreciation",
    "4 stars": "good appreciation",
    "5 stars": "excellent appreciation"
}

def perform_sentiment_analysis(comment):
    """
    Perform sentiment analysis by calling the API endpoint.
    """
    params = {"message": comment}
    response = requests.get(SENTIMENT_ANALYSIS_URL, params=params)
    result = response.json()
    return result

# Streamlit UI
st.title("Sentiment Analysis")

comment = st.text_input("Enter your comment:")
submit_button = st.button("Submit")

if submit_button and comment:
    result = perform_sentiment_analysis(comment)
    
    st.subheader("Sentiment Analysis Result:")
    st.json(result)

    st.subheader("Mapped Appreciation:")
    for item in result[0]:
        label = item["label"]
        score = item["score"]
        mapped_appreciation = sentiment_mapping[label]
        st.write(f"{label}: {mapped_appreciation}")
```

Make sure to replace `http://127.0.0.1:8000/sentiment-analysis/` with the correct URL of your sentiment analysis endpoint.

To run the Streamlit application, you can use the following command in your terminal:

```
streamlit run ux.py
```

This will start the Streamlit server, and you can access the application in your web browser. Users can enter a comment, click on the Submit button, and see the sentiment analysis result along with the mapped appreciation. The JSON result will be collapsible using the "Hidden result" button provided by Streamlit.

### PROMPT_2
**As a prominent developper, add a streamlit application in a file named "ux.py" that called the endpoint sentiment analysis. The user is able to type inside a field named "comment", click on button submit and get the result into a json array visible that can folded and unfolded with a button named "Hidden result". Here is a an exemple of th JSON provided by the API.**


### RESULT_PROMPT_3

I want you to act as a data scientist. What are the best visualization in Plotly to illustrate correlation between these columns: 'date','source','message','label','score' in a dataframe named 'df' that is provoded by the reading of the csv file in Pandas.

date is the record date in a french format including date and hour e.g "21/01/2024 17:38:46"
source is the source of a new with hashtags, emojis... etc like a kind of social netwok post.
message is the comment attached to this source, the previous column.
label is the sentiment analysis comrpised between 1 star (bad) to 5 stars (excelent)
score is the porbability for the highste label


,"🇲🇦🇨🇩 Le #Maroc et la #RDC se quittent sur un nul (1-1), ce dimanche 21 janvier au stade Laurent Pokou de #SanPedro 🇨🇮 ⚽🌍

➡️ Si les Lions de l’Atlas 🇲🇦 ont ouvert le score très rapidement (5’) grâce à Achraf Hakimi, les Léopards ont recollé ",La bagarre créée par le coach marocain prouve le dire du coach tanzanien les marocains ce crois tous permis,4 stars,0.3368487954139709





--- prompt_model
I want you to act as a data scientist coding in R. Given a dataframe {dataframe name} containing the columns {column names} Use ggplot2 to plot a {chart type and requirement}.

--- prompt_example_0
I want you to act as a data scientist coding in R. Given a dataframe 'gapminder' containing the columns 'country', 'gdp', 'year'. Use ggplot2 to plot a 'a line chart of GDP against the year of each country'.

--- prompt_example_1
I want you to act as a data scientist coding in Python for Streamlit. Given a dataframe named "result". The result is obtained by readinding a csv file named "full_quintly_commentaires_sentiment_analysis_1.csv" containing the columns "date,source,message,label,score". Use Plotly to plot a 'a line chart of label against the year of each score'.

--- prompt_example_2
I want you to act as a data scientist coding in Python for Streamlit. Given a dataframe named "result". The result is obtained by readinding a csv file named "full_quintly_commentaires_sentiment_analysis_1.csv" containing the columns "date,source,message,label,score". Use Plotly to plot a 'scatter' where you can see both label and score.


--- prompt_example_3
I want you to act as a data scientist coding in Python for Streamlit. Given a dataframe named "result". The result is obtained by readinding a csv file named "full_quintly_commentaires_sentiment_analysis_1.csv" containing the columns "date,source,message,label,score". Use Plotly to plot a 'scatter' where you can see both label and score. On the Y axis order the label increasing from 1 to 5 stars.

--- prompt_example_4
What are the different values possible for the following attribute 'barmode' in command 'fig = px.bar(result, x='score', y='label', color='score', barmode='group')'

'group': This places bars of the same x value next to each other, creating a grouped bar chart where each category has its own set of bars.

'stack': This stacks bars of the same x value on top of each other, creating a stacked bar chart. Each bar represents the total sum of values for that x value.

--- prompt_example_5
In python, for streamlit, give a different command to print a scatter where the score are between 0 to 1 on the X axis.

fig = px.scatter(
    result,
    x="score",
    y="label",
    color="score",
    opacity = .5,
    color_continuous_scale="reds",
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


If the values are like for instance '0.3923925757408142,0.2663969397544861,0.2479227781295776,0.4055523872375488,0.6419059038162231...' why the figure is empty eventhough the 'result_filtered' is not empty 






--- prompt_model
I want you to act as a data scientist coding in R. Given a dataframe {dataframe name} containing the columns {column names}. Use ggplot2 to plot a pair plot that shows the relationship of one variable against another.


--- prompt_model
I want you to act as a data scientist coding in R. Given a dataframe 
{dataframe name} containing the columns {column names}, use ggplot2 to plot a {chart type} the relationship between {variables}. {Insert annotation and formatting requirements}

--- prompt_model
I want you to act as a data scientist coding in R. Given a dataframe {dataframe name} containing the columns {column names}, use ggplot2 to to plot a {chart type} the relationship between {variables}. Change the color theme to match that of {theme}

--- prompt_model
I want you to act as a data scientist coding in Python. Given a dataframe 
{dataframe name} containing the columns {column names} Use matplotlib to plot a {chart type and requirement}.

--- prompt_model
I want you to act as a data scientist coding in Python. Given a dataframe {dataframe name} containing the columns {column names}. Use matplotlib to plot a pair plot that shows the relationship of one variable against another.

--- prompt_model
I want you to act as a data scientist coding in Python. Given a dataframe 
{dataframe name} containing the columns {column names}, use matplotlib to to plot a {chart type} the relationship between {variables}. {Insert annotation and formatting requirements}

--- prompt_model
I want you to act as a data scientist coding in Python. Given a dataframe {dataframe name} containing the columns {column names}, use matplotlib to to plot a {chart type} the relationship between {variables}. Change the color theme to match that of {theme} Plotly




