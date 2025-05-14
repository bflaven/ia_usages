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
python 009_ia_claude_api_key_testing.py




"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key with explicit fallback
API_KEY = os.getenv("CLAUDE_API_KEY")
if not API_KEY:
    API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Try alternative name

if not API_KEY:
    print("No API key found. Please enter your Claude API key:")
    API_KEY = input("> ").strip()

# Print first few characters of API key
if API_KEY:
    print(f"API key loaded (starts with: {API_KEY[:6]}...)")
else:
    print("No API key provided!")
    exit(1)

# Very simple test request
url = "https://api.anthropic.com/v1/messages"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "anthropic-version": "2023-06-01"
}

# Simplest possible request body
data = {
    "model": "claude-3-sonnet-20240229",
    "messages": [
        {"role": "user", "content": "Hello, this is a test."}
    ],
    "max_tokens": 100
}

print("\nSending test request to Claude API...")
response = requests.post(url, headers=headers, json=data)

print(f"Response status code: {response.status_code}")
print(f"Response body: {response.text[:500]}...")

if response.status_code == 200:
    print("\nSUCCESS! Your Claude API connection is working correctly.")
else:
    print("\nERROR: API request failed.")
    print("\nCommon issues and solutions:")
    print("1. Make sure your API key is correct and active")
    print("2. Check if your API key should include 'sk-' prefix")
    print("3. Your account may not have access to the model requested")
    print("4. Try wrapping the key in a different environment variable")
    
    print("\nDebug information:")
    print(f"- API URL: {url}")
    print(f"- Headers: Content-Type, Authorization (Bearer), anthropic-version: 2023-06-01")
    print(f"- Model requested: claude-3-sonnet-20240229")






