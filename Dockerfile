# Base image
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install dumb-init
RUN update-ca-certificates

RUN apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip install diffusers transformers

ENV HF_HOME=/cortex/.cache/huggingface

RUN python3 -c "print('starting downloading image weights'); import torch; from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('stabilityai/stable-diffusion-2-1', torch_dtype=torch.float16); print('done downloading model weights');"

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8192"]