https://github.com/larkintuckerllc/k8s-cka-tutorial
https://gist.github.com/texasdave2/8f4ce19a467180b6e3a02d7be0c765e7
https://levelup.gitconnected.com/kubernetes-cka-example-questions-practical-challenge-86318d85b4d
https://github.com/devopshubproject/cka-lab
https://github.com/stretchcloud/cka-lab-practice

## exam pages
documentation that you can use during the exam
- https://oreil.ly/w0vib --> https://kubernetes.io/docs/home/
- https://oreil.ly/XLYLj --> https://github.com/kubernetes/
- https://oreil.ly/1sr3B --> https://kubernetes.io/blog/

## tools
- kubectl command-line tool
- kubernetes cluster maintaince tool
  - kubeadm
  - etcdctl
- vi and vim

## tips
```bash
kubectl config set-context <context-of-question> --namespace=<namespace-of-question>
# setup alias
alias k=kubectl
k version
# kubectl bash auto-completion on linux
## check if installed
type _init_completion
## if not installed
apt-get install bash-completion
source <(kubectl completion bash) # for current session
echo "source <(kubectl completion bash)" >> ~/.bashrc # add autocomplete permanently to your bash shell. 
# tricks
kubectl describe pod <pod-name> | grep -C 10 "author=John Doe"
kubectl get pods -o yaml | grep -C 5 lables:
kubectl create --help
kubectl explain pods.spec
```

## Cluster Architecture, Installation & Configuration (25%)
### get into the minikube cluster
```bash
# ssh into the minikube main node
minikube ssh
minikube ssh -node=minikube

### creating a single control-plane sign on user for the cluster
```bash
mkdir cert && cd cert
# generate a private key and certificate signing request (CSR) for the user
openssl genrsa -out johndoe.key 2048
# generate a certificate signing request (CSR) for the user
openssl req -new -key johndoe.key -out johndoe.csr -subj "/CN=johndoe/O=cka-study-guide"
# sign the csr with cka ca, the ca can usually be found in /etc/kubernetes/pki and needs to contain the ca.crt and ca.key files. we are going to use minikube here
openssl x509 -req -in johndoe.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out johndoe.crt -days 500
# create the user in kubernetes by setting a user entry in kubeconfig for johndoe. Point to the CRT and key file. Set a context entry for the johndoe
kubectl config set-credentials johndoe --client-certificate=johndoe.crt --client-key=johndoe.key
kubectl config set-context johndoe-context --cluster=minikube --user=johndoe
```
- Manage role based access control (RBAC)
```bash
kubectl create serviceaccount build-bot
kubectl get serviceaccount build-bot -o yaml
kubectl describe serviceaccount build-bot
kubectl get secrets
kubectl run build-observer --image=alpine --serviceaccount=build-bot --restart=Never
```
### create rolebinding
```bash
kubectl create role read-only --verb=list,get,watach --resource=pods,services,deployments
kubectl create rolebinding read-only-binding --role=read-only --user=johndoe
kubectl get rolebinding read-only-binding -o yaml
kubectl describe rolebinding read-only-binding
```
```bash
kubectl config current-context
kubectl create deployment myapp --image=nginx --port 80 --replicas=2
kubectl config use-context johndoe-context
kubectl get deployments
kubectl get replicasets
kubectl delete deployment myapp

kubectl auth can-i --list --as johndoe
kubectl auth can-i list pods --as johndoe
```
or 
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: build-observer
spec:
  serviceAccountName: build-bot
  containers:
  - name: build-observer
    image: alpine
    command: ["/bin/sh"]
```

- Use Kubeadm to install a basic cluster
- upgrading a version of Kubernetes cluster with Kubeadm
- backing up and restoring etcd with etcdctl
- understanding a highly available Kubernetes cluster

### Manage role based access control (RBAC) (page 15)
- https://kubernetes.io/docs/reference/access-authn-authz/rbac/

#### table user accounts and groups
Authentication strategies for managing RBAC subjects
- this will be skipped as they are already been setup
| authentication strategy | Description |
| --- | --- |
| X509 Client Certs | Uses an OpenSSL client certificate to authenticate the user. |
| Basic authentication | Uses a username and password to authenticate the user. |
| Bearer tokens | Uses a bearer token (a unique string) to authenticate the user. |

- create service account
```bash
kubectl create serviceaccount build-bot
```
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-bot
```

## workloads and scheduling (15%)

```bash
kubectl create deployment app-cache --image=memcached:memcached:1.6.8 --replicas=4
# change the replicas nubmer to 3
kubectl scale deployment app-cache --replicas=3
# rolling out to a new version
kubectl set image deployment app-cache memcached=memcached:1.6.10 --record
kubectl rollout status deployment app-cache
kubectl rollout history deployment app-cache
kubectl rollout undo deployment app-cache --to-revision=1
kubectl annotate deployment app-cache kubernetes.io/change-cause="replia set to 3"
```

### manually scaling a statefulset
####  yaml manifest of a statefulset and service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: default
  labels:
    app: redis
spec:
  ports:
  - port: 6379
    protocol: TCP
  selector:
    app: redis
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: default
spec:
  selector:
    matchLabels:
      app: redis
  serviceName: "redis"
  replicas: 3
  template:
    metadata:
      labels:
        app: redis
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: redis
        image: redis:5.0.4
        ports:
        - containerPort: 6379
          name: redis
        volumeMounts:
        - name: data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
```bash
kubectl apply -f redis.yaml
kubectl scale statefulset redis --replicas=5 
```


## Services and Networking (20%)

## Storage (10%)

## Troubleshooting (30%)