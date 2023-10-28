# 004_tsadimas_fastapi_docker_compose

This projetc `fastapi-docker-compose` present a more advanced usage with .env, redis and so on

- https://github.com/tsadimas/fastapi-docker-compose


The nice add-on is the `.env` usage. The `.env` avoids storing sensitive information within your application.

Check python-dotenv for the use of .env at https://pypi.org/project/python-dotenv/


```bash
# clone the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/

git clone https://github.com/tsadimas/fastapi-docker-compose.git 004_tsadimas_fastapi_docker_compose

# go to the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/004_tsadimas_fastapi_docker_compose/

# if needed
rm -R 004_tsadimas_fastapi_docker_compose


# create a .env file in root directory adding these values
REDIS_SERVER=redis-server
REDIS_PASS=pass123

# NUKE DOCKER IMAGES
docker rm -f $(docker ps -aq)
docker system prune


# run the docker compose
docker-compose up --build

# check the url
http://0.0.0.0:8000/

```


# ORIGINAL_README


# Test
``dotenv -f .env run pytest app/tests/test_main.py``


# how to run
## create a .env file in root directory adding these values
```
REDIS_SERVER=redis-server
REDIS_PASS=pass123
```
## Run without docker
``dotenv -f .env run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
``
but need a local redis running


## run the docker compose
``docker-compose up --build``

# Run in http using
```
nginx:
    image: nginx:latest
    volumes:
      - ./nginx.http.config:/etc/nginx/nginx.conf
```
or using https, but first you have to create or obtain your own certificates and put on the directory certs with names ``server.crt`` and ``server.key``

```
nginx:
    image: nginx:latest
    volumes:
      - ./nginx.https.config:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
```

# K8S

## create a self signed certificate with your domain (e.g. tsadimas.eu)
```
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 --nodes -subj '/C=GR/O=fidemporiki/OU=it/CN=tsadimas.eu'i
openssl x509 -in server.crt -out server-crt.pem -outform PEM
openssl rsa -in server.key -out server-key.pem -outform PEM
 ```
## create a tls secret
```
kubectl create secret tls tls-secret --cert server-crt.pem --key server-key.pem
```
### apply the specific ingress with tls
```
kubectl apply -f k8s/fastapi-ingress-ssl.yaml
```
NOTE: because it is self signed certificate add the following to /etc/hosts
```
127.0.0.1 tsadimas.eu
```

