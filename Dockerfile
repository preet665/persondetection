# Use Ubuntu as the base image
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists
RUN apt-get update

# Install Python 3.8 and pip
#RUN apt-get install -y python3.9 python3.9-dev python3-pip

# Install additional system dependencies
#RUN apt-get install -y libcairo2-dev pkg-config command-not-found libsystemd-dev ubuntu-advantage-tools ufw unattended-upgrades
RUN apt-get update && apt-get install -y \
    python3.9 python3.9-dev python3-pip \
    libcairo2-dev pkg-config command-not-found libsystemd-dev ubuntu-advantage-tools ufw unattended-upgrades\
    libgirepository1.0-dev libglib2.0-dev libdbus-1-dev libdbus-glib-1-dev
# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Update pip and install Python dependencies from requirements.txt
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --ignore-installed -r requirment.txt

# Run your application
CMD ["python3", "./start_app.py"]
