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
pip install uv

pip install mcp
pip install typer



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/000_ia_generate_slides/ia_mcp_python/


# launch the file

# You can install this server in Claude Desktop and interact with it right away by running:
mcp install 001_server.py

# Alternatively, you can test it with the MCP Inspector:
mcp dev 001_server.py

pip install 'mcp[cli]'
uv run --with mcp mcp run server.py



Need to install the following packages:
@modelcontextprotocol/inspector@0.8.2


python --version
conda update conda
conda install python=3.11
conda search python
conda update --all







"""

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

