#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name ml_with_label_studio python=3.9.13
conda info --envs
source activate ml_with_label_studio
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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/ml_with_label_studio/sentiment_analysis/


python generate_predictions.py

"""
# Generates pre-annotated input from the IMDB sentiment dataset
#
# Example usage:
# python ./generate_predictions.py ../IMDB_train_labeled_100.csv ../IMDB_predictions_100.json

import sys
import csv
import json
import sentiment_cnn

# loads the model with the pre-generated weights and the vocabulary configuration
model = sentiment_cnn.SentimentCNN(
        state_dict='data/cnn.pt',
        vocab='data/vocab_obj.pt')

# read the input and output file names from the command line
infile = sys.argv[1]
outfile = sys.argv[2]

# a helper map to convert model predictions to Label Studio choices
label_map = {
    0: 'Negative',
    1: 'Positive'
}

predictions = []
prediction_id = 1000

with open(infile) as csvfile:
    header = None
    reader = csv.reader(csvfile)
    for row in reader:
        if not header:
            # first row is the header
            header = row
        else:
            # the rest of the rows are values
            values = row

            # turns the loaded data row into a dictionary, paired with the header
            data = dict(zip(header, values))
 
            # predict the sentiment and confidence score from the model
            sentiment, score = model.predict_sentiment(data['review'])

            # map the prediction to the choice expected by Label Studio
            label = label_map[sentiment]

            # create a python dictionary object for the prediction to be written as JSON
            prediction = {
                'model_version': 'SentimentCNN 1',
                'score': float(score),
                'result': [{
                    'id': str(prediction_id),
                    'from_name': 'sentiment',
                    'to_name': 'text',
                    'type': 'choices',
                    'value': {
                        'choices': [
                            label
                        ]
                    }
                }]
            }
            # pair the data with the predictions
            predictions.append({ 'data': data, 'predictions': [ prediction ] })

            prediction_id = prediction_id + 1

with open(outfile, 'w') as jsonfile:
    json.dump(predictions, jsonfile)
