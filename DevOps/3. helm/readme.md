## basic Helm commands
```bash
# Set Google Cloud configuration
gcloud config set core/custom_ca_certs_file /usr/local/lib/python3.9/site-packages/certifi/cacert.pem

# Get credentials for GKE or Anthos cluster
gcloud container fleet memberships get-credentials {cluster_name} --region {region} --project {project_id}
kubectl get all -n {namespace}

# Download Helm chart from Nexus
helm pull {chart_url} --username '{username}' --password '{password}' --untar --untardir {dir}

# Helm uninstall
helm uninstall {release_name} --namespace {namespace} --dry-run {helm_switches}
helm uninstall {release_name} --namespace {namespace} {helm_switches}

# Helm upgrade
helm upgrade {release_name} {temp_workflow_dir}/{chart_name} --namespace {namespace} --values {temp_workflow_dir}/values.yml --dry-run --install {helm_switches}
helm upgrade {release_name} {temp_workflow_dir}/{chart_name} --namespace {namespace} --values {temp_workflow_dir}/values.yml --install {helm_switches}

# Additional Helm upgrade switches
# '--atomic': Roll back to the previous state if the upgrade fails
# '--force': Force resource update through delete/recreate if needed

# Debug output
# Helm template to render charts locally
helm template {release_name} {temp_workflow_dir}/{chart_name}

# Kubectl print out events
kubectl get events -namespace {namespace} --sort-by=.metadata.creationTimestamp -o json

# Print out Helm revision history
helm history {release_name} --namespace {namespace}

# AKS deployment
az aks get-credentials --resource-group {resource_group} --name {cluster_name} --subscription {subscription_id}
kubelogin --version
kubelogin convert-kubeconfig -l spn
kubectl get all -n {namespace}

# Kubelogin is a credential plugin that allows using Azure AD to access AKS cluster
TOKEN_NAME='kubectl get serviceaccount {service_account_name} -n {namespace} -o jsonpath={{.secrets[0].name}}'
TOKEN='kubectl get secret {secret_name} -n {namespace} -o jsonpath={{.data.token}}' | base64 --decode
kubectl config set-credentials {cluster_name} --token={token}
kubectl config set-context {cluster_name} --cluster={cluster_name} --user={cluster_name}

# Basic Helm commands for chart creation and management
# helm create <chart_name>
helm create helloworld

# Basic Helm chart structure output
# helloworld/
# │   ├── ingress.yaml
# │   ├── service.yaml
# │   ├── serviceaccount.yaml
# └── values.yaml

# Install Helm charts
helm install myhelloworld ./helloworld
helm install my-python-flask-api ./python-flask-api

# Helm install dry-run
helm install myhelloworld ./helloworld --dry-run --debug

# Helm lint
helm lint ./helloworld

# Helm template (generate YAML locally)
helm template ./helloworld

# Delete Helm charts
helm delete myhelloworld
helm uninstall myhelloworld

# List all Helm charts
helm list -a

# Upgrade Helm chart after modification
helm upgrade myhelloworld ./helloworld

# Rollback Helm chart
helm rollback myhelloworld 2
```

## helm chart
Helm doesn't support for a multi-module or layered architecture. helm is designed to be a single chart per application.

#### Multiple Charts in a Repository:

Create separate Helm charts for each module or layer.
Organize these charts in a single repository or multiple repositories.
Use dependencies between charts if there are dependencies between modules.

#### Nested Charts:

Helm supports the concept of nested charts, where one chart includes another.
You can create a main chart that includes or depends on sub-charts for each module or layer.

#### Helm Chart Templates Organization:

Inside a single Helm chart, organize your templates into subdirectories representing different modules or layers.
Use labels and annotations to categorize resources and apply different configurations based on labels.
Values Files for Different Modules:

#### Use separate values files for each module or layer.
Customize the values files for each environment or use case.

```text
my-multimodule-chart/
├── charts/
│   ├── module1/
│   │   ├── charts/ (if module1 has dependencies)
│   │   ├── templates/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── values.yaml
│   └── module2/
│       ├── charts/ (if module2 has dependencies)
│       ├── templates/
│       │   ├── deployment.yaml
│       │   └── service.yaml
│       └── values.yaml
├── templates/
│   ├── _helpers.tpl
│   └── ingress.yaml
└── values.yaml
```
