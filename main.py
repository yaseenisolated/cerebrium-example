import io
import os
import requests

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from fastapi import FastAPI, HTTPException

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise RuntimeError("Please set the NEWSAPI_KEY environment variable")

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise RuntimeError("Please set the HF_TOKEN environment variable")
login(token=hf_token)


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

    prompt = f"Turn some of these news headlines into a funny cartoon-style scene. The scene should be a single panel. Headlines: '{headline}'\n\nCartoon description:"
    MODEL_ID = "EleutherAI/gpt-neo-2.7B"

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        use_auth_token=hf_token
    )

    # AutoModelForCausalLM loads the PyTorch weights onto GPU or CPU
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        use_auth_token=hf_token
    )
    model.to("cuda")

    text_gen = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    outputs = text_gen(
        prompt,
        max_new_tokens=100,
        do_sample=True,
        top_k=50,
        temperature=0.7,
        num_return_sequences=1,
    )

    del model
    torch.cuda.empty_cache()

    return outputs[0]["generated_text"]

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

    for idx, im in enumerate(ims):
        buf = io.BytesIO()
        im.save(buf, format="PNG")
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
