#!/bin/bash
#kubectl delete service my-deployment
#kubectl expose -f k8s-connor-app.yaml --type=LoadBalancer --name=my-deployment --port=8080 --target-port=4444
# kubectl port-forward pod/connor-app-64966f9f7c-8bcph 8080:8080
# kubectl port-forward service/nginx-loadbalancer 8080:31445
kubectl delete -f k8s-connor-app.yaml
kubectl create -f k8s-connor-app.yaml
#curl http://10.96.0.2:30001/health
#curl http://localhost:30001/health

#wget -o- http://localhost:30001/health
#wget - http://10.96.0.2:30001/health
#kubectl exec -it my-connor-app-deployment-64966f9f7c-4s5kc -- /bin/bash
minikube service my-node-port-service --url

