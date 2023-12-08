## aks deployment
```bash
az aks get-credentials --resource-group {resource_group} --name {cluster_name} --subscription {subscription_id}
kubelogin --version
kubelogin convert-kubeconfig -l spn
kubectl get all -n {namespace}
```
- kubelogin is a credential plugin that allows you use azure ad to access aks cluster

```bash
TOKEN_NAME = 'kubectl get serviceaccount {service_account_name} -n {namespace} -o jsonpath={{.secrets[0].name}}'
TOKEN = 'kubectl get secret {secret_name} -n {namespace} -o jsonpath={{.data.token}}' | base64 --decode
kubectl config set-credentials {cluster_name} --token={token}
kubectl config set-context {cluster_name} --cluster={cluster_name} --user={cluster_name}
```

Certainly! Below are examples and explanations for each Helm command:

### 1. `completion`
- **Example:**
  ```bash
  helm completion bash
  ```

- **Explanation:**
  - This command generates shell autocompletion scripts for the specified shell (in this case, Bash). Running the generated script enhances the Helm command-line interface by enabling autocompletion of commands, flags, and arguments.

### 2. `create`
- **Example:**
  ```bash
  helm create mychart
  ```

- **Explanation:**
  - Creates a new Helm chart named `mychart` in the current directory. This command initializes the basic directory structure and files needed for a Helm chart.

### 3. `dependency`
- **Example:**
  ```bash
  helm dependency update mychart
  ```

- **Explanation:**
  - Manages a chart's dependencies. This specific example updates the dependencies of the chart named `mychart`. Dependencies are defined in the `requirements.yaml` file of the chart.

### 4. `env`
- **Example:**
  ```bash
  helm env
  ```

- **Explanation:**
  - Provides information about the Helm client environment, including the version of Helm and Kubernetes, the location of the Helm home directory, and the active Kubernetes context.

### 5. `get`
- **Example:**
  ```bash
  helm get values myrelease
  ```

- **Explanation:**
  - Downloads extended information about a named release (`myrelease` in this case). This command can retrieve various details such as values, notes, hooks, and the rendered manifest of a release.

### 6. `help`
- **Example:**
  ```bash
  helm help
  ```

- **Explanation:**
  - Provides help and information about Helm commands. Running `helm help` without any specific command shows the general help menu, while `helm help <command>` provides detailed information about a specific command.

### 7. `history`
- **Example:**
  ```bash
  helm history myrelease
  ```

- **Explanation:**
  - Fetches the release history of a Helm release (`myrelease` in this case). It shows a revision history with timestamps, user information, and any rollback information.

### 8. `install`
- **Example:**
  ```bash
  helm install myrelease mychart
  ```

- **Explanation:**
  - Installs a Helm chart named `mychart` and creates a release named `myrelease`. This command deploys the chart to the Kubernetes cluster.

### 9. `lint`
- **Example:**
  ```bash
  helm lint mychart
  ```

- **Explanation:**
  - Examines a Helm chart (`mychart` in this case) for possible issues, ensuring that the chart follows best practices and is well-structured.

### 10. `list`
- **Example:**
  ```bash
  helm list
  ```

- **Explanation:**
  - Lists all releases deployed using Helm, showing information such as release name, chart name, status, and revision.

### 11. `package`
- **Example:**
  ```bash
  helm package mychart
  ```

- **Explanation:**
  - Packages a Helm chart directory (`mychart` in this case) into a chart archive (.tgz file). The packaged chart can be distributed and installed without needing access to the original chart directory.

### 12. `plugin`
- **Example:**
  ```bash
  helm plugin install https://example.com/my-plugin.tar.gz
  ```

- **Explanation:**
  - Installs, lists, or uninstalls Helm plugins. This example installs a Helm plugin from a remote URL.

### 13. `pull`
- **Example:**
  ```bash
  helm pull stable/mysql
  ```

- **Explanation:**
  - Downloads a Helm chart from a repository (`stable/mysql` in this case) and optionally unpacks it into the local directory.

### 14. `push`
- **Example:**
  ```bash
  helm push mychart/ myrepo/
  ```

- **Explanation:**
  - Pushes a Helm chart to a remote repository (`myrepo/` in this case).

### 15. `registry`
- **Example:**
  ```bash
  helm registry login myregistry
  ```

- **Explanation:**
  - Logs in to or logs out from a container registry (`myregistry` in this case).

### 16. `repo`
- **Example:**
  ```bash
  helm repo add myrepo https://charts.example.com
  ```

- **Explanation:**
  - Adds, lists, removes, updates, and indexes Helm chart repositories. This example adds a repository named `myrepo` with the specified URL.

### 17. `rollback`
- **Example:**
  ```bash
  helm rollback myrelease 2
  ```

- **Explanation:**
  - Rolls back a Helm release (`myrelease` in this case) to a previous revision (revision 2 in this example).

### 18. `search`
- **Example:**
  ```bash
  helm search repo mysql
  ```

- **Explanation:**
  - Searches for a keyword (`mysql` in this case) in Helm chart repositories.

### 19. `show`
- **Example:**
  ```bash
  helm show values mychart
  ```

- **Explanation:**
  - Shows information about a Helm chart (`mychart` in this case), such as the values, README, and other metadata.

### 20. `status`
- **Example:**
  ```bash
  helm status myrelease
  ```

- **Explanation:**
  - Displays the status of a named release (`myrelease` in this case), showing details about deployed resources, revisions, and notes.

### 21. `template`
- **Example:**
  ```bash
  helm template myrelease mychart
  ```

- **Explanation:**
  - Locally renders templates for a Helm chart (`mychart` in this case) without installing it. Useful for previewing the generated Kubernetes manifests.

These examples cover various Helm commands and their typical use cases in Helm chart development and deployment workflows.