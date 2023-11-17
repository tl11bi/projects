Certainly, I've added the provided commands and additional explanations to the Kubernetes Command Cheat Sheet:

# Kubernetes Command Cheat Sheet

## Cluster Information
- `kubectl version`: Display client and server Kubernetes versions.
- `kubectl cluster-info`: Show cluster information.


## Namespace Management

- `kubectl get namespaces`: List all namespaces.
- `kubectl create namespace <namespace-name>`: Create a new namespace.
- `kubectl delete namespace <namespace-name>`: Delete a namespace and its resources.

## Pod Management
- [definations](definations.md#pod)
- `kubectl run my-pod --image=nginx`: Create a pod from an image.
- `kubectl get pods`: List pods in the current namespace.
- `kubectl get pods -n <namespace-name>`: List pods in a specific namespace.
- `kubectl describe pod <pod-name>`: Show detailed information about a specific pod.
- `kubectl delete pod <pod-name>`: Delete a specific pod.

## Deployment Management

- `kubectl get deployments`: List deployments in the current namespace.
- `kubectl get deployments -n <namespace-name>`: List deployments in a specific namespace.
- `kubectl describe deployment <deployment-name>`: Show details of a specific deployment.
- `kubectl apply -f <deployment-file.yaml>`: Create or update a deployment from a YAML file.

## Service Management

- `kubectl get services`: List services in the current namespace.
- `kubectl get services -n <namespace-name>`: List services in a specific namespace.
- `kubectl describe service <service-name>`: Show details of a specific service.
- `kubectl expose deployment <deployment-name> --type=NodePort --name=<service-name>`: Expose a deployment as a service.

## ConfigMap and Secret Management

- `kubectl create configmap <configmap-name> --from-file=<file-path>`: Create a ConfigMap.
- `kubectl create secret generic <secret-name> --from-literal=<key>=<value>`: Create a secret.
- `kubectl get configmaps` or `kubectl get secrets`: List ConfigMaps or Secrets.

## Scaling

- `kubectl scale deployment <deployment-name> --replicas=<desired-replica-count>`: Scale a deployment.
- `kubectl autoscale deployment <deployment-name> --min=<min-replicas> --max=<max-replicas> --cpu-percent=<cpu-target>`: Autoscale a deployment based on CPU usage.

## Rolling Updates and Rollbacks

- `kubectl set image deployment/<deployment-name> <container-name>=<new-image>:<tag>`: Perform a rolling update.
- `kubectl rollout status deployment/<deployment-name>`: Check the status of a rollout.
- `kubectl rollout history deployment/<deployment-name>`: View rollout history.
- `kubectl rollout undo deployment/<deployment-name>`: Rollback a deployment.

## Debugging

- `kubectl logs <pod-name>`: View container logs.
- `kubectl exec -it <pod-name> -- /bin/sh`: Open a shell inside a pod for debugging.
- `kubectl get events`: List cluster events.

## Resource Quotas and Limits

- `kubectl describe resourcequotas -n <namespace-name>`: Describe resource quotas in a namespace.
- `kubectl describe pod <pod-name> -n <namespace-name>`: Check resource usage for a specific pod.

## Additional Commands

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