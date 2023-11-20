!#/bin/bash
docker build -t connorli0/connor-test:1.5 .
docker push connorli0/connor-test:1.5
# delete existing docker first
docker rm -f connortest
# run docker with docker image with name
docker run \
    -d --name connortest \
    -p 8888:8080 docker.io/connorli0/connor-test:1.5 
    
