#!/bin/bash

# install cuda
# https://developer.nvidia.com/cuda-downloads
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update

# install cudnn8
sudo apt-get install -y libcudnn9

# install cublas
sudo apt-get install -y libcublas-12-2

# setup virtualenv
sudo apt-get install -y virtualenv
virtualenv pyenv
source pyenv/bin/activate

# install faster-whisper
pip3 install faster-whisper
