# 004_pyyush_maskedlanguagemodeling





## Masked Language Modeling


## Setup
Before running the code, please ensure that you have installed the required dependencies mentioned in the requirements.txt file. You can do this by running the following command in your terminal:
```bash
pip3 install -r requirements.txt
```

# FastAPI
To run the FastAPI web server, you can use the following command in your terminal:
``` bash
uvicorn fastAPI:app 
```
Once the server is up and running, you can access the Swagger documentation for the API at <ins>http://127.0.0.1:8000/docs</ins> \
Alternatively, you can use the curl command to test the API as shown below:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hello <mask>",
  "model": "xlm-roberta-base"
}'
```

# Gradio
To run the Gradio web application, you can use the following command in your terminal:
``` bash
python Gradio.py
```
Once the server is up and running, you can access the web application at <ins>http://127.0.0.1:7860</ins>