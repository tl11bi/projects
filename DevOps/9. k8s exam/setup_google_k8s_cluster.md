# Self-managed Kubernetes in Google Compute Engine (GCE)

## Big Picture

Use Calico with a self-managed Kubernetes cluster in Google Compute Engine (GCE). Managing your own Kubernetes cluster provides flexibility in configuring Calico and Kubernetes. Calico offers flexible networking and "run-anywhere" security enforcement with native Linux kernel performance and true cloud-native scalability.

## Concepts

- **kubeadm:** Cluster management tool for installing Kubernetes.
- **Before you begin:** Install and configure Google Cloud CLI tools.

## How to

### kubeadm for Calico networking and network policy

1. **Create Cloud Resources:**
   - At least one VM for the control plane node and one or more worker nodes.
   - Consider using a dedicated infrastructure management tool like Terraform.

2. **Create VPC and Subnet:**
   ```bash
   gcloud compute networks create example-k8s --subnet-mode custom
   gcloud compute networks subnets create k8s-nodes \
       --region us-east1 \
       --network example-k8s \
       --range 10.240.0.0/24
   ```

3. **Create Firewall Rules:**
   ```bash
   gcloud compute firewall-rules create example-k8s-allow-internal \
       --allow tcp,udp,icmp,ipip \
       --network example-k8s \
       --source-ranges 10.240.0.0/24

   gcloud compute firewall-rules create example-k8s-allow-external \
       --allow tcp:22,tcp:6443,icmp \
       --network example-k8s \
       --source-ranges 0.0.0.0/0
   ```

4. **Create VM Instances:**
   ```bash
   gcloud compute instances create controller \
       --async \
       --boot-disk-size 200GB \
       --can-ip-forward \
       --image-family ubuntu-2204-lts \
       --image-project ubuntu-os-cloud \
       --machine-type n1-standard-2 \
       --private-network-ip 10.240.0.11 \
       --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
       --subnet k8s-nodes \
       --zone us-east1-c \
       --tags example-k8s,controller

   for i in 0 1 2; do
       gcloud compute instances create worker-${i} \
       --async \
       --boot-disk-size 200GB \
       --can-ip-forward \
       --image-family ubuntu-2204-lts \
       --image-project ubuntu-os-cloud \
       --machine-type n1-standard-2 \
       --private-network-ip 10.240.0.2${i} \
       --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
       --subnet k8s-nodes \
       --zone us-east1-c \
       --tags example-k8s,worker
   done
   ```

5. **Install Docker:**
   - On each VM, run:
     ```bash
     sudo apt update
     sudo apt install -y docker.io
     sudo systemctl enable docker.service
     sudo apt install -y apt-transport-https curl
     ```

6. **Install Kubernetes and Create Cluster:**
   - Install kubeadm, kubelet, and kubectl on each node.
    ```bash
    sudo apt-get update && sudo apt-get install -y apt-transport-https curl
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/kubernetes-archive-keyring.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update
    sudo apt-get install -y containerd kubelet kubeadm kubectl
    sudo apt-mark hold kubelet kubeadm kubectl
    ```
  - Connect to the controller VM, and run the following command

```bash
sudo kubeadm reset
sudo ipvsadm --clear
sudo kubeadm join 10.240.0.11:6443 --token 1xkvn2.p44etnvvxs1vv3d8 \
        --discovery-token-ca-cert-hash sha256:abb93c041d2242910ba54f79b05fefbae8fff129ab2c8d1fa658c44c5aea984a
sudo kubeadm init --pod-network-cidr 192.168.0.0/16
```

1. **Set up kubectl for Ubuntu User:**
   - Connect to the controller VM and run the provided commands.
```bash
rm -rf $HOME/.kube
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
```bash
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version= \
    $(kubectl version | base64 | tr -d '\n')"
```

2. **Join Worker Nodes to Controller:**
   - Run the provided join command on each worker node.
    ```bash
    kubeadm join 10.240.0.11:6443 --token ar77y2.7274jxuumt8vhhvw \
        --discovery-token-ca-cert-hash sha256:d913182b646660c7be5bd76c1b9e9fa3e613ed9c18ef36ad0d475f8f7c887331 
    ```

1.  **Verify Node Status:**
    - Run the following command on the controller node:
        ```bash
        kubectl get nodes
        ```
    - Output should indicate the status of controller and worker nodes.
        ```text
        NAME         STATUS     ROLES    AGE     VERSION
        controller   NotReady   master   5m49s   v1.17.2
        worker-0     NotReady   <none>   3m38s   v1.17.2
        worker-1     NotReady   <none>   3m7s    v1.17.2
        worker-2     NotReady   <none>   5s      v1.17.2
        ```

## upgrade
    
```bash
sudo apt update
sudo apt-cache madison kubeadm
sudo apt-mark unhold kubeadm && sudo apt-get update && sudo apt-get install \
-y kubeadm=1.19.0-00 && sudo apt-mark hold kubeadm