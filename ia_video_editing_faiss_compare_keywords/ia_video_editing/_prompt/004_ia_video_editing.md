
# 004_ia_video_editing.md

## PROMPT_1
As a Python expert, can you write a script that load a .srt file for instance e.g "germany_scholz_EN_20241122_081318_081504_CS_8000.srt" then convert into json file with a good data model that can be parsed easily.

A example of three lines given as example below extracted from the file "germany_scholz_EN_20241122_081318_081504_CS_8000.srt".

```text
1
00:00:00,000 --> 00:00:06,360
Some already saw him as head of Germany's Social Democratic Party instead of Olaf Scholz.

2
00:00:07,019 --> 00:00:13,020
But Defence Minister Boris Pistorius has quelled days of uncertainty about his Chancellor candidacy

3
00:00:13,020 --> 00:00:15,560
pulling out of the parliamentary election race.

```



## CLAUDE_1
I'll create a Python script that can load an SRT file and convert it into a well-structured JSON format.



```python
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
    input_file = "germany_scholz_EN_20241122_081318_081504_CS_8000.srt"
    convert_srt_to_json(input_file)

```

I've created a comprehensive Python script to convert SRT subtitle files to JSON. Here are the key features:

1. Robust Parsing:
   - Uses regular expressions to handle various SRT file formats
   - Can process multi-line subtitle entries
   - Handles potential variations in formatting

2. Enhanced JSON Data Model:
   - `index`: Original subtitle number
   - `start_time`: Original timestamp format
   - `end_time`: Original timestamp format
   - `text`: Subtitle text (with newlines removed)
   - `start_time_ms`: Start time converted to milliseconds
   - `end_time_ms`: End time converted to milliseconds
   - `duration_ms`: Duration of the subtitle in milliseconds

3. Flexible Usage:
   - Can be run as a script or imported as a module
   - Automatically generates output filename if not specified
   - Supports custom input and output file paths

4. Error Handling:
   - Uses UTF-8 encoding to support international characters
   - Strips and cleans subtitle text

Example JSON output will look like:
```json
[
  {
    "index": 1,
    "start_time": "00:00:00,000",
    "end_time": "00:00:06,360",
    "text": "Some already saw him as head of Germany's Social Democratic Party instead of Olaf Scholz.",
    "start_time_ms": 0,
    "end_time_ms": 6360,
    "duration_ms": 6360
  },
  ...
]
```

To use the script:
1. Save the script to a Python file (e.g., `srt_converter.py`)
2. Replace the input file path with your SRT file
3. Run the script: `python srt_converter.py`

Would you like me to modify anything about the converter or explain any part of the implementation in more detail?





