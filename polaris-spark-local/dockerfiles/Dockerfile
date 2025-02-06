## Ubuntu but slimmer
FROM debian:bullseye-slim

## Create and use a Non-Root User
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends dialog apt-utils
RUN apt-get update && apt-get -y install sudo wget curl nano
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker
WORKDIR /home/docker/


## Install Java 11 and Set JAVA_HOME
RUN sudo apt-get update && sudo apt-get install -y openjdk-11-jdk
# Set JAVA_HOME for all users
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' | sudo tee /etc/profile.d/jdk.sh
RUN echo 'export PATH=$PATH:$JAVA_HOME/bin' | sudo tee -a /etc/profile.d/jdk.sh

## Load JAVA_HOME variable in current shell for subsequent commands
RUN . /etc/profile.d/jdk.sh

## Install Python dependencies for Jupyter and Spark with UV
#RUN sudo apt-get install -y python3-pip python3-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

## Install git
RUN sudo apt-get -y install git

## mount apache spark
COPY /spark /opt/spark

# Copy your local Spark build into the image
RUN sudo chmod -R 777 /opt/spark
# Setting environment variables for Spark
RUN echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
RUN echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc
RUN echo 'export PYSPARK_PYTHON=/usr/bin/python3' >> ~/.bashrc
RUN echo 'SPARK_MASTER_HOST=0.0.0.0' >> ~/.bashrc

## Install PySpark
RUN uv init && rm hello.py

# Expose the necessary ports for Spark and Jupyter
EXPOSE 8888
EXPOSE 4040

## Start Container
CMD ["bash", "-c", "uv run --with jupyter jupyter lab --ip='0.0.0.0' --port=8888"]
