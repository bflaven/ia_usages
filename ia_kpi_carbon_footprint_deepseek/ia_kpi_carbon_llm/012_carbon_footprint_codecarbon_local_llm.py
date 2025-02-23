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
python -m pip install tensorflow
python -m pip install ollama


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm




# launch the file
python 012_carbon_footprint_codecarbon_local_llm.py

Codecarbon usage
https://mlco2.github.io/codecarbon/usage.html
https://asciinema.org/a/667970

https://mlco2.github.io/codecarbon/examples.html#using-the-explicit-object
https://github.com/mlco2/codecarbon/tree/master/examples

# remove model
ollama run mistral:latest
ollama rm mistral:latest

ollama run mistral-poet:latest
ollama rm mistral-poet:latest

# create model with modefile
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/

ollama create mistral-poet -f Modelfile_mistral_poet


"""
import os
import time
import ollama
from codecarbon import EmissionsTracker
import json
from typing import List, Dict
import logging
import warnings

# Suppress the FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_poems(model: str, n_poems: int) -> List[str]:
    """
    Generates poems using the specified model.
    
    Args:
        model (str): The name of the Ollama model to use
        n_poems (int): Number of poems to generate
    
    Returns:
        List[str]: List of generated poems
    """
    poems = []
    for i in range(n_poems):
        try:
            response = ollama.chat(model=model, 
                                 messages=[{
                                     'role': 'user', 
                                     'content': 'Write a poem for me about open source software'
                                 }])
            poems.append(response['message']['content'])
            logger.info(f"Generated poem {i+1}/{n_poems}")
            # Add a small delay to prevent overwhelming the API
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error generating poem {i+1}: {e}")
    
    return poems

def save_results(poems: List[str], emissions: float, output_file: str = "poetry_results.json"):
    """
    Saves the generated poems and emissions data to a JSON file.
    """
    results = {
        "poems": poems,
        "emissions": emissions,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")

def main():
    # Configuration
    MODEL_NAME = "mistral-poet"  # Use the existing mistral-poet model
    N_POEMS = 2
    OUTPUT_DIR = "emissions"
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Log that we're using an existing model
    logger.info(f"Using existing model: {MODEL_NAME}")
    
    # Initialize emissions tracker with local saving only
    tracker = EmissionsTracker(
        save_to_api=False,  # Disable API saving
        output_dir=OUTPUT_DIR,
        tracking_mode="process",
        log_level='warning'
    )
    
    # Start tracking emissions
    tracker.start()
    logger.info("Started emissions tracking")
    
    # Generate poems
    poems = generate_poems(MODEL_NAME, N_POEMS)
    
    # Stop tracking and get emissions
    emissions = tracker.stop()
    logger.info(f"Total emissions: {emissions:.4f} kg CO2eq")
    
    # Print the generated poems
    for i, poem in enumerate(poems):
        print(f"\nPoem {i+1}:\n{poem}")
    
    # Save results
    save_results(poems, emissions)

if __name__ == "__main__":
    main()




        

