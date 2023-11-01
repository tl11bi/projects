### Container Commands
- `docker create [IMAGE]`: Create a container.
  - create a container from an image named docker-i `docker create docker-i`
  - create a container from an image named docker-i and name it as mycontainer `docker create --name mycontainer docker-i`
  - create a container from an image and run it interactively `docker create -it docker-i`
- `docker container prune [OPTIONS]`: Removes all the stopped containers.
- `docker container commit [OPTIONS] CONTAINER [REPOSITORY [:TAG]]`: Create a new image from a container’s file changes.
- `docker rm [CONTAINER]`: Remove an existing container.
- `docker container ls`: List the running containers.
- `docker stop [CONTAINER_NAME]`: Stop a running container.
- `docker restart [CONTAINER]`: Restart a running container.
- `docker Kill [CONTAINER]`: Kill the running containers.
- `docker ps`: List the running containers.
  - `docker ps -a --filter name=forhahas` : List all containers with name forhahas
- `docker wait [CONTAINER]`: Block a container.


### Other Commands
- `docker rename [CONTAINER_NAME] [NEW_CONTAINER_NAME]`: Rename an existing container.
- `docker run [IMAGE] [COMMAND]`: Run a command in a new container.
  - `docker run -d --name forhahas connorli0/connor-test /user/bin/top -b` : Run a container in the background with name forhahas and run the command /user/bin/top -b
  - `docker run -itd --rm -p 80:80 --name stormbreaker nginx:latest` : Run a container, expose port 80 to the host
- `docker attach [CONTAINER]`: Attach local standard input, output, and error streams to a running container.

### General Commands
- `docker login`: Login into docker hub.
- `docker info`: Get information on the Docker tool.
- `docker history httpd`: Display the history of an image with the image name mentioned in the command.
- `docker volume create`: Create a volume for containers.

### Docker Share Command
- `docker pull [OPTIONS] NAME [:TAG]`: Pull an image from a registry.
- `docker push [OPTIONS] NAME [:TAG]`: Push an image to a registry.
- `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`: Run a command in a running container.
  - `docker exec forhahas ls -lash` : Run the command ls -lash in the container forhahas
  - `docker exec -it forhahas2 /bin/sh`: Run the command /bin/sh in the container forhahas2 interactively
### List of Docker Commands
- `docker build -t myimage:1.0 .`: Build an image from the Dockerfile in the current directory and tag the image.
- `docker images`: List all Docker images.
- `docker image rm alpine:3.4`: Delete an image from the docker image.

