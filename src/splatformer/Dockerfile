ARG UBUNTU_VERSION=22.04
ARG NVIDIA_CUDA_VERSION=11.8.0

FROM nvidia/cuda:${NVIDIA_CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}

# Set non-interactive frontend and configure timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone

# Set CUDA architecture for your GPU (3070 Ti)
ENV TORCH_CUDA_ARCH_LIST="8.6"

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

# Update pip & install packages
RUN pip install --upgrade pip
RUN pip install gin-config

# Install PyTorch
RUN pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
RUN pip install torch-scatter torch-sparse torch-cluster -f https://data.pyg.org/whl/torch-2.1.0+cu118.html
RUN pip install torch-geometric

# Install splatformer
RUN mkdir /SplatFormer
COPY SplatFormer /SplatFormer
RUN cd SplatFormer && pip install -r requirements.txt

# RUN pip install git+https://github.com/nerfstudio-project/gsplat.git@v0.1.11

RUN cd SplatFormer && pip install Pointcept/
RUN cd SplatFormer/Pointcept/libs/pointops && python3 setup.py install

RUN cd SplatFormer && pip install flash-attn --no-build-isolation

# Reset the environment variable
ENV DEBIAN_FRONTEND=dialog