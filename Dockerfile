# Base image
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HF_HOME=/persistent-storage/hf-home

RUN apt-get update && apt-get install dumb-init
RUN update-ca-certificates

RUN apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --upgrade pip

RUN pip install uvicorn
#RUN mkdir -p $HF_HOME && python3 -c "print('starting downloading image weights'); import torch; from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('stabilityai/stable-diffusion-2-1', torch_dtype=torch.float16); print('done downloading model weights');"

COPY . .

RUN pip install -r requirements.txt

# Install PyTorch and friends (matching CUDA 12.1)
RUN pip install \
  torch==2.2.2+cu121 \
  torchvision==0.17.2+cu121 \
  torchaudio==2.2.2+cu121 \
  diffusers transformers accelerate xformers pydantic safetensors "numpy<2.0" \
  --extra-index-url https://download.pytorch.org/whl/cu121

RUN pip install requests



CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8192"]