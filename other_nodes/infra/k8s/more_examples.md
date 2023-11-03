Here are the added commands to your Kubernetes cheat sheet:

### Start All Kubectl Commands

```bash
kubectl apply -f mongo-config.yaml
kubectl apply -f mongo-secret.yaml
kubectl apply -f mongo.yaml
kubectl apply -f webapp.yaml
```

### Stop All Kubectl Commands

```bash
kubectl delete -f mongo-config.yaml
kubectl delete -f mongo-secret.yaml
kubectl delete -f mongo.yaml
kubectl delete -f webapp.yaml
```

### List All Existing Pods

```bash
kubectl get pods
```

### Create a Pod with Simple One

```bash
kubectl run nginx --image=nginx
```

### Describe a Pod

```bash
kubectl describe pod nginx
```

### Get All Pods

```bash
kubectl get pods -o wide
```

```plaintext
NAME                                READY   STATUS    RESTARTS   AGE    IP            NODE       NOMINATED NODE   READINESS GATES
mongo-deployment-85d45f7888-lvfzl   1/1     Running   0          42h    10.244.0.15   minikube   <none>           <none>
nginx                               1/1     Running   0          103s   10.244.0.25   minikube   <none>           <none>
webapp-deployment-f8d7df85d-6rzcb   1/1     Running   0          42h    10.244.0.16   minikube   <none>           <none>
```

### Start Kubectl Dashboard

```bash
minikube apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml
kubectl proxy
```

### Kubectl Change Replica Set

```bash
kubectl scale --replicas=3 deployment/webapp-deployment
```

### Kubectl Get All Sets

```bash
kubectl get all
```

### Concentrated Commands

- `kubectl get pod` for getting all the pods.
- `kubectl get pod -o wide` for getting all the pods with more details.
- `kubectl describe pod <pod_name>` for getting the details of a specific pod.
- `kubectl delete pod <pod_name>` for deleting a specific pod.
- `kubectl run <pod_name> --image=<image_name>` for creating a pod with a specific image.
- `kubectl get deployment` for getting all the deployments.
- `kubectl get deployment -o wide` for getting all the deployments with more details.
- `kubectl describe deployment <deployment_name>` for getting the details of a specific deployment.
- `kubectl delete deployment <deployment_name>` for deleting a specific deployment.
- `kubectl exec -it my-connor-app-deployment -- curl http://localhost:30001/health` for executing a command in a specific pod.
- `kubectl create deployment <deployment_name> --image=<image_name>` for creating a deployment with a specific image.
- `kubectl scale --replicas=<number_of_replicas> deployment/<deployment_name>` for scaling a deployment.
- `kubectl get service` for getting all the services.
- `kubectl get service -o wide` for getting all the services with more details.
- `kubectl describe service <service_name>` for getting the details of a specific service.
- `kubectl delete service <service_name>` for deleting a specific service.
- `kubectl expose deployment <deployment_name> --type=NodePort --port=<port_number>` for exposing a deployment.
- `kubectl get all` for getting all resources.
- `kubectl get all -o wide` for getting all resources with more details.
- `kubectl describe all` for getting the details of all resources.
- `kubectl delete all --all` for deleting all resources.
- `kubectl apply -f <file_name>` for applying a file.
- `kubectl delete -f <file_name>` for deleting a file.