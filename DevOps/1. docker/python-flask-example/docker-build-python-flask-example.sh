!#/bin/bash
docker build -t connorli0/car-factory-app:1.6 .
docker push connorli0/car-factory-app:1.6
# delete existing docker first
docker rm -f car-factory-app
# run docker with docker image with name
docker run \
    -d --name car-factory-app \
    -p 8888:8080 docker.io/connorli0/car-factory-app:1.6
    
