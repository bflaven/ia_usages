# 002_mikecase_fastapi_docker

A small application but good explanations to understand the requirements for a deployment on Azure or elsewhere of API made with FastAPI.

It works fine. I have disable from the original all the scripts `.sh`. I just add a `Makefile` so you can easily run different commands without remembering the exact arguments but the explanations are great because they are simple, well-written and straightforward. What else ?

- See at [https://github.com/MikeCase/fastapi-docker](https://github.com/MikeCase/fastapi-docker)


If you want to install the original...

```bash

# In a terminal, require to have docker install

# clone the dir
git clone https://github.com/MikeCase/fastapi-docker.git 002_mikecase_fastapi_docker

# go to the dir
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/002_mikecase_fastapi_docker/

# if needed
rm -R 002_mikecase_fastapi_docker

docker build --pull --rm -f "Dockerfile" -t fastapiapp:latest "."
# or launch the build.sh

docker-compose -f "docker-compose.yml" up -d --build
# or launch the up.sh

# stop
docker-compose down


# check the url
http://127.0.0.1:8005/docs
http://0.0.0.0:8005/docs
http://localhost:8005/docs
```

# ORIGINAL_README

## Purpose
Create and setup a python development environment inside of docker in 5 minutes. (Also more or less a journal to myself of how to do this)

## What to know
You will need to understand virtual environments with python. I will place the commands that are needed for setting up the virtual environment but will not expand upon them. 

## What you need
Python 3.8 is the version I'll be using in this tutorial.
Python modules you will need are:
- fastapi
- hypercorn

a few files will need to be created.
- main.py
- Dockerfile
- .dockerignore
- docker-compose.yml

The following commands will install and create the files you need.

```sh
mkdir -p ~/projects/myproject
cd ~/projects/myproject
touch main.py Dockerfile .dockerignore docker-compose.yml
```
>Above we create the project directory and the initial files we'll need for the app.
```sh
python3.8 -m venv .venv
source .venv/bin/python
pip install fastapi hypercorn
pip freeze > requirements.txt
```
>This code above creates the virtual environment in the CWD.
In the above commands ~/projects/myproject should be whatever directory you want to put your code into. 

## The files
Now to modify the files you just created. Lets start with the fastapi application. 

## in `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'key' : 'value'}
```
The above code sets up a very basic fastapi application. 
First you import FastAPI from fastapi
next you instantiate the app.
then you decorate your index with `@app.get('/')`
and finally you return a dictionary. 

## Next in `Dockerfile`:

```docker
FROM python:3.8-slim

WORKDIR /app/
ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

EXPOSE 8005

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "--reload"]

```
The above file creates a configuration for docker. It pulls a base image from the dockerhub. This uses `python:3.8-slim` as the base image. Next we set our Work Directory to `/app/` in the container. 
after that we add only our `requirements.txt` to that app directory. then we can run pip install inside the container to install our app requirements, and setup our environment inside the container. After that we add the rest of our app to our `/app/` directory on the container expose the port we want to be able to connect to this on and run hypercorn which was installed when we did `pip install -r requirements.txt` 

## Now for `.dockerignore`:

you don't have a need to include your .venv folder because you will be creating a virtual environment in the container. 

Also you don't need the pycache directories on the container(waste of space).
```
.venv/
__pycache__/
```

## Now for `docker-compose.yml`
which will put it all together for us. 

## Note:
if you copy and paste and have issues with the .yml file you may need to check and see if the indentations are spaces or tabs. If they are tabs they will need to be converted to spaces. 
It's a yaml thing..

```yaml
version: '3.8'
services:
    api:
        build: .
        image: fastapiapp:latest
        ports:
            - 8005:8000
        volumes:
            - type: bind
              source: .
              target: /app/
```

Ok this is the last file. This file holds the container build/config instructions. It will also in this instance build the image for us. It will read the Dockerfile in the current working directory and build and app called `fastapiapp` with the tag `latest`

To run it all and see some progress, you should now be able to run `docker-compose buid && docker-compose up -d` and it should build and bring up your docker development environment. The first time it runs it may take a minute or to to come up, but after that it should be utilizing the build cache in docker to only rebuild/add the code that you modified. It will be accessable from [127.0.0.1:8005](http://127.0.0.1:8005)

> I chose port 8005 because I have containers running on the previous 5 ports. You can use in the Dockerfile and docker-compose.yml file what ever port you'd like. The mapping of the ports is `hostport:containerport`.

Bind mount volumes are used in this instance to allow you to modify the code in the current directory and it should also update in the container at the same time. The only time you will need to make a build is when/if you add new python modules. Because they will need to be recompiled and installed into the container. So also remember to run another `pip freeze > requirements.txt` if you install new modules. 

> A couple of helper scripts to make the process easier. 
`build.sh`
with the contents of:
```sh
docker build --pull --rm -f "Dockerfile" -t fastapiapp:latest "."
```
> And a script for running the container in `up.sh`
```sh
docker-compose -f "docker-compose.yml" up -d --build
```

## Things to check when it all goes wrong.
- Is port 8005 open on your firewall at least for the local connection? 
- Is the container running? 
- - `docker ps` the image name should be `fastapiapp:latest` if it is listed without running `docker ps -a` then it is running.
- If it's not running you need to check the logs `docker logs -f container_name` generally you can see the issue pretty clearly. 


## github repo
All of the above mentioned files will be in a [repository](https://github.com/MikeCase/fastapi-docker) on my github.

