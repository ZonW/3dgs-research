# Base image from COLMAP
FROM colmap/colmap:latest

# Set environment variable to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    git \
    vim \
    build-essential \
    python3 \
    python3-pip && \
    apt-get clean

# update pip & install dependencies
RUN pip install --upgrade pip
RUN pip install numpy

# Copy script
RUN mkdir /scripts
COPY scripts/ /scripts/

# Reset the environment variable
ENV DEBIAN_FRONTEND=dialog
