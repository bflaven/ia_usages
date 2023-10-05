#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name fastapi_database python=3.9.13
conda info --envs
source activate ner_spacy_fastapi_database
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_spacy_fastapi_database

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/003_bugbytes_io_crud_api_fastapi_sqlmodel/

# LAUNCH THE FILE
python database.py


Source: https://bugbytes.io/posts/setting-up-sqlmodel/

"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

# There should be one engine for the entire application
DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

class TrackModel(SQLModel, table=True):
    # Note: Optional fields are marked as Nullable in the database
    __tablename__ = 'track'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    artist: str
    duration: float
    last_play: datetime


def create_tables():
    """Create the tables registered with SQLModel.metadata (i.e classes with table=True).
    More info: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata
    """
    SQLModel.metadata.create_all(engine)
    print(f'database'+DB_FILE+' and tables has been created')

if __name__ == '__main__':
    # creates the table if this file is run independently, as a script
    create_tables()

