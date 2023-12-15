# docker, docker-compose commands
## Basic docker commands
- 'docker build -t registry.example.com/workspace/myimage:1.0 .': Build an image from the Dockerfile in the current directory and tag the image.
- 'docker push registry.example.com/workspace/myimage:1.0': Push an image tagged 1.0 to the registry.
- 'docker pull registry.example.com/workspace/myimage:1.0': Pull an image tagged 1.0 from the registry.
- 'docker create --name mycontainer registry.example.com/workspace/myimage:1.0': Create a container named mycontainer from the image tagged 1.0.
  - 'docker create -it --name mycontainer registry.example.com/workspace/myimage:1.0': Create a container named mycontainer from the image tagged 1.0 and run it interactively.
- 'docker run --name mycontainer registry.example.com/workspace/myimage:1.0 python3 /app/main.py': create a container named mycontainer from the image tagged 1.0 and run the command python3 /app/main.py.
  - 'docker run -it --name mycontainer registry.example.com/workspace/myimage:1.0 /bin/bash': create a container named mycontainer from the image tagged 1.0 and run the command /bin/bash interactively.
- 'docker start mycontainer': Start the container named mycontainer.
  - 'docker exec -it mycontainer /bin/bash': Run the command /bin/bash in the container mycontainer interactively.

## docker commands that do inventory
- 'docker ps': List the running containers.
  - 'docker ps -a': List all containers.
- 'docker container ls': List the running containers.
  - 'docker container ls -a': List all containers.
- 'docker container prune': Removes all the stopped containers.
- 'docker kill mycontainer': Kill the running container named mycontainer.
- 'docker rm mycontainer': Remove the container named mycontainer.
- 'docker images': List the images.'
- 'docker wait mycontainer': Block the container named mycontainer.
- 'docker rename mycontainer mynewcontainer': Rename the container named mycontainer to mynewcontainer.
- 'docker run -itd --rm -p 80:80 --name stormbreaker nginx:latest': Run a container, expose port 80 to the host.
- 'docker attach mycontainer': Attach local standard input, output, and error streams to a running container.
- 'docker history registry.example.com/workspace/myimage:1.0': Display the history of an image with the image name mentioned in the command.
- 'docker volume create': Create a volume for containers.
- 'docker login': Login into docker hub.

## docker compose commands
- 'docker-compose up': Start the containers.
  - 'docker-compose -f docker-compose.yml up': Start the containers.
  - 'docker-compose up -d': Start the containers in detached mode.
  - 'docker-compose up -d --scale service_name=desired_count': Scale a service.
- 'docker-compose down': Stop the containers.
  - 'docker-compose -f docker-compose.yml down': Stop the containers.

## Configuration

### Use YAML files to configure services

Create a `docker-compose.yml` file with service definitions. Here's a sample `docker-compose.yml` for a web application:
- [docker-compose.yaml example link](https://github.com/tl11bi/k8s-example/blob/master/docker-container-examples/python-flask-docker-i/k8s-connor-app.yaml)
- [dockerfile example](https://github.com/tl11bi/k8s-example/blob/master/docker-container-examples/python-flask-docker-i/Dockerfile)
- [docker build bash commands example](https://github.com/tl11bi/k8s-example/blob/master/docker-container-examples/python-flask-docker-i/docker-build.sh)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: connorli0/connor-test:1.5
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
      restartPolicy: Always
```
