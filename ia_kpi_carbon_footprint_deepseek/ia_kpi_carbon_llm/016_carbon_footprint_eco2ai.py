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


python -m pip install eco2ai

country_iso_code for france
FR  FRA 250
https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes



python -m pip install --upgrade eco2ai


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/



# launch the file
python 016_carbon_footprint_eco2ai.py

Eco2AI usage
https://github.com/sb-ai-lab/Eco2AI


"""

import os
import time
import ollama
import eco2ai
import json
from typing import List
import logging

# Suppress the FutureWarning
# warnings.simplefilter(action='ignore', category=FutureWarning)
# warnings.simplefilter(action='ignore', category=UserWarning)


# Constants
MODEL_NAME = "poetry-model"
N_POEMS = 2
OUTPUT_DIR = "emissions"
OUTPUT_FILE = "poetry_results.json"
COUNTRY_CODE = "FR"  # ISO Alpha-2 code for France (assuming CET timezone)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PoemGenerator:
    def __init__(self, model_name: str, n_poems: int):
        self.model_name = model_name
        self.n_poems = n_poems
        self.tracker = eco2ai.Tracker(
            project_name="Poetry Generation",
            experiment_description="Generating poems using Ollama model"
        )
        # Set the country code manually if the method exists
        if hasattr(self.tracker, 'set_country_code'):
            self.tracker.set_country_code(COUNTRY_CODE)

    def create_custom_model(self) -> bool:
        modelfile = '''
        FROM deepseek-r1:latest
        SYSTEM You are a poet but you like to keep it simple
        PARAMETER temperature 5
        '''
        
        try:
            with open('Modelfile', 'w') as f:
                f.write(modelfile)
            
            os.system(f'ollama create {self.model_name} -f Modelfile')
            os.remove('Modelfile')
            
            logger.info("Custom model created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating custom model: {e}")
            return False

    def generate_poems(self) -> List[str]:
        poems = []
        for i in range(self.n_poems):
            try:
                response = ollama.chat(model=self.model_name, 
                                     messages=[{
                                         'role': 'user', 
                                         'content': 'Write a poem for me about open source software'
                                     }])
                poems.append(response['message']['content'])
                logger.info(f"Generated poem {i+1}/{self.n_poems}")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error generating poem {i+1}: {e}")
        
        return poems

    def save_results(self, poems: List[str], emissions: float):
        results = {
            "poems": poems,
            "emissions": emissions,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(results, f, indent=4)
            logger.info(f"Results saved to {OUTPUT_FILE}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")

    def run(self):
        if not self.create_custom_model():
            logger.error("Failed to create custom model. Exiting.")
            return

        self.tracker.start()
        logger.info("Started emissions tracking")
        
        poems = self.generate_poems()
        
        self.tracker.stop()
        emissions = self.tracker.get_emissions()
        logger.info(f"Total emissions: {emissions:.4f} kg CO2eq")
        
        self.save_results(poems, emissions)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    generator = PoemGenerator(MODEL_NAME, N_POEMS)
    generator.run()

if __name__ == "__main__":
    main()






        

