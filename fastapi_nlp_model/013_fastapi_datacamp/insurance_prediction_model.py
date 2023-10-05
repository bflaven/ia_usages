# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.regression import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("insurance_prediction_model")

# Create input/output pydantic models
input_model = create_model("insurance_prediction_model_input", **{'age': 48, 'sex': 'male', 'bmi': 35.625, 'children': 4, 'smoker': 'no', 'region': 'northeast'})
output_model = create_model("insurance_prediction_model_output", prediction=16884.924)


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
