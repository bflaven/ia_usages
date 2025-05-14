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
mcp install 005_server.py

# Alternatively, you can test it with the MCP Inspector:
mcp dev 005_server.py



Source: https://github.com/ApoorvV/mcp-claude-enhancements/tree/main/src
"""

from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server named "FileCounter"
mcp = FastMCP("FileCounter")

@mcp.tool()
def count_desktop_files() -> str:
    """Count the number of files on the desktop"""
    desktop_path = os.path.expanduser("~/Desktop")  # Gets desktop path (e.g., /Users/apoorv/Desktop)
    try:
        # List all items in desktop directory, filter to files only
        files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]
        file_count = len(files)
        return f"There are {file_count} files on your desktop."
    except Exception as e:
        return f"Error counting files: {str(e)}"

if __name__ == "__main__":
    mcp.run()




