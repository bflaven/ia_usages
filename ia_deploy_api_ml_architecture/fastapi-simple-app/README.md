# fastapi-simple-app

```python
"""
# create the env: fastapi_simple_app
python -m venv fastapi_simple_app
python -m venv env

# activate the env: fastapi_simple_app
source env/bin/activate

# if you need to exit from the env fastapi_simple_app
deactivate

# If you need to update pip
pip install --upgrade pip
pip --version

# You can stay in the env  fastapi_simple_app or exit from this env to update pip

# install requirements
pip install fastapi uvicorn


# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/fastapi-simple-app/

# launch the app
uvicorn app.main:api --reload


# Check localhost
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

"""
```

- 1. Virtual environment with venv

--- model python -m venv env
python -m venv fastapi_simple_app

--- model source env/bin/activate
source fastapi_simple_app/bin/activate

--- if you need to exit from the env
deactivate

--- to test the env
which python
which pip

# to upgrade pip
python -m pip install --upgrade pip

- 2. create a FastAPI app (DONE)

mkdir app
...etc

- 3. create a dockerfile to enable the app to run in a container

---  check if docker is running
docker --version
---  build your image "azure-fastapi-simple-app"
docker build -t two-fastapi-app .

---  run the container of your image
docker run -p 80:80 -it two-fastapi-app
- Check http://localhost/docs or http://0.0.0.0/docs

- 4 - deploy to azure
A simple api made with FastAPI easy to deploy
