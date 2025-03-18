#!/bin/bash

mkdir src
mkdir dst

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
rm -f cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install -y virtualenv
sudo apt-get install -y python3-tk ffmpeg libcudnn8 libcublas-12-2 > /dev/null &

git clone https://github.com/hacksider/Deep-Live-Cam.git
cd Deep-Live-Cam/

cd models/
curl -sLO https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128_fp16.onnx &
curl -sLO https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128.onnx &
cd ..

virtualenv venv
venv/bin/pip3 install -r requirements.txt
# fix Frame processor face_enhancer not found
venv/bin/pip uninstall basicsr -y
venv/bin/pip install git+https://github.com/xinntao/BasicSR.git@master
venv/bin/pip uninstall gfpgan -y
venv/bin/pip install git+https://github.com/TencentARC/GFPGAN.git@master
