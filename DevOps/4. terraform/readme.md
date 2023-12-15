## main commands
- 'terraform init': initialize a workspace
- 'terraform plan': show changes required by the current configuration
- 'terraform apply': create or update infrastructure
- 'terraform destroy': destroy previously-created infrastructure
- 'terraform validate': check whether the configuration is valid

## other commands
- 'terraform console': try Terraform expressions at an interactive command prompt
- 'terraform fmt': reformat your configuration in the standard style
- 'terraform force-unlock': release a stuck lock on the current workspace
- 'terraform get': install or upgrade remote Terraform modules
- 'terraform graph': generate a Graphviz graph of the steps in an operation
- 'terraform import': associate existing infrastructure with a Terraform resource
- 'terraform login': obtain and save credentials for a remote host
- 'terraform logout': remove locally-stored credentials for a remote host
- 'terraform providers': show the providers required for this configuration
- 'terraform refresh': update the state to match remote systems
- 'terraform show': show the current state or a saved plan
- 'terraform state': advanced state management
- 'terraform taint': mark a resource instance as not fully functional
- 'terraform test': execute integration tests for Terraform modules
- 'terraform untaint': remove the 'tainted' state from a resource instance
- 'terraform version': show the current Terraform version
- 'terraform workspace': workspace management

## terraform folder structure
```text
|_ main.tf
|_ variables.tf
|_ outputs.tf
|_ terraform.tfvars
|_ provider.tf
|_ terraform.tfstate
|_ terraform.tfstate.backup
|_ .terraform
    |_ plugins
        |_ linux_amd64
            |_ lock.json
            |_ terraform-provider-aws_v2.70.0_x4
            |_ terraform-provider-null_v2.1.2_x4
            |_ terraform-provider-random_v3.1.0_x4
            |_ terraform-provider-template_v2.2.0_x4
|_ modules
    |_ moduleA
        |_ main.tf
        |_ variables.tf
        |_ outputs.tf
        |_ provider.tf
...
```
