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



"""
import os
import time
import ollama
from codecarbon import EmissionsTracker
import json
from typing import List, Dict
import logging

# Suppress the FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_custom_model() -> bool:
    """
    Creates a custom model based on deepseek-r1 with specific parameters.
    Returns True if successful, False otherwise.
    """
    modelfile = '''
    FROM deepseek-r1:latest
    SYSTEM You are a poet but you like to keep it simple
    PARAMETER temperature 5
    '''
    
    try:
        # Write modelfile to a temporary file
        with open('Modelfile', 'w') as f:
            f.write(modelfile)
        
        # Create the model using the Modelfile
        os.system('ollama create poetry-model -f Modelfile')
        
        # Clean up the temporary file
        os.remove('Modelfile')
        
        logger.info("Custom model created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating custom model: {e}")
        return False

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
    MODEL_NAME = "poetry-model"  # Our custom model name
    N_POEMS = 2
    OUTPUT_DIR = "emissions"
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create custom model
    if not create_custom_model():
        logger.error("Failed to create custom model. Exiting.")
        return

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
    
    # Save results
    save_results(poems, emissions)

if __name__ == "__main__":
    main()






        

