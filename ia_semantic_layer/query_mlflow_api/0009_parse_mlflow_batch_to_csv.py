#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse MLflow Batch Output to CSV
Extracts run outputs from the batch JSON file and creates a CSV
with columns: title, summary, keywords, supertag

conda install -c conda-forge mlflow

pip install beautifulsoup4
pip install requests

Author: Generated for Bruno Flaven
Date: November 2025

# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/mlflow_python_api/

# LAUNCH the file
python 0009_parse_mlflow_batch_to_csv.py
"""

import json
import csv
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION - Update these values as needed
# ============================================================================

# Input JSON file (batch output from previous script)
INPUT_JSON_FILE = "bf-auto-batch-20251105-151608.json"

# Output CSV file (will be auto-generated with timestamp if not specified)
OUTPUT_CSV_FILE = None  # Set to None for auto-generation, or specify a filename like "output.csv"

# ============================================================================
# END CONFIGURATION
# ============================================================================


def generate_output_filename(input_filename: str) -> str:
    """
    Generate output CSV filename based on input filename
    
    Args:
        input_filename: Input JSON filename
        
    Returns:
        Output CSV filename
    """
    # Remove .json extension and add _parsed.csv
    base_name = os.path.splitext(input_filename)[0]
    output_name = f"{base_name}_parsed.csv"
    return output_name


def load_batch_json(json_file: str) -> Dict[str, Any]:
    """
    Load the batch output JSON file
    
    Args:
        json_file: Path to the JSON file
        
    Returns:
        Dictionary containing the batch data
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded batch data from {json_file}")
        return data
        
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_file}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading batch data: {e}")
        return None


def parse_output_json(output_str: str) -> Dict[str, Any]:
    """
    Parse the output string which should contain JSON
    
    Args:
        output_str: String containing JSON output
        
    Returns:
        Parsed JSON dictionary or None if parsing fails
    """
    try:
        # Try to parse as JSON directly
        output_data = json.loads(output_str)
        return output_data
    except json.JSONDecodeError:
        # Try to extract JSON from text if it's embedded
        try:
            # Look for JSON object pattern
            start_idx = output_str.find('{')
            end_idx = output_str.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = output_str[start_idx:end_idx]
                output_data = json.loads(json_str)
                return output_data
            else:
                logger.warning("Could not find JSON object in output string")
                return None
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse output as JSON: {e}")
            return None
    except Exception as e:
        logger.error(f"Error parsing output: {e}")
        return None


def extract_csv_row(run_data: Dict[str, Any], run_index: int) -> Dict[str, Any]:
    """
    Extract CSV row data from a single run
    
    Args:
        run_data: Dictionary containing run information
        run_index: Index of the run for reference
        
    Returns:
        Dictionary with CSV column data
    """
    # Get the output string
    output_str = run_data.get('output', '')
    
    if not output_str:
        logger.warning(f"Run {run_index} has no output")
        return None
    
    # Parse the output JSON
    output_json = parse_output_json(output_str)
    
    if not output_json:
        logger.warning(f"Run {run_index} output could not be parsed as JSON")
        return None
    
    # Extract values based on the expected JSON structure
    try:
        title = output_json.get('1', '')
        summary = output_json.get('2', '')
        keywords_list = output_json.get('3', [])
        supertag = output_json.get('4', '')
        
        # Convert keywords list to comma-separated string
        if isinstance(keywords_list, list):
            keywords = ', '.join(keywords_list)
        else:
            keywords = str(keywords_list)
        
        # Create CSV row
        csv_row = {
            'run_id': run_data.get('run_id', ''),
            'source': run_data.get('source', ''),
            'item_index': run_data.get('item_index', run_index),
            'title': title,
            'summary': summary,
            'keywords': keywords,
            'supertag': supertag,
            'status': run_data.get('status', 'completed')
        }
        
        return csv_row
        
    except Exception as e:
        logger.error(f"Error extracting data from run {run_index}: {e}")
        return None


def write_to_csv(rows: List[Dict[str, Any]], output_file: str):
    """
    Write extracted data to CSV file
    
    Args:
        rows: List of dictionaries containing row data
        output_file: Output CSV filename
    """
    if not rows:
        logger.error("No data to write to CSV")
        return False
    
    try:
        # Define CSV columns
        fieldnames = [
            'run_id',
            'source',
            'item_index',
            'title',
            'summary',
            'keywords',
            'supertag',
            'status'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write rows
            for row in rows:
                writer.writerow(row)
        
        logger.info(f"Successfully wrote {len(rows)} rows to {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}")
        return False


def main():
    """
    Main function to parse batch JSON and create CSV
    """
    print("="*80)
    print("MLflow Batch Output Parser - JSON to CSV")
    print("="*80)
    print(f"Input JSON: {INPUT_JSON_FILE}")
    
    # Generate output filename if not specified
    output_csv = OUTPUT_CSV_FILE
    if output_csv is None:
        output_csv = generate_output_filename(INPUT_JSON_FILE)
    
    print(f"Output CSV: {output_csv}")
    print("="*80)
    
    # Load the batch JSON file
    print("\n[1] Loading batch JSON file...")
    batch_data = load_batch_json(INPUT_JSON_FILE)
    
    if not batch_data:
        logger.error("Failed to load batch data. Exiting.")
        sys.exit(1)
    
    # Get the runs array
    runs = batch_data.get('runs', [])
    total_runs = batch_data.get('total_runs', len(runs))
    
    print(f"✓ Found {len(runs)} runs in batch data")
    print(f"  Total runs reported: {total_runs}")
    
    if not runs:
        logger.error("No runs found in batch data. Exiting.")
        sys.exit(1)
    
    # Process each run and extract CSV data
    print("\n[2] Processing runs and extracting data...")
    print("-"*80)
    
    csv_rows = []
    successful = 0
    failed = 0
    
    for index, run in enumerate(runs, start=1):
        print(f"Processing run {index}/{len(runs)}...", end=" ")
        
        csv_row = extract_csv_row(run, index)
        
        if csv_row:
            csv_rows.append(csv_row)
            successful += 1
            print("✓")
        else:
            failed += 1
            print("✗ (failed to extract)")
    
    print("-"*80)
    print(f"Extraction complete: {successful} successful, {failed} failed")
    
    if not csv_rows:
        logger.error("No data extracted from runs. Exiting.")
        sys.exit(1)
    
    # Write to CSV
    print("\n[3] Writing data to CSV...")
    if write_to_csv(csv_rows, output_csv):
        print(f"✓ Successfully created CSV file: {output_csv}")
    else:
        logger.error("Failed to create CSV file")
        sys.exit(1)
    
    # Print summary
    print("\n" + "="*80)
    print("PARSING COMPLETE")
    print("="*80)
    print(f"Input file: {INPUT_JSON_FILE}")
    print(f"Output file: {output_csv}")
    print(f"Total runs processed: {len(runs)}")
    print(f"Rows written to CSV: {len(csv_rows)}")
    print(f"Success rate: {successful}/{len(runs)} ({(successful/len(runs)*100):.1f}%)")
    print("="*80)
    
    # Show preview of first few rows
    if csv_rows:
        print("\nPreview of first row:")
        print("-"*80)
        first_row = csv_rows[0]
        for key, value in first_row.items():
            # Truncate long values for display
            display_value = str(value)
            if len(display_value) > 100:
                display_value = display_value[:100] + "..."
            print(f"{key}: {display_value}")
        print("-"*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
