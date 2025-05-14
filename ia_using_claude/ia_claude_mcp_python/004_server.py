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
mcp install 004_server.py

# Alternatively, you can test it with the MCP Inspector:
mcp dev 004_server.py



Source: https://github.com/ApoorvV/mcp-claude-enhancements/tree/main/src
"""
from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime

mcp = FastMCP("ConversationSaver")

@mcp.tool()
def save_conversation(conversation: str) -> str:
    """Save the current conversation to a text file on the desktop"""
    desktop_path = os.path.expanduser("~/Desktop")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(desktop_path, f"claude_chat_{timestamp}.txt")
    try:
        with open(file_path, "w") as f:
            f.write(conversation)
        return f"Conversation saved at: {file_path}"
    except Exception as e:
        return f"Error saving conversation: {str(e)}"

if __name__ == "__main__":
    mcp.run()





