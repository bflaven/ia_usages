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
pip install "mcp[cli]"
pip install mcp
python -m pip install mcp



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/000_ia_generate_slides/ia_mcp_python/


# launch the file

# You can install this server in Claude Desktop and interact with it right away by running:
mcp install 002_server.py

# Alternatively, you can test it with the MCP Inspector:
mcp dev 002_server.py


python 002_server.py

count the number of Rs in the word "astronomy" using the "count-r" tool
count the number of Rs in the word "strawberry" using the "count-r" tool

"""
from mcp.server.fastmcp import FastMCP
import time
import signal
import sys

# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    print("Shutting down server gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create an MCP server with increased timeout
mcp = FastMCP(
    name="count-r",
    host="127.0.0.1",
    port=5000,
    # Add this to make the server more resilient
    timeout=30  # Increase timeout to 30 seconds
)

# Define our tool
@mcp.tool()
def count_r(word: str) -> int:
    """Count the number of 'r' letters in a given word."""
    try:
        # Add robust error handling
        if not isinstance(word, str):
            return 0
        return word.lower().count("r")
    except Exception as e:
        # Return 0 on any error
        return 0

if __name__ == "__main__":
    try:
        print("Starting MCP server 'count-r' on 127.0.0.1:5000")
        # Use this approach to keep the server running
        mcp.run()
    except Exception as e:
        print(f"Error: {e}")
        # Sleep before exiting to give time for error logs
        time.sleep(5)



