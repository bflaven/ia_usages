#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name fastapi_database python=3.9.13
conda info --envs
source activate fastapi_database
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fastapi_database

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/002_bugbytes_io_crud_api_fastapi/

# LAUNCH THE API
python show_records.py

Source: https://bugbytes.io/posts/creating-a-music-track-api-with-fastapi-in-python/

"""
import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
except sqlite3.OperationalError:
    print("You need to create the database - python database.py")
else:
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM track").fetchone()[0]
    print(f"There are {count} records in the Track table")
finally:
    conn.close()