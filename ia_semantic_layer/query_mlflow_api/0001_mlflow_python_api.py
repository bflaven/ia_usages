#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[check]
pip --version
python --version

[env]
Recommended: Use Built-in venv

Create a new environment:
python -m venv mlflow_python_api

Activate the environment:
source mlflow_python_api/bin/activate

Install packages inside the environment:
pip install package_name

pip install mlflow
pip install mlflow==3.3.1
python -m pip install mlflow==3.3.1

python -m pip install --upgrade pip setuptools wheel

brew install cmake
brew install apache-arrow
export CMAKE_PREFIX_PATH=$(brew --prefix apache-arrow)/lib/cmake


Deactivate:
deactivate

To easily reproduce environments:
pip freeze > requirements.txt

Install everything in a new environment:
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/mlflow_python_api/

# LAUNCH the file
python 0001_mlflow_python_api.py

MLflow Experiments Listing Script
Connects to a remote MLflow server with HTTP Basic Authentication
and retrieves all experiments.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025
"""

import mlflow
from mlflow.tracking import MlflowClient
import os
import sys
from typing import List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLflowExperimentLister:
    """
    Class to handle MLflow experiments listing with HTTP Basic Authentication
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
        # MLflow will automatically use these for HTTP Basic Auth
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
    
    def list_all_experiments(self) -> List:
        """
        List all experiments from the MLflow tracking server
        
        Returns:
            List of Experiment objects
        """
        try:
            # Search for all experiments
            # By default, this returns active experiments
            experiments = self.client.search_experiments()
            
            logger.info(f"Found {len(experiments)} experiments")
            return experiments
            
        except Exception as e:
            logger.error(f"Error listing experiments: {e}")
            return []
    
    def list_all_experiments_including_deleted(self) -> List:
        """
        List all experiments including deleted ones
        
        Returns:
            List of Experiment objects including deleted ones
        """
        try:
            # ViewType.ALL includes active and deleted experiments
            from mlflow.entities import ViewType
            experiments = self.client.search_experiments(
                view_type=ViewType.ALL
            )
            
            logger.info(f"Found {len(experiments)} experiments (including deleted)")
            return experiments
            
        except Exception as e:
            logger.error(f"Error listing experiments: {e}")
            return []
    
    def print_experiment_details(self, experiments: List):
        """
        Print detailed information about experiments
        
        Args:
            experiments: List of Experiment objects
        """
        if not experiments:
            print("\nNo experiments found.")
            return
        
        print("\n" + "="*80)
        print(f"EXPERIMENTS LIST - Total: {len(experiments)}")
        print("="*80)
        
        for idx, exp in enumerate(experiments, 1):
            print(f"\n{idx}. Experiment Details:")
            print(f"   Name: {exp.name}")
            print(f"   Experiment ID: {exp.experiment_id}")
            print(f"   Artifact Location: {exp.artifact_location}")
            print(f"   Lifecycle Stage: {exp.lifecycle_stage}")
            
            # Print tags if available
            if exp.tags:
                print(f"   Tags:")
                for key, value in exp.tags.items():
                    print(f"      - {key}: {value}")
            
            # Print creation time if available
            if hasattr(exp, 'creation_time') and exp.creation_time:
                from datetime import datetime
                creation_date = datetime.fromtimestamp(exp.creation_time / 1000.0)
                print(f"   Created: {creation_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Print last update time if available
            if hasattr(exp, 'last_update_time') and exp.last_update_time:
                from datetime import datetime
                update_date = datetime.fromtimestamp(exp.last_update_time / 1000.0)
                print(f"   Last Updated: {update_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("-" * 80)
    
    def export_experiments_to_dict(self, experiments: List) -> List[dict]:
        """
        Export experiments data to a list of dictionaries
        
        Args:
            experiments: List of Experiment objects
            
        Returns:
            List of dictionaries containing experiment data
        """
        experiments_data = []
        
        for exp in experiments:
            exp_dict = {
                'name': exp.name,
                'experiment_id': exp.experiment_id,
                'artifact_location': exp.artifact_location,
                'lifecycle_stage': exp.lifecycle_stage,
                'tags': exp.tags if exp.tags else {},
                'creation_time': exp.creation_time if hasattr(exp, 'creation_time') else None,
                'last_update_time': exp.last_update_time if hasattr(exp, 'last_update_time') else None
            }
            experiments_data.append(exp_dict)
        
        return experiments_data
    
    def save_experiments_to_json(self, experiments: List, output_file: str = 'mlflow_experiments.json'):
        """
        Save experiments data to a JSON file
        
        Args:
            experiments: List of Experiment objects
            output_file: Output JSON file path
        """
        import json
        
        experiments_data = self.export_experiments_to_dict(experiments)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(experiments_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Experiments data saved to {output_file}")
            print(f"\n✓ Experiments data exported to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving experiments to JSON: {e}")


def main():
    """
    Main function to list MLflow experiments
    """
    # Configuration - Set your credentials here
    MLFLOW_TRACKING_URI = "[site-mlflow]mlflow"
    USERNAME = "[username]"
    PASSWORD = "[password]"
    
    print("="*80)
    print("MLflow Experiments Lister")
    print("="*80)
    print(f"MLflow Version: {mlflow.__version__}")
    print(f"Tracking URI: {MLFLOW_TRACKING_URI}")
    print("="*80)
    
    # Initialize the lister with credentials
    # This will automatically set the environment variables
    lister = MLflowExperimentLister(
        tracking_uri=MLFLOW_TRACKING_URI,
        username=USERNAME,
        password=PASSWORD
    )
    
    # Initialize client
    if not lister.initialize_client():
        logger.error("Failed to initialize MLflow client. Exiting.")
        sys.exit(1)
    
    try:
        # List all active experiments
        print("\n[1] Fetching active experiments...")
        experiments = lister.list_all_experiments()
        
        # Print experiment details
        lister.print_experiment_details(experiments)
        
        # Optional: Export to JSON
        export_choice = input("\nDo you want to export experiments to JSON? (y/n): ").strip().lower()
        if export_choice == 'y':
            output_file = input("Enter output filename (default: mlflow_experiments.json): ").strip()
            if not output_file:
                output_file = 'mlflow_experiments.json'
            lister.save_experiments_to_json(experiments, output_file)
        
        # Optional: Show deleted experiments
        show_deleted = input("\nDo you want to see deleted experiments? (y/n): ").strip().lower()
        if show_deleted == 'y':
            print("\n[2] Fetching all experiments (including deleted)...")
            all_experiments = lister.list_all_experiments_including_deleted()
            lister.print_experiment_details(all_experiments)
        
        print("\n" + "="*80)
        print("✓ Script completed successfully")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()




