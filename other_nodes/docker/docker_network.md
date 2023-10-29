# Advantages of Docker Networking

Some of the major benefits of using Docker Networking are:

- They share a single operating system and maintain containers in an isolated environment.
- It requires fewer OS instances to run the workload.
- It helps in the fast delivery of software.
- It helps in application portability.

## How Does Docker Networking Work?

For a more in-depth understanding, let’s have a look at how Docker Networking works. Below is a diagrammatic representation of the Docker Networking workflow:

![Docker Networking Workflow](insert_image_url_here)

**Docker File** builds the Docker Image.

**Docker Image** is a template with instructions, which is used to build Docker Containers.

Docker has its own cloud-based registry called **Docker Hub**, where users store and distribute container images.

**Docker Container** is an executable package of an application and its dependencies together.

Functionalities of the different components:

- **Docker File** has the responsibility of building a Docker Image using the build command.
- **Docker Image** contains all the project’s code.
- Using Docker Image, any user can run the code to create Docker Containers.
- Once Docker Image is built, it’s either uploaded in a registry or a Docker Hub.

Now that you know how Docker networking works, it is important to understand the container network model.

## Container Network Model

This concept will help you to build and deploy your applications in the Docker tool.

Let’s discuss the components of the container network model in detail:

1. **Network Sandbox**: It is an isolated sandbox that holds the network configuration of containers. Sandbox is created when a user requests to generate an endpoint on the network.

2. **Endpoints**: It can have several endpoints in a network, as it represents a container’s network configuration such as IP-address, MAC-address, DNS, etc. The endpoint establishes the connectivity for container services (within a network) with other services. It helps in providing connectivity among the endpoints that belong to the same network and isolate them from the rest. So, whenever a network is created, or configuration is changed, the corresponding Network Driver will be notified with an event.

3. **Docker Engine**: It is the base engine installed on your host machine to build and run containers using Docker components and services. Its task is to manage the network with multiple drivers. It provides the entry-point into libnetwork to maintain networks, whereas libnetwork supports multiple virtual drivers.

So, those were the key concepts in the container network model. Going ahead, let’s have a look at the network drivers.

## Network Drivers

Docker supports networking for its containers via network drivers. These drivers have several network drivers.

In this article, we will be discussing how to connect your containers with suitable network drivers. The network drivers used in Docker are below:

- **Bridge**: It is a private default network created on the host. Containers linked to this network have an internal IP address through which they communicate with each other easily. The Docker server (daemon) creates a virtual ethernet bridge docker0 that operates automatically, by delivering packets among various network interfaces. These are widely used when applications are executed in a standalone container.

- **Host**: It is a public network. It utilizes the host’s IP address and TCP port space to display the services running inside the container. It effectively disables network isolation between the docker host and the docker containers, which means using this network driver a user will be unable to run multiple containers on the same host.

- **None**: In this network driver, the Docker containers will neither have any access to external networks nor will it be able to communicate with other containers. This option is used when a user wants to disable the networking access to a container. In simple terms, None is called a loopback interface, which means it has no external network interfaces.

- **Overlay**: This is utilized for creating an internal private network to the Docker nodes in the Docker swarm cluster. (Note: Docker Swarm is a service for containers which facilitates developer teams to build and manage a cluster of swarm nodes within the Docker platform.) It is an important network driver in Docker networking. It helps in providing the interaction between the stand-alone container and the Docker swarm service.

- **Macvlan**: It simplifies the communication process between containers. This network assigns a MAC address to the Docker container. With this Mac address, the Docker server (daemon) routes the network traffic to a router. (Note: Docker Daemon is a server which interacts with the operating system and performs all kinds of services.) It is suitable when a user wants to directly connect the container to the physical network rather than the Docker host.

## Basic Docker Networking Commands

Let’s discuss some of the important networking commands that are widely used by developer teams.

- **List down the Networks associated with Docker**
  ```
  docker network ls
  ```
  The above command displays all the networks available on the Docker ecosystem.

- **Connect a Running Container to a Network**
  ```bash
  $ docker network connect multi-host-network container
  ```
  In the command shown above, you can also use the docker network option to start a container and immediately connect it to multiple host networks.

- **Specify the IP Address that you want to assign to the Container**
  ```bash
  $ docker network connect --IP 10.10.36.122 multi-host-network container
  ```
  In the above command, you can specify the IP address (for example, 10.10.36.122) that you want to assign to the container interface.

- **Create a Network alias for a Container**
  ```bash
  $ docker network connect --alias db --alias mysql multi-host-network container2
  ```
  In the above command, we have specified aliases to define new commands and to rectify incorrect input.

- **Disconnect a Container from a Network**
  ```bash
  $ docker network disconnect multi-host-network container1
  ```
  In the above command, the disconnect option is used to stop the running docker containers on multiple host network.

- **Remove a Network**
  ```bash
  $ docker network rm network_name
  ```
  In the

 above command, the rm option is used to remove a network from the Docker ecosystem.

- **Remove Multiple Networks**
  ```bash
  $ docker network rm 3695c422697f network_name
  ```
  The above command can be used when a user wants to remove multiple networks at a time.

- **Remove all Unused Networks**
  ```bash
  $ docker network prune
  ```
  The above ‘prune’ command can be used when a user wants to remove all unused networks at a time.
```
