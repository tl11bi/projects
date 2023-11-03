# Kubernetes Command Cheat Sheet

This cheat sheet provides commonly used `kubectl` commands for managing and interacting with Kubernetes clusters.

## Cluster Information

- `kubectl version`: Display client and server Kubernetes versions.
- `kubectl cluster-info`: Show cluster information.

## Namespace Management

- `kubectl get namespaces`: List all namespaces.
- `kubectl create namespace <namespace-name>`: Create a new namespace.
- `kubectl delete namespace <namespace-name>`: Delete a namespace and its resources.

## Pod Management

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