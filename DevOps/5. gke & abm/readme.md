## Helm Deployment
```bash
# the difference between anthos and gke is that anthos doesn't has --region flag
gcloud config set core/custom_ca_certs_file /usr/local/lib/python3.9/site-packages/certifi/cacert.pem
gcloud container fleet memberships get-credentials {cluster_name} --region {region} --project {project_id}
kubectl get all -n {namespace}
```

## download the helm chart from nexus
```bash
# download the helm chart from nexus, and untar it
helm pull {chart_url} --username '{username}' --password '{password}' --untar --untardir {dir}
```

## helm uninstall
```bash
helm uninstall {release_name} --namespace {namespace} --dry-run {helm_switches}
helm uninstall {release_name} --namespace {namespace} {helm_switches}
```

## helm upgrade

```bash
helm upgrade {release_name} {temp_workflow_dir}/{chart_name} --namespace {namespace} --values {temp_workflow_dir}/values.yml --dry-run --install {helm_switches}
helm upgrade {release_name} {temp_workflow_dir}/{chart_name} --namespace {namespace} --values {temp_workflow_dir}/values.yml --install {helm_switches}
```

#### additional helm upgrade switches
- '--atomic' : if the upgrade fails, roll back to the previous state
- '--force' : force resource update through delete/recreate if needed

## helm uninstall
```bash
helm uninstall {release_name} --namespace {namespace} --dry-run {helm_switches}
```
## debug output
- helm template is used to render charts locally and displays the output in the terminal
```bash
helm template {release_name} {temp_workflow_dir}/{chart_name}
```
- kubectl print out events
```bash
kubectl get events -namespace {namespace} --sort-by=.metadata.creationTimestamp -o json
```
- print out helm revision history
```bash
helm history {release_name} --namespace {namespace}
```

