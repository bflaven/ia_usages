# ai_openai_whisper

Exploring the ability to extract text from audio file (.mp3) and video file (.mp4) with the help of Python libraries Whisper &Faster-Whisper and exposing this extraction feature through FastAPI.

Post on the Blog is coming soon at <a href="https://flaven.fr" target="_blank">https://flaven.fr</a>/


- whisper: <a href="https://openai.com/research/whisper" target="_blank" >https://openai.com/research/whisper</a>

- faster-whisper: <a href="https://github.com/guillaumekln/faster-whisper" target="_blank" >https://github.com/guillaumekln/faster-whisper</a></li>

- whisper on Github: <a href="https://github.com/openai/whisper" target="_blank" >https://github.com/openai/whisper</a>


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


