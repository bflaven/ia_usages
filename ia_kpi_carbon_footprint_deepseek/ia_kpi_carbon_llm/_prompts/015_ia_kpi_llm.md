
# 012_ia_kpi_llm.md



## INPUT_1
rewrite the complete two files with the same and correct the error. 
```text
    ollama.create(model='mistral:latest', modelfile=modelfile)
TypeError: create() got an unexpected keyword argument 'modelfile'
```


```python
# PART_1
import ollama
from codecarbon import EmissionsTracker
# PART_2

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd


## PART_1
"""
modelfile='''
FROM llama2-uncensored
SYSTEM You are a poet but you like to keep it simple
PARAMETER temperature 5
'''
"""

# modelfile='''
# FROM deepseek-r1:latest
# SYSTEM You are a poet but you like to keep it simple
# PARAMETER temperature 5
# '''

modelfile='''
FROM mistral:latest
SYSTEM You are a poet but you like to keep it simple
PARAMETER temperature 5
'''



# ollama.create(model='deepseek-r1:latest', modelfile=modelfile)
# tracker = EmissionsTracker(save_to_api=True, tracking_mode="process")
# # You need to pull the model from the CLI
# model = "deepseek-r1:latest" 


ollama.create(model='mistral:latest', modelfile=modelfile)
tracker = EmissionsTracker(save_to_api=True, tracking_mode="process")
# You need to pull the model from the CLI
model = "mistral:latest"

# up to 5 
n_poems = 1

# Start tracking
tracker.start()
poems = []
for i in range(n_poems):
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': 'Write a poem for me about open source software'}])
    poems.append(response['message']['content'])

emmissions = tracker.stop()

```



## prompt_2

Change this script to make it work with the model mistral-poet

```python
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
```
