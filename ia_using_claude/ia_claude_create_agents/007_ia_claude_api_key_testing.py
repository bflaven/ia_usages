#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name mcp_server_demo python=3.9.13
conda info --envs
source activate mcp_server_demo
conda deactivate

# BURN AFTER READING
source activate mcp_server_demo

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n mcp_server_demo


# install packages with pip
python -m pip install requests python-dotenv
python -m pip install anthropic


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/000_ia_generate_slides/ia_create_agents


# launch the file
python 007_ia_claude_api_key_testing.py




"""
CLAUDE_API_KEY = "type-your-api-key-for-claude"

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=CLAUDE_API_KEY,
)
message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)



