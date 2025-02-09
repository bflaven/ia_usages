#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss

# BURN AFTER READING
conda env remove -n ia_using_faiss


# other libraries
python -m pip install spacy 

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

python -m pip install streamlit pandas plotly
python -m pip install pandas plotly


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_deepseek

# launch the file
streamlit run 001_ia_deepseek.py

"""

# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly  # Import plotly to get its version

# Define a class to handle the Streamlit app
class TimelineVisualizer:
    def __init__(self):
        # Set the page configuration to full screen and add a title and icon
        st.set_page_config(page_title="Timeline Visualizer", page_icon="🚀", layout="wide")
        # Display package versions in a st.info box
        st.info(
            f"Streamlit version: {st.__version__}, "
            f"Pandas version: {pd.__version__}, "
            f"Plotly version: {plotly.__version__}"
        )
        # Set the main title of the app
        st.title("Timeline Visualizer 🚀")
        # Create two tabs: Viewer and Credits
        self.tab1, self.tab2 = st.tabs(["Viewer", "Credits"])
        # Initialize the app
        self.initialize_app()

    def initialize_app(self):
        # Load and display data in the Viewer tab
        with self.tab1:
            self.display_viewer_tab()
        # Display credits in the Credits tab
        with self.tab2:
            self.display_credits_tab()

    def display_viewer_tab(self):
        # Load the CSV file (for demonstration, we create a sample DataFrame)
        sample_data = {
            "Date": ["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01"],
            "Value": [10, 20, 15, 25]
        }
        df = pd.DataFrame(sample_data)
        # Convert the 'Date' column to datetime format for better plotting
        df["Date"] = pd.to_datetime(df["Date"])
        # Display the DataFrame
        st.write("### Sample Timeline Data")
        st.dataframe(df)
        # Create a Plotly line chart to visualize the data
        fig = px.line(df, x="Date", y="Value", title="Timeline Visualization")
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

    def display_credits_tab(self):
        # Display credits in the Credits tab
        st.write("### Credits")
        st.write("IA generated code by deepseek")

# Main function to run the app
if __name__ == "__main__":
    # Create an instance of the TimelineVisualizer class
    app = TimelineVisualizer()

    
