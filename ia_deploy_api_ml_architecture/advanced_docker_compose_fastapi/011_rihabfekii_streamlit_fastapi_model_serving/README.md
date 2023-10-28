# 009_davidefiocco_streamlit_fastapi_model_serving

It is about "Machine learning model serving in Python using FastAPI and streamlit".  I have changed the FastAPI and the Streamlit app, make something much more simpler but keep the principles for Docker usage especially.

- Original Source: [https://github.com/RihabFekii/streamlit-app](https://github.com/RihabFekii/streamlit-app)


```bash
# Get the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/

# Clone git repo
git clone https://github.com/RihabFekii/streamlit-app.git 010_rihabfekii_streamlit_fastapi_model_serving


# Get into the dir
cd 010_rihabfekii_streamlit_fastapi_model_serving

# Create the network "AIService"
docker network create AIservice

# to create the network
docker network create AIservice

# to list the network
docker network ls 
# bridge, host, none are pre-defined networks and cannot be removed

# to remove the network
docker network rm AIservice


# NUKE DOCKER IMAGES
docker ps
docker rm -f $(docker ps -aq)
docker system prune



# Run the whole application
docker compose build
docker compose up
docker compose down

# check streamlit
http://localhost:8501/

# check fastapi
http://localhost:8000/docs
```


