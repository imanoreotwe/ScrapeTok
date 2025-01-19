# ScrapeTok

Simple tool to scrape tiktok collections & comments

videos, audios, and images are scraped into their respective formats in the given directory.
post metadata is stored in a json including information about the creator and the comments.

its janky and I don't care

## how to use
+ create venv, install `requests`
+ edit the scrape collection id at the bottom of `scrape.py`
+ ????
+ ~~profit~~ Tiktoks & comments on your computer

## todo
+ [ ] figure out profile scraping?
+ [ ] skip over already downloaded content

this is most likely against TOS use at your own risk

## future plans

I want to turn this into a searchable database of information from the saved Tiktoks, mostly with the goal of learning machine learning concepts at a deep level.
- First, I am going to get high quality descriptions (probably using [tarsier](https://github.com/bytedance/tarsier)) and transcriptions (probably with [whisper](https://github.com/openai/whisper)) from the videos and photos.
- Next, I want to build my own embedding for this data, maybe compare it to other "off the shelf" embedings.
In my experience generic embedings can be kind of hot/cold with niche topics.
- Finally, store these embedings in my ite vector database [vite](https://github.com/imanoreotwe/vlite) and build a RAG application to retrieve and serve relevant tiktoks and informed answers to queries.
