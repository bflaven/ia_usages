
+ Machine learning model serving in Python using FastAPI and streamlit
--- Post: https://ichi.pro/fr/deployer-des-modeles-de-machine-learning-avec-streamlit-fastapi-et-docker-205706317327249
--- Source: https://github.com/RihabFekii/streamlit-app.git 

- Get the dir
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/

- Clone git repo
git clone https://github.com/RihabFekii/streamlit-app.git 010_rihabfekii_streamlit_fastapi_model_serving


- Get into the dir
cd 010_rihabfekii_streamlit_fastapi_model_serving

- Create the network "AIService"
docker network create AIservice

- to create the network
docker network create AIservice

- to list the network
docker network ls 
--- bridge, host, none are pre-defined networks and cannot be removed

- to remove the network
docker network rm AIservice


! NUKE DOCKER IMAGES
docker ps
docker rm -f $(docker ps -aq)
docker system prune



- Run the whole application
docker compose build
docker compose up
docker compose down


http://localhost:8501/
http://localhost:8000/docs



