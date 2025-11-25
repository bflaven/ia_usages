#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name dbt_env python=3.9.13
conda info --envs
source activate dbt_env
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n dbt_env


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests


# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/mlflow_python_api/

# LAUNCH the file
python 0003_mlflow_python_api.py

MLflow Experiments Listing Script
Connects to a remote MLflow server with HTTP Basic Authentication
and retrieves all experiments.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025

"""

#!/usr/bin/env python3
"""
MLflow Run Creation Script with Prompt Template
Creates a run inside a specified MLflow experiment with configurable parameters
for LLM prompt testing and evaluation.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025
"""

import mlflow
from mlflow.tracking import MlflowClient
import os
import sys
import json
from datetime import datetime
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLflowRunCreator:
    """
    Class to handle MLflow run creation with prompt templates and LLM parameters
    """
    
    def __init__(self, tracking_uri: str, username: str, password: str):
        """
        Initialize the MLflow client with authentication
        
        Args:
            tracking_uri: The MLflow tracking server URL
            username: HTTP Basic Auth username
            password: HTTP Basic Auth password
        """
        self.tracking_uri = tracking_uri
        self.username = username
        self.password = password
        self._setup_authentication()
        self.client = None
        
    def _setup_authentication(self):
        """
        Set up authentication credentials in environment variables
        MLflow uses these for HTTP Basic Authentication
        """
        # Set authentication credentials as environment variables
        os.environ['MLFLOW_TRACKING_USERNAME'] = self.username
        os.environ['MLFLOW_TRACKING_PASSWORD'] = self.password
        
        # Set the tracking URI
        mlflow.set_tracking_uri(self.tracking_uri)
        
        logger.info(f"Configured MLflow tracking URI: {self.tracking_uri}")
        logger.info(f"Authentication credentials set for user: {self.username}")
        
    def initialize_client(self):
        """
        Initialize the MLflow client
        """
        try:
            self.client = MlflowClient()
            logger.info("MLflow client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MLflow client: {e}")
            return False
    
    def get_experiment_by_name(self, experiment_name: str):
        """
        Get experiment by name
        
        Args:
            experiment_name: Name of the experiment
            
        Returns:
            Experiment object or None if not found
        """
        try:
            experiment = self.client.get_experiment_by_name(experiment_name)
            if experiment:
                logger.info(f"Found experiment: {experiment_name} (ID: {experiment.experiment_id})")
                return experiment
            else:
                logger.error(f"Experiment '{experiment_name}' not found")
                return None
        except Exception as e:
            logger.error(f"Error getting experiment: {e}")
            return None
    
    def replace_template_variables(self, prompt_template: str, variables: Dict[str, str]) -> str:
        """
        Replace template variables in prompt with actual values
        
        Args:
            prompt_template: Prompt template with {{ variable }} placeholders
            variables: Dictionary of variable names and their values
            
        Returns:
            Processed prompt with variables replaced
        """
        processed_prompt = prompt_template
        for var_name, var_value in variables.items():
            placeholder = f"{{{{ {var_name} }}}}"
            processed_prompt = processed_prompt.replace(placeholder, var_value)
        
        logger.info(f"Processed prompt: {processed_prompt}")
        return processed_prompt
    
    def create_run_with_prompt(
        self,
        experiment_name: str,
        run_name: str,
        prompt_template: str,
        prompt_variables: Dict[str, str],
        model_name: str,
        temperature: float,
        max_tokens: int,
        additional_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a new run in the specified experiment with prompt and LLM parameters
        
        Args:
            experiment_name: Name of the experiment
            run_name: Name for the run
            prompt_template: Prompt template with variables
            prompt_variables: Dictionary of variables to replace in template
            model_name: Name of the LLM model
            temperature: Temperature parameter for model
            max_tokens: Maximum tokens for model response
            additional_params: Additional parameters to log
            
        Returns:
            Dictionary with run information and results
        """
        # Get the experiment
        experiment = self.get_experiment_by_name(experiment_name)
        if not experiment:
            logger.error(f"Cannot create run: experiment '{experiment_name}' not found")
            return None
        
        # Process the prompt template
        processed_prompt = self.replace_template_variables(prompt_template, prompt_variables)
        
        try:
            # Start a new MLflow run
            with mlflow.start_run(
                experiment_id=experiment.experiment_id,
                run_name=run_name
            ) as run:
                
                # Log the prompt template and variables
                mlflow.log_param("prompt_template", prompt_template)
                mlflow.log_param("processed_prompt", processed_prompt)
                
                # Log prompt variables
                for var_name, var_value in prompt_variables.items():
                    mlflow.log_param(f"prompt_var_{var_name}", var_value)
                
                # Log model parameters
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("temperature", temperature)
                mlflow.log_param("max_tokens", max_tokens)
                
                # Log additional parameters if provided
                if additional_params:
                    for key, value in additional_params.items():
                        mlflow.log_param(key, value)
                
                # Log timestamp
                mlflow.log_param("run_timestamp", datetime.now().isoformat())
                
                # Prepare run information
                run_info = {
                    "run_id": run.info.run_id,
                    "run_name": run_name,
                    "experiment_id": experiment.experiment_id,
                    "experiment_name": experiment_name,
                    "prompt_template": prompt_template,
                    "prompt_variables": prompt_variables,
                    "processed_prompt": processed_prompt,
                    "model_name": model_name,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed"
                }
                
                # Add additional params to run_info
                if additional_params:
                    run_info["additional_params"] = additional_params
                
                logger.info(f"Run created successfully: {run.info.run_id}")
                logger.info(f"Run name: {run_name}")
                logger.info(f"Experiment: {experiment_name}")
                
                return run_info
                
        except Exception as e:
            logger.error(f"Error creating run: {e}")
            return None
    
    def save_run_to_json(self, run_info: Dict[str, Any], output_file: str):
        """
        Save run information to a JSON file
        
        Args:
            run_info: Dictionary containing run information
            output_file: Output JSON file path
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(run_info, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Run information saved to {output_file}")
            print(f"\n✓ Run data exported to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving run to JSON: {e}")


def generate_timestamp() -> str:
    """
    Generate timestamp in format: YYYYMMDD-HHMMSS
    """
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def main():
    """
    Main function to create MLflow run with prompt template
    """
    
    # ============================================================================
    # CONFIGURATION - Modify these values for different runs
    # ============================================================================
    
    # MLflow Server Configuration
    MLFLOW_TRACKING_URI = "[site-mlflow]mlflow"
    USERNAME = "[username]"
    PASSWORD = "[password]"
    
    # Experiment Selection
    EXPERIMENT_NAME = "gold_dataset"
    
    # Prompt Template Configuration
    PROMPT_TEMPLATE = "I have an online store selling {{ stock_type }}. Write a one-sentence advertisement for use in social media."
    
    # Prompt Variables (replace {{ variable_name }} in template)
    PROMPT_VARIABLES = {
        "stock_type": "books"
    }
    
    # LLM Model Configuration
    MODEL_NAME = "mistral-ollama"
    TEMPERATURE = 0.2
    MAX_TOKENS = 20000
    
    # Run Name Configuration (with timestamp)
    timestamp = generate_timestamp()
    RUN_NAME = f"bf-auto-{timestamp}"
    
    # Output JSON file name (with timestamp)
    OUTPUT_JSON_FILE = f"bf-auto-{timestamp}.json"
    
    # Additional Parameters (optional)
    ADDITIONAL_PARAMS = {
        "created_by": "python_script",
        "purpose": "prompt_testing"
    }
    
    # ============================================================================
    # END CONFIGURATION
    # ============================================================================
    
    print("="*80)
    print("MLflow Run Creator - Prompt Template Testing")
    print("="*80)
    print(f"MLflow Version: {mlflow.__version__}")
    print(f"Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"Experiment: {EXPERIMENT_NAME}")
    print(f"Run Name: {RUN_NAME}")
    print("="*80)
    
    # Initialize the run creator with credentials
    creator = MLflowRunCreator(
        tracking_uri=MLFLOW_TRACKING_URI,
        username=USERNAME,
        password=PASSWORD
    )
    
    # Initialize client
    if not creator.initialize_client():
        logger.error("Failed to initialize MLflow client. Exiting.")
        sys.exit(1)
    
    try:
        # Display configuration
        print("\n" + "-"*80)
        print("RUN CONFIGURATION:")
        print("-"*80)
        print(f"Prompt Template: {PROMPT_TEMPLATE}")
        print(f"Prompt Variables: {PROMPT_VARIABLES}")
        print(f"Model: {MODEL_NAME}")
        print(f"Temperature: {TEMPERATURE}")
        print(f"Max Tokens: {MAX_TOKENS}")
        print(f"Output File: {OUTPUT_JSON_FILE}")
        print("-"*80)
        
        # Create the run
        print("\n[1] Creating MLflow run...")
        run_info = creator.create_run_with_prompt(
            experiment_name=EXPERIMENT_NAME,
            run_name=RUN_NAME,
            prompt_template=PROMPT_TEMPLATE,
            prompt_variables=PROMPT_VARIABLES,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            additional_params=ADDITIONAL_PARAMS
        )
        
        if run_info:
            print("\n" + "="*80)
            print("RUN CREATED SUCCESSFULLY")
            print("="*80)
            print(f"Run ID: {run_info['run_id']}")
            print(f"Run Name: {run_info['run_name']}")
            print(f"Experiment: {run_info['experiment_name']}")
            print(f"Processed Prompt: {run_info['processed_prompt']}")
            print("="*80)
            
            # Save run information to JSON
            print("\n[2] Saving run information to JSON...")
            creator.save_run_to_json(run_info, OUTPUT_JSON_FILE)
            
            print("\n" + "="*80)
            print("✓ Script completed successfully")
            print(f"✓ View your run in MLflow UI at: {MLFLOW_TRACKING_URI}")
            print("="*80)
        else:
            logger.error("Failed to create run")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()







