FROM python:3.9

COPY ./api /api
COPY requirements.txt /api

WORKDIR /api

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]