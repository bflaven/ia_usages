#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_debunk python=3.9.13
conda create --name carbon_footprint python=3.9.13
conda info --envs
source activate ia_debunk
source activate carbon_footprint
conda deactivate


# BURN AFTER READING
source activate ia_debunk
source activate carbon_footprint

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_debunk
conda env remove -n carbon_footprint

# install packages
python -m pip install streamlit 
python -m pip install codecarbon


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/



# launch the file
python 003_carbon_footprint_codecarbon_basic_usage.py

Codecarbon usage
https://mlco2.github.io/codecarbon/usage.html
https://asciinema.org/a/667970


"""

from codecarbon import track_emissions

# Global variables
PROJECT_NAME = "DecoratorExample"

@track_emissions(project_name=PROJECT_NAME)
def process_data(data):
    """
    Process the given data and return the result.
    
    Args:
        data (list): Input data to process.
    
    Returns:
        list: Processed data.
    """
    return [x ** 2 for x in data]

def main():
    """Main function to demonstrate CodeCarbon decorator usage."""
    input_data = list(range(1, 1000001))
    result = process_data(input_data)
    print(f"Processed {len(result)} items")

if __name__ == "__main__":
    main()

    

    
        
        

