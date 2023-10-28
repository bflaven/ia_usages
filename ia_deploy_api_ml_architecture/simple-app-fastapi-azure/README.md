# simple-app-fastapi-azure

**You need to have an app to deploy! Right? Here is a simple one below. You can find some more on my github account in `simple-app-fastapi-azure` and in `mamamia-fastapi-azure`**

```bash

# go to the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture

# make a directory named "simple-app-fastapi-azure"
mkdir simple-app-fastapi-azure

# get into the directory named "simple-app-fastapi-azure"
cd simple-app-fastapi-azure

# command to delete the all directory
rm -R simple-app-fastapi-azure

# create the FastAPI files
# you can create all the files at once
touch main.py requirements.txt Dockerfile .dockerignore
# and the cut and paste the code for each file.
```


**For the code to put in each file. See below. It reduces to the minimum.**

- **1. main.py**
```bash
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from fastapi import FastAPI, File, status
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
 
app = FastAPI()

# home
@app.get("/")
async def home():
    # return RedirectResponse("/docs")
    return {'Azure FastAPI test api': 'It is running'}

    
    
```

- **2. requirements.txt**
```bash
fastapi
uvicorn
```

- **3. Dockerfil**
```bash
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
```

- **4. .dockerignore**

I have picked an extended model for .dockerignore on this site: <a href="https://shisho.dev/blog/posts/how-to-use-dockerignore/" target="_blank" rel="noopener">https://shisho.dev/blog/posts/how-to-use-dockerignore/</a>


```bash
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
Makefile
README.md
```



**If you have a development environment, you can test your API.  A development environment is made with tools like Anaconda, Poetry, Venv... etc. I am using Anaconda.**

```bash

# V1
# launch the app
uvicorn main:app --reload

# in a browser you can check type URL
http://127.0.0.1:8000
http://localhost:8000
# I have declared in my hosts file cypress.mydomain.priv pointed to 127.0.0.1
http://cypress.mydomain.priv:8000

# ctrl+c to stop the server

# V2
# launch the app
uvicorn main:app --host 0.0.0.0 --port 80 --reload

# in a browser you can check type URL
http://127.0.0.1
http://localhost
# I have declared in my hosts file cypress.mydomain.priv pointed to 127.0.0.1
http://cypress.mydomain.priv


# See more at https://fastapi.tiangolo.com/deployment/manually/
```