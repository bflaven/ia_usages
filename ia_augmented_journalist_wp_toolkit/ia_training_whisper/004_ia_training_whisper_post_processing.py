"""
[env]
# Conda Environment
conda create --name whisper_train python=3.10
conda info --envs
source activate whisper_train
conda deactivate


# BURN AFTER READING
source activate whisper_train

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n whisper_train


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
# Install core dependencies
pip install openai-whisper
pip install datasets
pip install transformers
pip install accelerate
pip install evaluate jiwer
pip install torch torchvision torchaudio  # For Mac M1/M2, this gets MPS support

# Install PyTorch from conda (better Mac compatibility)
conda install pytorch torchvision torchaudio -c pytorch

# Then install the rest with pip
pip install openai-whisper datasets transformers accelerate evaluate jiwer

# Check Installation
python -c "import whisper; print(whisper.__version__)"
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_training_whisper/

# launch the file
python 004_ia_training_whisper_post_processing.py


"""
"""
Whisper Transcription Post-Processing with NER
Supports: Kiswahili (SW), Brazilian Portuguese (PT), Chinese (ZH), Hausa (HA), Vietnamese (VI)
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path
import json
import importlib.util
from typing import Dict, List, Set
import re
import numpy as np

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================

# Language configurations
LANGUAGE_CONFIGS = {
    'sw': {
        'name': 'Kiswahili',
        'transcript_dir': 'source/kiswahili',
        'tags_file': 'source_thema/RFI_SW_thematicTags.py'
    },
    'pt': {
        'name': 'Portuguese (Brazilian)',
        'transcript_dir': 'source/brazilian',
        'tags_file': 'source_thema/RFI_BR_thematicTags.py'
    },
    'zh': {
        'name': 'Chinese (Simplified)',
        'transcript_dir': 'source/chinese',
        'tags_file': 'source_thema/RFI_CN_thematicTags.py'
    },
    'ha': {
        'name': 'Hausa',
        'transcript_dir': 'source/hausa',
        'tags_file': 'source_thema/RFI_HA_thematicTags.py'
    },
    'vi': {
        'name': 'Vietnamese',
        'transcript_dir': 'source/vietnamese',
        'tags_file': 'source_thema/RFI_VI_thematicTags.py'
    }
}

# Select language and model
# LANGUAGE = "sw"  # Change this to: sw, pt, zh, ha, or vi
# MODEL_SIZE = "small"  # Options: tiny, base, small, medium, large
# BASE_FILENAME = "APPELS_ACTU_14-01-26" # Base filename (without model suffix)

# LANGUAGE = "pt"  # Change this to: sw, pt, zh, ha, or vi
# MODEL_SIZE = "large"  # Options: tiny, base, small, medium, large
# BASE_FILENAME = "LINHA_DIRETA_22_1" # Base filename (without model suffix)

# LANGUAGE = "zh"  # Change this to: sw, pt, zh, ha, or vi
# MODEL_SIZE = "large"  # Options: tiny, base, small, medium, large
# BASE_FILENAME = "Trump_FED_ANTHONY_21_01_2026" # Base filename (without model suffix)


LANGUAGE = "sw"  # Change this to: sw, pt, zh, ha, or vi
MODEL_SIZE = "Whisper Large"  # Options: tiny, base, small, medium, large
BASE_FILENAME = "SIHA_NJEMA13-01-26_OK_whisper_large_kiswahili.txt" # Base filename (without model suffix)



# Auto-configure paths
config = LANGUAGE_CONFIGS[LANGUAGE]
TRANSCRIPT_FILE = f"{config['transcript_dir']}/{BASE_FILENAME}"
TAGS_FILE = config['tags_file']

# Output format
OUTPUT_FORMAT = "both"  # Options: json, txt, both

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
packages_ok &= check_package("numpy")

print(f"\n{'Python version':20} {sys.version.split()[0]}")

# Check conda environment
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

print("=" * 70)

if not packages_ok:
    print("\n⚠️  ERROR: Some packages are missing!")
    print("Run: pip install transformers torch pydantic numpy sentencepiece")
    sys.exit(1)

if conda_env != "whisper_train":
    print(f"\n⚠️  WARNING: Current environment is '{conda_env}', expected 'whisper_train'")
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        sys.exit(1)

print("\n✅ Environment check passed!\n")

# Display configuration
print("=" * 70)
print("CONFIGURATION")
print("=" * 70)
print(f"Language: {config['name']} ({LANGUAGE})")
print(f"Transcript: {TRANSCRIPT_FILE}")
print(f"Model used: {MODEL_SIZE}")
print(f"Tags file: {TAGS_FILE}")
print(f"Output format: {OUTPUT_FORMAT}")
print("=" * 70 + "\n")

# ============================================================================
# 2. LOAD TAGS FROM PYTHON FILE
# ============================================================================
print("=" * 70)
print("LOADING THEMATIC TAGS")
print("=" * 70)

def load_tags_from_python_file(tags_file_path: str) -> Set[str]:
    """
    Load tags from a Python file containing a Pydantic model with Literal types
    Fixed for Pydantic V2 - uses model_fields instead of __fields__
    """
    tags_path = Path(tags_file_path)
    
    if not tags_path.exists():
        print(f"✗ ERROR: Tags file not found: {tags_path}")
        print(f"  Looking for: {tags_path.absolute()}")
        sys.exit(1)
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("tags_module", tags_path)
    tags_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tags_module)
    
    # Extract all Pydantic models from the module
    tags = set()
    for attr_name in dir(tags_module):
        attr = getattr(tags_module, attr_name)
        
        # Check if it's a Pydantic model (V2 compatible)
        if hasattr(attr, 'model_fields'):
            # Pydantic V2
            for field_name, field in attr.model_fields.items():
                # Extract Literal values
                if hasattr(field.annotation, '__args__'):
                    for literal_value in field.annotation.__args__:
                        if isinstance(literal_value, str):
                            tags.add(literal_value)
        elif hasattr(attr, '__fields__'):
            # Pydantic V1 fallback (deprecated but keep for compatibility)
            for field_name, field in attr.__fields__.items():
                if hasattr(field.annotation, '__args__'):
                    for literal_value in field.annotation.__args__:
                        if isinstance(literal_value, str):
                            tags.add(literal_value)
    
    return tags

try:
    known_tags = load_tags_from_python_file(TAGS_FILE)
    print(f"✓ Loaded {len(known_tags)} tags from: {TAGS_FILE}")
    sample_tags = sorted(list(known_tags))[:5]
    print(f"  Sample tags: {sample_tags}")
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
    print(f"  Supports: 176 languages including SW, PT, ZH, HA, VI")
except Exception as e:
    print(f"✗ Error loading NER model: {e}")
    import traceback
    traceback.print_exc()
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
    print(f"\nCurrent directory: {Path.cwd()}")
    print(f"\nMake sure the file exists at: {transcript_path}")
    sys.exit(1)

with open(transcript_path, 'r', encoding='utf-8') as f:
    transcript_text = f.read()

# Remove metadata if present (from transcription script)
if transcript_text.startswith("Model:"):
    lines = transcript_text.split('\n')
    # Skip metadata lines (first 4 lines)
    transcript_text = '\n'.join(lines[4:]) if len(lines) > 4 else transcript_text

transcript_text = transcript_text.strip()

print(f"✓ Transcript loaded: {transcript_path}")
print(f"  Length: {len(transcript_text)} characters")
print(f"  Word count: ~{len(transcript_text.split())} words")
print(f"  Preview: {transcript_text[:100]}...")

# ============================================================================
# 5. RUN NER
# ============================================================================
print("\n" + "=" * 70)
print("RUNNING NER DETECTION")
print("=" * 70)

print(f"Detecting entities in {config['name']} text...")
print("(This may take a moment depending on transcript length)")

try:
    # Run NER on the transcript
    ner_results = ner_pipeline(transcript_text)
    
    print(f"✓ NER detection complete")
    print(f"  Detected {len(ner_results)} entity mentions")
    
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

def convert_to_python_types(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def fuzzy_match(entity: str, known_tags: Set[str], threshold: float = 0.8) -> str:
    """
    Find the best matching tag for an entity
    Uses case-insensitive matching and partial matching
    """
    entity_lower = entity.lower()
    
    # Exact match (case-insensitive)
    for tag in known_tags:
        if tag.lower() == entity_lower:
            return tag
    
    # Partial match - entity contains tag or tag contains entity
    for tag in known_tags:
        tag_lower = tag.lower()
        # Check if tag is contained in entity or vice versa
        if len(tag_lower) > 3:  # Avoid matching very short strings
            if tag_lower in entity_lower or entity_lower in tag_lower:
                return tag
    
    return None

# Process entities
enhanced_entities = []
matched_tags = set()
unmatched_entities = []

for entity in ner_results:
    entity_text = entity['word']
    entity_type = entity['entity_group']
    score = convert_to_python_types(entity['score'])
    
    # Try to match against known tags
    matched_tag = fuzzy_match(entity_text, known_tags)
    
    if matched_tag:
        enhanced_entities.append({
            'text': entity_text,
            'matched_tag': matched_tag,
            'type': entity_type,
            'score': score,
            'start': convert_to_python_types(entity['start']),
            'end': convert_to_python_types(entity['end'])
        })
        matched_tags.add(matched_tag)
    else:
        # Keep entity even if not matched to a tag
        enhanced_entities.append({
            'text': entity_text,
            'matched_tag': None,
            'type': entity_type,
            'score': score,
            'start': convert_to_python_types(entity['start']),
            'end': convert_to_python_types(entity['end'])
        })
        unmatched_entities.append(entity_text)

print(f"✓ Post-processing complete")
print(f"  Total entity mentions: {len(enhanced_entities)}")
print(f"  Matched to thematic tags: {len(matched_tags)}")
print(f"  Unmatched entities: {len(unmatched_entities)}")

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
    print(f"\n{entity_type} ({len(entities)} mentions):")
    unique_entities = {}
    for entity in entities:
        key = entity['text'].lower()
        if key not in unique_entities:
            unique_entities[key] = entity
    
    displayed = 0
    for entity in list(unique_entities.values())[:10]:
        matched = f" → {entity['matched_tag']}" if entity['matched_tag'] else ""
        print(f"  • {entity['text']}{matched} (confidence: {entity['score']:.2f})")
        displayed += 1
    
    if len(unique_entities) > 10:
        print(f"  ... and {len(unique_entities) - 10} more unique entities")

if matched_tags:
    print(f"\n" + "=" * 70)
    print("MATCHED THEMATIC TAGS")
    print("=" * 70)
    sorted_tags = sorted(list(matched_tags))
    for i, tag in enumerate(sorted_tags[:20], 1):
        print(f"  {i:2d}. {tag}")
    if len(matched_tags) > 20:
        print(f"  ... and {len(matched_tags) - 20} more tags")

# ============================================================================
# 8. SAVE RESULTS
# ============================================================================
print("\n" + "=" * 70)
print("SAVING RESULTS")
print("=" * 70)

output_base = transcript_path.parent / f"{transcript_path.stem}_ner"

# Prepare results structure (all values converted to Python types)
results = {
    'metadata': {
        'language': LANGUAGE,
        'language_name': config['name'],
        'model_size': MODEL_SIZE,
        'transcript_file': str(transcript_path),
        'tags_file': TAGS_FILE,
        'ner_model': NER_MODEL
    },
    'statistics': {
        'transcript_length': len(transcript_text),
        'total_entities': len(enhanced_entities),
        'unique_entities': len({e['text'].lower() for e in enhanced_entities}),
        'matched_tags_count': len(matched_tags),
        'unmatched_count': len(unmatched_entities)
    },
    'transcript': transcript_text,
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
        
        f.write(f"Language: {config['name']} ({LANGUAGE})\n")
        f.write(f"Model size: {MODEL_SIZE}\n")
        f.write(f"Transcript file: {transcript_path}\n")
        f.write(f"Tags file: {TAGS_FILE}\n\n")
        
        f.write(f"Total entity mentions: {len(enhanced_entities)}\n")
        f.write(f"Unique entities: {len({e['text'].lower() for e in enhanced_entities})}\n")
        f.write(f"Matched to thematic tags: {len(matched_tags)}\n")
        f.write(f"Unmatched entities: {len(unmatched_entities)}\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("ENTITIES BY TYPE\n")
        f.write("=" * 70 + "\n\n")
        
        for entity_type, entities in sorted(entities_by_type.items()):
            f.write(f"{entity_type} ({len(entities)} mentions):\n")
            unique_entities = {}
            for entity in entities:
                key = entity['text'].lower()
                if key not in unique_entities:
                    unique_entities[key] = entity
            
            for entity in unique_entities.values():
                matched = f" → {entity['matched_tag']}" if entity['matched_tag'] else ""
                f.write(f"  • {entity['text']}{matched} (confidence: {entity['score']:.2f})\n")
            f.write("\n")
        
        if matched_tags:
            f.write("=" * 70 + "\n")
            f.write("MATCHED THEMATIC TAGS\n")
            f.write("=" * 70 + "\n\n")
            for i, tag in enumerate(sorted(list(matched_tags)), 1):
                f.write(f"  {i:3d}. {tag}\n")
    
    print(f"✓ Text results saved to: {txt_output}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Language: {config['name']} ({LANGUAGE})")
print(f"Total entities detected: {len(enhanced_entities)}")
print(f"Matched thematic tags: {len(matched_tags)}")
print(f"Match rate: {len(matched_tags)/max(1,len(enhanced_entities))*100:.1f}%")

print("\nOutput files:")
if OUTPUT_FORMAT in ['json', 'both']:
    print(f"  - JSON: {json_output}")
if OUTPUT_FORMAT in ['txt', 'both']:
    print(f"  - TXT:  {txt_output}")

print("\n✅ NER post-processing completed successfully!")





