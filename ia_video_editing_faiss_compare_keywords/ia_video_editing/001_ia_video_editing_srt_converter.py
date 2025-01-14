#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_seo_llm python=3.9.13
conda info --envs
source activate ia_seo_llm
conda deactivate


# BURN AFTER READING
source activate ia_seo_llm

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_seo_llm

# BURN AFTER READING
conda env remove -n ia_seo_llm


# other libraries
python -m pip install spacy 

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_video_editing/


# launch the file
python 001_ia_video_editing_srt_converter.py


"""

import re
import json
from typing import List, Dict

def parse_srt(file_path: str) -> List[Dict]:
    """
    Parse an SRT subtitle file and convert it to a structured JSON format.
    
    Args:
        file_path (str): Path to the .srt subtitle file
    
    Returns:
        List[Dict]: A list of subtitle entries with structured information
    """
    subtitles = []
    
    # Read the SRT file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to parse SRT entries
    # Matches: 
    # 1. Subtitle number
    # 2. Timestamp (start --> end)
    # 3. Subtitle text (can be multiple lines)
    pattern = re.compile(
        r'(\d+)\n'  # Subtitle number
        r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n'  # Timestamps
        r'(.*?)\n\n'  # Subtitle text (non-greedy to handle multiple lines)
        , re.DOTALL
    )
    
    # Find all matches in the file
    for match in pattern.finditer(content):
        # Extract components
        subtitle_number = int(match.group(1))
        start_time = match.group(2)
        end_time = match.group(3)
        
        # Clean and process subtitle text
        text = match.group(4).replace('\n', ' ').strip()
        
        # Create subtitle entry
        subtitle_entry = {
            "index": subtitle_number,
            "start_time": start_time,
            "end_time": end_time,
            "text": text,
            "start_time_ms": _convert_to_milliseconds(start_time),
            "end_time_ms": _convert_to_milliseconds(end_time),
            "duration_ms": _convert_to_milliseconds(end_time) - _convert_to_milliseconds(start_time)
        }
        
        subtitles.append(subtitle_entry)
    
    return subtitles

def _convert_to_milliseconds(timestamp: str) -> int:
    """
    Convert SRT timestamp to total milliseconds.
    
    Args:
        timestamp (str): SRT format timestamp (HH:MM:SS,mmm)
    
    Returns:
        int: Total milliseconds
    """
    hours, minutes, seconds_ms = timestamp.split(':')
    seconds, milliseconds = seconds_ms.split(',')
    
    total_ms = (
        int(hours) * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(milliseconds)
    )
    
    return total_ms

def convert_srt_to_json(input_file: str, output_file: str = None) -> None:
    """
    Convert SRT file to JSON file.
    
    Args:
        input_file (str): Path to input .srt file
        output_file (str, optional): Path to output .json file. 
                                     If not provided, uses input filename with .json extension
    """
    # Parse subtitles
    subtitles = parse_srt(input_file)
    
    # Determine output file path
    if output_file is None:
        output_file = input_file.rsplit('.', 1)[0] + '.json'
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(subtitles, file, indent=2, ensure_ascii=False)
    
    print(f"Converted {input_file} to {output_file}")

# Example usage
if __name__ == "__main__":
    # Example file path (replace with your actual file path)
    # input_file = "source/germany_scholz_EN_20241122_081318_081504_CS_8000.srt"
    input_file = "source/putin_issues_EN_20241122_013120_013320_CS_8000.srt"

    convert_srt_to_json(input_file)




    
