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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm




# launch the file
python 003_carbon_footprint_codecarbon_basic_usage.py

Codecarbon usage
https://mlco2.github.io/codecarbon/usage.html
https://asciinema.org/a/667970


"""

from codecarbon import EmissionsTracker

# Global variables
PROJECT_NAME = "BasicUsageExample"
MEASURE_POWER_SECS = 15

def compute_intensive_task():
    """Simulate a compute-intensive task."""
    result = 0
    for i in range(10**7):
        result += i
    return result

def main():
    """Main function to demonstrate basic CodeCarbon usage."""
    # Initialize the EmissionsTracker
    tracker = EmissionsTracker(project_name=PROJECT_NAME, measure_power_secs=MEASURE_POWER_SECS)
    
    # Start tracking emissions
    tracker.start()
    
    try:
        # Perform a compute-intensive task
        result = compute_intensive_task()
        print(f"Computation result: {result}")
    finally:
        # Stop tracking and print the emissions
        emissions = tracker.stop()
        print(f"Carbon emissions: {emissions} kg")

if __name__ == "__main__":
    main()

    

    
        
        

