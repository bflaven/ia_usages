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
python 006_carbon_footprint_codecarbon_task_manager_usage.py

Codecarbon usage
https://mlco2.github.io/codecarbon/usage.html
https://asciinema.org/a/667970


"""
import warnings
from codecarbon import EmissionsTracker

# Suppress the FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


class DataProcessor:
    """A class to demonstrate CodeCarbon usage with multiple tasks."""

    def __init__(self, project_name):
        """
        Initialize the DataProcessor.

        Args:
            project_name (str): Name of the project for emissions tracking.
        """
        self.tracker = EmissionsTracker(project_name=project_name, measure_power_secs=10)

    def load_data(self):
        """Simulate loading data."""
        self.tracker.start_task("load_data")
        # Simulating data loading
        data = list(range(1, 1000001))
        self.tracker.stop_task()
        return data

    def process_data(self, data):
        """
        Process the given data.

        Args:
            data (list): Input data to process.

        Returns:
            list: Processed data.
        """
        self.tracker.start_task("process_data")
        processed_data = [x ** 2 for x in data]
        self.tracker.stop_task()
        return processed_data

    def analyze_results(self, data):
        """
        Analyze the processed data.

        Args:
            data (list): Processed data to analyze.

        Returns:
            dict: Analysis results.
        """
        self.tracker.start_task("analyze_results")
        analysis = {
            "sum": sum(data),
            "average": sum(data) / len(data),
            "max": max(data),
            "min": min(data)
        }
        self.tracker.stop_task()
        return analysis

def main():
    """Main function to demonstrate CodeCarbon task manager usage."""
    processor = DataProcessor("TaskManagerExample")

    try:
        # Execute the data processing pipeline
        raw_data = processor.load_data()
        processed_data = processor.process_data(raw_data)
        analysis = processor.analyze_results(processed_data)

        print("Analysis results:")
        for key, value in analysis.items():
            print(f"{key}: {value}")

    finally:
        # Stop tracking and print the emissions
        emissions = processor.tracker.stop()
        print(f"Total carbon emissions: {emissions} kg")

if __name__ == "__main__":
    main()




    

    
        
        

