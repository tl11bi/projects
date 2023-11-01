# Docker Interview Questions

## Basic Docker Interview Questions for Beginners

1. **What is Docker?**
   - Docker is an open-source containerization platform used to automate the deployment of applications with lightweight, portable containers.

2. **What are Docker's most notable features?**
   - Features include application agility, developer productivity, easy modeling, operational efficiencies, placement and affinity, and version control.

3. **Why should anyone use Docker?**
   - Docker offers efficient setup, detailed application lifecycle description, simple configuration, well-documented, and can run on different systems.

4. **What are the downsides of Docker?**
   - Downsides include a lack of storage options, less-than-ideal monitoring, no automatic rescheduling of inactive nodes, and complicated automatic horizontal scaling setup.

5. **Name and explain the various Docker components.**
   - Components are Docker Client, Docker Host, and Registry, which store Docker images.

6. **What is a container?**
   - A container is a bundled application with dependencies and configuration files, sharing the same OS kernel, allowing it to run on different systems or the cloud.

7. **Explain virtualization.**
   - Virtualization uses software (Hypervisor) to create virtual versions of resources, such as servers or applications.

8. **What's the difference between virtualization and containerization?**
   - Virtualization abstracts physical machines, while containerization abstracts applications.

9. **Describe a Docker container's lifecycle.**
   - Common steps include create, run, pause, unpause, start, stop, restart, kill, and destroy.

## Intermediate Docker Interview Questions

10. **Name essential Docker commands and their functions.**
    - Commands include build, commit, create, daemon, kill, etc.

11. **What are Docker object labels?**
    - Labels apply metadata to Docker objects like containers, images, and more.

12. **How do you find stored Docker volumes?**
    - Use the command `/var/lib/docker/volumes`.

13. **How do you check Docker Client and Server versions?**
    - Run `docker version` to get version information.

14. **How to create a container from an image?**
    - Use `docker run -it -d <image_name>` to pull an image and create a container.

15. **How to stop a container?**
    - Use `docker stop <container_name>` to stop a container.

16. **How to list running containers?**
    - Use `docker ps` to list running containers.

17. **What's involved in scaling a Docker container?**
    - Docker containers can be scaled as needed, from a few to millions, with access to required resources.

18. **What is the Docker system prune command?**
    - `docker system prune` removes stopped containers, unused networks, build caches, and dangling images.

## Advanced Docker Interview Questions for Experienced Professionals

19. **List some advanced Docker commands and their functions.**
    - Commands like `docker info`, `docker pull`, `docker stats`, and `docker images` provide system-wide information and manage images.

20. **Can you lose data stored in a container?**
    - Data stored in a container remains unless the container is deleted.

21. **On what platforms can Docker run?**
    - Docker runs on various Linux platforms and cloud-based platforms like AWS, Google Compute Engine, and Microsoft Azure.

22. **Which is the best method for removing a container: stop and remove or just remove?**
    - Stop the container first and then remove it.

23. **Can a container restart on its own?**
    - Containers do not restart by themselves by default.

24. **How do Docker daemon and Docker client communicate with each other?**
    - They communicate using a combination of REST API, socket.IO, and TCP.

25. **Can you implement continuous development (CD) and continuous integration (CI) in Docker?**
    - Yes, you can use Docker to run Jenkins and Docker Compose for integration tests.

26. **How do you create a Docker swarm?**
    - Use the command `docker swarm init --advertise-addr <manager_IP>` to create a Docker swarm.

These questions cover a range of Docker concepts, from the basics to more advanced topics, and can be useful for Docker interviews at different skill levels.
