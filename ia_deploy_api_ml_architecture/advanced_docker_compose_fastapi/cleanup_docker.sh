#!/bin/bash

# Stop all containers
docker stop $(docker ps -a -q)
# Delete all containers
docker rm $(docker ps -a -q)
# Delete all images
# docker rmi $(docker images -q)
# Prune it
docker system prune



