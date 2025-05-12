Hi!

This is an attempt to chain a few AI examples together with the custom Dockerfile cerebrium environment.

You can find my stream of consciousness notes in braindump.md where all my roadbumps are listed.

This took me more like 4-5 hours as I got over invested in making all of this work.

# What is this?

This pipeline attempts to generate an image that summarises the days news into a cartoon image. It's pretty unsuccessful at doing that.

It first fetches a json dump of the top headlines from newsapi.org, and then pipes that into a Llama model (I didn't get acccess from huggingface in time to get this to work correctly) to generate a shorter decsription of a cartoon that we can generate. This is then piped into a stable diffusion model to actually generate the image.

I haven't had much time getting this to actually generate a good enough input into stable diffusion to product useful output. I'd love more time to tune this to produce actually interesting outputs.

Send a blank post request to /run using the cerebrium dashboard to trigger the pipeline.

## What I accomplished

1. Running the image generation models under custom dockerfile environment.
2. Running the text generation model.
3. Deploying and running the app in cerebrium.

## What I did not accomplish

1. Getting meaningful output after experimenting with this combination of models.

# Roadblocks and feedback

1. I had lots of trouble getting the model weights cached when using custom Dockerfiles. For some reason the runtime was unable to find the weights downloaded during the build step. I worked around this by storing weights in /persistent-storage. See the saga in braindump.md. The existing approach of running comamnds during the build step also does not seem to work the same with custom dockerfiles.

2. It's not clear to me how the API works and what format is used to pass outputs back to the user. I can see that pydantic is somehow used to parse inputs from the user but not how to pass data back. Again I'm storing image outputs in /persistent-storage.

3. I haven't spent much time building on AI models for a while so a lot of time was spent getting pytorch and pytorch vision to work nicely. This is more an ecosystem problem but there are dependency conflicts around pytorch vision and numpy and cuda. These libraries also don't make their dependencies very clear. There were a number of times where I was missing a dependency that was only really possible to identify at runtime.

#1 and #2 are likely just documentation fixes.

The cerebrium deploy command was definitely a highlight. When the Dockerfile was organised appropriately compiling and deploying took less than 30s which gave really fast debugging loops and made this project a lot easier.

I really liked the streaming logs in various places especially as part of the build step. It helped a ton when debugging.

What a "run" is was not clear to me for a while and i'm not really sure how to interact with it.

For a blow by blow of using cerebrium and getting bits working see my braindump.

I've definitely hit the maximum hours and stopping here.
