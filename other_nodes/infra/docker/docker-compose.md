# Docker Compose Quick Reference

This guide provides a quick reference for using Docker Compose to manage multi-container Docker applications. Docker Compose simplifies the orchestration of containers. It is especially useful for defining and running complex applications with multiple interconnected services.

## Installation

To install Docker Compose, you can use pip. Make sure you have Docker and pip installed on your system.

```shell
pip install -U docker-compose
```

## Docker Compose Basics

### Start all services
```shell
docker-compose up
```
or ```docker-compose -f your-custom-compose-file.yml up``` for spesific names

### Stop all services
```shell
docker-compose down
```

### Check Docker Compose version
```shell
docker-compose --version
```

### Run in detached mode
```shell
docker-compose up -d
```

### List running containers
```shell
docker ps
```

## Service Scaling

### Scale a service
```shell
docker-compose up -d --scale service_name=desired_count
```

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

- Customize the service names, image names, ports, and environment variables to fit your application's requirements.
- Run `docker-compose up` to start the services based on the `docker-compose.yml` configuration.
- Run the commands from the directory where your `docker-compose.yml` file is located.
- Replace `service_name` and `desired_count` with appropriate values when scaling services.
```

You can save this content in a file named `README.md` within your project's directory to serve as documentation and a quick reference for using Docker Compose.
