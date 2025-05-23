# Objective:

Build _something_ on cerebrium. Has to be deployed with a Dockerfile.

Potentially something using AI? Doesn't seem to be a requirement.

# What are we gonna do?

## What is available on cerebrium:

- GPU access.
- Arbitrary compute
- Secrets
- Volumes, unclear if this necessarily works with dockerfile stuff

## What can I do in 3 hours?

- Multiplayer tic-tac-toe just to run _some_ app. State management will possibly be tricky. I suspect that volumes + custom dockerfiles may be a bit fiddly.
- Fun image generation app (AI something?).
  - Upload image of yourself and get a cartoonified thing?
  - News of the day image. Download some dumps of frontpage news and then do some image generation to do some cartoonification of it? Would be cool to wake up with a new background photo every day.
  - Pull your GOogle Photos for the week and summarise it all up for you with a post? That would be cool.
- Real-time voice interaction with my Obsidian notes? Transcription + lookup would be insanely cool. Very jarvisy.

## Decide

I think i'm going to do the news of the day thing because it has nice and limited scope.

I haven't written any python in maybe 10 years so this may be a bit tricky but we can get it to work!

# Getting started

## Running something locally

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

## running on cerebrium

```bash
rye run cerebrium deploy

...

 pip
15:37:49 Exporting to image
15:37:52
15:37:52 App built in 26s
15:37:53 Deploying App...
15:37:54 Image size: 236.53 Mb
15:37:54 App created. Checking that it starts correctly...
15:37:57 INFO:     Started server process [7]
15:37:57 INFO:     Waiting for application startup.
15:37:57 INFO:     Application startup complete.
15:37:57 INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
15:37:57 Successfully initialized user app
15:37:58 App initialized in 4s
15:37:58 App started successfully!
⠸ Building App...
╭───────────────────────────────────  my-first-project is now live!   ────────────────────────────────────╮
│ App Dashboard: https://dashboard.cerebrium.ai/projects/p-793a971b/apps/p-793a971b-my-first-project      │
│                                                                                                         │
│ Endpoints:                                                                                              │
│ POST https://api.cortex.cerebrium.ai/v4/p-793a971b/my-first-project/hello                               │
│ POST https://api.cortex.cerebrium.ai/v4/p-793a971b/my-first-project/health                              │
│ POST https://api.cortex.cerebrium.ai/v4/p-793a971b/my-first-project/ready                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
➜  my-first-project git:(main)


curl https://api.cortex.cerebrium.ai/v4/p-793a971b/my-first-project/health
No Authorization token found
```

Ok so cerebrium apps run with some auth stuff in the front. let's figure out how that works.

```bash
curl -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0SWQiOiJwLTc5M2E5NzFiIiwiaWF0IjoxNzQ2OTgxNDU2LCJleHAiOjIwNjI1NTc0NTZ9.ktmQ_hJ5J2gD39dv9-8uZRMOvYVDO-Qx0fDlD9BpCNmokJnItGVBTCa34ro1WpRbyD4oivlioD12FqEXSAUSX4KzPiuGD0efVQMUwOvqx2TU1TPdxq8k2zsumQu0qUbRMoNVYbRohq8HtlitrsVCMBRx7IlgChhoH1oI1NhyhErfy17Zde29YnYJITmpH8nRAEFZqIFt75rP4U9wTopDjTx2Ca4vQulFKAXd6FzU1_2llH1Dl-AzH9wy5dCjogI1tBOOFLT-32z3cGR3hBQTQltJ6ysFyauzrP_5BU48kVi-ajJhU4KaW2x2jIGinobpY7OuXE4I8QGQNEMGmSMkMQ" https://api.cortex.cerebrium.ai/v4/p-793a971b/my-first-project/health                              -X POST
{"run_id":"3c68292b-6f88-9b7e-949a-ba8ae0a218ea","result":"OK","run_time_ms":0.9446144104003906}%
```

ok i'm clearly getting the model of how this works incorrect. cerebrium provides some wrapper around the APIs. similar to goog.Operation that helps us manage long running processes? What's the run thing and how can I view it?

this was just a fundamental misunderstanding of what Cerebrium was at all. This bits are clearly not meant as generic http servers :p.

### storing results

ok so how do i store output into places? I assume that without the dockerfile stuff there's some harness that records our output but how do i do this in the dockerfile case? where do i put results?

If I'm going to be doing the image generation thing I need to be able to fetch the image from somewhere. Where would that be?

Managing files! https://docs.cerebrium.ai/cerebrium/storage/managing-files Let's just store the output here somewhere.

# dockerfile

oh wait. i hadn't configured cerebrium to actually be using the custom dockerfile. I left out the

```
[cerebrium.runtime.custom]
port = 8192
healthcheck_endpoint = "/health"
readycheck_endpoint = "/ready"
dockerfile_path = "./Dockerfile"
```

bit from the cerebrium.toml. let's add that and see what happens.

this seems to be taking longer which probably indicates it's doing some docker things.

ok that deployed successfully but i'm still not convinced it's using a dockkerfile. let me purposefully break the dockerfile and see what happens.

## purposefully broken dockerfile

15:56:51 Error: failed to solve: dockerfile parse error on line 11: unknown instruction: asdfadsfasdf

ok yay with a purposefully broken dockerfile it breaks so yay.
lets continnue.

# Running image generation model with some random input

Ok let's expand from running just an echo to running image model with a constant prompt and then store the result in /persistent-storage with the current date as the filename.

I'm going to copy from the examples to do this. Let's see if it works fine with the dockerfile stuff added.

from the example

model weights in the base image, which loads faster. The total response time is around 18 seconds.

The key part is the shell_commands in the cerebrium.toml file

shell_commands = ["export HF_HOME=/cortex/.cache/huggingface","python3 -c \"import torch; from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('stabilityai/stable-diffusion-2-1', torch_dtype=torch.float16)\""]

This will download the model at build time.

We probably want to do this in our Dockerfile instead? do shell_commands still work from cerebrium.toml? Let's find out!

## pulling stablediffusion weights

change docker base image to nvidia/cuda:12.1.1-runtime-ubuntu22.04 hopefully the rest works as it.

```
16:01:11 /bin/sh: 1: pip: not found
16:01:11 #13 ERROR: process "/bin/sh -c pip install -r requirements.txt" did not complete successfully: exit code: 127
16:01:11 ------
16:01:11 > RUN pip install -r requirements.txt:
16:01:11
16:01:11 Error: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete successfully: exit code: 127
16:01:11 Error: App build failed
```

that's mostly to be expected I guess. we're using a different base image.

try some modifications to dockerfile to pip install stuff gives uuss....

```

16:05:53 CUDA Version 12.1.1
16:05:53 Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
16:05:53 This container image and its contents are governed by the NVIDIA Deep Learning Container License.
16:05:53 By pulling and using the container, you accept the terms and conditions of this license:
16:05:53 https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
16:05:53 A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.
16:05:53 WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
16:05:53 Use the NVIDIA Container Toolkit to start this container with GPU support; see
16:05:53 https://docs.nvidia.com/datacenter/cloud-native/ .
16:05:53 /opt/nvidia/nvidia_entrypoint.sh: line 67: exec: python: not found
```

lame. maybe let's just abandon the fast api stuff for now since i don't actually need it.

Here's the docs for the nvidia/cuda docker image https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/README.md

trying to run the image generation main.py within the docker environment.

i really hope cerebrium has build caching on the server side because the builds are starting to take time to run now. hopefully we can have some short development loops. maybe layer caching stuff from docker?

### missing python modules...

```bash
16:16:58 File "/main.py", line 22, in <module>
16:16:58 pipe = StableDiffusionPipeline.from_pretrained(
16:16:58 File "/usr/local/lib/python3.10/dist-packages/diffusers/utils/dummy_torch_and_transformers_objects.py", line 2147, in from_pretrained
16:16:58 requires_backends(cls, ["torch", "transformers"])
16:16:58 File "/usr/local/lib/python3.10/dist-packages/diffusers/utils/import_utils.py", line 525, in requires_backends
16:16:58 raise ImportError("".join(failed))
16:16:58 ImportError:
16:16:58 StableDiffusionPipeline requires the transformers library but it was not found in your environment. You can install it with pip: `pip
16:16:58 install transformers`
16:16:58 Loading model...
```

sigh

added pip install transformers. i should probably be pinning this versions but for expediency reasons i'm not making this too prod safe.

also it looks like there is build caching! that went much faster yay.

ok yay it looks like that worked lets try again.

### missing snapshots (stability ai weights)

```
16:19:17 huggingface_hub.errors.LocalEntryNotFoundError: Cannot find an appropriate cached snapshot folder for the specified revision on the local disk and outgoing traffic has been disabled. To enable repo look-ups
and downloads online, pass 'local_files_only=False' as input.
```

I assume this means that the step where we fetch the image in the cerebrium.toml doesn't work anymore and we have to do it in the dockerfile.

saw this in my output but i have no idea what it means

```
16:22:20 Cannot initialize model with low cpu memory usage because `accelerate` was not found in the environment. Defaulting to `low_cpu_mem_usage=False`. It is strongly recommended to install `accelerate` for
faster and less memory-intense model loading. You can do so with:
```

oh is it about my new pull model weights step?

the model still seems to not be in the right place....

```
download.py", line 220, in snapshot_download
16:24:42 raise LocalEntryNotFoundError(
16:24:42 huggingface_hub.errors.LocalEntryNotFoundError: Cannot find an appropriate cached snapshot folder for the specified revision on the local disk and outgoing traffic has been disabled. To enable repo look-ups
and downloads online, pass 'local_files_only=False' as input.
```

hmmm maybe it's because the HF_HOME env variable isn't being passed into the api server thing? let's try that and see.

nope that wasn't it.

```
16:31:25 starting downloading image weights
Fetching 13 files: 100%|██████████| 13/13
Loading pipeline components: 100%|██████████| 6/6
16:31:37 done downloading model weights
```

the weights are being downloaded.... but then not read appropriately?

maybe the dir for HF_HOME is not useful? really unclear for me.

this bit is turning into a nightmare. how can i debug this? i want to echo the snapshot dir after the caching and then before the runtime tries to use it so that hopefully we can see if they match or don't match.

let's try and use /persistent-storage as the place we store our models and check if that helps at all. at the very least it iwll give us visibility into what's working or not.

it looks like that works! not ideal but we move.

### incompatible torchvision + torch version issues.

```
18:04:56 operator torchvision::nms does not exist
```

on the internet found that the versions of torch and torchvision compatibility matters.

i think i'm not at ~2.5 hours invested which is coming close to the 3 hours mentioned in the doc.

i've also gone ahead and changed the machine type to one that contains a GPU.

i suspect that i don't actually need torchvision.... i can't see where the dependency comes from. maybe in the next build attempt i'll remove it and see how far we get.

### numpy

numpy!

```
22:59:37 File "/main.py", line 24, in <module>
22:59:37 pipe = StableDiffusionPipeline.from_pretrained(
22:59:37 File "/usr/local/lib/python3.10/dist-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
22:59:37 return fn(*args, **kwargs)
22:59:37 File "/usr/local/lib/python3.10/dist-packages/diffusers/pipelines/pipeline_utils.py", line 961, in from_pretrained
22:59:37 loaded_sub_model = load_sub_model(
22:59:37 File "/usr/local/lib/python3.10/dist-packages/diffusers/pipelines/pipeline_loading_utils.py", line 777, in load_sub_model
22:59:37 loaded_sub_model = load_method(os.path.join(cached_folder, name), **loading_kwargs)
22:59:37 File "/usr/local/lib/python3.10/dist-packages/diffusers/schedulers/scheduling_utils.py", line 158, in from_pretrained
22:59:37 return cls.from_config(config, return_unused_kwargs=return_unused_kwargs, **kwargs)
22:59:37 File "/usr/local/lib/python3.10/dist-packages/diffusers/configuration_utils.py", line 263, in from_config
22:59:37 model = cls(**init_dict)
22:59:37 File "/usr/local/lib/python3.10/dist-packages/diffusers/configuration_utils.py", line 693, in inner_init
22:59:37 init(self, *args, **init_kwargs)
22:59:37 File "/usr/local/lib/python3.10/dist-packages/diffusers/schedulers/scheduling_ddim.py", line 234, in __init__
22:59:37 self.timesteps = torch.from_numpy(np.arange(0, num_train_timesteps)[::-1].copy().astype(np.int64))
22:59:37 RuntimeError: Numpy is not available
```

23:04:00 CUDA Version 12.1.1

```
23:04:35 A module that was compiled using NumPy 1.x cannot be run in
23:04:35 NumPy 2.2.5 as it may crash. To support both 1.x and 2.x
23:04:35 versions of NumPy, modules must be compiled with NumPy 2.0.
23:04:35 Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.
23:04:35 If you are a user of the module, the easiest solution will be to
23:04:35 downgrade to 'numpy<2' or try to upgrade the affected module.
23:04:35 We expect that some modules will need time to support NumPy 2.
23:04:35 Traceback (most recent call last):  File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
23:04:35 return _run_code(code, main_globals, None,
```

did i install the wrong version of numpy maybe?

yup. gotta do "numpy<2.0"

successs!!!!

```bash

23:09:45 ==========
23:09:45 == CUDA ==
23:09:45 CUDA Version 12.1.1
23:09:45 Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
23:09:45 This container image and its contents are governed by the NVIDIA Deep Learning Container License.
23:09:45 By pulling and using the container, you accept the terms and conditions of this license:
23:09:45 https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
23:09:45 A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.
23:09:58 Loading model...
Loading pipeline components...: 100%|██████████| 6/6 [00:05<00:00,  1.17it/s]
23:10:04 INFO:     Started server process [1]
23:10:04 INFO:     Waiting for application startup.
23:10:04 INFO:     Application startup complete.
23:10:04 INFO:     Uvicorn running on http://0.0.0.0:8192 (Press CTRL+C to quit)
23:10:04 Loaded.
23:10:04 Loaded scheduler.
23:10:04 Enabled memory efficient attention.
23:10:04 Moved to GPU.
23:10:04 cuda:0
23:10:04 INFO:     127.0.0.1:54924 - "GET /ready HTTP/1.1" 200 OK
23:10:06 INFO:     127.0.0.1:43066 - "GET /ready HTTP/1.1" 200 OK
23:10:07 App initialized in 24s
23:10:07 App started successfully!
```

### Run the model

rye run cerebrium ls
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name ┃ Size ┃ Last Modified ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ output-0.png │ 495.2 kB │ 2025-05-12 21:17:26 │

tada! we've got output from the model.

# Chain llama model that cartoonises

using secrets to store NEWSAPI_KEY. fetch with requests api.

## couldn't load llama 7b

```
File "/main.py", line 44, in generate_cartoon_description
text_gen = hf_pipeline(

raise ValueError(

ValueError: Could not load model TheBloke/LLaMA-2-7B-Chat-GGML with any of the following classes: (<class 'transformers.models.auto.modeling_auto.AutoModelForCausalLM'>,). See the original errors:

while loading with AutoModelForCausalLM, an error is thrown:

OSError: TheBloke/LLaMA-2-7B-Chat-GGML does not appear to have a file named pytorch_model.bin but there is a file for TensorFlow weights. Use `from_tf=True` to load this model from those weights
```

the internet suggests that we use "meta-llama/Llama-2-7b-hf" instead. something about the serialization format ggml vs hf .

```
Access to model meta-llama/Llama-2-7b-hf is restricted. You must have access to it and be authenticated to access it. Please log in.
```

urgh.

changed the model

## need protobufs as a dependency apparently.

```bash
File "/usr/local/lib/python3.10/dist-packages/transformers/tokenization_utils_base.py", line 2303, in _from_pretrained

except import_protobuf_decode_error():

File "/usr/local/lib/python3.10/dist-packages/transformers/tokenization_utils_base.py", line 87, in import_protobuf_decode_error
raise ImportError(PROTOBUF_IMPORT_ERROR.format(error_message))
requires the protobuf library but it was not found in your environment. Checkout the instructions on the
installation page of its repo: https://github.com/protocolbuffers/protobuf/tree/master/python#installation and follow the ones
that match your environment. Please note that you may need to restart your runtime after installation.
```

## incorrect tokenizer on llama

```
ValueError: Converting from SentencePiece and Tiktoken failed, if a converter for SentencePiece is available, provide a model path with a SentencePiece tokenizer.model file.Currently available slow->fast converters: ['AlbertTokenizer', 'BartTokenizer', 'BarthezTokenizer', 'BertTokenizer', 'BigBirdTokenizer', 'BlenderbotTokenizer', 'CamembertTokenizer', 'CLIPTokenizer', 'CodeGenTokenizer', 'ConvBertTokenizer', 'DebertaTokenizer', 'DebertaV2Tokenizer', 'DistilBertTokenizer', 'DPRReaderTokenizer', 'DPRQuestionEncoderTokenizer', 'DPRContextEncoderTokenizer', 'ElectraTokenizer', 'FNetTokenizer', 'FunnelTokenizer', 'GPT2Tokenizer', 'HerbertTokenizer', 'LayoutLMTokenizer', 'LayoutLMv2Tokenizer', 'LayoutLMv3Tokenizer', 'LayoutXLMTokenizer', 'LongformerTokenizer', 'LEDTokenizer', 'LxmertTokenizer', 'MarkupLMTokenizer', 'MBartTokenizer', 'MBart50Tokenizer', 'MPNetTokenizer', 'MobileBertTokenizer', 'MvpTokenizer', 'NllbTokenizer', 'OpenAIGPTTokenizer', 'PegasusTokenizer', 'Qwen2Tokenizer', 'RealmTokenizer', 'ReformerTokenizer', 'RemBertTokenizer', 'RetriBertTokenizer', 'RobertaTokenizer', 'RoFormerTokenizer', 'SeamlessM4TTokenizer', 'SqueezeBertTokenizer', 'T5Tokenizer', 'UdopTokenizer', 'WhisperTokenizer', 'XLMRobertaTokenizer', 'XLNetTokenizer', 'SplinterTokenizer', 'XGLMTokenizer', 'LlamaTokenizer', 'CodeLlamaTokenizer', 'GemmaTokenizer', 'Phi3Tokenizer']

```

lets just use example code from https://huggingface.co/openlm-research/open_llama_7b

did not realize this is an entirely different model but will go ahead with it for now.

`LlamaTokenizer requires the SentencePiece library but it was not found in your environment. Checkout the instructions on the`

## mismatched device

`RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu! (when checking argument for argument index in method wrapper_CUDA__index_select)`

# Cartoon description is nonsense

The output from the open_llama model is mostly nonsense. I suspect that this is because it's an instruct model and i'm formatting my request incorrectly?
