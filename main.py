import base64
import io
import os
import requests

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from fastapi import FastAPI, HTTPException

from transformers import LlamaTokenizer, LlamaForCausalLM


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

    tokenizer = LlamaTokenizer.from_pretrained('openlm-research/open_llama_3b', device_map='cuda')
    model = LlamaForCausalLM.from_pretrained(
        'openlm-research/open_llama_3b', torch_dtype=torch.float16, device_map='cuda',
    )

    prompt_req = f"Turn some of these news headlines into a funny cartoon-style scene. The scene should be a single panel. Headlines: '{headline}'\n\nCartoon description:"


    input_ids = tokenizer(prompt_req, return_tensors="pt").input_ids
    input_ids = input_ids.to('cuda')

    generation_output = model.generate(
        input_ids=input_ids, max_new_tokens=32
    )

    description = tokenizer.decode(generation_output[0], skip_special_tokens=True)


    # Unload LLaMA to free VRAM
    del model
    torch.cuda.empty_cache()

    return description

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
