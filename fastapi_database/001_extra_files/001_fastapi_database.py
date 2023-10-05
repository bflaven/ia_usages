#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name ner_spacy_fastapi_database python=3.9.13
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
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/001_extra_files/

# LAUNCH THE FILE
python 001_fastapi_database.py

"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///example.db', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)


session = Session()
# record_1
user_1 = User(name='Guido Italo', email='guido.italo@example.com')
session.add(user_1)
session.commit()

# record_2
user_2 = User(name='Prisca Jore', email='prisca.jore@example.com')
session.add(user_2)
session.commit()

print('\n--- first row')
# user = session.query(User).filter_by(name='Guido Italo').first()
user = session.query(User).first()
print(user.name, user.email)

print('\n--- all users')
users = session.query(User).all()
for count, user in enumerate(users):
   print(count, user.name, user.email)


print('\n--- success')
print('The db has been created example.db and two records has been added. See above')


