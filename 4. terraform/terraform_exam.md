## terraform file and directory structure
- .terraform.lock.hcl is the file that contains the exact version of the provider, it is for tracking the exact version of the provider

```text
my-terraform-project/
|-- main.tf
|-- variables.tf
|-- outputs.tf
|-- provider.tf
|-- terraform.tfvars
|-- .gitignore
|-- terraform.lock.hcl
|-- backend.tf
|-- modules/
|   |-- module1/
|   |   |-- main.tf
|   |   |-- variables.tf
|   |   |-- outputs.tf
|   |   |-- ...
|   |-- module2/
|   |   |-- main.tf
|   |   |-- variables.tf
|   |   |-- outputs.tf
|   |   |-- ...
|-- environments/
|   |-- dev/
|   |   |-- main.tf
|   |   |-- variables.tf
|   |   |-- outputs.tf
|   |   |-- terraform.tfvars
|   |-- prod/
|   |   |-- main.tf
|   |   |-- variables.tf
|   |   |-- outputs.tf
|   |   |-- terraform.tfvars

```
## Terraform provisioners
- built-in provisioners: file, local-exec, remote-exec
  - local-exec is for local script execution
  - remote-exec is for executing code on remote
  - file is for copying files to the remote machine 
- 65 Terraform provisioner must be nested inside a resource configuration block
- 114 terraform provisioners can be added to any resource block
- terraform provisioners are the last resort for configuration management 
- 290 if a terraform creation-time provisioner fails, terraform will mark the resource as tainted
#### terraform provisioner file
```terraform
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  provisioner "file" {
    source      = "index.html"
    destination = "/var/www/html/index.html"
  }
}
```
#### terraform provisioner local-exec
```terraform
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  provisioner "local-exec" {
    command = "echo ${aws_instance.web_server.public_ip} > ip_address.txt"
  }
}
```

#### terraform provisioner remote-exec
```terraform
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  provisioner "remote-exec" {
    inline = [
      "sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2",
      "sudo yum -y install httpd",
      "sudo systemctl start httpd",
      "sudo systemctl enable httpd",
      "sudo usermod -a -G apache ec2-user",
      "sudo chown -R ec2-user:apache /var/www",
      "sudo chmod 2775 /var/www",
      "find /var/www -type d -exec sudo chmod 2775 {} +",
      "find /var/www -type f -exec sudo chmod 0664 {} +",
      "echo '<h1>Hello World from $(hostname -f)</h1>' > /var/www/html/index.html"
    ]
  }
}
```
## terraform providers
- 11 is not required to have a provider for every Terraform configuration
  - 103 Outside of the required_providers block, terraform configurations always refer to providers by their local names
  - terraform provisioners that require authentication can use the connection block
- 105 terraform providers doesn't have to be installed from the internet every time: it can get from terraform registry, local mirror, or cache
- 111 terraform provider is not responsible for provisioning infrastructure in multiple clouds
- 156 terraform provider version
  - version = "~> 2.0" to allow the rightmost digit to change
  - version = "2.0" to get the exact version of the provider
  - version = ">= 2.0" to get any version of the provider that is greater or equal to 2.0
#### terraform provider block
```terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 2.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
  version = "~> 2.0"
}

provider "google" {
  credentials = file("account.json")
  project     = "my-project"
}
# aws prefix is the local name of the provider
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"


  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("id_rsa")
  }
}
# google prefix is the local name of the provider
resource "google_compute_instance" "example" {
  name         = "example-instance"
  machine_type = "n1-standard-1"
}

```
- 179 reference to multi-provider situation
```
provider "aws" {
  region = "us-west-2"
}

provider "aws" {
  alias  = "west"
  region = "us-east-1"
}

resource "aws_instance" "example" {
  provider = aws.west
  # ...
}

```
## terraform dynamic blocks
- 167 terraform dynamic block
  - Dynamic block in Terraform is used to construct nested configuration blocks dynamically based on a collection of values
#### terraform dynamic block example
```terraform
 resource "aws_security_group" "example" {
  name = "example"

  dynamic "ingress" {
    for_each = var.cidr_blocks
    content {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }
}
```

## terraform password management
- 87 securities: for password
  - Terraform provides provider (vault)
  - environment variables with -var method on the command line, this will keep the value out of the configuration and state
  - mark the variable as sensitive still in the state file, but you can do lifecycle block to prevent it from being written to the state file
  - Terraform provider will not in the state file
  - terraform -var flag will keep the value out of the configuration and state file
  - There is no secure string in Terraform
## terraform format
- 220 `terraform fmt`
  - `terraform fmt -check` to check if the files are formatted correctly, `terraform fmt -check -recursive` to check all the files in the directory
  - `terraform fmt -recursive` to format all the files in the directory
  - `terraform fmt` to format the files in the current directory 
## terraform putputs
- 188 example of output
#### terraform output from its own instance
```terraform
output "instance_ip_addr" {
  value = aws_instance.example.private_ip
}
```
#### terraform output from its parent module

```terraform
output "instance_ip_addr" {
  value = module.my_network.vnet_id
}
```
#### example of ${} ( or interpolation syntax)
```terraform
output "instance_ip_addr" {
  value = "The IP address is ${aws_instance.example.private_ip}"
}
```
## terraform variables types
- String, Number, List, Map, Bool, Object, Tuple
## terraform rename
- 231 terraform mv for renaming
  - terraform mv aws_security_group.htp aws_security_group.http
```
resource "aws_security_group" "htp" {
  name = "htp"
  # ...
}

# to 
resource "aws_security_group" "http" {
  name = "http"
  # ...
}
```
## terraform workspaces
- 104 `terraform workspace list` to list all the workspaces
- Type of terraform Backend
  - Local file system
  - Remote, s3, etcd, artifactory, etc
  - Enhanced, terraform cloud, terraform enterprise
## splat expression
- 77 var.list[*].Id or [for o in var.list:o.id]
  - aws_instance.exxample.ebs_block_device[*].volume_id or aws_instance.exxample.ebs_block_device.*.volume_id
- 243 splat expression only works for list, not map
  - for each generates a map, not a list 
## terraform state
- 32 Terraform does not process the configuration file while running refresh
  - Whenever possible, avoid using the refresh command explicitly
  - as terraform refresh will be run automatically when you run terraform plan or terraform apply
  - it is only for backword compatibility
  - terraform refresh will update state file with the real-world infrastructure
- terraform plan and terraform apply will run terraform refresh automatically with the state file
## terraform sentinel policy
- 189 Sentinel policy as a code framework for integrates with terraform enterprise to enforce policies
- 266 sentinel policy is applied before the apply phase

## terraform dependency
- 275 use terraform graph to see the dependency

## terraform init
- 247 terraform init can migrate the state file to the cloud
- 280 terraform init, the configuration is search for module blocks, and the source code for referenced modules is retrieved from the locations specified in the source argument

## terraform env
- 294 terraform env is used to switch between different work environments
  
## terraform state file
- 120 terraform.tfstate is the default file where terraform stores the state
  - 25 description is not saved in the state file
  - terraform plan, terraform apply, terraform refresh will update the state file


## Golden Images and System Base Image
- 23 golden images describe the base image of the system

## Terraform Commands and Functions
- 40 `slice` is not a valid string function in Terraform
- 54 Terraform does not require Go runtime as they are in binary
- 56 `force-unlock` when auto-unlock failed
- 61 `terraform plan -destroy` and `terraform destroy`
- 119 `terraform plan -out=FILENAME` to save the plan to a file
- 140 `terraform plan -target=resource.name` when resource is deleted outside of Terraform, in the console

## Terraform Configuration
- 63 `servers = var.num_servers`
- 79 It is possible to declare a variable without any of the given arguments
- 102 Terraform block to specify the backend
- 234 Terraform variables are not stored in the state file

## Debugging and Logging in Terraform
- 99 `tf_log` to set the debug level
  - `tf_log` levels: TRACE, DEBUG, INFO, WARN, ERROR
  - Also needs `tf_log_path` to save the log to a file; otherwise, they just print to stderr

## Terraform Style and Best Practices
- 169 Terraform style
  - Indent 2 spaces for each nested block
  - When multiple arguments with single-line values, align the equal signs

## Provider and Versioning in Terraform
- 217 The release tags in the associated GitHub repo are the way to specify the version of the provider

