## chapter 2: Cluster Architecture, Installation & Configuration (25%)
### creating and managing a kubernetes cluster
- bootstrapping a control plane node

```bash
# the following command will create a single control plane cluster, the pod network cidr is the cidr of the pod network, the apiserver-advertise-address is the ip address of the control plane node
sudo kubeadm init --pod-network-cidr 172.18.0.1/16 --apiserver-advertise-address 10.138.0.8
sudo kubeadm reset
sudo ipvsadm --clear
sudo rm /etc/apt/sources.list.d/kubernetes.list

```

```
sudo rm /etc/containerd/config.toml
sudo systemctl restart containerd

```
- bootstrapping worker nodes
- bootstrapping kubernetes networking

https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-public-cloud/gce



