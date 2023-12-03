# Helm Chat
[instructions](https://www.youtube.com/watch?v=DQk8HOVlumI&ab_channel=RahulWagh)
## Basic Helm Commands
```shell
# helm install <name> <chart>
helm create helloworld
```
- output, basic helm chart structure
```text
helloworld/
│   ├── ingress.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml
```
## basic helm chart commands
```shell
# helm install <name> <chart>
helm install myhelloworld ./helloworld
helm install my-python-flask-api ./python-flask-api
# helm install dry-run
helm install myhelloworld ./helloworld --dry-run --debug
# helm lint
helm lint ./helloworld
# helm template, it will generate the yaml file locally on your screen
helm template ./helloworld
# delete the running chart
helm delete myhelloworld
helm uninstall myhelloworld
# list all the helm charts
helm list -a
# upgrade the helm chart after the modification
helm upgrade myhelloworld ./helloworld
# rollback the helm chart, if the current version is 3, after rollback, it will show as 4
helm rollback myhelloworld 2
```
## 