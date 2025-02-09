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
python -m pip install streamlit

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/examples_codecarbon_master


# launch the file
python 001_api_call_demo.py

CODECARBON
Estimate and track carbon emissions from your computer, quantify and analyze their impact.
See https://github.com/mlco2/codecarbon/tree/master/examples


"""

import time

from codecarbon import track_emissions


@track_emissions(
    # api_endpoint="http://your api if you want",
    # experiment_id="3a202149-8be2-408c-a3d8-baeae2de2987",
    api_endpoint="    https://fooapi.com/api/todos",
    experiment_id="test3a202149-8be2-408c-a3d8-baeae2de2987",
    api_key="",
    save_to_api=True,


)
def train_model():
    """
    This function will do nothing during (occurrence * delay) seconds.
    The Code Carbon API will be called every (measure_power_secs * api_call_interval)
    seconds.
    """
    occurrence = 60 * 24
    delay = 60  # Seconds
    for i in range(occurrence):
        print(f"{occurrence * delay - i * delay} seconds before ending script...")
        time.sleep(delay)


if __name__ == "__main__":
    train_model()
