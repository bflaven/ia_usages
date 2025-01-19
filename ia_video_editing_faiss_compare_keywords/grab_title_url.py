#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name grab_title_url python=3.9.13
conda info --envs
source activate grab_title_url
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n grab_title_url


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords


# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

"""
# Using Faiss# 
https://medium.com/loopio-tech/how-to-use-faiss-to-build-your-first-similarity-search-bf0f708aa772
https://github.com/TamerOnLine/sentence-embeddings-similarity-search
https://cheatsheet.md/vector-database/faiss-python-api.en
https://github.com/guilherme-pombo/SimpleRAG
https://github.com/abinthomasonline/clip-faiss


# Useful python packages for images and videos

# using clip (open_clip)
https://huggingface.co/laion/CLIP-ViT-B-32-laion2B-s34B-b79K
https://stability.ai/
This model was trained with the 2 Billion sample English subset of LAION-5B
https://laion.ai/blog/laion-5b/

# computer vision
https://github.com/openai/CLIP

# speaker-identification
# Whisper transcription and diarization (speaker-identification)
https://github.com/lablab-ai/Whisper-transcription_and_diarization-speaker-identification-/blob/main/transcribtion_diarization.ipynb
https://community.openai.com/t/can-whisper-distinguish-two-speakers/291253/9

# face_recognition
https://pypi.org/project/face-recognition/

# cv2
https://pypi.org/project/opencv-python/


# Video Editing
https://github.com/topics/ai-video-generator
https://cloudinary.com/guides/front-end-development/python-video-processing-6-useful-libraries-and-a-quick-tutorial
https://www.restack.io/p/ai-video-synthesis-answer-python-ai-editing-cat-ai
https://towardsdatascience.com/automate-video-editing-with-python-4e0c43edef36
https://github.com/Breakthrough/PySceneDetect
https://github.com/octimot/StoryToolkitAI



# alternative to Ollama
https://nexa.ai/models


# D3lta
https://github.com/VIGINUM-FR/D3lta



"""


# List of URLs
urls = [
# Using Faiss# 
"https://medium.com/loopio-tech/how-to-use-faiss-to-build-your-first-similarity-search-bf0f708aa772",
"https://github.com/TamerOnLine/sentence-embeddings-similarity-search",
"https://cheatsheet.md/vector-database/faiss-python-api.en",
"https://github.com/guilherme-pombo/SimpleRAG",
"https://github.com/abinthomasonline/clip-faiss",
# Useful python packages for images and videos
# using clip (open_clip)
"https://huggingface.co/laion/CLIP-ViT-B-32-laion2B-s34B-b79K",
"https://stability.ai/",
# This model was trained with the 2 Billion sample English subset of LAION-5B
"https://laion.ai/blog/laion-5b/",
# computer vision
"https://github.com/openai/CLIP",
# speaker-identification
# Whisper transcription and diarization (speaker-identification)
"https://github.com/lablab-ai/Whisper-transcription_and_diarization-speaker-identification-/blob/main/transcribtion_diarization.ipynb",
"https://community.openai.com/t/can-whisper-distinguish-two-speakers/291253/9",
# face_recognition
"https://pypi.org/project/face-recognition/",
# cv2
"https://pypi.org/project/opencv-python/",
# Video Editing
"https://github.com/topics/ai-video-generator",
"https://cloudinary.com/guides/front-end-development/python-video-processing-6-useful-libraries-and-a-quick-tutorial",
"https://www.restack.io/p/ai-video-synthesis-answer-python-ai-editing-cat-ai",
"https://towardsdatascience.com/automate-video-editing-with-python-4e0c43edef36",
"https://github.com/Breakthrough/PySceneDetect",
"https://github.com/octimot/StoryToolkitAI",
# alternative to Ollama
"https://nexa.ai/models",
# D3lta
"https://github.com/VIGINUM-FR/D3lta",


]

"""


"""
# Store the HTML code
html_code = ""

# Iterate through each URL
for url in urls:
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        html_content = response.text

        # Parse HTML using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the title tag
        title_tag = soup.title

        # Extract text from the title tag
        title_text = title_tag.text if title_tag else "Title Not Found"

        # Print the URL and the title text
        # print(f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>")

        # Append to the HTML code
        html_code += f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>"

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Print the full HTML code
print("\n--- Full HTML Code")
print("\n\n")
print(html_code)
print("\n\n")