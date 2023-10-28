FROM python:3.10.1-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

# streamlit run --server.port 8080 --server.enableCORS false app/streamlit_app.py
CMD ["streamlit", "run", "ui.py"]
