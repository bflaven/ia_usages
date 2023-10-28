# Choose our version of Python
FROM python:3.9

# Set up a working directory
WORKDIR /code

# Copy just the requirements into the working directory so it gets cached by itself
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the code
COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]