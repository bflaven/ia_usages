#!/usr/bin/env python3
"""
Script to request locally installed Mistral 7B model via Ollama
All configurable variables are externalized in config.py for easy updating.

cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_using_n8n_io/ollama_querying/
python query_ollama.py

"""

import requests
import json
import sys
import os

# Import configuration variables from config.py
from config import (
    OLLAMA_URL,
    MODEL_NAME,
    cms_section_keywords_list,
    lang,
    content,
    prompt_template,
    STREAM,
    OUTPUT_FILE
)

def create_prompt(template, lang_var, content_var, cms_keywords_var):
    """
    Create the final prompt by replacing template variables
    """
    return (template.replace("{{ lang }}", lang_var)
                   .replace("{{content}}", content_var)
                   .replace("{{ cms_section_keywords_list }}", cms_keywords_var))

def make_ollama_request(url, model, prompt, stream=False):
    """
    Make a request to Ollama API
    
    Args:
        url (str): Ollama server URL
        model (str): Model name
        prompt (str): The prompt to send
        stream (bool): Whether to stream the response
    
    Returns:
        dict: Response from Ollama or error information
    """
    endpoint = f"{url}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Sending request to {endpoint}")
        print(f"Model: {model}")
        print(f"Prompt length: {len(prompt)} characters")
        print("=" * 50)
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection failed",
            "message": f"Could not connect to Ollama at {url}. Make sure Ollama is running."
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": "HTTP error",
            "message": f"HTTP {e.response.status_code}: {e.response.text}"
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e)
        }

def save_json_to_file(json_data, filename):
    """
    Save JSON data to a file
    
    Args:
        json_data (dict): JSON data to save
        filename (str): Output filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving to file: {e}")
        return False

def main():
    """
    Main function to execute the script
    """
    print("Ollama Request Script")
    print("=" * 50)
    
    # Create the final prompt
    final_prompt = create_prompt(prompt_template, lang, content, cms_section_keywords_list)
    
    # Make the request
    result = make_ollama_request(
        OLLAMA_URL,
        MODEL_NAME,
        final_prompt,
        STREAM
    )
    
    # Handle the response
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print(f"Message: {result['message']}")
        sys.exit(1)
    else:
        print("✅ Request successful!")
        print("=" * 50)
        print("Response:")
        
        if "response" in result:
            # Print the model's response
            print(result["response"])
            
            # Try to parse as JSON to validate
            try:
                json_response = json.loads(result["response"])
                print("\n" + "=" * 50)
                print("✅ Valid JSON response received")
                print("Formatted JSON:")
                print(json.dumps(json_response, ensure_ascii=False, indent=2))
                
                # Save to file
                if save_json_to_file(json_response, OUTPUT_FILE):
                    print(f"\n✅ JSON response saved to {OUTPUT_FILE}")
                else:
                    print(f"\n❌ Failed to save JSON to {OUTPUT_FILE}")
                    
            except json.JSONDecodeError:
                print("\n" + "=" * 50)
                print("⚠️  Response is not valid JSON")
                print("Cannot save to JSON file")
                
                # Save raw response to text file as fallback
                try:
                    raw_filename = OUTPUT_FILE.replace('.json', '_raw.txt')
                    with open(raw_filename, 'w', encoding='utf-8') as f:
                        f.write(result["response"])
                    print(f"💾 Raw response saved to {raw_filename}")
                except Exception as e:
                    print(f"❌ Error saving raw response: {e}")
        else:
            print("Unexpected response format:")
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
