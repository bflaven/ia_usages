#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
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


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_llms_usecases/fastapi_usecase_1_sentiment_analysis


[install]
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

http://127.0.0.1:8000/sentiment-analysis/?message=Your%20message%20goes%20here


# LAUNCH THE API
uvicorn app.main:app --reload

# LAUNCH THE WEBAPP
streamlit run ux.py


# local
http://localhost:8000
http://127.0.0.1:8000

# docker
http://localhost
http://0.0.0.0:80


[source]
https://huggingface.co/cmarkea/distilcamembert-base-sentiment

The dataset comprises 204,993 reviews for training and 4,999 reviews for the test from Amazon, and 235,516 and 4,729 critics from Allocine website. The dataset is labeled into five categories:


1 étoile : représente une appréciation terrible,
2 étoiles : mauvaise appréciation,
3 étoiles : appréciation neutre,
4 étoiles : bonne appréciation,
5 étoiles : excellente appréciation.

1 star: represents a terrible appreciation,
2 stars: bad appreciation,
3 stars: neutral appreciation,
4 stars: good appreciation,
5 stars: excellent appreciation.

"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# @st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    
    return data

# @st.cache(ttl=60*60*12, allow_output_mutation=True)
# @st.cache_resource(ttl=60*60*12)
# def fetch_emojis():
#     resp = requests.get(
#         'https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json')
#     json = resp.json()
#     codes, emojis = zip(*json.items())
#     return pd.DataFrame({
#         'Emojis': emojis,
#         'Shortcodes': [f':{code}:' for code in codes],
#     })

st.set_page_config(layout="wide")
# Define the URL of the sentiment analysis endpoint
SENTIMENT_ANALYSIS_URL = "http://127.0.0.1:8000/sentiment-analysis/"

tab1, tab2, tab3 = st.tabs(["Source", "API", "Result"])

with tab1:
    st.header("Source")

    # DATE_COLUMN = 'ProductId'
    DATA_URL = ('data_source/sentiment_analysis_reviews_0.csv')

    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')


    # data analysis
    # "dim1","dim2","message"
    # data = pd.read_csv("csv_practice.csv") #path folder of the data file
    st.write(data) 

with tab2:
    st.header("API")
   
            # Mapping of sentiment labels to appreciation

            # English
            # sentiment_mapping = {
            #     "1 star": "terrible appreciation",
            #     "2 stars": "bad appreciation",
            #     "3 stars": "neutral appreciation",
            #     "4 stars": "good appreciation",
            #     "5 stars": "excellent appreciation"
            # }

            # add some emoji
            # :crown:
            # :clap:
            # :-1:
            # :+1:

    # French
    sentiment_mapping = {
        "1 star": ":-1: :-1: Archi-nul",
        "2 stars": ":-1: Super mauvais",
        "3 stars": ":+1: Rien à dire",
        "4 stars": ":clap: Pas mal",
        "5 stars": ":crown: Super bien"
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


    with st.expander('Explications', expanded=False):
            st.markdown(
"""

We present DistilCamemBERT-Sentiment, which is DistilCamemBERT fine-tuned for the sentiment analysis task for the French language. This model is built using two datasets: Amazon Reviews and Allociné.fr to minimize the bias. Indeed, Amazon reviews are similar in messages and relatively shorts, contrary to Allociné critics, who are long and rich texts.


**The dataset comprises 204,993 reviews for training and 4,999 reviews for the test from Amazon, and 235,516 and 4,729 critics from Allocine website.** 

See at https://huggingface.co/cmarkea/distilcamembert-base-sentiment

**The dataset is labeled into five categories:**


- 1 étoile : représente une appréciation terrible,
- 2 étoiles : mauvaise appréciation,
- 3 étoiles : appréciation neutre,
- 4 étoiles : bonne appréciation,
- 5 étoiles : excellente appréciation.

""")

    comment = st.text_input("Enter your comment:")
    submit_button = st.button("Submit")

    st.markdown('**Example : BAD comment on movie in French**')
    st.code('Je déteste ce film, les acteurs sont nuls !')

    st.markdown('**Example : GOOD comment on movie in French**')
    st.code('J\'adore ce film, le scénario est un chef d\'oeuvre et le travail de la réalisatrice est époustouflant.')

    if submit_button and comment:
        result = perform_sentiment_analysis(comment)
        
        st.subheader("Sentiment Analysis Result:")
        st.json(result)

        # Initialize variables to track the maximum score
        max_score = float('-inf')  # Initialize with negative infinity
        max_score_label = None
        st.subheader("Highest score:")
        for item in result[0]:
            label = item["label"]
            score = item["score"]
            
            # in french
            # mapped_appreciation = sentiment_mapping[label]
            # st.write(f"{label}: {mapped_appreciation}")

            # only one
                # Check if the current score is greater than the maximum score
            if score > max_score:
                max_score = score
                max_score_label = label

                # At this point, max_score will contain the maximum score
                st.write("Maximum score :", max_score)
                st.markdown(f"Label : **{max_score_label}**")

                mapped_appreciation = sentiment_mapping[label]
                st.write(f"En français : **{mapped_appreciation}**")
with tab3:
    st.header("Result")

    DATA_URL_RESULT = ('data_destination/full_sentiment_analysis_reviews_sample_analysis_1.csv')


    # "dim1","dim2","message"
    st.subheader('Data')
    result = pd.read_csv(DATA_URL_RESULT) 
    st.write(result)

    # Define the order of labels
    label_order = ['1 star', '2 stars', '3 stars', '4 stars', '5 stars']

    # Convert the 'label' column to categorical with specified order
    result['label'] = pd.Categorical(result['label'], categories=label_order, ordered=True)

    # dim1,dim2,message,label,score
    # fig_1
    st.subheader('Figure_1')
    fig = px.scatter(
    result,
    x="score",
    y="label",
    color="score",
    opacity = 0.5,
    color_continuous_scale="reds",
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    # Filter the DataFrame to include only scores between 0 and 1
    # result_filtered = result[(result['score'] >= 0) & (result['score'] <= 1)]

    # st.write(result_filtered)
    # Create a scatter plot using Plotly
    # fig = px.scatter(
    # result_filtered,
    # # result,
    # x="score",
    # y="label",
    # color="score",
    # opacity=0.5,
    # color_continuous_scale="reds",
    # symbol='label'  # Use 'label' column to determine marker size
    # )

    # st.plotly_chart(fig, theme="streamlit", use_container_width=True)
 

    st.subheader('Figure_2')
    ## Create a bar chart using Plotly
    fig = px.bar(result, x='label', y='score', color='score', barmode='group')
    # fig = px.bar(result, x='score', y='label', color='score', barmode='stack')

    ## Display the figure in Streamlit
    st.plotly_chart(fig)

    # st.subheader('Figure_3')

    # # Order the 'label' column
    # result['label'] = result['label'].astype('category')
    # result['label'] = result['label'].cat.set_categories(['1 star', '2 stars', '3 stars', '4 stars', '5 stars'])

    # # Create a scatter plot using Plotly
    # # scatter_plot = px.scatter(result, x='label', y='score', title='Scatter Plot of Label vs Score', labels={'label': 'Label', 'score': 'Score'})
    
    # scatter_plot = px.scatter(result, x='score', y='label', title='Scatter Plot of Label vs Score', labels={'label': 'Label', 'score': 'Score'})

    # # Display the scatter plot using Streamlit
    # st.plotly_chart(scatter_plot)


    # st.subheader('Figure_4')

    # # Convert the 'date' column to datetime format
    # result['date'] = pd.to_datetime(result['date'], format='%d/%m/%Y %H:%M:%S')

    # # Extract the year from the 'date' column
    # result['year'] = result['date'].dt.year

    # # Create a line chart using Plotly
    # line_chart = px.line(result, x='year', y='label', title='Label vs Year of Score')

    # # Display the line chart using Streamlit
    # st.plotly_chart(line_chart)


