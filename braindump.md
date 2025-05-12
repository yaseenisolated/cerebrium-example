# Objective:

Build *something* on cerebrium. Has to be deployed with a Dockerfile. 

Potentially something using AI? Doesn't seem to be a requirement.

# What are we gonna do?

## What is available on cerebrium:
- GPU access. 
- Arbitrary compute
- Secrets
- Volumes, unclear if this necessarily works with dockerfile stuff


## What can I do in 3 hours?
- Multiplayer tic-tac-toe just to run *some* app. State management will possibly be tricky. I suspect that volumes + custom dockerfiles may be a bit fiddly.
- Fun image generation app (AI something?). 
  - Upload image of yourself and get a cartoonified thing?
  - News of the day image. Download some dumps of frontpage news and then do some image generation to do some cartoonification of it? Would be cool to wake up with a new background photo every day.
  - Pull your GOogle Photos for the week and summarise it all up for you with a post? That would be cool.
- Real-time voice interaction with my Obsidian notes? Transcription + lookup would be insanely cool. Very jarvisy.

## Decide

I think i'm going to do the news of the day thing because it has nice and limited scope.

I haven't written any python in maybe 10 years so this may be a bit tricky but we can get it to work!


# Getting started

Step 1. lets get a simple echo app running on cerebrium. With a dockerfile. Let's follow the guide at https://docs.cerebrium.ai/cerebrium/container-images/custom-dockerfiles

Just gonna copy-paste that dockerfile... I've never heard of uvicorn what's that? apparently the async version of gunicorn + django. I've clearly been out of the ecosystem for a while. Post-modern twisted framework.

```bash

(cerebrium) ➜  my-first-project git:(main) ✗ cerebrium deploy

╭──────────  Deployment parameters for my-first-project  ──────────╮
│                                                                  │
│   Parameter               Value                                  │
│  ──────────────────────────────────────────────────────────────  │
│   HARDWARE PARAMETERS                                            │
│   Compute                 CPU                                    │
│   CPU                     2.0                                    │
│   Memory                  12.0                                   │
│   Region                  us-east-1                              │
│   Provider                aws                                    │
│                                                                  │
│   DEPLOYMENT PARAMETERS                                          │
│   Python Version          3.13                                   │
│   Include Pattern         ['./*', 'main.py', 'cerebrium.toml']   │
│   Exclude Pattern         ['.*']                                 │
│   Base Image              debian:bookworm-slim                   │
│                                                                  │
│   SCALING PARAMETERS                                             │
│   Cooldown                30                                     │
│   Minimum Replicas        0                                      │
│   Maximum Replicas        5                                      │
│                                                                  │
│   DEPENDENCIES                                                   │
│   pip                                                            │
│   apt                                                            │
│   conda                                                          │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯

Do you want to continue with the deployment? [Y/n]:
```

Interesting stuff. Why does it care about dependencies? How does it know dependencies?

```bash
09:33:28 INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
09:33:28 || ERROR || Failure to initialize user app || END ERROR ||
09:33:28 || ERROR || Error: No module named 'fastapi' || END ERROR ||
```

I didn't add a requirements file. Easy fix.

```bash
 uv pip freeze > requirements.txt
 ```


 https://newsapi.org/register/success

 use rye to install python and uv to manage dependencies. 

```bash
 rye run uv pip install -r requirements.txto
 rye run python -m uvicorn main:app
 ```

 and I get

 ```bash
 INFO:     Started server process [72876]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:64371 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:64372 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:64406 - "GET /hello HTTP/1.1" 405 Method Not Allowed
 ```

 tada! now lets get this working on cerebrium.