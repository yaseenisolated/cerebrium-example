Hi!

This is an attempt to chain a few AI examples together with the custom Dockerfile cerebrium environment.

You can find my stream of consciousness notes in braindump.md where all my roadbumps are listed.

This took me more like 4-5 hours as I got over invested in making all of this work.

# What is this?

This pipeline attempts to generate an image that summarises the days news into a cartoon image. It's pretty unsuccessful at doing that.

It first fetches a json dump of the top headlines from newsapi.org, and then pipes that into a Llama model (I didn't get acccess from huggingface in time to get this to work correctly) to generate a shorter decsription of a cartoon that we can generate. This is then piped into a stable diffusion model to actually generate the image.

I haven't had much time getting this to actually generate a good enough input into stable diffusion.

# Roadblocks and feedback