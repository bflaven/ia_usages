# 001a_giladd123_nllb_fastapi



## Original readme nllb-fastapi

This is a simple implementation of an api server that uses nllb and ctranslate2 to translate text to different languages

## Prerequisites

This was written in python-3.10 and might not work with older versions of python.

## Setting up the server

1. Install python requirements `pip install -r requirements.txt`
2. Change model to ct2 format `ct2-transformers-converter --model <model_dir> --output_dir=<output_dir>`
3. Start the server by running `python webserver.py --tokenizer-dir <tokenizer_dir> --model-dir <ct2_model_dir>`

Notice that the tokenizer dir is the regular model directory (as gotten from huggingface), left only with the tokenizer files (model files can be left in but are heavy):

```
config.json
special_tokens_map.json
tokenizer_config.json
tokenizer.json
```
