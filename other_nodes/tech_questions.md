# Dockerfile Cheatsheet

A Dockerfile is used to define the configuration and steps required to create a Docker image. Below are some common Dockerfile instructions and their descriptions:

### Instructions for Building the Image:

- **FROM**:
  Defines the base image used to start the build process.
  
- **MAINTAINER** (Deprecated):
  Specifies the full name and email address of the image creator (Consider using LABEL for metadata).

- **RUN**:
  Executes a command during the build process. Commonly used for installing software or performing setup tasks.

- **CMD**:
  Specifies the default command to run when the container starts. Can be overridden when running the container.

- **ENTRYPOINT**:
  Similar to CMD but sets an executable as the default command. It's less easily overridden.

- **LABEL**:
  Allows you to add metadata and labels to your Docker image.

- **EXPOSE**:
  Associates a specific port with the container for networking purposes (does not actually publish the port).

- **ENV**:
  Sets environment variables within the container.

- **ADD**:
  Copies files from the host into the container's filesystem at a specified destination.

- **COPY**:
  Similar to ADD but is recommended for copying local files into the container.

- **WORKDIR**:
  Sets the working directory for subsequent CMD and RUN instructions.

- **VOLUME**:
  Creates a mount point within the container for accessing a directory on the host machine.

- **USER**:
  Sets the user or UID under which the container runs (enhances security).

### Example Usage:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV APP_DIR /app
ENV FLASK_APP app.py

# Create a directory for the app
WORKDIR $APP_DIR

# Copy the current directory contents into the container at /app
COPY . $APP_DIR

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run your application
CMD ["python", "app.py"]
```
