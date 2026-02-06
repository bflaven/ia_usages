## PROMPT_1

As a Docker and WP expert, give me 

1. The set of commands for the terminal on a MAC e.g Apple M4 Max, 26.2 (25C56) to install WordPress (WP) with phpmyadmin and mysql that will be the environment to develop some WordPress (WP) plugins. I have already installed Docker 4.57.0 (215387)

2. I also want the main to start, stop, remove, list... make a quick reminder of the main commands for Docker.

3. Explain also in a reminder the principles of docker and the size taken by images because I want to be savvy with my space disk.





## OUTPUT_1


Here is a minimal, opinionated setup tailored for local plugin development on macOS with Docker Desktop already installed. [datanovia](https://www.datanovia.com/en/lessons/wordpress-docker-setup-files-example-for-local-development/)

***

## 1. Commands to set up WP + MySQL + phpMyAdmin

This uses a single `docker-compose.yml` (v2 syntax works fine on current Docker). [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)

In a terminal:

```bash


# mkdir -p ~/dev/wp-docker
# cd ~/dev/wp-docker

cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_3d_architecture_ocr/ia_wp_plugin_related_content_steps
mkdir wp_docker
cd wp_docker
```

Create `docker-compose.yml` (use `nano`, `vim`, or your editor):

```bash
touch docker-compose.yml
```


```yaml
version: "3.9"

services:
  db:
    image: mysql:8.0
    command: --default-authentication-plugin=mysql_native_password
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"

  wordpress:
    image: wordpress:latest
    depends_on:
      - db
    restart: unless-stopped
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    ports:
      - "8080:80"
    volumes:
      # Your plugin/theme development lives here
      - ./wp-content:/var/www/html/wp-content

  phpmyadmin:
    image: phpmyadmin/phpmyadmin:latest
    depends_on:
      - db
    restart: unless-stopped
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: root
    ports:
      - "8081:80"

volumes:
  db_data:
```

Then:

```bash
# Start in foreground (good for first run to see logs)
docker compose up

# Or start in background
docker compose up -d
```

Access in browser:

- WordPress: http://localhost:8080 [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)
- phpMyAdmin: http://localhost:8081 (host: `db`, user: `root`, pass: `root`) [datanovia](https://www.datanovia.com/en/lessons/wordpress-docker-setup-files-example-for-local-development/)

For plugin development, your code will be in:

```bash
cd ~/dev/wp-docker/wp-content/plugins
# create your plugin folder here; it is live in the container
```

***

## 2. Main Docker commands cheat sheet

Essential everyday commands (new syntax `docker compose` preferred). [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)

**Containers**

- List running containers:  
  `docker ps` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- List all containers (including stopped):  
  `docker ps -a` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Start a stopped container:  
  `docker start <container_name_or_id>` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Stop a running container:  
  `docker stop <container_name_or_id>` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Restart:  
  `docker restart <container_name_or_id>` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Remove a container:  
  `docker rm <container_name_or_id>` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Remove all stopped containers:  
  `docker container prune` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)

**Images**

- List images:  
  `docker images` [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)
- Remove one image:  
  `docker rmi <image_id>` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Remove unused images:  
  `docker image prune` (add `-a` to remove all unused) [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)

**Docker Compose (in your project directory)**

- Start services (detached):  
  `docker compose up -d` [community.hetzner](https://community.hetzner.com/tutorials/run-wordpress-in-a-container-using-docker-compose/)
- Stop and keep containers:  
  `docker compose stop` [community.hetzner](https://community.hetzner.com/tutorials/run-wordpress-in-a-container-using-docker-compose/)
- Stop and remove containers, networks, but keep volumes:  
  `docker compose down` [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)
- Stop and remove everything, including db volume:  
  `docker compose down -v` [community.hetzner](https://community.hetzner.com/tutorials/run-wordpress-in-a-container-using-docker-compose/)
- See logs:  
  `docker compose logs -f` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
- Run a one‑off command inside a service (e.g. WP-CLI if you add it):  
  `docker compose exec wordpress bash` [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)

**Disk usage and cleanup**

- Show global Docker disk usage:  
  `docker system df` [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)
- Aggressive cleanup of unused stuff (careful):  
  `docker system prune` (add `-a --volumes` to also drop images and volumes) [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)

***

## 3. Principles of Docker and disk usage

Docker is based on **images**, **containers**, **layers**, **volumes**, and **networks**. [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)

- Images: Read‑only templates (e.g. `wordpress:latest`, `mysql:8.0`). An image is built from layers; different images often share layers, saving space. [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)
- Containers: Running instances of images plus a thin writable layer for runtime changes. Removing a container usually does not remove the image. [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)
- Volumes: Persistent data, stored outside the container’s writable layer (e.g. your MySQL `db_data` volume). This is where most stateful data lives and can grow large. [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)
- Networks: Virtual networks that let containers talk to each other (here: WordPress, MySQL, phpMyAdmin on the same default network). [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)

About disk usage on macOS:

- Listing usage: `docker system df` shows how much space images, containers, volumes, and build cache take. [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)
- Large consumers:
  - Images you do not use anymore, including old tags. [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)
  - Volumes with databases and uploads (e.g. `db_data`, `wp-content` if you map to a volume instead of bind‑mount). [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)
  - Build cache if you build lots of images locally. [stackoverflow](https://stackoverflow.com/questions/61482601/why-docker-is-taking-up-so-much-storage-in-my-mac)
- Good hygiene:
  - Regularly prune unused containers and images: `docker container prune`, `docker image prune -a`. [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
  - Prune unused volumes once you are sure you do not need the data: `docker volume prune`. [spacelift](https://spacelift.io/blog/docker-commands-cheat-sheet)
  - Prefer bind‑mounts (like `./wp-content:/var/www/html/wp-content`) for source code so that your git repo reflects your work and Docker volumes stay smaller. [datanovia](https://www.datanovia.com/en/lessons/wordpress-docker-setup-files-example-for-local-development/)

As a simple mental model: each image is like a base VM snapshot, each container is a lightweight running VM using that snapshot, and volumes are your “virtual disks” where persistent data accumulates. [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-and-phpmyadmin-with-docker-compose-on-ubuntu-14-04)



Attaching to db-1, phpmyadmin-1, wordpress-1
Error response from daemon: ports are not available: exposing port TCP 0.0.0.0:3306 -> 127.0.0.1:0: listen tcp 0.0.0.0:3306: bind: address already in use




