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
python 005_ia_training_check_loading_thema.py


"""
"""
Thematic Tags File Debugger and Validator
Tests and validates RFI thematic tags Python files
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path
import importlib.util
from typing import Set, List, Dict
import inspect

# ============================================================================
# CONFIGURATION - Select which file to debug
# ============================================================================

# Available tags files
TAGS_FILES = {
    'sw': 'source_thema/RFI_SW_thematicTags.py',
    'br': 'source_thema/RFI_BR_thematicTags.py',
    'cn': 'source_thema/RFI_CN_thematicTags.py',
    'ha': 'source_thema/RFI_HA_thematicTags.py',
    'vi': 'source_thema/RFI_VI_thematicTags.py'
}

# Select which file to debug (or use 'all' to check all files)
# Options: sw, br, cn, ha, vi, or 'all'
DEBUG_LANGUAGE = "sw"  
# DEBUG_LANGUAGE = "br"  
# DEBUG_LANGUAGE = "cn" 
# DEBUG_LANGUAGE = "ha" 
# DEBUG_LANGUAGE = "vi" 

# Number of sample tags to display
SAMPLE_SIZE = 20

# ============================================================================
# 1. ENVIRONMENT CHECK
# ============================================================================
print("=" * 70)
print("THEMATIC TAGS DEBUGGER - ENVIRONMENT CHECK")
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
packages_ok &= check_package("pydantic")

print(f"\n{'Python version':20} {sys.version.split()[0]}")

# Check conda environment
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

print("=" * 70)

if not packages_ok:
    print("\n⚠️  ERROR: Pydantic is missing!")
    print("Run: pip install pydantic")
    sys.exit(1)

if conda_env != "whisper_train":
    print(f"\n⚠️  WARNING: Current environment is '{conda_env}', expected 'whisper_train'")

print("\n✅ Environment check passed!\n")

# ============================================================================
# 2. LOAD AND VALIDATE TAGS FILE
# ============================================================================

def load_and_validate_tags_file(tags_file_path: str, language_code: str) -> Dict:
    """
    Load and validate a tags file, extract all tags and metadata
    Returns a dictionary with validation results
    """
    result = {
        'language_code': language_code,
        'file_path': tags_file_path,
        'file_exists': False,
        'file_size': 0,
        'loaded_successfully': False,
        'pydantic_models': [],
        'total_tags': 0,
        'tags': set(),
        'tags_by_model': {},
        'errors': []
    }
    
    tags_path = Path(tags_file_path)
    
    # Check if file exists
    if not tags_path.exists():
        result['errors'].append(f"File not found: {tags_path.absolute()}")
        return result
    
    result['file_exists'] = True
    result['file_size'] = tags_path.stat().st_size
    
    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(f"tags_module_{language_code}", tags_path)
        tags_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tags_module)
        
        result['loaded_successfully'] = True
        
        # Extract all Pydantic models from the module
        for attr_name in dir(tags_module):
            # Skip private/magic attributes
            if attr_name.startswith('_'):
                continue
                
            attr = getattr(tags_module, attr_name)
            
            # Check if it's a class
            if not inspect.isclass(attr):
                continue
            
            # Check if it's a Pydantic model
            model_tags = []
            is_pydantic_model = False
            
            # Try Pydantic V2
            if hasattr(attr, 'model_fields'):
                is_pydantic_model = True
                result['pydantic_models'].append({
                    'name': attr_name,
                    'version': 'V2',
                    'field_count': len(attr.model_fields)
                })
                
                for field_name, field in attr.model_fields.items():
                    # Extract Literal values
                    if hasattr(field.annotation, '__args__'):
                        for literal_value in field.annotation.__args__:
                            if isinstance(literal_value, str):
                                model_tags.append(literal_value)
                                result['tags'].add(literal_value)
            
            # Try Pydantic V1 fallback
            elif hasattr(attr, '__fields__'):
                is_pydantic_model = True
                result['pydantic_models'].append({
                    'name': attr_name,
                    'version': 'V1',
                    'field_count': len(attr.__fields__)
                })
                
                for field_name, field in attr.__fields__.items():
                    if hasattr(field.annotation, '__args__'):
                        for literal_value in field.annotation.__args__:
                            if isinstance(literal_value, str):
                                model_tags.append(literal_value)
                                result['tags'].add(literal_value)
            
            if is_pydantic_model:
                result['tags_by_model'][attr_name] = model_tags
        
        result['total_tags'] = len(result['tags'])
        
        # Validate that we found at least one model
        if not result['pydantic_models']:
            result['errors'].append("No Pydantic models found in file")
        
        # Validate that we found tags
        if result['total_tags'] == 0:
            result['errors'].append("No tags extracted from Pydantic models")
    
    except SyntaxError as e:
        result['errors'].append(f"Syntax error in file: {e}")
    except Exception as e:
        result['errors'].append(f"Error loading file: {e}")
    
    return result

# ============================================================================
# 3. DEBUG FILES
# ============================================================================

def debug_file(language_code: str):
    """Debug a single tags file"""
    
    if language_code not in TAGS_FILES:
        print(f"✗ Unknown language code: {language_code}")
        print(f"  Available: {', '.join(TAGS_FILES.keys())}")
        return False
    
    tags_file = TAGS_FILES[language_code]
    
    print("=" * 70)
    print(f"DEBUGGING: {language_code.upper()} - {tags_file}")
    print("=" * 70)
    
    result = load_and_validate_tags_file(tags_file, language_code)
    
    # Display results
    print(f"\n📄 File Information:")
    print(f"  Path: {result['file_path']}")
    print(f"  Exists: {'✓ Yes' if result['file_exists'] else '✗ No'}")
    
    if result['file_exists']:
        print(f"  Size: {result['file_size']:,} bytes ({result['file_size']/1024:.1f} KB)")
    
    if result['errors']:
        print(f"\n❌ ERRORS FOUND:")
        for error in result['errors']:
            print(f"  • {error}")
        return False
    
    print(f"\n✅ File loaded successfully!")
    
    # Display Pydantic models
    print(f"\n📦 Pydantic Models Found: {len(result['pydantic_models'])}")
    for model in result['pydantic_models']:
        print(f"  • {model['name']}")
        print(f"    - Pydantic version: {model['version']}")
        print(f"    - Fields: {model['field_count']}")
    
    # Display tags statistics
    print(f"\n📊 Tags Statistics:")
    print(f"  Total unique tags: {result['total_tags']}")
    
    # Tags by model
    print(f"\n📋 Tags by Model:")
    for model_name, tags in result['tags_by_model'].items():
        print(f"  • {model_name}: {len(tags)} tags")
    
    # Display sample tags
    print(f"\n🏷️  Sample Tags (first {min(SAMPLE_SIZE, len(result['tags']))}):")
    sorted_tags = sorted(list(result['tags']))
    for i, tag in enumerate(sorted_tags[:SAMPLE_SIZE], 1):
        print(f"  {i:3d}. {tag}")
    
    if len(result['tags']) > SAMPLE_SIZE:
        print(f"  ... and {len(result['tags']) - SAMPLE_SIZE} more tags")
    
    # Check for duplicates
    all_tags_list = []
    for tags in result['tags_by_model'].values():
        all_tags_list.extend(tags)
    
    if len(all_tags_list) != len(result['tags']):
        duplicates = len(all_tags_list) - len(result['tags'])
        print(f"\n⚠️  Warning: {duplicates} duplicate tags found across models")
    
    # Tag length analysis
    tag_lengths = [len(tag) for tag in result['tags']]
    if tag_lengths:
        print(f"\n📏 Tag Length Analysis:")
        print(f"  Shortest: {min(tag_lengths)} chars")
        print(f"  Longest: {max(tag_lengths)} chars")
        print(f"  Average: {sum(tag_lengths)/len(tag_lengths):.1f} chars")
    
    # Find potentially problematic tags
    problematic = []
    for tag in result['tags']:
        if '  ' in tag:  # Double spaces
            problematic.append((tag, 'Contains double spaces'))
        if tag != tag.strip():  # Leading/trailing whitespace
            problematic.append((tag, 'Has leading/trailing whitespace'))
        if any(char in tag for char in ['\n', '\t', '\r']):
            problematic.append((tag, 'Contains newline/tab characters'))
    
    if problematic:
        print(f"\n⚠️  Potentially Problematic Tags ({len(problematic)}):")
        for tag, issue in problematic[:10]:
            print(f"  • '{tag}' - {issue}")
        if len(problematic) > 10:
            print(f"  ... and {len(problematic) - 10} more")
    
    print(f"\n{'=' * 70}")
    print(f"✅ {language_code.upper()} validation complete - File is OK!")
    print(f"{'=' * 70}\n")
    
    return True

# ============================================================================
# 4. RUN DEBUGGER
# ============================================================================

print("=" * 70)
print("STARTING VALIDATION")
print("=" * 70)

if DEBUG_LANGUAGE == 'all':
    # Debug all files
    print(f"\nDebugging all {len(TAGS_FILES)} files...\n")
    
    results = {}
    for lang_code in TAGS_FILES.keys():
        success = debug_file(lang_code)
        results[lang_code] = success
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - ALL FILES")
    print("=" * 70)
    
    for lang_code, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{lang_code.upper():4} - {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} files passed validation")
    
    if passed == total:
        print("🎉 All files are valid!")
    else:
        print(f"⚠️  {total - passed} file(s) have issues")

else:
    # Debug single file
    success = debug_file(DEBUG_LANGUAGE)
    
    if success:
        print("🎉 File validation successful!")
    else:
        print("❌ File validation failed - check errors above")
        sys.exit(1)

print("\n✅ Debugging complete!\n")




