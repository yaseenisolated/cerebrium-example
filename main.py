import base64
import io
import os
import requests

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from fastapi import FastAPI, HTTPException

from transformers import pipeline as hf_pipeline



NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise RuntimeError("Please set the NEWSAPI_KEY environment variable")

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"


app = FastAPI()

def fetch_news():
    resp = requests.get(
        NEWSAPI_URL,
        params={
            "apiKey": NEWSAPI_KEY,
            "country": "us",
            "pageSize": 20,
        },
        timeout=5,
    )
    resp.raise_for_status()
    articles = resp.json().get("articles")
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")
    
    headlines = [article["title"] for article in articles]
    return ". ".join(headlines)

def generate_cartoon_description(headline):
    text_gen = hf_pipeline(
        "text-generation",
        model="openlm-research/open_llama_7b",
        device=0,
        torch_dtype=torch.float16,
    )

    prompt_req = f"Turn this news headline into a funny cartoon-style scene: '{headline}'"
    cartoon = text_gen(
        prompt_req,
        max_length=100,
        do_sample=True,
        top_k=50,
        temperature=0.7,
        num_return_sequences=1,
    )[0]["generated_text"]

    # Unload LLaMA to free VRAM
    del text_gen
    torch.cuda.empty_cache()

    return cartoon

def generate_cartoon_image(description):
    sd_pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1",
        torch_dtype=torch.float16,
    )
    sd_pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        sd_pipe.scheduler.config
    )
    sd_pipe.enable_xformers_memory_efficient_attention()
    sd_pipe = sd_pipe.to("cuda")

    # Generate the image(s)
    ims = sd_pipe(
        prompt=description,
        height=512,
        width=512,
        num_inference_steps=25,
        num_images_per_prompt=1,
    ).images

    # Encode and persist
    result_b64 = []
    for idx, im in enumerate(ims):
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        result_b64.append(base64.b64encode(buf.getvalue()).decode())
        im.save(f"/persistent-storage/cartoon-{idx}.png")

    # unload the model
    del sd_pipe
    torch.cuda.empty_cache()


@app.get("/health")
def health():
    return "OK"

@app.get("/ready")
def ready():
    return "OK"


@app.post("/run")
def predict():
    headline = fetch_news()
    print('got headlines')
    print(headline)
    description = generate_cartoon_description(headline)
    print('got description')
    print(description)
    images = generate_cartoon_image(description)
    print('got images')
    print(images)
    return images
