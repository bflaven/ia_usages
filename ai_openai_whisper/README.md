# ai_openai_whisper

Exploring the ability to extract text from audio file (.mp3) and video file (.mp4) with the help of Python libraries Whisper &Faster-Whisper and exposing this extraction feature through FastAPI.

Check "Unlocking Speech-to-Text: Harnessing the Power of the OpenAI Whisper API with FastAPI Integration" <a href="https://wp.me/p3Vuhl-3gJ" target="_blank">https://wp.me/p3Vuhl-3gJ</a>/

- whisper: <a href="https://openai.com/research/whisper" target="_blank" >https://openai.com/research/whisper</a>

- faster-whisper: <a href="https://github.com/guillaumekln/faster-whisper" target="_blank" >https://github.com/guillaumekln/faster-whisper</a></li>

- whisper on Github: <a href="https://github.com/openai/whisper" target="_blank" >https://github.com/openai/whisper</a>


## FILES

**All files and directory described for this POC.**

- `001_openai_whisper.py`: minimum loading and usage of WHISPER
- `002_openai_whisper.py`: minimum loading and usage of WHISPER with languages (AR, ES, CN, RU, FR)
- `003_openai_whisper.py`: output the WHISPER transcription into a text file
- `004_openai_whisper_panda.py`: output the WHISPER transcription in a .cvs file with PANDA
- `005_openai_whisper.py`: WHISPER few attempts on languages detection (AR, ES, CN, RU, FR)
- `006_openai_whisper_pytube.py`: make WHISPER transcription for YOUTUBE video
- `006_openai_whisper_pytube_ffmpeg.py`: make WHISPER transcription for YOUTUBE video leveraging on FFMPEG
- `007_openai_whisper.py`: ditto to 001_openai_whisper.py
- `008_openai_whisper_fastapi.py`: Integration of WHISPER into FASTAPI to provide an POC for an API
- `009_openai_whisper_fastapi.py`: POC with WHISPER and FASTAPI, managing audio and video upload and extract transcription
- `010_request_files_fastapi.py`: Other way to managing files upload in FASTAPI
- `011_faster_whisper.py`: experiments with FASTER-WHISPER
- `012_openai_whisper.py`: build WHISPER transcription function
- `013_openai_whisper.py`: WHISPER transcription in different formats (.json, .srt, .tsv, .txt, .vtt)
- `README.md`: the readme for the main Github directory
- `audio_files_sources`: some audio samples in different languages
- `ffmpeg_python`: experiments with ffmpeg-python
- `output_srtfiles_writer`: output directory for transcription
- `prompts_chatgpt_samples.diff`: some prompts related to the post and to WHISPER
- `requirements.txt`: the python requirements for WHISPER
- `tests_from_whisper`: some tests (pytest) extracted from the original WHISPER project
- `video_download_from_yt`: output audio extraction from a YT video



## EXTRA INFOS

**Audio Transcription with Whisper - Environment**
```bash
# create an environment with anaconda
# Name: openai_whisper

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
```

**FFMPEG**
```bash
# INSTALL FFMPEG

# require ffmpeg install with homebrew 
brew doctor
brew cleanup
brew install ffmpeg

# check the install
ffmpeg -version

# presentation starts from 32:04 and ends at 1:13:59
# QA starts from 1:13:59
# https://www.metric-conversions.org/time/minutes-to-seconds.htm

# command example
# ffmpeg -ss 1924 -i "/content/earnings_call_microsoft_q4_2022.mp4/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515
"earnings_call_microsoft_q4_2022_filtered.mp4"

# command example
#ffmpeg -ss 1924 -i "/Users/brunoflaven/Documents/01_work/blog_articles/openai_whisper/test_earnings_call_microsoft_q4_2022/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515 "earnings_call_microsoft_q4_2022_filtered.mp4"

# command example
# ffmpeg -ss 1924 -i "test_earnings_call_microsoft_q4_2022/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515
"earnings_call_microsoft_q4_2022_filtered.mp4"


# requirements
pip install pytube
pip install ffmpeg-python

```
**PYTEST**
```bash


# launch the test
python -m pytest

# Run a single test and specify a function
pytest tests_from_whisper/test_normalizer.py::test_text_normalizer

# Run all test inside a specif files
pytest tests_from_whisper/test_audio.py
pytest tests_from_whisper/test_normalizer.py
pytest tests_from_whisper/test_tokenizer.py

# Collect information test suite / dry run
pytest tests_from_whisper/test_tokenizer.py --collect-only  

# Output verbose messages
pytest tests_from_whisper/test_tokenizer.py -v  

# Source:  https://gist.github.com/kwmiebach/3fd49612ef7a52b5ce3a


# Other commands
python -m pytest --disable-warnings
pytest -q tests_from_whisper/test_tokenizer.py --disable-warnings

--- requirements
pip install pytest
pip install scipy



```


