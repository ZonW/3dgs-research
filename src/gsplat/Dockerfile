ARG UBUNTU_VERSION=22.04
ARG NVIDIA_CUDA_VERSION=12.1.0

FROM nvidia/cuda:${NVIDIA_CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}

# Set non-interactive frontend and configure timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    git \
    vim \
    build-essential \
    python3 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libglm-dev \
    && \
    apt-get clean

# Set CUDA architecture for your GPU (3070 Ti)
ENV TORCH_CUDA_ARCH_LIST="8.6"

# Update pip & install dependencies
RUN pip install --upgrade pip
RUN pip install ninja numpy jaxtyping rich

# install torch
RUN pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121

# Build gsplat
RUN mkdir /gsplat
COPY gsplat /gsplat
RUN pip install -r /gsplat/examples/requirements.txt
RUN cd /gsplat && python3 setup.py install

# Copy script
RUN mkdir /scripts
COPY scripts /scripts

# Reset the environment variable
ENV DEBIAN_FRONTEND=dialog
