
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]




# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/tagging_entity_extraction/project_6_spacy_experiences/

[file]
python 006_project_6_spacy_experiences_import_package.py

Source: https://www.codingem.com/what-is-init-py-file-in-python/

"""

import my_package
print(my_package.myVar)  # Outputs "Hello world"



