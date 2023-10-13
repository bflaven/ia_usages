#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name faster_whisper python=3.9.13
conda info --envs
source activate faster_whisper
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n faster_whisper

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_openai_whisper/

python 011_faster_whisper.py


[Source]
Source: https://github.com/guillaumekln/faster-whisper
git clone https://github.com/guillaumekln/faster-whisper.git

# requirements
pip install faster_whisper
pip install ctranslate2



tiny
base
small
medium
large

Args:
model_size_or_path: Size of the model to use (tiny, tiny.en, base, base.en, small, small.en, medium, medium.en, large-v1, large-v2, or large), a path to a converted model directory, or a CTranslate2-converted Whisper model ID from the Hugging Face Hub. When a size or a model ID is configured, the converted model is downloaded from the Hugging Face Hub.

device: Device to use for computation ("cpu", "cuda", "auto").
        
compute_type: Type to use for computation.
See https://opennmt.net/CTranslate2/quantization.html


int8_float32
int8_float32
int8_float32
int16
float32
float32



"""

from faster_whisper import WhisperModel

# english
audio_input = "audio_files_sources/english/sample_1.mp3"
file_output = "003_openai_whisper_en_sample_1_output.txt"

# spanish
# audio_input = "audio_files_sources/foreign/sp_sample_1.mp3"
# file_output = "003_openai_whisper_sp_sample_1_output.txt"


# model_size = "large-v2"
# model_size = "base"
model_size = "small"



# Run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")

# or run on CPU with INT8
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# segments, info = model.transcribe(audio_input, beam_size=1)

segments, info = model.transcribe(audio_input, beam_size=1, word_timestamps=True)


print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

for segment in segments:
    for word in segment.words:
        print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
