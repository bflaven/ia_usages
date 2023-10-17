# Makefile
# 
# Yolo8, fastapi, DevOps - get a popular real-time object detection model and with FastAPI
#
# Run "make ok" to check
# Run "make install_build" to install with build
   

#VALUES
MAKEFILEMAKEIT = Yolo8, fastapi, DevOps
MAKEYOLO8FASTAPIBUILD = docker-compose up
MAKEYOLO8FASTAPIDOWN = docker-compose down
MAKELISTIMAGES = docker ps


#ACTIONS
# make ok
ok:
	@echo "\n--- You are OK $(MAKEFILEMAKEIT) ---\n\n"

# make start (install with docker build)
start:
	@echo "\n--- Start ---\n\n"
	$(MAKEYOLO8FASTAPIBUILD)


# make stop (stop all containers)
stop:
	@echo "\n--- Stop ---\n\n"
	$(MAKEYOLO8FASTAPIDOWN)
	
	# docker stop $(docker ps -a -q) ## you can type manually this command :)
	## @docker stop $$(docker images -aq) ## not working

# make list (lsit all containers)
# Find the container ID:
list:
	@echo "\n--- List ---\n\n"
	$(MAKELISTIMAGES)

# # Connect inside the container:
# docker exec -it {CONTAINER_ID}

# make rmc (remove all containers)
rmc:
	@echo "\n--- copy and paste manually the command to remove all containers ---\n\n"
	# docker rm -f $(docker ps -aq) ## you can type manually this command :)
	# @docker rm -f $$(docker ps -aq) ## not working

# make rmi (remove all containers)
rmi:
	@echo "\n--- copy and paste manually the command to remove all images ---\n\n"
	# docker rmi -f $(docker images -aq) ## you can type manually this command :)
	# @docker rmi -f $$(docker images -aq) ## not working

# make prune (nuke them all)
prune:
	@echo "\n--- clean all ---\n\n"
	docker system prune


# SOURCE: https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes