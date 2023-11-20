## Containerization and Virtualization Terminology

### Container Images:
- Container images package everything needed for an application, including code and dependencies.
- Images are immutable, read-only, and platform-agnostic, ensuring high portability.

### Container Registry:
- A container registry is a centralized repository for storing container images.
- Registries can be public or private, facilitating image distribution and access control.

### Kubernetes Client (kubectl):
- `kubectl` is the official command-line tool for interacting with the Kubernetes API.
- It is used for creating, managing, and inspecting Kubernetes objects like pods, services, and deployments.

### Docker:
- Docker is a widely used tool for creating, managing, and working with containers.
- It includes Docker Engine, comprising dockerd (server), APIs, and the CLI client (docker command).

### Docker Images:
- Docker images are collections of files containing binaries, source code, and dependencies for container deployment.
- They are used to create and run containers.

### Container Runtime:
- The container runtime is responsible for executing containers on a host system.
- It manages the container lifecycle, including creation and termination.
- Docker and Google Kubernetes Engine (GKE) use containerd as their container runtime.

## Main Kubernetes Components

### Pod
- What it is
  - pod can contain ***multiple containers***
  - each container maybe for different purpose
  - pod shares the same network and storage
  - smallest unit of deployment in Kubernetes
  - has its own cgroup, but share a number of Linux namespaces
- What goes into the container
  - i.e. web serving container and a git-sync container 
- ***init containers***
  - init containers are containers that run before the main container
  - init containers are used to perform tasks like database migrations, downloading assets, and running tests
  - [init container example](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/#examples)
- [example commands](k8s_command_cheat_sheet.md#pod-management)

### Creating K8S clusters
- Imperative commands
  - Commands through console or terminal such as:
    - `kubectl run nginx --image=nginx`
    - `kubectl create deployment nginx --image=nginx`
- Declarative commands
  - Commands through configuration files such as:
    - `kubectl apply -f nginx.yaml`
    - `kubectl create -f nginx.yaml`

### Namespaces
- namespace is a way to organize cluster resources and isolate them from each other
- multi-tendency (a way of implementing multi-tenancy)
- default namespace is `default`
- build-in namespaces
  - `kube-system`: contains resources created by the Kubernetes system
  - `kube-public`: contains resources that are publicly available
  - `kube-node-lease`: contains node lease objects that are created automatically

### Labels
- labels are key-value pairs attached to Kubernetes objects
- labels are used to organize and select subsets of objects
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    release: stable
    environment: prod
    tier: frontend
...
```

### ReplicaSets
- Multiple replicas of a pod
- A specified number of identical pods are running at all times
#### replica set example
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset
  lables:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      name: nginx
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:lastest
```
### controllers
- controllers are control loops that watch the shared state of the cluster
- thermostat --> current state to match desired state
- controllers tracks at least one Kubernetes resource type
  - replicaSetController for ReplicaSet

### Deployments
- Deployments are a declarative way to manage ReplicaSets
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
    replicas: 3
    selector:
        matchLabels:
        app: nginx
    template:
        metadata:
        name: nginx
        labels:
            app: nginx
        spec:
        containers:
        - name: nginx
            image: nginx:lastest
    ```
```

### DaemonSets
- DaemonSets are used to run a copy of a pod on each node
  - when a new node is added to the cluster, a pod is added to it
  - when a node is removed from the cluster, the pod is garbage collected
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nginx-elasitcsearch
sepc:
    selector:
        matchLabels:
        app: nginx-elasticsearch
    template:
        metadata:
        labels:
            app: nginx-elasticsearch
        spec:
        containers:
        - name: nginx-elasticsearch
            image: nginx-elasticsearch:lastest
            volumeMounts:
            - name: data
                mountPath: /data
    ```
```

### Jobs
- Jobs are used to run a pod until it completes a task 
#### Cronjobs example
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
    schedule: "*/1 * * * *"
    jobTemplate:
        spec:
        template:
            spec:
            containers:
            - name: hello
                image: busybox
                command: 
                - curl -s --head --request GET http://www.google.com | grep "200 OK" | wc -l
    ```
```
## Managing resources
### Limits / requests
- Limits and requests are used to specify the amount of resources a container can use
  - kubernetes can kill a container if it exceeds its limits
  - kubernetes requests resources for a container
- Requests
  - can specify the minimum amount of resources a container needs
- Limits
  - can specify the maximum amount of resources a container can use
#### limits/request example
```yaml
...
spec:
    containers:
    - name: nginx
        image: nginx
        resources:
            requests:
               memory: "64Mi"
                cpu: "250m"
            limits:
                memory: "128Mi"
                cpu: "500m"
    - name: log-aggregator
        image: log-aggregator
        resources:
            requests:
                memory: "64Mi"
                cpu: "250m"
            limits:
                memory: "128Mi"
                cpu: "500m"
...                
```

### Resource Quotas
- provides constraints that limit aggregate resource consumption per namespace
- good way to ensuring don't use more resources than you need
- run `kubectl create -f my-resource-quota.yaml --namespace=app-a`
```yaml
# my-resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-resource-quota
spec:
  hard:
    requests.cpu: 2
    requests.memory: 1Gi
    limits.cpu: 3
    limits.memory: 2Gi
```
### scaling
- horizontal scaling
  - A ReplicaSet or Deployment can be scaled up or down by updating the .spec.replicas field
  - `kubectl scale --replicas=3 rs/nginx-replicaset`
- Horizontal Autoscaling
  - Horizontal Pod Autoscaler (HPA)
    - Average CPU utilization
    - Average memory utilization
    - Custom metric
  - `kubectl autoscale rs nginx-deployment --max=10 --min=3 --cpu-percent=50`
```yaml
# nginx-scaler.yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-scaler
spec:
  scaleTargetRef:
    kind: Deployment
    name: nginx-deployment
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
...
```
- Vertical pod autoscaler
  - Vertical Pod autoscaling provides recommendations for CPU and memory limits/requests
- Cluster Autoscaler
  - Cluster autoscaling automatically resizes the number of nodes in a given node pool, based on the demands of your workloads
  - Specify a minimum andmaximum size for the node pool - GKE handles the scaling
### health checks
- Kubernetes has liveness, readiness and startup probes for containers to determine a Pod's state:
  - Liveness probe — Determines if a container is operating
  - Readiness probe - Determines if a container is ready to accept requests
  - Startup probe - Determines if container's application is running
- Probes can be:
  - HTTP request (GET)
  - TCP connection (Specific port)
  - Command ($cat /var/myfile)
#### Liveness probe example
```yaml
	apiVersion: v1
kind: Pod
metadata:
  name: website-pod
spec:
  containers:
  - name: website
    image: website:latest
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 3
      periodSeconds: 3
```
#### Readiness probe example
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: website-pod
spec:
  containers:
  - name: website
    image: website:latest
    ports:
    - containerPort: 8080
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
```
#### startup probe example
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: application-pod
spec:
  containers:
  - name: application
    image: busybox:latest
    args:
    - /bin/sh
    - -c
    - touch /var/myfile
    startupProbe:
    exec:
        command:
        - cat
        - /var/myfile
    periodSeconds: 10
    failureThreshold: 10
```

### assign pods to nodes
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd

```
### node affinity example
```yaml
	apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - antarctica-east1
            - antarctica-west1
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
  containers:
  - name: with-node-affinity
    image: registry.k8s.io/pause:2.0
```

## deployments & releasing new versions
#### Deployment Image Update Example
```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
#      annotations: # added annotations
#        kubernetes.io/change-cause: "upgrade to 1.25"
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
#        image: nginx:1.25 # updated image
        ports:
        - containerPort: 80
```
- `kubectl rollout status deployment nginx-deployment` to check the status of the rollout
- `kubectl rollout pause deployment nginx-deployment` to pause the rollout
- `kubectl rollout resume deployment nginx-deployment` to resume the rollout
- `kubectl rollout history deployment nginx-deployment` to see the rollout history
- `kubectl rollout history deployment nginx-deployment --revision=2` to see the rollout history of a specific revision



### Control Plane (Master Node)

1. **API Server**:
   - The API server serves as the entry point to the Kubernetes cluster, handling RESTful requests, validation, and cluster state updates.

2. **Controller Manager**:
   - The controller manager monitors the cluster's state and maintains the desired state, utilizing controllers like the Replication Controller, Node Controller, and Endpoints Controller.

3. **Scheduler**:
   - The scheduler assigns workloads to worker nodes based on factors like resource requirements and node capacity.

4. **etcd**:
   - etcd is a distributed key-value store, acting as the authoritative data store for cluster configuration and state information.

### Virtual Network

- Kubernetes networking relies on Container Network Interfaces (CNI) plugins, including Flannel, Calico, Weave, and Cilium, to manage communication between pods on different nodes.

### Multiple Worker Nodes

- Worker nodes execute workloads, host pods, and offer resources for applications to run efficiently, scaling as needed.



### ConfigMap

- An API object storing configuration data as key-value pairs, decoupling configuration from application code. ConfigMaps can inject configuration into pods at runtime.

### StatefulSet

- A workload API object for managing stateful applications, ensuring predictable pod creation and scaling. Commonly used for stateful services like databases.

### Service

- A Kubernetes resource defining a logical set of pods and an access policy. Services provide network connectivity, making pods discoverable and accessible within the cluster.

### Secret

- Secure storage for sensitive data, such as authentication tokens and passwords. Secrets can be injected into pods as environment variables or mounted as files.

### Deployment

- A higher-level resource managing ReplicaSets
- enabling declarative application creation, updates, and scaling, along with rolling updates and rollbacks.

### Ingress

- A set of rules for inbound connections to cluster services, offering HTTP/HTTPS routing, load balancing, and SSL termination.

### DaemonSet

- A workload API object ensuring specific pods run on all or a subset of nodes. Commonly used for agents like monitoring or logging.

### Volume

- Persistent volumes (PVs) provide storage independent of pods, offering an abstraction layer and dynamic provisioning through storage classes.

## StatefulSet vs. StatelessSet

- **StatefulSet**: Used for stateful applications requiring stable network identities and storage, such as databases.
- **StatelessSet**: Not a native Kubernetes resource; suitable for stateless applications that can scale without needing unique network identities or stable storage.

In Kubernetes, stateful applications like databases are often hosted outside the cluster for stability and data persistence. StatefulSets are designed for managing such workloads.

The provided URL appears to be related to accessing the Kubernetes Dashboard, offering a web-based graphical interface for Kubernetes cluster management.