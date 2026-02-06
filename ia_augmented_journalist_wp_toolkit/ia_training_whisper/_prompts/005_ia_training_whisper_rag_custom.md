## PROMPT_1

As a python and whisper expert, can you write a python script that will do the post-processing as Whisper doesn't do NER.
1. I want something more flexible so I can feed the Kiswahili transcript into a lightweight NER model (spaCy, transformers, or a small LLM) and then post‑filter with your JSON list instead of relying purely on exact matches. Make the simplest choice for the lightweight NER model as it is just for a POC and I want also to have the same principles for other languages: BR (brazilian), CN (simplified chinese), HA (haoussa), VI ( vietnamese)
2. For instance, the list of tags is not a json but inside a python file e.g `RFI_SW_thematicTags.py`. I give an extract to give you the structure and the path is `source_thema`. It is a directory that stores the tags.

```python
# NB OF TAGS: 2005
from typing import Literal
from pydantic import BaseModel
# RFI_SW_thematicTags
class BachSectionTag(BaseModel):
    label: Literal["1899 Hoffenheim", "AC Leopards", "AC Milan", "ADC Ikibiri", "ADF", "AFCON"]
```


3. I am using anaconda to manage the python environment. The name of the env is `whisper_train`


## OUTPUT_1

Here's a comprehensive NER post-processing script that uses a lightweight multilingual model:

```python
#!/usr/bin/env python3
"""
Whisper Transcription Post-Processing with NER
Supports: Kiswahili (SW), Brazilian Portuguese (BR), Chinese (CN), Hausa (HA), Vietnamese (VI)
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path
import json
import importlib.util
from typing import Dict, List, Set
import re

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================
TRANSCRIPT_FILE = "source/kiswahili/APPELS_ACTU_14-01-26_small.txt"
TAGS_FILE = "source_thema/RFI_SW_thematicTags.py"
LANGUAGE = "sw"  # Options: sw, br, cn, ha, vi
OUTPUT_FORMAT = "json"  # Options: json, txt, both

# NER Model Configuration
NER_MODEL = "Davlan/xlm-roberta-base-wikiann-ner"  # Multilingual, 176 languages

# ============================================================================
# 1. ENVIRONMENT CHECK
# ============================================================================
print("=" * 70)
print("NER POST-PROCESSING ENVIRONMENT CHECK")
print("=" * 70)

def check_package(package_name, import_name=None):
    """Check if a package is installed and print version"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {package_name:20} {version}")
        return True
    except ImportError:
        print(f"✗ {package_name:20} NOT INSTALLED")
        return False

# Check required packages
packages_ok = True
packages_ok &= check_package("transformers")
packages_ok &= check_package("torch")
packages_ok &= check_package("pydantic")

print("=" * 70)

if not packages_ok:
    print("\n⚠️  ERROR: Some packages are missing!")
    print("Run: pip install transformers torch pydantic")
    sys.exit(1)

print("\n✅ Environment check passed!\n")

# ============================================================================
# 2. LOAD TAGS FROM PYTHON FILE
# ============================================================================
print("=" * 70)
print("LOADING THEMATIC TAGS")
print("=" * 70)

def load_tags_from_python_file(tags_file_path: str) -> Set[str]:
    """
    Load tags from a Python file containing a Pydantic model with Literal types
    """
    tags_path = Path(tags_file_path)
    
    if not tags_path.exists():
        print(f"✗ ERROR: Tags file not found: {tags_path}")
        sys.exit(1)
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("tags_module", tags_path)
    tags_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tags_module)
    
    # Extract all Pydantic models from the module
    tags = set()
    for attr_name in dir(tags_module):
        attr = getattr(tags_module, attr_name)
        
        # Check if it's a Pydantic model
        if hasattr(attr, '__fields__'):
            for field_name, field in attr.__fields__.items():
                # Extract Literal values
                if hasattr(field.annotation, '__args__'):
                    for literal_value in field.annotation.__args__:
                        if isinstance(literal_value, str):
                            tags.add(literal_value)
    
    return tags

try:
    known_tags = load_tags_from_python_file(TAGS_FILE)
    print(f"✓ Loaded {len(known_tags)} tags from: {TAGS_FILE}")
    print(f"  Sample tags: {list(known_tags)[:5]}")
except Exception as e:
    print(f"✗ Error loading tags: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 3. LOAD NER MODEL
# ============================================================================
print("\n" + "=" * 70)
print("LOADING NER MODEL")
print("=" * 70)

from transformers import pipeline

print(f"Loading model: {NER_MODEL}")
print("(First run will download the model - ~500MB)")

try:
    # Load NER pipeline
    ner_pipeline = pipeline(
        "ner",
        model=NER_MODEL,
        aggregation_strategy="simple"  # Combines subword tokens
    )
    print(f"✓ NER model loaded successfully")
    print(f"  Supports: 176 languages including SW, BR, CN, HA, VI")
except Exception as e:
    print(f"✗ Error loading NER model: {e}")
    sys.exit(1)

# ============================================================================
# 4. LOAD TRANSCRIPT
# ============================================================================
print("\n" + "=" * 70)
print("LOADING TRANSCRIPT")
print("=" * 70)

transcript_path = Path(TRANSCRIPT_FILE)

if not transcript_path.exists():
    print(f"✗ ERROR: Transcript file not found!")
    print(f"  Looking for: {transcript_path.absolute()}")
    sys.exit(1)

with open(transcript_path, 'r', encoding='utf-8') as f:
    transcript_text = f.read()

# Remove metadata if present (from our previous script)
if transcript_text.startswith("Model:"):
    lines = transcript_text.split('\n')
    # Skip metadata lines
    transcript_text = '\n'.join(lines[4:]) if len(lines) > 4 else transcript_text

transcript_text = transcript_text.strip()

print(f"✓ Transcript loaded: {transcript_path}")
print(f"  Length: {len(transcript_text)} characters")
print(f"  Preview: {transcript_text[:100]}...")

# ============================================================================
# 5. RUN NER
# ============================================================================
print("\n" + "=" * 70)
print("RUNNING NER DETECTION")
print("=" * 70)

print("Detecting entities... (this may take a moment)")

try:
    # Run NER on the transcript
    ner_results = ner_pipeline(transcript_text)
    
    print(f"✓ NER detection complete")
    print(f"  Detected {len(ner_results)} entities")
    
except Exception as e:
    print(f"✗ Error during NER: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 6. POST-PROCESS WITH KNOWN TAGS
# ============================================================================
print("\n" + "=" * 70)
print("POST-PROCESSING WITH KNOWN TAGS")
print("=" * 70)

def fuzzy_match(entity: str, known_tags: Set[str], threshold: float = 0.8) -> str:
    """
    Find the best matching tag for an entity
    Uses simple case-insensitive matching and partial matching
    """
    entity_lower = entity.lower()
    
    # Exact match (case-insensitive)
    for tag in known_tags:
        if tag.lower() == entity_lower:
            return tag
    
    # Partial match - entity contains tag or tag contains entity
    for tag in known_tags:
        tag_lower = tag.lower()
        if tag_lower in entity_lower or entity_lower in tag_lower:
            # Check if it's a significant match
            if len(entity_lower) > 3:  # Avoid matching very short strings
                return tag
    
    return None

# Process entities
enhanced_entities = []
matched_tags = set()
unmatched_entities = []

for entity in ner_results:
    entity_text = entity['word']
    entity_type = entity['entity_group']
    score = entity['score']
    
    # Try to match against known tags
    matched_tag = fuzzy_match(entity_text, known_tags)
    
    if matched_tag:
        enhanced_entities.append({
            'text': entity_text,
            'matched_tag': matched_tag,
            'type': entity_type,
            'score': score,
            'start': entity['start'],
            'end': entity['end']
        })
        matched_tags.add(matched_tag)
    else:
        # Keep entity even if not matched to a tag
        enhanced_entities.append({
            'text': entity_text,
            'matched_tag': None,
            'type': entity_type,
            'score': score,
            'start': entity['start'],
            'end': entity['end']
        })
        unmatched_entities.append(entity_text)

print(f"✓ Post-processing complete")
print(f"  Entities matched to tags: {len(matched_tags)}")
print(f"  Entities not in tag list: {len(unmatched_entities)}")

# ============================================================================
# 7. DISPLAY RESULTS
# ============================================================================
print("\n" + "=" * 70)
print("DETECTED ENTITIES")
print("=" * 70)

# Group by entity type
entities_by_type = {}
for entity in enhanced_entities:
    entity_type = entity['type']
    if entity_type not in entities_by_type:
        entities_by_type[entity_type] = []
    entities_by_type[entity_type].append(entity)

for entity_type, entities in sorted(entities_by_type.items()):
    print(f"\n{entity_type}:")
    for entity in entities[:10]:  # Show first 10 of each type
        matched = f" → {entity['matched_tag']}" if entity['matched_tag'] else ""
        print(f"  • {entity['text']}{matched} (confidence: {entity['score']:.2f})")
    
    if len(entities) > 10:
        print(f"  ... and {len(entities) - 10} more")

if matched_tags:
    print(f"\n" + "=" * 70)
    print("MATCHED THEMATIC TAGS")
    print("=" * 70)
    for tag in sorted(matched_tags)[:20]:
        print(f"  ✓ {tag}")
    if len(matched_tags) > 20:
        print(f"  ... and {len(matched_tags) - 20} more")

# ============================================================================
# 8. SAVE RESULTS
# ============================================================================
print("\n" + "=" * 70)
print("SAVING RESULTS")
print("=" * 70)

output_base = transcript_path.parent / f"{transcript_path.stem}_ner"

# Prepare results structure
results = {
    'transcript': transcript_text,
    'language': LANGUAGE,
    'total_entities': len(enhanced_entities),
    'matched_tags_count': len(matched_tags),
    'entities': enhanced_entities,
    'matched_tags': sorted(list(matched_tags)),
    'entities_by_type': {
        entity_type: [e['text'] for e in entities]
        for entity_type, entities in entities_by_type.items()
    }
}

# Save JSON
if OUTPUT_FORMAT in ['json', 'both']:
    json_output = output_base.with_suffix('.json')
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON results saved to: {json_output}")

# Save TXT (human-readable)
if OUTPUT_FORMAT in ['txt', 'both']:
    txt_output = output_base.with_suffix('.txt')
    with open(txt_output, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("NER RESULTS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Language: {LANGUAGE}\n")
        f.write(f"Total entities detected: {len(enhanced_entities)}\n")
        f.write(f"Matched to thematic tags: {len(matched_tags)}\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("ENTITIES BY TYPE\n")
        f.write("=" * 70 + "\n\n")
        
        for entity_type, entities in sorted(entities_by_type.items()):
            f.write(f"{entity_type}:\n")
            for entity in entities:
                matched = f" → {entity['matched_tag']}" if entity['matched_tag'] else ""
                f.write(f"  • {entity['text']}{matched} (confidence: {entity['score']:.2f})\n")
            f.write("\n")
        
        if matched_tags:
            f.write("=" * 70 + "\n")
            f.write("MATCHED THEMATIC TAGS\n")
            f.write("=" * 70 + "\n\n")
            for tag in sorted(matched_tags):
                f.write(f"  ✓ {tag}\n")
    
    print(f"✓ Text results saved to: {txt_output}")

print("\n✅ NER post-processing completed successfully!")
```

## Installation

Add these packages to your environment:

```bash
conda activate whisper_train
pip install transformers torch pydantic sentencepiece
```

## Configuration for Different Languages

Just change the `LANGUAGE` variable:

```python
# For Kiswahili
LANGUAGE = "sw"
TAGS_FILE = "source_thema/RFI_SW_thematicTags.py"

# For Brazilian Portuguese
LANGUAGE = "br"
TAGS_FILE = "source_thema/RFI_BR_thematicTags.py"

# For Chinese
LANGUAGE = "cn"
TAGS_FILE = "source_thema/RFI_CN_thematicTags.py"

# For Hausa
LANGUAGE = "ha"
TAGS_FILE = "source_thema/RFI_HA_thematicTags.py"

# For Vietnamese
LANGUAGE = "vi"
TAGS_FILE = "source_thema/RFI_VI_thematicTags.py"
```

## How It Works

1. **Loads your tags** from the Pydantic file (extracts all Literal values)
2. **Runs multilingual NER** using XLM-RoBERTa (supports 176 languages)
3. **Matches entities** against your known tags (fuzzy matching)
4. **Outputs results** in JSON and/or TXT format

## Sample Output

```
======================================================================
NER RESULTS
======================================================================

Language: sw
Total entities detected: 45
Matched to thematic tags: 12

======================================================================
ENTITIES BY TYPE
======================================================================

PER (Person):
  • William Ruto (confidence: 0.95)
  • Samia Suluhu Hassan (confidence: 0.92)

LOC (Location):
  • Dar es Salaam → Dar es Salaam (confidence: 0.98)
  • Nairobi → Nairobi (confidence: 0.96)

ORG (Organization):
  • AC Milan → AC Milan (confidence: 0.91)
  • ADF → ADF (confidence: 0.89)

======================================================================
MATCHED THEMATIC TAGS
======================================================================
  ✓ AC Milan
  ✓ ADF
  ✓ Dar es Salaam
  ...
```

## Why This Model?

**`Davlan/xlm-roberta-base-wikiann-ner`**:
- ✅ Supports ALL your languages (SW, BR, CN, HA, VI)
- ✅ Lightweight (~500MB)
- ✅ Good for POC
- ✅ Pre-trained on WikiANN (high quality)
- ✅ Works with transformers pipeline (simple API)

## Run It

```bash
conda activate whisper_train
python ner_postprocess.py
```

Want me to add features like confidence threshold filtering or better fuzzy matching algorithms?


