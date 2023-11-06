# Google Cloud Training
## setting up google cloud shell
- `gcloud config set project connor-first-project` for setting the project up
- Create a Local Bin Dir
```shell
cd $HOME
mkdir $HOME/bin
PATH=$HOME/bin:$PATH
```
- download and install Helm
```shell
curl -fsSL -o $HOME/bin/helm-v3.12.1-linux-amd64.tar.gz https://get.helm.sh/helm-v3.12.1-linux-amd64.tar.gz
tar -zxvf $HOME/bin/helm-v3.12.1-linux-amd64.tar.gz -C $HOME/bin && mv $HOME/bin/linux-amd64/helm $HOME/bin/helm
```
- download vault
```angular2html
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

```
- download and install terraform
```shell
curl -fsSL -o $HOME/bin/terraform_1.5.7_linux_amd64.zip https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
unzip $HOME/bin/terraform_1.5.7_linux_amd64.zip -d $HOME/bin/
rm $HOME/bin/terraform_1.5.7_linux_amd64.zip
```
- `sudo apt install apache2-utils -y` to install the Apache ab tool.
- Configuring kubectl to Connect to Your GKE Cluster: To connect to your GKE cluster, navigate to the hamburger icon in
  the top left of the Cloud Console and click “Kubernetes Engine”. You will see your GKE cluster listed. Click the three
  vertical dots and click “Connect”. Finally, click “RUN IN CLOUD SHELL” and hit enter.

## build first container image with simple python app
- have the following file structure created

```
├── create-dockerfile
│   └── src
│       ├── app.py
│       └── templates
│           └── home.html
```

#### home.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Workshop App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            padding: 20px;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 30px;
        }

        .fact-container {
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 500px;
            margin: 0 auto;
        }

        .fact-text {
            font-size: 24px;
            margin-bottom: 20px;
        }

        .new-fact-btn {
            background-color: #007bff;
            border: none;
            border-radius: 3px;
            color: #fff;
            font-size: 16px;
            padding: 10px 20px;
            cursor: pointer;
        }

        .new-fact-btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
<div class="fact-container">
    <h1>Random Fact Generator</h1>
    <p class="fact-text">{{ fact }}</p>
    <button class="new-fact-btn" onclick="window.location.reload();">Get New Fact</button>
</div>
</body>
</html>
```

#### app.py
```python

# import Flask module
from flask import Flask, render_template
import requests
app = Flask(__name__)
# Define root endpoint
@app.route('/', methods=['GET'])
def index():
    # Make a request to the open API
    response = requests.get('http://numbersapi.com/random/trivia?json')
    fact_data = response.json()
    # Extract the fact from the response
    fact = fact_data['text']
    # Render the home.html template and pass the fact to it
    return render_template('home.html', fact=fact)
# Define health endpoint
@app.route('/healthz', methods=['GET'])
def health():
    return 'All good.', 200

# Main driver function
if __name__ == "__main__":
    app.run()
```

#### dockerfile
```dockerfile
# Use the python:3.12.0b1-alpine image as the base image
FROM python:3.12.0b1-alpine
# Install Flask and Requests Python packages
RUN pip install Flask requests
# Create a non-root user for running the application
RUN adduser -D -h /app python-user
# Set the working directory for subsequent commands
WORKDIR /app
# Copy the application code from the local src directory to the container image
COPY src/ .
# Switch to the non-root user
USER python-user
# Inform Docker that the container listens on port 5000
EXPOSE 5000
# Start the application and listen on port 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

- `docker build --tag random-facts-app:latest --tag random-facts-app:1.0 .`
- `docker images` to see the images
- `docker run --publish 8080:5000 random-facts-app:1.0` to run the image
- `docker ps` to see the running containers
- `docker stop <container_id>` to stop the container
- `docker start <container_id>` to start the container
- `docker container purne` to remove all the stopped containers

## google cloud registry setup and push

- `gcloud artifacts repositories list` to list all the repositories
- `gcloud auth configure-docker us-central1-docker.pkg.dev` to configure docker to use the gcloud registry
- push docker images with `random-facts-app:1.0` and `random-facts-app:latest .`

```shell
docker tag random-facts-app:1.0 us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REPOSITORY_NAME>/random-facts-app:1.0
docker tag random-facts-app:latest us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REPOSITORY_NAME>/random-facts-app:latest
```

- where with `conite-26806` and `connor-first-repo` as the project id and repository name

```shell
docker tag random-facts-app:1.0 us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app:1.0
docker tag random-facts-app:latest us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app:latest
```

- `docker push us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REPOSITORY_NAME>/random-facts-app --all-tags` to push
  the images

```shell
docker push us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app --all-tags
```

- `gcloud artifacts docker images list us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REPOSITORY_NAME>` to list the
  images

```shell
gcloud artifacts docker images list us-central1-docker.pkg.dev/conite-26806/connor-first-repo
```

## Kubernetes pods

- make a new dir

```bash
cd ~
mkdir random-facts-app-pod && cd random-facts-app-pod
```

- create a Namespace manifest file name with `my_first_namespace_manifest_file.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: random-facts-app-pod
  labels:
    lab: random-facts-app-pod
```

- `kubectl apply -f my_first_namespace_manifest_file.yaml` to create the namespace
    - `kubectl get namespaces` to list the namespaces
- Create the Pod manifest file named `my_first_pod_manifest_file.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-facts-app
  namespace: random-facts-app-pod
  labels:
    lab: random-facts-app
spec:
  containers:
    - name: random-facts-app
      #image: us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REGISTRY_NAME>/random-facts-app:1.0
      image: us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app:1.0
      resources:
        requests:
          memory: "256Mi"
          cpu: "500m"
      ports:
        - containerPort: 5000
      livenessProbe:
        httpGet:
          path: /healthz
          port: 5000
        initialDelaySeconds: 10
        periodSeconds: 5
        failureThreshold: 5
      readinessProbe:
        httpGet:
          path: /healthz
          port: 5000
        initialDelaySeconds: 10
        periodSeconds: 5
        failureThreshold: 5
```

- `kubectl apply -f my_first_pod_manifest_file.yaml` to create the pod
- `kubectl get pods -n random-facts-app-pod` to list the pods
- `kubectl logs` to see the logs
- `kubectl logs -f random-facts-app -n random-facts-app-pod` to see the logs in real time

## kubernetes replica sets
- `cd ~ && mkdir random-facts-app-deployment && cd random-facts-app-deployment` to create a new dir
#### my_first_namespace_replica_set_manifest_file.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: random-facts-app-deployment
  labels:
    lab: random-facts-app-deployment
```
- `kubectl apply -f my_first_namespace_replica_set_manifest_file.yaml` to create the namespace
#### my_first_replica_set_manifest_file.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: random-facts-app
  namespace: random-facts-app-deployment
  labels:
    lab: random-facts-app-deployment
spec:
  #replicas: 1
  replicas: 3
  selector:
    matchLabels:
      lab: random-facts-app-deployment
  template:
    metadata:
      labels:
        lab: random-facts-app-deployment
#      annotations:
#        kubernetes.io/change-cause: "Upgrade to latest tag."
    spec:
      containers:
        - name: random-facts-app
#          image: us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REGISTRY_NAME>/random-facts-app:1.0
#          image: us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app:1.0
          image: us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app:latest
          ports:
            - containerPort: 5000
```
- `kubectl apply -f my_first_replica_set_manifest_file.yaml` to create the replica set
- update the container image tag to `random-facts-app:latest`
- add annotations to the pod template
- role out the new deployment with `kubectl apply -f my_first_replica_set_manifest_file.yaml`
    - check the status with `kubectl rollout status deployment/random-facts-app -n random-facts-app-deployment`
    - roll back the deployment with `kubectl rollout undo deployment/random-facts-app -n random-facts-app-deployment`
    - `kubectl rollout history deployment/random-facts-app -n random-facts-app-deployment` to see the history

#### my_first_service_manifest_file.yaml 
```yaml
apiVersion: v1
kind: Service
metadata:
  name: random-facts-app-service
  namespace: random-facts-app-deployment
  labels:
    lab: random-facts-app-deployment
spec:
  selector:
    lab: random-facts-app-deployment
  ports:
    - name: http
      port: 5000
      protocol: TCP
      targetPort: 5000
  type: ClusterIP
```
- `kubectl apply -f my_first_service_manifest_file.yaml` to create the service
- Frontend your Deployment with a Service
    - 'kubectl port-forward service/random-facts-app-service 5000:5000 -n random-facts-app-deployment' to forward the
      service to localhost

## kubernetes horizontal pod autoscaling
- `cd ~ && mkdir random-facts-app-autoscaling && cd random-facts-app-autoscaling` to create a new dir
#### my_first_namespace_autoscaling_manifest_file.yaml
```dockerfile
apiVersion: v1
kind: Namespace
metadata:
  name: random-facts-app-autoscaling
  labels:
    lab: random-facts-app-autoscaling
```
- `kubectl apply -f my_first_namespace_autoscaling_manifest_file.yaml` to create the namespace
#### my_first_autoscaling_deployment_manifest_file.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: random-facts-app
  namespace: random-facts-app-autoscaling
  labels:
    lab: random-facts-app-autoscaling
spec:
  replicas: 1
  selector:
    matchLabels:
      lab: random-facts-app-autoscaling
  template:
    metadata:
      labels:
        lab: random-facts-app-autoscaling
    spec:
      containers:
      - name: random-facts-app
#        image: us-central1-docker.pkg.dev/<YOUR_PROJECT_ID>/<YOUR_REGISTRY_NAME>/random-facts-app:1.0
        image: us-central1-docker.pkg.dev/conite-26806/connor-first-repo/random-facts-app:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            cpu: "0.1"
            memory: 256M
```
- `kubectl apply -f my_first_autoscaling_deployment_manifest_file.yaml` to create the deployment
#### my_first_autoscaling_service_manifest_file.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: random-facts-app-service
  namespace: random-facts-app-autoscaling
  labels:
    lab: random-facts-app-autoscaling
spec:
  selector:
    lab: random-facts-app-autoscaling
  ports:
  - name: http
    port: 5000
    protocol: TCP
    targetPort: 5000
  type: LoadBalancer
```
- `kubectl apply -f my_first_autoscaling_service_manifest_file.yaml` to create the service
#### my_first_horizontal_autoscaler_manifest_file.yaml
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: random-facts-app-autoscaler
  namespace: random-facts-app-autoscaling
  labels:
    lab: random-facts-app-autoscaling
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: random-facts-app
  minReplicas: 1
  maxReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 15
```
- `kubectl apply -f my_first_horizontal_autoscaler_manifest_file.yaml` to create the autoscaler
- file structure
```
folder random-facts-app-autoscaling
├── my_first_autoscaling_deployment_manifest_file.yaml
├── my_first_autoscaling_service_manifest_file.yaml
├── my_first_horizontal_autoscaler_manifest_file.yaml
└── my_first_namespace_autoscaling_manifest_file.yaml
```
- `kubectl get hpa -n random-facts-app-autoscaling` to see the autoscaler
- `kubectl get pods -n random-facts-app-autoscaling` to see the pods
- `kubectl get service -n random-facts-app-autoscaling` to see the ip address
```shell
$ kubectl get service -n random-facts-app-autoscaling
# NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)          AGE
# random-facts-app-service   LoadBalancer   34.118.228.82   34.172.240.142   5000:31259/TCP   2m23s 
```
- `ab -n 100000000 -c 10 http://<YOUR_EXTERNAL_IP>:5000/` to test the autoscaling
  - `ab -n 100000000 -c 10 http://34.172.240.142:5000/` to test the autoscaling
- clean up, delete all the resources
  - `kubectl delete namespace random-facts-app-autoscaling`
## kubernetes networking, ingress, and egress

```shell
cd ~
mkdir networking-ingress && cd networking-ingress

# Kubernetes Service Discovery
kubectl run --rm -it toolbox --image=jacobmammoliti/toolbox -- sh
dig random-facts-app-service.random-facts-app-deployment.svc.cluster.local

# CHALLENGE #1: Create a Headless service
# Use kubectl explain to understand how to create a Headless service
# Apply the service manifest to the cluster
# Create a "debug" Pod and use dig against the new headless service

# Kubernetes Services Extended
# CHALLENGE #2: Create a LoadBalancer service
# Update your existing Service manifest and change the type to LoadBalancer
# Apply the updated service manifest
# Access the service using the external IP

# Ingress Controllers
# Deploy NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.1/deploy/static/provider/cloud/deploy.yaml

# Get the reserved IP address
gcloud compute addresses list

# Patch the Ingress Controller to use the reserved IP
kubectl patch svc ingress-nginx-controller --namespace ingress-nginx --patch '{"spec":{"loadBalancerIP":"<YOUR_EXTERNAL_IP>"}}'

# Validate Ingress Controller
kubectl get pods,services --namespace ingress-nginx

# Path Based Routing
# Create an Ingress manifest with mistakes (to be corrected by the user)
# Apply the Ingress manifest and access the application at the IP address

# Host Based Routing
# CHALLENGE #3: Update the Ingress object to specify the host as an additional rule
# Access the application at the specified domain

# Adding TLS with cert-manager
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml

# Create a ClusterIssuer for Let's Encrypt Staging CA
# Use the provided YAML to create the ClusterIssuer
# Validate the ClusterIssuer is created successfully
kubectl get clusterissuer

# Update Ingress object for HTTPS
# Add tls stanza and an annotation to request a certificate from cert-manager
# Validate cert-manager successfully created the certificate
kubectl get certificate --namespace random-facts-app-deployment

# CHALLENGE #4: Create a new ClusterIssuer for Let's Encrypt production server
# Update Ingress object to request a certificate from the production server
# Access the application through a web browser via HTTPS

# Validate Ingress with an instructor before moving to the next labs

```

```shell
cd ~ && mkdir networking-ingress && cd networking-ingress
kubectl run --rm -it toolbox --image=jacobmammoliti/toolbox -- sh
```
```shell
dig random-facts-app-service.random-facts-app-deployment.svc.cluster.local
```

- CHALLENGE #1: Using your Service manifest from the previous lab as a starting point, create another one that defines a Headless service.
#### my_first_headless_service_manifest_file.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: random-facts-app-service-headless
  namespace: random-facts-app-deployment
spec:
    selector:
        lab: random-facts-app-deployment
    ports:
    - name: http
      port: 5000
      protocol: TCP
      targetPort: 5000
```
- CHALLENGE #2: Using your previous Service manifests as a starting point, create a new Service manifest and change the type to LoadBalancer.
#### my_first_loadbalancer_service_manifest_file.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: random-facts-app-service-loadbalancer
  namespace: random-facts-app-deployment
spec:
    selector:
        lab: random-facts-app-deployment
    ports:
    - name: http
      port: 5000
      protocol: TCP
      targetPort: 5000
    type: LoadBalancer
```

- `kubectl apply -f my_first_headless_service_manifest_file.yaml` to create the headless service
- `dig random-facts-app-service-headless.random-facts-app-deployment.svc.cluster.local` to get the ip address

- `kubectl apply -f my_first_loadbalancer_service_manifest_file.yaml` to create the loadbalancer service
- `kubectl get service -n random-facts-app-deployment` to get the ip address
```shell
$ kubectl get service -n random-facts-app-deployment
#                        TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)          AGE
#random-facts-app-service                ClusterIP      34.118.229.184   <none>         5000/TCP         175m
#random-facts-app-service-headless       ClusterIP      34.118.239.144   <none>         5000/TCP         10m
#random-facts-app-service-loadbalancer   LoadBalancer   34.118.234.140   34.134.144.6   5000:30727/TCP   98s
```

### ingress Controllers

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.1/deploy/static/provider/cloud/deploy.yaml # to install the ingress controller
gcloud compute address list # to get the ip address

# patch command to tell ingress controller to use the ip address
kubectl patch svc ingress-nginx-controller \
--namespace ingress-nginx \
--patch '{"spec":{"loadBalancerIP":"<34.42.102.53>"}}'
```
```shell
# to see the ingress controller
$ kubectl get pods,services --namespace ingress-nginx
```
- return
```text
#NAME                                            READY   STATUS      RESTARTS   AGE
#pod/ingress-nginx-admission-create-2mcjn        0/1     Completed   0          4m41s
#pod/ingress-nginx-admission-patch-h4nmm         0/1     Completed   0          4m40s
#pod/ingress-nginx-controller-56b4fc9b8c-vhhfw   1/1     Running     0          4m41s
#
#NAME                                         TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)                      AGE
#service/ingress-nginx-controller             LoadBalancer   34.118.226.94    34.42.102.53   80:31868/TCP,443:30986/TCP   4m43s
#service/ingress-nginx-controller-admission   ClusterIP      34.118.234.186   <none>         443/TCP                      4m42s
```

#### path based routing with my_first_ingress_manifest_file.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: random-facts-app-ingress
  namespace: default
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app
            port:
              number: 8080
```

#### host based routing
- Update your Ingress object to now specify the host as an additional rule.
- `*.<YOUR_STUDENT_ID>.<RANDOM_ID>.workshops.acceleratorlabs.ca`
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: random-facts-app-ingress
  namespace: default
spec:
    ingressClassName: nginx
    rules:
    - host: *.<YOUR_STUDENT_ID>.<RANDOM_ID>.workshops.acceleratorlabs.ca
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
            service:
                name: my-app
                port:
                number: 8080
    
```
```text
NAMESPACE                     NAME                       CLASS   HOSTS                                                                         ADDRESS          PORTS   AGE
random-facts-app-deployment   random-facts-app-ingress   nginx   app.<YOUR_STUDENT_ID>.<RANDOM_ID>.workshops.acceleratorlabs.ca                35.239.236.127   80      29
```

#### adding TLS with Cert-Manager
```shell
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml

```

## Applying Kubenetes NetworkPolicy
```shell
Kubernetes NetworkPolicy allows you to control traffic flow between services at the IP address and port level. In this lab, you will configure your GKE cluster with two NetworkPolicies to finely allow traffic.

Default Deny All Ingress Traffic #
Let’s create a NetworkPolicy that denies all traffic coming into your random-facts-app-deployment namespace.

To begin, create a dedicated directory for this lab and switch into it:

cd ~

mkdir network-policy && cd network-policy
Create a NetworkPolicy manifest with the following contents and apply it to your cluster:

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-ingress
  namespace: random-facts-app-deployment
spec:
  podSelector: {}
  policyTypes:
  - Ingress
To test this NetworkPolicy, create a new Namespace called network-policy with the label lab=network-policy where you will test the connections from.

Run the following command to create a pod in the newly created network-policy namespace:

kubectl run --rm -it toolbox --namespace network-policy --image=jacobmammoliti/toolbox -- sh
Once a prompt comes up, run the following cURL command against your application in the random-facts-app-deployment namespace with the following command:

curl random-facts-app-service.random-facts-app-deployment.svc.cluster.local:5000 --max-time 5 -I
After 5 seconds, you will see that it has timed out. This is due to the NetworkPolicy blocking the connection.

Enter exit into the shell to exit and terminate the pod.

Layering on Additional NetworkPolicy #
In some cases, you may need pods in one namespace to be able to communicate with pods in another namespace. You can layer on additional policies to achieve this. In this lab, you will allow communication from pods with the label lab=network-policy that reside in the network-policy namespace to pods in the random-facts-app-deployment namespace.

You can begin by using the following NetworkPolicy manifest as a starting point to create a rule. This rule should only permit Pods with the lab=network-policy label from the network-policy namespace to communicate with pods within the random-facts-app-deployment namespace.

NOTE
Ensure that the following NetworkPolicy is deployed in the appropriate namespace and that you have added a podSelector.
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-random-facts-app-deployment
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            lab: network-policy
Once you have written the policy, apply it and try the connection again with the following command:

kubectl run --rm -it toolbox --namespace network-policy --labels='lab=network-policy' --image=jacobmammoliti/toolbox -- sh
Once a prompt comes up, run the following cURL command against your application in the random-facts-app-deployment namespace with the following command:

curl random-facts-app-service.random-facts-app-deployment.svc.cluster.local:5000 -I
You will now see an output similar to below:

HTTP/1.1 200 OK
Server: Werkzeug/2.3.4 Python/3.12.0b1
...
Connection: close
With that, you have successfully configured NetworkPolicy. NetworkPolicy is just one piece of the puzzle when it comes to securing your GKE cluster. In future labs, you will explore additional methods to further enhance the security of your cluster.


```



## anthos on bare metal
### create anthos on bare metal admin cluster
- assume project id is now `conite-26806`, run following
```shell
export PROJECT_ID=conite-26806
gcloud config set project $PROJECT_ID
gcloud iam service-accounts create anthos-baremetal-gcr
```
- anthos-baremetal-connect service account
```shell
gcloud iam service-accounts create anthos-baremetal-connect

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:anthos-baremetal-connect@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/gkehub.connect" \
  --no-user-output-enabled
```
- anthos-baremetal-register service account
```shell
gcloud iam service-accounts create anthos-baremetal-register

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:anthos-baremetal-register@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/gkehub.admin" \
  --no-user-output-enabled
```
- anthos-baremetal-cloud-ops service account with the following roles
  - roles/logging.logWriter - roles/monitoring.metricWriter - roles/stackdriver.resourceMetadata.writer - roles/opsconfigmonitoring.resourceMetadata.writer - roles/monitoring.dashboardEditor
```shell
gcloud iam service-accounts create anthos-baremetal-cloud-ops

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:anthos-baremetal-cloud-ops@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter" \
    --role="roles/monitoring.metricWriter" \
    --role="roles/stackdriver.resourceMetadata.writer" \
    --role="roles/opsconfigmonitoring.resourceMetadata.writer" \
    --role="roles/monitoring.dashboardEditor" \
    --no-user-output-enabled
```
### create admin workstation
- `gcloud compute ssh root@abm-cluster-ws --zone us-central1-a` to ssh into the admin workstation
- set env
```shell
export PROJECT_ID=$(gcloud config get-value project)
export ZONE=us-central1-a
export BMCTL_VERSION=1.15.4
```
- install bmctl
```shell
export BMCTL_VERSION=1.16.1
mkdir baremetal && cd baremetal
gsutil cp gs://anthos-baremetal-release/bmctl/$BMCTL_VERSION/linux-amd64/bmctl .
chmod a+x bmctl
mv bmctl /usr/local/sbin/
```
- install kubectl
```shell
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl /usr/local/sbin/
```
- install docker
```shell
cd ~
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```
- to create a new dir
```shell
mkdir sa-keys
```
- go through the created service account keys
```shell
gcloud iam service-accounts keys create ./sa-keys/bm-gcr.json \
    --iam-account=anthos-baremetal-gcr@"${PROJECT_ID}".iam.gserviceaccount.com

gcloud iam service-accounts keys create ./sa-keys/bm-register.json \
    --iam-account=anthos-baremetal-register@"${PROJECT_ID}".iam.gserviceaccount.com

gcloud iam service-accounts keys create ./sa-keys/bm-cloud-ops.json \
      --iam-account=anthos-baremetal-cloud-ops@"${PROJECT_ID}".iam.gserviceaccount.com
      
gcloud iam service-accounts keys create ./sa-keys/bm-connect.json \
      --iam-account=anthos-baremetal-connect@"${PROJECT_ID}".iam.gserviceaccount.com
```

- create an ssh key pair `ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa`
- we add instance metadata of our vms `sed 's/ssh-rsa/root:ssh-rsa/' ~/.ssh/id_rsa.pub > ssh-metadata`
- `gcloud compute instances add-metadata abm-admin-cluster-cp1 --zone $ZONE --metadata-from-file ssh-keys=ssh-metadata` to add the metadata to the vm
#### run above commands in bulk
```shell
ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa
sed 's/ssh-rsa/root:ssh-rsa/' ~/.ssh/id_rsa.pub > ssh-metadata
gcloud compute instances add-metadata abm-admin-cluster-cp1 --zone $ZONE --metadata-from-file ssh-keys=ssh-metadata
```
## create admin cluster
| VM Name                | IP Address  | VxLAN IP  |
|------------------------|-------------|-----------|
| abm-cluster-ws         | 10.0.1.100  | 10.200.0.2|
| abm-admin-cluster-cp1  | 10.0.1.101  | 10.200.0.3|

#### register the bootstrap cluster
```shell
cd ~
export ADMIN_CLUSTER_NAME=admin-cluster # replace with your admin cluster name
export CONNECT_AGENT_KEY_LOCATION=/root/sa-keys/bm-connect.json # replace with your connect agent key location


bmctl register bootstrap \
  --ssh-key=/root/.ssh/id_rsa \
  --name=bootstrap-${ADMIN_CLUSTER_NAME} \
  --project-id=$PROJECT_ID \
  --gcr-service-account-key=./sa-keys/bm-gcr.json \
  --gke-register-service-account-key=./sa-keys/bm-register.json \
  --cloud-operation-service-account-key=./sa-keys/bm-cloud-ops.json \
  --gke-agent-service-account-key=$CONNECT_AGENT_KEY_LOCATION
```
- while the above command is running, you will see the following output, you need to go to [following command while they are running](#create-the-cluster-in-the-same-time-as-previous-command-is-running)
```text
[2023-03-22 17:35:24+0000] Waiting for the temporary cluster to be registered... OK
[2023-03-22 17:35:37+0000] Please go to https://console.cloud.google.com/home/dashboard?project=example-project-12345 to create the cluster
[2023-03-22 17:35:37+0000] Waiting for preflight checks and cluster to run..
```
#### create the cluster in the same time as previous command is running
- assume project id is now `conite-26806`, run following
```shell
export PROJECT_ID=conite-26806
export ON_PREM_API_REGION=us-central1
export ADMIN_CLUSTER_NAME=admin-cluster
export BMCTL_VERSION=1.15.4
gcloud config set project $PROJECT_ID
```
- Now we will use the following command to create the admin cluster
```shell
export ADMIN_CLUSTER_CP1_VXLAN=10.200.0.3
export ADMIN ADMIN_CLUSTER_NAME=admin-cluster
gcloud container bare-metal admin-clusters create $ADMIN_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$ON_PREM_API_REGION \
  --version=$BMCTL_VERSION \
  --max-pods-per-node=110 \
  --control-plane-vip=10.200.0.48 \
  --control-plane-load-balancer-port=443 \
  --control-plane-node-configs node-ip=$ADMIN_CLUSTER_CP1_VXLAN \
  --island-mode-service-address-cidr-blocks=10.96.0.0/20 \
  --island-mode-pod-address-cidr-blocks=192.168.0.0/16 \
  --lvp-share-path=/mnt/localpv-share \
  --lvp-share-storage-class=local-shared \
  --lvp-node-mounts-config-path=/mnt/localpv-disk \
  --lvp-node-mounts-config-storage-class=local-disks
```
- example output, wait until the cluster is created
```text
Waiting for operation [projects/my-project/locations/us-central1/operations/operation-1698357997564-608a5c925728a-8ef2c9be-cbedb2ee] to complete...working...
```
- after successful creation of above command, you will see the output of [previous command](#register-the-bootstrap-cluster) as follows
```text
[2023-03-22 23:12:47+0000] Waiting for cluster kubeconfig to become ready OK
[2023-03-22 23:15:47+0000] Writing kubeconfig file
[2023-03-22 23:15:47+0000] kubeconfig of cluster being created is present at bmctl-workspace/abm-cluster-1/abm-cluster-1-kubeconfig
[2023-03-22 23:15:47+0000] Please restrict access to this file as it contains authentication credentials of your cluster.
[2023-03-22 23:15:47+0000] Waiting for cluster to become ready OK
[2023-03-22 23:20:17+0000] Please run
[2023-03-22 23:20:17+0000] kubectl --kubeconfig bmctl-workspace/abm-cluster-1/abm-cluster-1-kubeconfig get nodes
[2023-03-22 23:20:17+0000] to get cluster nodes status.
[2023-03-22 23:20:17+0000] Waiting for node pools to become ready OK
[2023-03-22 23:20:37+0000] Waiting for metrics to become ready in GCP OK
[2023-03-22 23:25:38+0000] Waiting for cluster API provider to install in the created admin cluster OK
[2023-03-22 23:25:48+0000] Moving admin cluster resources to the created admin cluster
[2023-03-22 23:25:51+0000] Waiting for node update jobs to finish OK
[2023-03-22 23:27:41+0000] Flushing logs... OK
[2023-03-22 23:27:41+0000] Deleting membership... OK
[2023-03-22 23:27:42+0000] Deleting bootstrap cluster.
```

```shell
kubectl get nodes
#NAME                    STATUS   ROLES           AGE   VERSION
#abm-admin-cluster-cp1   Ready    control-plane   1m   v1.26.5-gke.2100
```
#### connect to admin cluster
```shell
export ADMIN ADMIN_CLUSTER_NAME=admin-cluster
export KUBECONFIG=/root/bmctl-workspace/$ADMIN_CLUSTER_NAME/$ADMIN_CLUSTER_NAME-kubeconfig
export PROJECT_ID=conite-26806
export YOUR_EMAIL_ADDRESS=connorleekite@gmail.com
export CONTEXT="$(kubectl config current-context)"

gcloud container fleet memberships generate-gateway-rbac  \
    --membership=$ADMIN_CLUSTER_NAME \
    --role=clusterrole/cluster-admin \
    --users=$YOUR_EMAIL_ADDRESS \
    --project=$PROJECT_ID \
    --kubeconfig=$KUBECONFIG \
    --context=$CONTEXT\
    --apply
```
- returns
```text
Writing RBAC policy for user: first.last@domain.com to cluster.
Successfully applied the RBAC policy to cluster.
```
#### testing the connection
```shell
gcloud container fleet memberships get-credentials $ADMIN_CLUSTER_NAME
```

## Create anthos on bare metal user cluster

| VM Name                 | IP Address   | VxLAN IP   |
|-------------------------|--------------|------------|
| abm-cluster-ws          | 10.0.1.100   | 10.200.0.2 |
| abm-admin-cluster-cp1   | 10.0.1.101   | 10.200.0.3 |
| abm-user-cluster-cp1    | 10.0.1.102   | 10.200.0.4 |


- export the following variables
```shell
export PROJECT_ID=conite-26806
export ON_PREM_API_REGION=us-central1
export BMCTL_VERSION=1.15.4
export ADMIN_CLUSTER_NAME=admin-cluster
export USER_CLUSTER_NAME=user-cluster-1
```
- ssh into the admin workstation
```shell
gcloud compute ssh root@abm-cluster-ws --zone us-central1-a
```
- create the user cluster

```shell
gcloud compute instances add-metadata abm-user-cluster-cp1 --zone us-central1-a --metadata-from-file ssh-keys=ssh-metadata
```

```shell
export YOUR_EMAIL_ADDRESS=connorleekite@gmail.com
#replace with abm-user-cluster-cp1
export ON_PREM_API_REGION=us-central1
export USER_CLUSTER_NAME=user-cluster-1
export PROJECT_ID=conite-26806
export YOUR_EMAIL_ADDRESS=connorleekite@gmail.com
export BMCTL_VERSION=1.15.4
export ADMIN_CLUSTER_NAME=admin-cluster
export PROJECT_ID=conite-26806

# the following command will create the user cluster
gcloud container bare-metal clusters create $USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --admin-cluster-membership=projects/$PROJECT_ID/locations/global/memberships/$ADMIN_CLUSTER_NAME \
  --location=$ON_PREM_API_REGION \
  --version=$BMCTL_VERSION \
  --admin-users=$YOUR_EMAIL_ADDRESS \
  --metal-lb-address-pools='pool=lb-pool-1,manual-assign=True,addresses=10.200.0.51-10.200.0.70' \
  --control-plane-node-configs='node-ip=10.200.0.4' \
  --control-plane-vip=10.200.0.50 \
  --control-plane-load-balancer-port=443 \
  --ingress-vip=10.200.0.51 \
  --island-mode-service-address-cidr-blocks=10.96.0.0/20 \
  --island-mode-pod-address-cidr-blocks=192.168.0.0/16 \
  --lvp-share-path=/mnt/localpv-share \
  --lvp-share-storage-class=local-shared \
  --lvp-node-mounts-config-path=/mnt/localpv-disk \
  --lvp-node-mounts-config-storage-class=local-disks
```
- waiting output
```text
Waiting for operation [projects/my-project/locations/us-central1/operations/operation-1698432741461-608b7303acf99-652b06f0-49d957df] to complete...working...
```

- successful shell output
```text
Created Anthos cluster on bare metal [https://gkeonprem.googleapis.com/v1/projects/my-project/locations/us-central1/bareMetalClusters/user-cluster-1].
NAME: user-cluster-1
LOCATION: us-central1
VERSION: 1.15.4
ADMIN_CLUSTER: admin-cluster
STATE: RUNNING
```
- We can also connect to our user cluster on the command line
```shell
export USER_CLUSTER_NAME=user-cluster-1
gcloud container fleet memberships get-credentials $USER_CLUSTER_NAME
```

## manage Node Pools in a cluster
| VM Name              | IP Address  | VxLAN IP  |
|----------------------|-------------|-----------|
| abm-cluster-ws       | 10.0.1.100  | 10.200.0.2|
| abm-admin-cluster-cp1| 10.0.1.101  | 10.200.0.3|
| abm-user-cluster-cp1 | 10.0.1.102  | 10.200.0.4|
| abm-user-cluster-w1  | 10.0.1.104  | 10.200.0.6|
| abm-user-cluster-w2  | 10.0.1.105  | 10.200.0.7|

```shell
gcloud compute ssh root@abm-cluster-ws --zone us-central1-a
```

```shell
# add our ssh key to the metadata
gcloud compute instances add-metadata abm-user-cluster-w1 --zone us-central1-a --metadata-from-file ssh-keys=ssh-metadata
gcloud compute instances add-metadata abm-user-cluster-w2 --zone us-central1-a --metadata-from-file ssh-keys=ssh-metadata

```
```shell
export PROJECT_ID=conite-26806
export USER_CLUSTER_NAME=user-cluster-1
export LOCATION=us-central1
# list the node pool
gcloud container bare-metal node-pools list \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION
```


#### configuration file format
```yaml
nodeConfigs:
- nodeIP: 10.200.0.10
  labels:
    key1: value1
    key2: value2
- nodeIP: 10.200.0.11
  labels:
    key3: value3
    key4: value4
```
- Have us include the abm-user-cluster-w1 VM as one of the nodes
- Assign the node a label of environment=production.
#### node-pool-config.yaml
```yaml
nodeConfigs:
- nodeIP: 10.0.1.104
  labels:
    environment: production
```

```shell
mkdir node-pool-config && cd node-pool-config
export NODE_POOL_NAME=node-pool-1
export NODE_CONFIG_FILE=/root/configs/node-pool-config.yaml
```
```shell
# create the node pool config file
gcloud container bare-metal node-pools create $NODE_POOL_NAME \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION \
  --node-configs-from-file=$NODE_CONFIG_FILE

```
- returns
```text
Created node pool in Anthos cluster on bare metal [https://gkeonprem.googleapis.com/v1/projects/my-project/locations/us-central1/bareMetalClusters/user-cluster-name/bareMetalNodePools/node-pool-1].

NAME         LOCATION     STATE
node-pool-1  us-central1  RUNNING
```

#### checking nodes status
```shell
# list the node pools
gcloud container bare-metal node-pools list \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION
```
- returns
```text
NAME         LOCATION     STATE
node-pool-1  us-central1  RUNNING
```
```shell
# describe the node pool  
gcloud container bare-metal node-pools describe $NODE_POOL_NAME \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION
```
- returns
```text
annotations:
  baremetal.cluster.gke.io/version: 1.15.4
createTime: '2023-11-08T20:42:02.866735585Z'
etag: lb56NjZ-0euBHcq3HQIaE01GBKOyIOuKkE01IsDHdAk
name: projects/conite-26806/locations/us-central1/bareMetalClusters/user-cluster-1/bareMetalNodePools/node-pool-1
nodePoolConfig:
  nodeConfigs:
  - labels:
      environment: production
    nodeIp: 10.0.1.104
  operatingSystem: LINUX
state: RUNNING
status:
  conditions:
  - lastTransitionTime: '2023-11-08T20:45:39Z'
    reason: NodepoolReady
    state: STATE_TRUE
    type: Ready
uid: 99fbf1bb-6d1c-4d71-b072-2474f0423d27
updateTime: '2023-11-08T20:45:22.801770124Z'
```

#### remove a node pool
```shell
# remove the node pool
gcloud container bare-metal node-pools delete $NODE_POOL_NAME  \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION
```

#### update a node pool with node-pool-config.yaml

- add a new node to the node pool
  - Have us include the abm-user-cluster-w2 VM as one of the nodes
  - Assign the node a label of environment=staging.

```yaml
nodeConfigs:
- nodeIP: 10.0.1.104
  labels:
    environment: production
- nodeIP: 10.0.1.105
  labels:
    environment: staging
```

```shell
gcloud container bare-metal node-pools update $NODE_POOL_NAME  \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION \
  --node-configs-from-file=$NODE_CONFIG_FILE
```

## Using Terraform, create user cluster and node pool
| VM Name              | IP Address  | VxLAN IP  |
|----------------------|-------------|-----------|
| abm-cluster-ws       | 10.0.1.100  | 10.200.0.2|
| abm-user-cluster-cp2 | 10.0.1.103  | 10.200.0.5|
| abm-user-cluster-w3  | 10.0.1.106  | 10.200.0.8|

```shell
gcloud compute ssh root@abm-cluster-ws --zone us-central1-a
```

```shell
export PROJECT_ID=conite-26806

gcloud compute instances add-metadata abm-user-cluster-cp2 --zone us-central1-a --metadata-from-file ssh-keys=ssh-metadata
gcloud compute instances add-metadata abm-user-cluster-w3 --zone us-central1-a --metadata-from-file ssh-keys=ssh-metadata
```

```shell
mkdir cluster-terraform && cd cluster-terraform
touch providers.tf
touch main.tf

```

#### providers.tf
```text
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.4.0"
    }
  }
}

provider "google" {
  # Configuration options
  project= "conite-26806"
  region = "us-central1"
}
```

#### main.tf
```text
resource "google_gkeonprem_bare_metal_cluster" "user-cluster" {
  name = "user-cluster-2"
  location = "us-central1"
  # admin_cluster_membership = "projects/<PROJECT_ID>/locations/global/memberships/<ADMIN_CLUSTER_NAME>"
  admin_cluster_membership = "projects/conite-26806/locations/global/memberships/admin-cluster"
  bare_metal_version = "1.15.4"
  network_config {
    island_mode_cidr {
      service_address_cidr_blocks = ["10.96.0.0/20"]
      pod_address_cidr_blocks = ["192.168.0.0/16"]
    }
  }
  control_plane {
    control_plane_node_pool_config {
      node_pool_config {
        labels = {}
        operating_system = "LINUX"
        node_configs {
          labels = {}
          # node_ip = <USER_CLUSTER_CP2_VXLAN>
          node_ip = "10.0.1.103"
        }
      }
    }
  }
  load_balancer {
    port_config {
      control_plane_load_balancer_port = 443
    }
    vip_config {
      control_plane_vip = "10.200.0.100"
      ingress_vip = "10.200.0.101"
    }
    metal_lb_config {
      address_pools {
        pool = "lb-pool-1"
        addresses = [
          "10.200.0.101-10.200.0.120"
        ]
        avoid_buggy_ips = true
        manual_assign = true
      }
    }
  }
  storage {
    lvp_share_config {
      lvp_config {
        path = "/mnt/localpv-share"
        storage_class = "local-shared"
      }
      shared_path_pv_count = 5
    }
    lvp_node_mounts_config {
      path = "/mnt/localpv-disk"
      storage_class = "local-disks"
    }
  }
  security_config {
    authorization {
      admin_users {
        username = "connorleekite@gmail.com"
      }
    }
  }
}
```

## Putting a Node into Maintenance Mode
| VM Name               | IP Address  | VxLAN IP  |
|-----------------------|-------------|-----------|
| abm-cluster-ws        | 10.0.1.100  | 10.200.0.2|
| abm-admin-cluster-cp1 | 10.0.1.101  | 10.200.0.3|
| abm-user-cluster-cp1  | 10.0.1.102  | 10.200.0.4|
| abm-user-cluster-w1   | 10.0.1.104  | 10.200.0.6|
| abm-user-cluster-w2   | 10.0.1.105  | 10.200.0.7|

```shell
export PROJECT_ID=conite-26806
export USER_CLUSTER_NAME="user-cluster-1"
export ADMIN_CLUSTER_NAME="admin-cluster"

# interact with user
gcloud container fleet memberships get-credentials $USER_CLUSTER_NAME --project $PROJECT_ID
kubectl create deployment nginx --image nginx --replicas 5 
```

```shell
kubectl get pods -o wide
kubectl get nodes -o wide
```
- returns
```text
NAME                  STATUS   ROLES           AGE   VERSION           INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
NAME                     READY   STATUS    RESTARTS   AGE   IP              NODE                  NOMINATED NODE   READINESS GATES
nginx-748c667d99-6thwt   1/1     Running   0          10s   192.168.3.93    abm-user-cluster-w2   <none>           <none>
nginx-748c667d99-bbsb6   1/1     Running   0          10s   192.168.3.35    abm-user-cluster-w2   <none>           <none>
nginx-748c667d99-krtmh   1/1     Running   0          10s   192.168.2.62    abm-user-cluster-w1   <none>           <none>
nginx-748c667d99-mvwpv   1/1     Running   0          10s   192.168.3.44    abm-user-cluster-w2   <none>           <none>
nginx-748c667d99-v7w9j   1/1     Running   0          10s   192.168.2.224   abm-user-cluster-w1   <none>           <none>
NAME                   STATUS   ROLES           AGE   VERSION            INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
abm-user-cluster-cp1   Ready    control-plane   20h   v1.26.5-gke.2100   10.200.0.4    <none>        Ubuntu 20.04.6 LTS   5.15.0-1046-gcp   containerd://1.6.21-gke.2
abm-user-cluster-w1    Ready    worker          19h   v1.26.5-gke.2100   10.0.1.104    <none>        Ubuntu 20.04.6 LTS   5.15.0-1046-gcp   containerd://1.6.21-gke.2
abm-user-cluster-w2    Ready    worker          19h   v1.26.5-gke.2100   10.0.1.105    <none>        Ubuntu 20.04.6 LTS   5.15.0-1046-gcp   containerd://1.6.21-gke.2
```

```shell
# interact with admin cluster
gcloud container fleet memberships get-credentials $ADMIN_CLUSTER_NAME --project $PROJECT_ID
# interactive shell with kubeconfig
kubectl -n cluster-${USER_CLUSTER_NAME} edit cluster $USER_CLUSTER_NAME
# explain the user cluster
kubectl -n cluster-${USER_CLUSTER_NAME} get cluster $USER_CLUSTER_NAME -o yaml


```
- returns
```yaml
apiVersion: baremetal.cluster.gke.io/v1
kind: Cluster
metadata:
  annotations:
    alpha.baremetal.cluster.gke.io/cluster-metrics-webhook: "true"
    baremetal.cluster.gke.io/install-version: 1.15.4
    baremetal.cluster.gke.io/operation: install
    baremetal.cluster.gke.io/operation-id: ff95c9b8-75c7-4ded-9330-788ed6f82550
    baremetal.cluster.gke.io/start-time: "2023-11-08T20:19:34Z"
    onprem.cluster.gke.io/user-cluster-resource-link: //gkeonprem.googleapis.com/projects/15980817592/locations/us-central1/bareMetalClusters/user-cluster-1
    preview.baremetal.cluster.gke.io/incremental-network-preflight-checks: Enable
  creationTimestamp: "2023-11-08T20:19:34Z"
  finalizers:
  - baremetal.cluster.gke.io/cluster-finalizer
  generation: 1
  labels:
    baremetal.cluster.gke.io/cluster-version: 1.15.4
  name: user-cluster-1
  namespace: cluster-user-cluster-1
  resourceVersion: "606903"
  uid: b1a49ddc-8033-4a99-9e1b-d9ba5cb497c1
spec:
  maintenanceBlocks: # this puts the specified node into maintenance mode for abm-user-cluster-w1
    cidrBlocks:
    - 10.0.1.104 # this ip address should match the ip address of the node
 .....
```

```shell
kubectl config use-context connectgateway_${PROJECT_ID}_global_${USER_CLUSTER_NAME}
kubectl get node abm-user-cluster-w1  -o=jsonpath="{.spec.taints}"
```
- returns
```text
[{"effect":"NoSchedule","key":"baremetal.cluster.gke.io/maintenance"},{"effect":"NoExecute","key":"baremetal.cluster.gke.io/maintenance"}]
```

```shell
kubectl config use-context connectgateway_${PROJECT_ID}_global_${ADMIN_CLUSTER_NAME}
kubectl get nodepools -A
```
- returns
```text
NAMESPACE                NAME             READY   RECONCILING   STALLED   UNDERMAINTENANCE   UNKNOWN
cluster-admin-cluster    admin-cluster    1       0             0         0                  0
cluster-user-cluster-1   node-pool-1      2       0             0         1                  0 # this shows that the node is under maintenance
cluster-user-cluster-1   user-cluster-1   1       0             0         0                  0
```

```shell
kubectl config use-context connectgateway_${PROJECT_ID}_global_${USER_CLUSTER_NAME}
kubectl get pods -o wide
```
- returns
```text
NAME                     READY   STATUS    RESTARTS   AGE    IP              NODE                  NOMINATED NODE   READINESS GATES
nginx-748c667d99-6thwt   1/1     Running   0          31m    192.168.3.93    abm-user-cluster-w2   <none>           <none>
nginx-748c667d99-bbsb6   1/1     Running   0          31m    192.168.3.35    abm-user-cluster-w2   <none>           <none>
nginx-748c667d99-mvwpv   1/1     Running   0          31m    192.168.3.44    abm-user-cluster-w2   <none>           <none>
nginx-748c667d99-swksq   1/1     Running   0          4m3s   192.168.3.119   abm-user-cluster-w2   <none>           <none> # this nginx pod has been moved to abm-user-cluster-w2
nginx-748c667d99-xggsd   1/1     Running   0          4m3s   192.168.3.104   abm-user-cluster-w2   <none>           <none> # this nginx pod has been moved to abm-user-cluster-w2
```

### ok, lets remove the node from maintenance mode
```shell
kubectl config use-context connectgateway_${PROJECT_ID}_global_${ADMIN_CLUSTER_NAME}
kubectl -n cluster-${USER_CLUSTER_NAME} edit cluster $USER_CLUSTER_NAME
# then remove the maintenanceBlocks section
```
- lets scale up the nginx deployment
```shell
kubectl config user-context connectgateway_${PROJECT_ID}_global_${USER_CLUSTER_NAME}
kubectl scale deployment nginx --replicas=10
```

## Upgrade admin/ user cluster
```shell
export PROJECT_ID=conite-26806
export ADMIN_CLUSTER_NAME="admin-cluster"
export USER_CLUSTER_NAME="user-cluster-1"
export REGION="us-central1"

gcloud container bare-metal admin-clusters list \
  --project=$PROJECT_ID \
  --location=$REGION
  
gcloud container bare-metal clusters list \
  --project=$PROJECT_ID \
  --location=$REGION
```
- return 
```text
NAME: admin-cluster
LOCATION: us-central1
VERSION: 1.15.4
MEMBERSHIP: admin-cluster
STATE: RUNNING

NAME: user-cluster-2
LOCATION: us-central1
VERSION: 1.15.4
ADMIN_CLUSTER: admin-cluster
STATE: DEGRADED

NAME: user-cluster-1
LOCATION: us-central1
VERSION: 1.15.4
ADMIN_CLUSTER: admin-cluster
STATE: RUNNING
```

```shell
gcloud container bare-metal admin-clusters query-version-config \
  --admin-cluster=$ADMIN_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$REGION
```
- return
```text
versions:
- version: 1.16.1
- version: 1.16.0
- version: 1.15.5
```

```shell
export VERSION="1.16.1"
gcloud container bare-metal admin-clusters update $ADMIN_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$REGION \
  --version=$VERSION
```
- returns
```text
Waiting for operation [projects/conite-26806/locations/us-central1/operations/operation-1699552433527-609bbe313dc75-b90684bc-d3d01bb9] to complete...working
```                                         

```shell
# check status
export OPERATION_ID=operation-1699552433527-609bbe313dc75-b90684bc-d3d01bb9
export REGION=us-central1
gcloud container bare-metal operations describe $OPERATION_ID \
  --project=$PROJECT_ID \
  --location=$REGION
```

```shell
gcloud container bare-metal clusters query-version-config \
  --cluster=$USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$REGION

export VERSION="1.16.1"
# upgrading user cluster
gcloud container bare-metal clusters update USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$REGION \
  --version=$VERSION
```

## Backup and restore clusters
```shell
export ADMIN_CLUSTER_NAME=admin-cluster
export USER_CLUSTER_NAME=user-cluster-1
export PROJECT_ID=conite-26806
export ADMIN_CLUSTER_NAMESPACE=cluster-admin-cluster
export REGION=us-central1

```

```shell
# change context to admin cluster
gcloud container fleet memberships get-credentials $ADMIN_CLUSTER_NAME --project $PROJECT_ID

kubectl get cluster $ADMIN_CLUSTER_NAME -n $ADMIN_CLUSTER_NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Reconciling")]}{"\n"}'

kubectl create secret generic database-a \
  --from-literal=host=database-a.company.local \
  --from-literal=username=admin \
  --from-literal=password=SuperSecure

kubectl get secret database-a -o yaml
```
- returns
```yaml
apiVersion: v1
data:
  host: ZGF0YWJhc2UtYS5jb21wYW55LmxvY2Fs
  password: U3VwZXJTZWN1cmU=
  username: YWRtaW4=
kind: Secret
metadata:
  creationTimestamp: "2023-11-09T18:28:41Z"
  name: database-a
  namespace: default
  resourceVersion: "676235"
  uid: eb180135-dbe1-4404-a8e5-03306ec89b61
type: Opaque
```

```shell
# change context to user cluster
gcloud container fleet memberships get-credentials $USER_CLUSTER_NAME --project $PROJECT_ID
# remember to install bmctl mentioned previously
export KUBECONFIG=/root/bmctl-workspace/$ADMIN_CLUSTER_NAME/${ADMIN_CLUSTER_NAME}-kubeconfig
bmctl backup cluster -c $ADMIN_CLUSTER_NAME --backup-file admin-cluster-backup.tar.gz --kubeconfig $KUBECONFIG
bmctl restore cluster -c $ADMIN_CLUSTER_NAME --backup-file $BACKUP_FILE_NAME --kubeconfig $KUBECONFIG
```

## Reset Nodes and delete admin/user cluster
```shell
export PROJECT_ID=conite-26806
export USER_CLUSTER_NAME="user-cluster-1"
export ADMIN_CLUSTER_NAME="admin-cluster"
export LOCATION="us-central1"

gcloud container fleet memberships get-credentials $USER_CLUSTER_NAME --project $PROJECT_ID

kubectl get nodes -o wide
gcloud compute instances list

gcloud compute instances suspend abm-user-cluster-w2 --zone us-central1-a


# Remove the unresponsive node from the node pool
# Update the node configuration file in the node-pool-config directory
# Use gcloud to update the node pool
# If needed, force remove the node
# kubectl delete node abm-user-cluster-w2

# Resume the VM
gcloud compute instances resume abm-user-cluster-w2 --zone us-central1-a


# SSH into the admin workstation
gcloud compute ssh root@abm-cluster-ws --zone us-central1-a

export NODE_IP_ADDRESS=10.0.0.1

# Reset the node
bmctl reset nodes --addresses $NODE_IP_ADDRESS \
    --ssh-private-key-path /root/.ssh/id_rsa \
    --gcr-service-account-key /root/sa-keys/bm-gcr.json \
    --login-user root

kubectl get nodes

# Delete the user cluster
gcloud container bare-metal clusters delete $USER_CLUSTER_NAME \
  --project=$PROJECT_ID \
  --location=$LOCATION \
  --force

# Unenroll the admin cluster from Anthos On-Prem API
gcloud container bare-metal admin-clusters unenroll $ADMIN_CLUSTER_NAME \
    --project=$PROJECT_ID \
    --location=$LOCATION

# SSH back into the admin workstation
gcloud compute ssh root@abm-cluster-ws --zone us-central1-a

# Use bmctl to unregister the admin cluster from the fleet and delete it
export ADMIN_CLUSTER_NAME="admin-cluster"
bmctl reset -c $ADMIN_CLUSTER_NAME

```