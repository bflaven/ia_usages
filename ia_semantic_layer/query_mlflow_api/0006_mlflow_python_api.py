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

conda install -c conda-forge mlflow
pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/mlflow_python_api/

# LAUNCH the file
python 0006_mlflow_python_api.py


MLflow Run Creation Script with MLflow Gateway/Deployments
Creates a run inside a specified MLflow experiment and calls the LLM model
through MLflow Gateway/Deployments using chat format.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025
"""

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.deployments import get_deploy_client
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


class MLflowLLMRunner:
    """
    Class to handle MLflow run creation with MLflow Gateway/Deployments inference
    """
    
    def __init__(self, tracking_uri: str, username: str, password: str, deployments_target: str):
        """
        Initialize the MLflow client with authentication
        
        Args:
            tracking_uri: The MLflow tracking server URL
            username: HTTP Basic Auth username
            password: HTTP Basic Auth password
            deployments_target: MLflow Gateway/Deployments target URL
        """
        self.tracking_uri = tracking_uri
        self.username = username
        self.password = password
        self.deployments_target = deployments_target
        self._setup_authentication()
        self.client = None
        self.deploy_client = None
        
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
        
        # Set deployments target
        os.environ['MLFLOW_DEPLOYMENTS_TARGET'] = self.deployments_target
        
        logger.info(f"Configured MLflow tracking URI: {self.tracking_uri}")
        logger.info(f"Configured MLflow deployments target: {self.deployments_target}")
        logger.info(f"Authentication credentials set for user: {self.username}")
        
    def initialize_client(self):
        """
        Initialize the MLflow tracking client
        """
        try:
            self.client = MlflowClient()
            logger.info("MLflow tracking client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MLflow client: {e}")
            return False
    
    def initialize_deploy_client(self):
        """
        Initialize the MLflow deployments client
        """
        try:
            self.deploy_client = get_deploy_client(self.deployments_target)
            logger.info("MLflow deployments client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MLflow deployments client: {e}")
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
    
    def call_gateway_model(
        self,
        endpoint_name: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 20000
    ) -> Dict[str, Any]:
        """
        Call MLflow Gateway/Deployments model to generate response using chat format
        
        Args:
            endpoint_name: Name of the gateway endpoint/route
            prompt: The prompt to send to the model
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with model response and metadata
        """
        try:
            logger.info(f"Calling MLflow Gateway endpoint: {endpoint_name}")
            logger.info(f"Gateway target: {self.deployments_target}")
            
            # Use CHAT format (messages) as expected by the gateway
            inputs = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            logger.info(f"Sending payload: {json.dumps(inputs, indent=2)}")
            
            # Call the gateway endpoint
            response = self.deploy_client.predict(
                endpoint=endpoint_name,
                inputs=inputs
            )
            
            logger.info(f"Response type: {type(response)}")
            logger.info(f"Full response structure: {json.dumps(response, indent=2) if isinstance(response, dict) else response}")
            
            # Extract output based on response format
            # For chat endpoints, response typically has 'choices' with 'message' or 'text'
            output_text = ""
            
            if isinstance(response, dict):
                # Print all keys to help debug
                logger.info(f"Response keys: {response.keys()}")
                
                # Try different possible chat response formats in order of likelihood
                if 'choices' in response and len(response['choices']) > 0:
                    first_choice = response['choices'][0]
                    logger.info(f"First choice structure: {first_choice}")
                    
                    # OpenAI-style chat response with message.content
                    if 'message' in first_choice:
                        message = first_choice['message']
                        output_text = message.get('content', '')
                    # Completions-style response with text
                    elif 'text' in first_choice:
                        output_text = first_choice['text']
                    # Direct content in choice
                    elif 'content' in first_choice:
                        output_text = first_choice['content']
                    else:
                        logger.warning(f"Unknown choice format: {first_choice}")
                        output_text = str(first_choice)
                
                # Ollama-style direct response
                elif 'response' in response:
                    output_text = response['response']
                
                # Direct message format
                elif 'message' in response:
                    if isinstance(response['message'], dict):
                        output_text = response['message'].get('content', str(response['message']))
                    else:
                        output_text = str(response['message'])
                
                # Other possible formats
                elif 'predictions' in response:
                    predictions = response['predictions']
                    output_text = predictions[0] if isinstance(predictions, list) and predictions else str(predictions)
                elif 'text' in response:
                    output_text = response['text']
                elif 'output' in response:
                    output_text = response['output']
                elif 'content' in response:
                    output_text = response['content']
                else:
                    logger.warning(f"Unknown response format, dumping entire response")
                    output_text = json.dumps(response)
                    
            elif isinstance(response, str):
                output_text = response
            elif isinstance(response, list) and len(response) > 0:
                output_text = str(response[0])
            else:
                output_text = str(response)
            
            logger.info(f"Extracted output text: {output_text[:200]}...")
            
            return {
                "success": True,
                "output": output_text,
                "raw_response": response
            }
            
        except Exception as e:
            logger.error(f"Error calling MLflow Gateway: {e}")
            import traceback
            traceback.print_exc()
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
        endpoint_name: str,
        temperature: float,
        max_tokens: int,
        additional_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a new run in the specified experiment with Gateway model inference
        
        Args:
            experiment_name: Name of the experiment
            run_name: Name for the run
            prompt_template: Prompt template with variables
            prompt_variables: Dictionary of variables to replace in template
            model_name: Name of the model (for logging)
            endpoint_name: Name of the gateway endpoint/route
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
        
        # Call the Gateway model
        logger.info("Calling MLflow Gateway to generate output...")
        llm_response = self.call_gateway_model(
            endpoint_name=endpoint_name,
            prompt=processed_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if not llm_response.get('success'):
            logger.error(f"LLM inference failed: {llm_response.get('error')}")
            return None
        
        output = llm_response.get('output', '')
        
        # Ensure output is not empty
        if not output or output.strip() == "":
            logger.error("LLM returned empty output!")
            logger.error(f"Raw response was: {llm_response.get('raw_response')}")
            return None
        
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
                
                # Log the output - this is the key field
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
                logger.info(f"stock_type: {prompt_variables.get('stock_type', 'N/A')}")
                logger.info(f"Output: {output}")
                
                return run_info
                
        except Exception as e:
            logger.error(f"Error creating run: {e}")
            import traceback
            traceback.print_exc()
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
    Main function to create MLflow run with Gateway model inference
    """
    
    # ============================================================================
    # CONFIGURATION - Modify these values for different runs
    # ============================================================================
    
    # MLflow Server Configuration
    MLFLOW_TRACKING_URI = "[site-mlflow]mlflow"
    USERNAME = "[username]"
    PASSWORD = "[password]"
    
    # MLflow Gateway/Deployments Configuration
    MLFLOW_DEPLOYMENTS_TARGET = "[site-mlflow]mlflow_gateway"
    
    # Gateway Endpoint/Route Name (chat endpoint)
    GATEWAY_ENDPOINT_NAME = "mistral-ollama"
    
    # Experiment Selection
    EXPERIMENT_NAME = "gold_dataset"
    
    # Prompt Template Configuration
    PROMPT_TEMPLATE = "I have an online store selling {{ stock_type }}. Write a one-sentence advertisement for use in social media."
    
    # Prompt Variables (replace {{ variable_name }} in template)
    PROMPT_VARIABLES = {
        # "stock_type": "books"
        "stock_type": "sportswear"
    }
    
    # LLM Model Configuration
    MODEL_NAME = "mistral-ollama"
    TEMPERATURE = 0.8
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
    print("MLflow LLM Runner - Gateway/Deployments with Chat Inference")
    print("="*80)
    print(f"MLflow Version: {mlflow.__version__}")
    print(f"Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"Deployments Target: {MLFLOW_DEPLOYMENTS_TARGET}")
    print(f"Gateway Endpoint: {GATEWAY_ENDPOINT_NAME}")
    print(f"Experiment: {EXPERIMENT_NAME}")
    print(f"Run Name: {RUN_NAME}")
    print("="*80)
    
    # Initialize the runner with credentials
    runner = MLflowLLMRunner(
        tracking_uri=MLFLOW_TRACKING_URI,
        username=USERNAME,
        password=PASSWORD,
        deployments_target=MLFLOW_DEPLOYMENTS_TARGET
    )
    
    # Initialize tracking client
    if not runner.initialize_client():
        logger.error("Failed to initialize MLflow tracking client. Exiting.")
        sys.exit(1)
    
    # Initialize deployments client
    if not runner.initialize_deploy_client():
        logger.error("Failed to initialize MLflow deployments client. Exiting.")
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
        print("\n[1] Creating MLflow run with Gateway inference...")
        run_info = runner.create_run_with_llm_inference(
            experiment_name=EXPERIMENT_NAME,
            run_name=RUN_NAME,
            prompt_template=PROMPT_TEMPLATE,
            prompt_variables=PROMPT_VARIABLES,
            model_name=MODEL_NAME,
            endpoint_name=GATEWAY_ENDPOINT_NAME,
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
            print(f"stock_type: {run_info['prompt_variables'].get('stock_type')}")
            print("-"*80)
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






