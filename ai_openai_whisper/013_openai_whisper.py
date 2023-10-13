#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name openai_whisper python=3.9.13
conda info --envs
source activate openai_whisper
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n openai_whisper

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_openai_whisper/

python 013_openai_whisper.py

[Source]
Source: https://github.com/openai/whisper/tree/main
git clone https://github.com/openai/whisper.git

[MODELS AND LANGUAGES]
Available models and languages
There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed.

tiny
base
small
medium
large

See https://github.com/openai/whisper/tree/main#available-models-and-languages


pip install -U openai-whisper
pip install setuptools-rust


"""
"""

- english
060123_john_willinsky_economics_knowledge_public.mp3
sample_0.mp3
sample_1.mp3
sample_2.mp3
sample_3.mp3
sample_4.mp3

- foreign
ar_sample_1.mp3
cn_sample_1.mp3
fr_sample_1.mp3
ru_sample_1.mp3
sp_sample_1.mp3

- more audio samples
https://commons.wikimedia.org/wiki/Category:Audio_files_of_speeches
https://audio-samples.github.io/
https://audio-lingua.ac-versailles.fr/?lang=en


- source
https://wandb.ai/wandb_fc/gentle-intros/reports/OpenAI-Whisper-How-to-Transcribe-Your-Audio-to-Text-for-Free-with-SRTs-VTTs---VmlldzozNDczNTI0

https://github.com/openai/whisper/discussions/98


"""


import whisper
from whisper.utils import get_writer
import os


# english
audio_input = "audio_files_sources/english/sample_1.mp3"
file_output_txt = "003_openai_whisper_en_sample_1_output.txt"
file_output_srt = "003_openai_whisper_en_sample_1_output.srt"
language_selected="english"


model = whisper.load_model("base")
result = model.transcribe(audio_input, fp16=False, verbose=True, language=language_selected)


output_directory = "./output_srtfiles_writer"

# Set some initial options values
options = {
    'max_line_width': None,
    'max_line_count': None,
    'highlight_words': True
}


# Save as a TXT file without any line breaks
# txtFilename = os.path.join("output_srtfiles_writer", f"{file_output_txt}")
# with open(txtFilename, "w", encoding="utf-8") as txt:
#     txt.write(result["text"])


# Save as a TXT file with hard line breaks
txt_writer = get_writer("txt", output_directory)
txt_writer(result, audio_input, options)

# Save as a JSON file
json_writer = get_writer("json",  output_directory)
json_writer(result, audio_input, options)

# Save as a VTT file [Web Video Text Tracks (WebVTT)]
vtt_writer = get_writer("vtt", output_directory)
vtt_writer(result, audio_input, options)

# Save as a TSV file (Tab Separated Values)
tsv_writer = get_writer("tsv", output_directory)
tsv_writer(result, audio_input, options)

# Save as a SRT file SubRip Subtitle File
srt_writer = get_writer("srt", output_directory)
srt_writer(result, audio_input, options)
