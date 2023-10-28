# Use an existing docker image as a base
FROM python:3.7-buster

#Change working directory
WORKDIR /api

# COPY requirements.txt
COPY ./requirements.txt ./

RUN pip install -r requirements.txt 
# Copy main.py file
COPY ./api ./

# Tell what to do when it starts as a container
CMD ["uvicorn","main:api","--host","0.0.0.0","--port","8000"]

