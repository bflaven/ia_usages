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
python 0005_mlflow_python_api.py



MLflow Run Creation Script with MLflow-Served Model Inference
Creates a run inside a specified MLflow experiment and calls the MLflow-served LLM model.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025
"""

import mlflow
from mlflow.tracking import MlflowClient
import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLflowLLMRunner:
    """
    Class to handle MLflow run creation with MLflow-served model inference
    """
    
    def __init__(self, tracking_uri: str, username: str, password: str, served_model_name: str):
        """
        Initialize the MLflow client with authentication
        
        Args:
            tracking_uri: The MLflow tracking server URL
            username: HTTP Basic Auth username
            password: HTTP Basic Auth password
            served_model_name: Name of the served model endpoint in MLflow
        """
        self.tracking_uri = tracking_uri
        self.username = username
        self.password = password
        self.served_model_name = served_model_name
        self.auth = (username, password)  # HTTP Basic Auth tuple
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
    
    def call_mlflow_served_model(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 20000
    ) -> Dict[str, Any]:
        """
        Call MLflow-served model to generate response
        
        Args:
            prompt: The prompt to send to the model
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with model response and metadata
        """
        # Construct the MLflow served model endpoint URL
        # Format: https://<mlflow-base-url>/model-endpoint/<model-name>/invocations
        base_url = self.tracking_uri.rstrip('/')
        endpoint_url = f"{base_url}/model-endpoint/{self.served_model_name}/invocations"
        
        # Prepare the payload for MLflow serving
        payload = {
            "inputs": {
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"Calling MLflow served model: {self.served_model_name}")
            logger.info(f"Endpoint URL: {endpoint_url}")
            
            response = requests.post(
                endpoint_url,
                json=payload,
                headers=headers,
                auth=self.auth,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract output based on MLflow serving response format
            if isinstance(result, dict):
                output_text = result.get('predictions', [''])[0] if 'predictions' in result else result.get('output', '')
            elif isinstance(result, list):
                output_text = result[0] if result else ''
            else:
                output_text = str(result)
            
            logger.info(f"Model response received: {output_text[:100]}...")
            
            return {
                "success": True,
                "output": output_text,
                "raw_response": result
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling MLflow served model: {e}")
            return {
                "success": False,
                "error": str(e),
                "output": None
            }
    
    def create_run_with_llm_inference(
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
        Create a new run in the specified experiment with MLflow-served model inference
        
        Args:
            experiment_name: Name of the experiment
            run_name: Name for the run
            prompt_template: Prompt template with variables
            prompt_variables: Dictionary of variables to replace in template
            model_name: Name of the served model
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
        
        # Call the MLflow-served model
        logger.info("Calling MLflow-served model to generate output...")
        llm_response = self.call_mlflow_served_model(
            prompt=processed_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if not llm_response.get('success'):
            logger.error(f"LLM inference failed: {llm_response.get('error')}")
            return None
        
        output = llm_response.get('output', '')
        
        try:
            # Start a new MLflow run
            with mlflow.start_run(
                experiment_id=experiment.experiment_id,
                run_name=run_name
            ) as run:
                
                # Log the prompt template
                mlflow.log_param("prompt_template", prompt_template)
                
                # Log prompt variables individually
                for var_name, var_value in prompt_variables.items():
                    mlflow.log_param(var_name, var_value)
                
                # Log model parameters
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("temperature", temperature)
                mlflow.log_param("max_tokens", max_tokens)
                
                # Log the output
                mlflow.log_param("output", output)
                
                # Log additional parameters if provided
                if additional_params:
                    for key, value in additional_params.items():
                        mlflow.log_param(key, value)
                
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
                    "output": output,
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed"
                }
                
                logger.info(f"Run created successfully: {run.info.run_id}")
                logger.info(f"Run name: {run_name}")
                logger.info(f"Experiment: {experiment_name}")
                logger.info(f"Output: {output}")
                
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
    Main function to create MLflow run with MLflow-served model inference
    """
    
    # ============================================================================
    # CONFIGURATION - Modify these values for different runs
    # ============================================================================
    
    # MLflow Server Configuration
    MLFLOW_TRACKING_URI = "[site-mlflow]mlflow"
    USERNAME = "[username]"
    PASSWORD = "[password]"
    
    # MLflow Served Model Configuration
    # This is the name of your model deployment endpoint in MLflow
    SERVED_MODEL_NAME = "mistral-ollama"
    
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
    print("MLflow LLM Runner - Prompt Template Testing with MLflow Serving")
    print("="*80)
    print(f"MLflow Version: {mlflow.__version__}")
    print(f"Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"Served Model: {SERVED_MODEL_NAME}")
    print(f"Experiment: {EXPERIMENT_NAME}")
    print(f"Run Name: {RUN_NAME}")
    print("="*80)
    
    # Initialize the runner with credentials
    runner = MLflowLLMRunner(
        tracking_uri=MLFLOW_TRACKING_URI,
        username=USERNAME,
        password=PASSWORD,
        served_model_name=SERVED_MODEL_NAME
    )
    
    # Initialize client
    if not runner.initialize_client():
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
        
        # Create the run with LLM inference
        print("\n[1] Creating MLflow run with MLflow-served model inference...")
        run_info = runner.create_run_with_llm_inference(
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
            print("-"*80)
            print(f"OUTPUT: {run_info['output']}")
            print("="*80)
            
            # Save run information to JSON
            print("\n[2] Saving run information to JSON...")
            runner.save_run_to_json(run_info, OUTPUT_JSON_FILE)
            
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
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

