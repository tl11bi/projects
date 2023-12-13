
```bash
# build docker image with name and tag
docker build -t connorli0/car-factory-app:connor-test .
# tag the docker image
docker tag car-factory-app:1.7 connorli0/car-factory-app:connor-test
docker push connorli0/car-factory-app:connor-test
```

```bash
# show docker log
docker logs -f car-factory-app
```

```bash
# delete existing docker first
docker rm -f car-factory-app
# run docker with docker image with name
docker run \
    -d --name car-factory-app \
    -p 8888:8080 docker.io/connorli0/car-factory-app:connor-test
```

### Verify the running container
Verify by checking the container ip and hostname (ID):
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-container
172.17.0.2
docker inspect -f '{{ .Config.Hostname }}' my-container
6095273a4e9b
```