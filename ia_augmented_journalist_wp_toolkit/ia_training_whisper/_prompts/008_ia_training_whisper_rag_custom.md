## PROMPT_2
As a python, can you rewrite the python script so I can select more models and language for instance for the Kiswahili, I want to be able with only a config change to select a combination of language and model e.g. kiswahili with facebook/mms-1b-all or kiswahili with whisper large or kiswahili with whisper small... etc.


1. Here are the two models that I want to use :
MODEL_1 : https://huggingface.co/PaschalK/whisper-swahili-small
MODEL_2 : https://huggingface.co/RafatK/Whisper_Largev2-Swahili-Decodis_Comb_FT

2. Do not mess up with the language abbreviation for both models, it seems different for facebook/mms-1b-all or whisper.


## OUTPUT_1

Here's the enhanced script that supports multiple model types including the HuggingFace fine-tuned Whisper models:

```python
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
python 009_ia_training_kiswahili.py
"""

"""
Transcription Multi-Langues - Whisper + MMS + Fine-tuned Models
Supporte: Kiswahili, Portugais, Chinois, Hausa, Vietnamien, WOLOF
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path
import time

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================

# Language configurations with model codes
LANGUAGE_CONFIGS = {
    'kiswahili': {
        'name': 'Kiswahili',
        'audio_dir': 'source/kiswahili',
        'whisper_code': 'sw',      # ISO 639-1 for Whisper
        'mms_code': 'swh'          # ISO 639-3 for MMS
    },
    'portuguese': {
        'name': 'Portuguese (Brazilian)',
        'audio_dir': 'source/brazilian',
        'whisper_code': 'pt',
        'mms_code': 'por'          # ISO 639-3
    },
    'chinese': {
        'name': 'Chinese (Simplified)',
        'audio_dir': 'source/chinese',
        'whisper_code': 'zh',
        'mms_code': 'cmn'          # ISO 639-3 (Mandarin)
    },
    'hausa': {
        'name': 'Hausa',
        'audio_dir': 'source/hausa',
        'whisper_code': 'ha',
        'mms_code': 'hau'          # ISO 639-3
    },
    'vietnamese': {
        'name': 'Vietnamese',
        'audio_dir': 'source/vietnamese',
        'whisper_code': 'vi',
        'mms_code': 'vie'          # ISO 639-3
    },
    'wolof': {
        'name': 'Wolof',
        'audio_dir': 'source/wolof',
        'whisper_code': 'wo',      # Whisper might not support this well
        'mms_code': 'wol'          # ISO 639-3
    }
}

# Model configurations
# Types: 'whisper' (OpenAI), 'whisper_hf' (HuggingFace), 'mms' (Meta)
MODEL_CONFIGS = {
    # OpenAI Whisper models (using whisper library)
    'whisper_tiny': {
        'type': 'whisper',
        'size': 'tiny',
        'display_name': 'Whisper Tiny',
        'requires_lang': True
    },
    'whisper_base': {
        'type': 'whisper',
        'size': 'base',
        'display_name': 'Whisper Base',
        'requires_lang': True
    },
    'whisper_small': {
        'type': 'whisper',
        'size': 'small',
        'display_name': 'Whisper Small',
        'requires_lang': True
    },
    'whisper_medium': {
        'type': 'whisper',
        'size': 'medium',
        'display_name': 'Whisper Medium',
        'requires_lang': True
    },
    'whisper_large': {
        'type': 'whisper',
        'size': 'large',
        'display_name': 'Whisper Large',
        'requires_lang': True
    },
    'whisper_large_v2': {
        'type': 'whisper',
        'size': 'large-v2',
        'display_name': 'Whisper Large V2',
        'requires_lang': True
    },
    'whisper_large_v3': {
        'type': 'whisper',
        'size': 'large-v3',
        'display_name': 'Whisper Large V3',
        'requires_lang': True
    },
    
    # Meta MMS model
    'mms': {
        'type': 'mms',
        'model_name': 'facebook/mms-1b-all',
        'display_name': 'Meta MMS 1B',
        'requires_lang': True
    },
    
    # HuggingFace Fine-tuned Whisper models for Swahili
    'whisper_swahili_small': {
        'type': 'whisper_hf',
        'model_name': 'PaschalK/whisper-swahili-small',
        'display_name': 'Whisper Swahili Small (Fine-tuned)',
        'requires_lang': False,  # Already trained for Swahili
        'target_language': 'kiswahili'
    },
    'whisper_swahili_large': {
        'type': 'whisper_hf',
        'model_name': 'RafatK/Whisper_Largev2-Swahili-Decodis_Comb_FT',
        'display_name': 'Whisper Large V2 Swahili (Fine-tuned)',
        'requires_lang': False,  # Already trained for Swahili
        'target_language': 'kiswahili'
    },
    
    # You can add more HuggingFace models here
    # Example for other languages:
    # 'whisper_portuguese_small': {
    #     'type': 'whisper_hf',
    #     'model_name': 'username/whisper-portuguese-small',
    #     'display_name': 'Whisper Portuguese Small (Fine-tuned)',
    #     'requires_lang': False,
    #     'target_language': 'portuguese'
    # },
}

# ============================================================================
# SELECT YOUR CONFIGURATION HERE
# ============================================================================

# Choose language: kiswahili, portuguese, chinese, hausa, vietnamese, wolof
SELECTED_LANGUAGE = "kiswahili"

# Choose model from MODEL_CONFIGS keys above
# Options: whisper_tiny, whisper_base, whisper_small, whisper_medium, 
#          whisper_large, whisper_large_v2, whisper_large_v3,
#          mms, whisper_swahili_small, whisper_swahili_large
SELECTED_MODEL = "whisper_swahili_small"

# Audio file to transcribe
AUDIO_FILE = "SIHA_NJEMA13-01-26_OK.mp3"

# ============================================================================
# AUTO-CONFIGURATION (Don't edit below this line)
# ============================================================================

# Validate selections
if SELECTED_LANGUAGE not in LANGUAGE_CONFIGS:
    print(f"✗ ERROR: Invalid language '{SELECTED_LANGUAGE}'")
    print(f"  Available languages: {', '.join(LANGUAGE_CONFIGS.keys())}")
    sys.exit(1)

if SELECTED_MODEL not in MODEL_CONFIGS:
    print(f"✗ ERROR: Invalid model '{SELECTED_MODEL}'")
    print(f"  Available models: {', '.join(MODEL_CONFIGS.keys())}")
    sys.exit(1)

# Get configurations
lang_config = LANGUAGE_CONFIGS[SELECTED_LANGUAGE]
model_config = MODEL_CONFIGS[SELECTED_MODEL]

# Check if model is compatible with selected language
if 'target_language' in model_config:
    if model_config['target_language'] != SELECTED_LANGUAGE:
        print(f"⚠️  WARNING: Model '{SELECTED_MODEL}' is fine-tuned for '{model_config['target_language']}' "
              f"but you selected language '{SELECTED_LANGUAGE}'")
        print(f"   This may produce poor results. Consider using a different model.")
        response = input("   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

AUDIO_DIR = lang_config['audio_dir']
MODEL_TYPE = model_config['type']

# ============================================================================
# 1. ENVIRONMENT CHECK
# ============================================================================
print("=" * 70)
print("MULTI-LANGUAGE TRANSCRIPTION - ENVIRONMENT CHECK")
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
if MODEL_TYPE == 'whisper':
    packages_ok &= check_package("whisper")
elif MODEL_TYPE in ['mms', 'whisper_hf']:
    packages_ok &= check_package("transformers")

packages_ok &= check_package("torch")

print(f"\n{'Python version':20} {sys.version.split()[0]}")
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

# Check for MPS/CUDA
import torch
if torch.backends.mps.is_available():
    device = "mps"
    print(f"{'Device':20} MPS (Apple Silicon)")
elif torch.cuda.is_available():
    device = "cuda"
    print(f"{'Device':20} CUDA (GPU)")
else:
    device = "cpu"
    print(f"{'Device':20} CPU")

print("=" * 70)

if not packages_ok:
    print("\n⚠️  ERROR: Some packages are missing!")
    if MODEL_TYPE == 'whisper':
        print("Run: pip install openai-whisper")
    else:
        print("Run: pip install transformers accelerate")
    sys.exit(1)

print("\n✅ Environment check passed!\n")

# Display configuration
print("=" * 70)
print("CONFIGURATION")
print("=" * 70)
print(f"Language: {lang_config['name']} ({SELECTED_LANGUAGE})")
print(f"Model: {model_config['display_name']}")
print(f"Model type: {MODEL_TYPE.upper()}")

if MODEL_TYPE == 'whisper':
    print(f"Whisper size: {model_config['size']}")
    print(f"Language code: {lang_config['whisper_code']}")
elif MODEL_TYPE == 'mms':
    print(f"MMS model: {model_config['model_name']}")
    print(f"Language code: {lang_config['mms_code']}")
elif MODEL_TYPE == 'whisper_hf':
    print(f"HuggingFace model: {model_config['model_name']}")
    if model_config['requires_lang']:
        print(f"Language code: {lang_config['whisper_code']}")
    else:
        print(f"Pre-trained for: {model_config.get('target_language', 'specific language')}")

print(f"Audio file: {AUDIO_FILE}")
print(f"Audio directory: {AUDIO_DIR}")
print("=" * 70 + "\n")

# ============================================================================
# 2. LOAD MODEL
# ============================================================================
print("=" * 70)
print(f"LOADING {model_config['display_name'].upper()}")
print("=" * 70)

try:
    load_start = time.time()
    
    if MODEL_TYPE == 'whisper':
        # Load OpenAI Whisper
        import whisper
        
        model_size = model_config['size']
        cache_dir = Path.home() / '.cache' / 'whisper'
        model_file = cache_dir / f'{model_size}.pt'
        
        if model_file.exists():
            print(f"✓ Using cached Whisper model: {model_size}")
            print(f"  Location: {model_file}")
            print(f"  Size: {model_file.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print(f"⬇ Downloading Whisper model: {model_size}")
        
        model = whisper.load_model(model_size)
        
    elif MODEL_TYPE == 'mms':
        # Load Meta MMS
        from transformers import pipeline
        
        model_name = model_config['model_name']
        print(f"Loading MMS model: {model_name}")
        print("(First run will download ~1.2 GB)")
        
        model = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            device=0 if device == "cuda" else -1
        )
    
    elif MODEL_TYPE == 'whisper_hf':
        # Load HuggingFace Whisper model
        from transformers import pipeline
        
        model_name = model_config['model_name']
        print(f"Loading HuggingFace model: {model_name}")
        print("(First run will download the model)")
        
        # Determine device for pipeline
        if device == "cuda":
            device_id = 0
        elif device == "mps":
            device_id = 0  # MPS support in transformers
        else:
            device_id = -1  # CPU
        
        model = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            device=device_id
        )
    
    load_time = time.time() - load_start
    print(f"✓ Model loaded successfully in {load_time:.1f} seconds")
    
except Exception as e:
    print(f"✗ Error loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 3. TRANSCRIBE
# ============================================================================
print("\n" + "=" * 70)
print("TRANSCRIPTION")
print("=" * 70)

audio_path = Path(AUDIO_DIR) / AUDIO_FILE

if not audio_path.exists():
    print(f"✗ ERROR: Audio file not found!")
    print(f"  Looking for: {audio_path.absolute()}")
    sys.exit(1)

print(f"Audio file: {audio_path}")
print(f"File size: {audio_path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"Language: {lang_config['name']}")
print(f"\nTranscribing...")

try:
    transcribe_start = time.time()
    
    if MODEL_TYPE == 'whisper':
        # OpenAI Whisper transcription
        lang_code = lang_config['whisper_code']
        use_fp16 = device == "cuda"
        
        result = model.transcribe(
            str(audio_path),
            language=lang_code,
            task="transcribe",
            verbose=True,
            fp16=use_fp16
        )
        
        transcript_text = result["text"]
        
    elif MODEL_TYPE == 'mms':
        # MMS transcription
        lang_code = lang_config['mms_code']
        
        result = model(
            str(audio_path),
            generate_kwargs={"language": lang_code}
        )
        
        transcript_text = result["text"]
    
    elif MODEL_TYPE == 'whisper_hf':
        # HuggingFace Whisper transcription
        
        # Prepare generation kwargs
        generate_kwargs = {}
        
        # Only add language if model requires it
        if model_config['requires_lang']:
            lang_code = lang_config['whisper_code']
            generate_kwargs["language"] = lang_code
            generate_kwargs["task"] = "transcribe"
        else:
            # Model is already fine-tuned for specific language
            lang_code = f"pre-trained ({model_config.get('target_language', 'unknown')})"
        
        result = model(
            str(audio_path),
            generate_kwargs=generate_kwargs if generate_kwargs else None
        )
        
        transcript_text = result["text"]
    
    transcribe_time = time.time() - transcribe_start
    
    print("\n" + "=" * 70)
    print("TRANSCRIPTION RESULT")
    print("=" * 70)
    print(transcript_text)
    print("=" * 70)
    
    # Save to file
    output_file = audio_path.parent / f"{audio_path.stem}_{SELECTED_MODEL}_{SELECTED_LANGUAGE}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Model: {model_config['display_name']}\n")
        if MODEL_TYPE in ['mms', 'whisper_hf']:
            f.write(f"Model ID: {model_config.get('model_name', 'N/A')}\n")
        f.write(f"Language: {lang_config['name']} ({SELECTED_LANGUAGE})\n")
        f.write(f"Language code: {lang_code}\n")
        f.write(f"Transcription time: {transcribe_time:.1f}s\n")
        f.write(f"\n{transcript_text}\n")
    
    print(f"\n✓ Transcription saved to: {output_file}")
    print(f"⏱  Transcription time: {transcribe_time:.1f} seconds ({transcribe_time/60:.1f} minutes)")
    
except Exception as e:
    print(f"\n✗ Error during transcription: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Transcription completed successfully!")
```

## Key Features:

### 1. **Three Model Types Supported:**
- `whisper` - OpenAI Whisper models (using openai-whisper library)
- `whisper_hf` - HuggingFace fine-tuned Whisper models (using transformers)
- `mms` - Meta MMS models (using transformers)

### 2. **Easy Configuration:**
```python
# Just change these two lines:
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "whisper_swahili_small"  # or "whisper_swahili_large"
```

### 3. **Language Code Handling:**
- **OpenAI Whisper**: Uses ISO 639-1 (`sw` for Kiswahili)
- **MMS**: Uses ISO 639-3 (`swh` for Kiswahili)
- **Fine-tuned models**: No language code needed (already trained for specific language)

### 4. **Model Compatibility Check:**
The script warns you if you try to use a language-specific model with the wrong language.

### 5. **Usage Examples:**

```python
# Kiswahili with fine-tuned small model
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "whisper_swahili_small"

# Kiswahili with fine-tuned large model
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "whisper_swahili_large"

# Kiswahili with standard Whisper
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "whisper_large"

# Kiswahili with MMS
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "mms"

# Portuguese with standard Whisper
SELECTED_LANGUAGE = "portuguese"
SELECTED_MODEL = "whisper_medium"
```

### 6. **Adding More Models:**
To add more HuggingFace models, just add to `MODEL_CONFIGS`:

```python
'your_model_name': {
    'type': 'whisper_hf',
    'model_name': 'username/model-name-on-huggingface',
    'display_name': 'Your Model Display Name',
    'requires_lang': False,  # True if generic, False if language-specific
    'target_language': 'portuguese'  # Only if language-specific
}
```




## PROMPT_1

As a python, can you rewrite the python script below so I will be able to define the model that I want to use for each language for instance for the Kiswahili, I want to be able with only a config change to select a combination of language and model e.g. kiswahili with facebook/mms-1b-all or kiswahili with whisper large or kiswahili with whisper small... etc.

Do not mess up with the language abbreviation for both models, it seems different for facebook/mms-1b-all or whisper.

```python
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
python 009_ia_training_kiswahili.py


"""

"""
Transcription Multi-Langues - Whisper + MMS
Supporte: Kiswahili, Portugais, Chinois, Hausa, Vietnamien, WOLOF
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path
import time

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================

# Language configurations
LANGUAGE_CONFIGS = {
    'sw': {
        'name': 'Kiswahili',
        'audio_dir': 'source/kiswahili',
        'model': 'whisper',
        'whisper_code': 'sw'
    },
    'pt': {
        'name': 'Portuguese (Brazilian)',
        'audio_dir': 'source/brazilian',
        'model': 'whisper',
        'whisper_code': 'pt'
    },
    'zh': {
        'name': 'Chinese (Simplified)',
        'audio_dir': 'source/chinese',
        'model': 'whisper',
        'whisper_code': 'zh'
    },
    'ha': {
        'name': 'Hausa',
        'audio_dir': 'source/hausa',
        'model': 'whisper',
        'whisper_code': 'ha'
    },
    'vi': {
        'name': 'Vietnamese',
        'audio_dir': 'source/vietnamese',
        'model': 'whisper',
        'whisper_code': 'vi'
    },
    'wol': {
        'name': 'Wolof',
        'audio_dir': 'source/wolof',
        'model': 'mms',
        'mms_code': 'wol'
    }
}

# Select language and model
# Change to: sw, pt, zh, ha, vi, or wol
LANGUAGE = "sw"  
AUDIO_FILE = "SIHA_NJEMA13-01-26_OK.mp3"
# For Whisper: tiny, base, small, medium, large
WHISPER_MODEL_SIZE = "small"  

# Auto-configure
config = LANGUAGE_CONFIGS[LANGUAGE]
AUDIO_DIR = config['audio_dir']
MODEL_TYPE = config['model']

# ============================================================================
# 1. ENVIRONMENT CHECK
# ============================================================================
print("=" * 70)
print("MULTI-LANGUAGE TRANSCRIPTION - ENVIRONMENT CHECK")
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
if MODEL_TYPE == 'whisper':
    packages_ok &= check_package("whisper")
elif MODEL_TYPE == 'mms':
    packages_ok &= check_package("transformers")

packages_ok &= check_package("torch")

print(f"\n{'Python version':20} {sys.version.split()[0]}")
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

# Check for MPS/CUDA
import torch
if torch.backends.mps.is_available():
    device = "mps"
    print(f"{'Device':20} MPS (Apple Silicon)")
elif torch.cuda.is_available():
    device = "cuda"
    print(f"{'Device':20} CUDA (GPU)")
else:
    device = "cpu"
    print(f"{'Device':20} CPU")

print("=" * 70)

if not packages_ok:
    print("\n⚠️  ERROR: Some packages are missing!")
    if MODEL_TYPE == 'whisper':
        print("Run: pip install openai-whisper")
    else:
        print("Run: pip install transformers accelerate")
    sys.exit(1)

print("\n✅ Environment check passed!\n")

# Display configuration
print("=" * 70)
print("CONFIGURATION")
print("=" * 70)
print(f"Language: {config['name']} ({LANGUAGE})")
print(f"Model type: {MODEL_TYPE.upper()}")
print(f"Audio file: {AUDIO_FILE}")
print(f"Audio directory: {AUDIO_DIR}")
print("=" * 70 + "\n")

# ============================================================================
# 2. LOAD MODEL
# ============================================================================
print("=" * 70)
print(f"LOADING {MODEL_TYPE.upper()} MODEL")
print("=" * 70)

try:
    load_start = time.time()
    
    if MODEL_TYPE == 'whisper':
        # Load Whisper
        import whisper
        
        cache_dir = Path.home() / '.cache' / 'whisper'
        model_file = cache_dir / f'{WHISPER_MODEL_SIZE}.pt'
        
        if model_file.exists():
            print(f"✓ Using cached Whisper model: {WHISPER_MODEL_SIZE}")
            print(f"  Location: {model_file}")
            print(f"  Size: {model_file.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print(f"⬇ Downloading Whisper model: {WHISPER_MODEL_SIZE}")
        
        model = whisper.load_model(WHISPER_MODEL_SIZE)
        
    elif MODEL_TYPE == 'mms':
        # Load MMS
        from transformers import pipeline
        
        print("Loading MMS model: facebook/mms-1b-all")
        print("(First run will download ~1.2 GB)")
        
        model = pipeline(
            "automatic-speech-recognition",
            model="facebook/mms-1b-all",
            device=0 if device == "cuda" else -1
        )
    
    load_time = time.time() - load_start
    print(f"✓ Model loaded successfully in {load_time:.1f} seconds")
    
except Exception as e:
    print(f"✗ Error loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 3. TRANSCRIBE
# ============================================================================
print("\n" + "=" * 70)
print("TRANSCRIPTION")
print("=" * 70)

audio_path = Path(AUDIO_DIR) / AUDIO_FILE

if not audio_path.exists():
    print(f"✗ ERROR: Audio file not found!")
    print(f"  Looking for: {audio_path.absolute()}")
    sys.exit(1)

print(f"Audio file: {audio_path}")
print(f"File size: {audio_path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"Language: {config['name']}")
print(f"\nTranscribing...")

try:
    transcribe_start = time.time()
    
    if MODEL_TYPE == 'whisper':
        # Whisper transcription
        lang_code = config['whisper_code']
        use_fp16 = device == "cuda"
        
        result = model.transcribe(
            str(audio_path),
            language=lang_code,
            task="transcribe",
            verbose=True,
            fp16=use_fp16
        )
        
        transcript_text = result["text"]
        
    elif MODEL_TYPE == 'mms':
        # MMS transcription
        lang_code = config['mms_code']
        
        result = model(
            str(audio_path),
            generate_kwargs={"language": lang_code}
        )
        
        transcript_text = result["text"]
    
    transcribe_time = time.time() - transcribe_start
    
    print("\n" + "=" * 70)
    print("TRANSCRIPTION RESULT")
    print("=" * 70)
    print(transcript_text)
    print("=" * 70)
    
    # Save to file
    output_file = audio_path.parent / f"{audio_path.stem}_{MODEL_TYPE}_{LANGUAGE}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Model: {MODEL_TYPE.upper()}\n")
        f.write(f"Language: {config['name']} ({LANGUAGE})\n")
        f.write(f"Transcription time: {transcribe_time:.1f}s\n")
        f.write(f"\n{transcript_text}\n")
    
    print(f"\n✓ Transcription saved to: {output_file}")
    print(f"⏱  Transcription time: {transcribe_time:.1f} seconds ({transcribe_time/60:.1f} minutes)")
    
except Exception as e:
    print(f"\n✗ Error during transcription: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Transcription completed successfully!")
```

## OUTPUT_1

Here's the refactored script that allows you to easily configure language and model combinations:

```python
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
python 009_ia_training_kiswahili.py
"""

"""
Transcription Multi-Langues - Whisper + MMS
Supporte: Kiswahili, Portugais, Chinois, Hausa, Vietnamien, WOLOF
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path
import time

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================

# Language configurations with model codes
LANGUAGE_CONFIGS = {
    'kiswahili': {
        'name': 'Kiswahili',
        'audio_dir': 'source/kiswahili',
        'whisper_code': 'sw',      # ISO 639-1 for Whisper
        'mms_code': 'swh'          # ISO 639-3 for MMS
    },
    'portuguese': {
        'name': 'Portuguese (Brazilian)',
        'audio_dir': 'source/brazilian',
        'whisper_code': 'pt',
        'mms_code': 'por'          # ISO 639-3
    },
    'chinese': {
        'name': 'Chinese (Simplified)',
        'audio_dir': 'source/chinese',
        'whisper_code': 'zh',
        'mms_code': 'cmn'          # ISO 639-3 (Mandarin)
    },
    'hausa': {
        'name': 'Hausa',
        'audio_dir': 'source/hausa',
        'whisper_code': 'ha',
        'mms_code': 'hau'          # ISO 639-3
    },
    'vietnamese': {
        'name': 'Vietnamese',
        'audio_dir': 'source/vietnamese',
        'whisper_code': 'vi',
        'mms_code': 'vie'          # ISO 639-3
    },
    'wolof': {
        'name': 'Wolof',
        'audio_dir': 'source/wolof',
        'whisper_code': 'wo',      # Whisper might not support this well
        'mms_code': 'wol'          # ISO 639-3
    }
}

# Model configurations
MODEL_CONFIGS = {
    'whisper_tiny': {
        'type': 'whisper',
        'size': 'tiny',
        'display_name': 'Whisper Tiny'
    },
    'whisper_base': {
        'type': 'whisper',
        'size': 'base',
        'display_name': 'Whisper Base'
    },
    'whisper_small': {
        'type': 'whisper',
        'size': 'small',
        'display_name': 'Whisper Small'
    },
    'whisper_medium': {
        'type': 'whisper',
        'size': 'medium',
        'display_name': 'Whisper Medium'
    },
    'whisper_large': {
        'type': 'whisper',
        'size': 'large',
        'display_name': 'Whisper Large'
    },
    'mms': {
        'type': 'mms',
        'model_name': 'facebook/mms-1b-all',
        'display_name': 'Meta MMS 1B'
    }
}

# ============================================================================
# SELECT YOUR CONFIGURATION HERE
# ============================================================================

# Choose language: kiswahili, portuguese, chinese, hausa, vietnamese, wolof
SELECTED_LANGUAGE = "kiswahili"

# Choose model: whisper_tiny, whisper_base, whisper_small, whisper_medium, whisper_large, mms
SELECTED_MODEL = "whisper_small"

# Audio file to transcribe
AUDIO_FILE = "SIHA_NJEMA13-01-26_OK.mp3"

# ============================================================================
# AUTO-CONFIGURATION (Don't edit below this line)
# ============================================================================

# Validate selections
if SELECTED_LANGUAGE not in LANGUAGE_CONFIGS:
    print(f"✗ ERROR: Invalid language '{SELECTED_LANGUAGE}'")
    print(f"  Available languages: {', '.join(LANGUAGE_CONFIGS.keys())}")
    sys.exit(1)

if SELECTED_MODEL not in MODEL_CONFIGS:
    print(f"✗ ERROR: Invalid model '{SELECTED_MODEL}'")
    print(f"  Available models: {', '.join(MODEL_CONFIGS.keys())}")
    sys.exit(1)

# Get configurations
lang_config = LANGUAGE_CONFIGS[SELECTED_LANGUAGE]
model_config = MODEL_CONFIGS[SELECTED_MODEL]

AUDIO_DIR = lang_config['audio_dir']
MODEL_TYPE = model_config['type']

# ============================================================================
# 1. ENVIRONMENT CHECK
# ============================================================================
print("=" * 70)
print("MULTI-LANGUAGE TRANSCRIPTION - ENVIRONMENT CHECK")
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
if MODEL_TYPE == 'whisper':
    packages_ok &= check_package("whisper")
elif MODEL_TYPE == 'mms':
    packages_ok &= check_package("transformers")

packages_ok &= check_package("torch")

print(f"\n{'Python version':20} {sys.version.split()[0]}")
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

# Check for MPS/CUDA
import torch
if torch.backends.mps.is_available():
    device = "mps"
    print(f"{'Device':20} MPS (Apple Silicon)")
elif torch.cuda.is_available():
    device = "cuda"
    print(f"{'Device':20} CUDA (GPU)")
else:
    device = "cpu"
    print(f"{'Device':20} CPU")

print("=" * 70)

if not packages_ok:
    print("\n⚠️  ERROR: Some packages are missing!")
    if MODEL_TYPE == 'whisper':
        print("Run: pip install openai-whisper")
    else:
        print("Run: pip install transformers accelerate")
    sys.exit(1)

print("\n✅ Environment check passed!\n")

# Display configuration
print("=" * 70)
print("CONFIGURATION")
print("=" * 70)
print(f"Language: {lang_config['name']} ({SELECTED_LANGUAGE})")
print(f"Model: {model_config['display_name']}")
print(f"Model type: {MODEL_TYPE.upper()}")
if MODEL_TYPE == 'whisper':
    print(f"Whisper size: {model_config['size']}")
    print(f"Language code: {lang_config['whisper_code']}")
else:
    print(f"MMS model: {model_config['model_name']}")
    print(f"Language code: {lang_config['mms_code']}")
print(f"Audio file: {AUDIO_FILE}")
print(f"Audio directory: {AUDIO_DIR}")
print("=" * 70 + "\n")

# ============================================================================
# 2. LOAD MODEL
# ============================================================================
print("=" * 70)
print(f"LOADING {model_config['display_name'].upper()}")
print("=" * 70)

try:
    load_start = time.time()
    
    if MODEL_TYPE == 'whisper':
        # Load Whisper
        import whisper
        
        model_size = model_config['size']
        cache_dir = Path.home() / '.cache' / 'whisper'
        model_file = cache_dir / f'{model_size}.pt'
        
        if model_file.exists():
            print(f"✓ Using cached Whisper model: {model_size}")
            print(f"  Location: {model_file}")
            print(f"  Size: {model_file.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print(f"⬇ Downloading Whisper model: {model_size}")
        
        model = whisper.load_model(model_size)
        
    elif MODEL_TYPE == 'mms':
        # Load MMS
        from transformers import pipeline
        
        model_name = model_config['model_name']
        print(f"Loading MMS model: {model_name}")
        print("(First run will download ~1.2 GB)")
        
        model = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            device=0 if device == "cuda" else -1
        )
    
    load_time = time.time() - load_start
    print(f"✓ Model loaded successfully in {load_time:.1f} seconds")
    
except Exception as e:
    print(f"✗ Error loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 3. TRANSCRIBE
# ============================================================================
print("\n" + "=" * 70)
print("TRANSCRIPTION")
print("=" * 70)

audio_path = Path(AUDIO_DIR) / AUDIO_FILE

if not audio_path.exists():
    print(f"✗ ERROR: Audio file not found!")
    print(f"  Looking for: {audio_path.absolute()}")
    sys.exit(1)

print(f"Audio file: {audio_path}")
print(f"File size: {audio_path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"Language: {lang_config['name']}")
print(f"\nTranscribing...")

try:
    transcribe_start = time.time()
    
    if MODEL_TYPE == 'whisper':
        # Whisper transcription
        lang_code = lang_config['whisper_code']
        use_fp16 = device == "cuda"
        
        result = model.transcribe(
            str(audio_path),
            language=lang_code,
            task="transcribe",
            verbose=True,
            fp16=use_fp16
        )
        
        transcript_text = result["text"]
        
    elif MODEL_TYPE == 'mms':
        # MMS transcription
        lang_code = lang_config['mms_code']
        
        result = model(
            str(audio_path),
            generate_kwargs={"language": lang_code}
        )
        
        transcript_text = result["text"]
    
    transcribe_time = time.time() - transcribe_start
    
    print("\n" + "=" * 70)
    print("TRANSCRIPTION RESULT")
    print("=" * 70)
    print(transcript_text)
    print("=" * 70)
    
    # Save to file
    output_file = audio_path.parent / f"{audio_path.stem}_{SELECTED_MODEL}_{SELECTED_LANGUAGE}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Model: {model_config['display_name']}\n")
        f.write(f"Language: {lang_config['name']} ({SELECTED_LANGUAGE})\n")
        f.write(f"Language code: {lang_code}\n")
        f.write(f"Transcription time: {transcribe_time:.1f}s\n")
        f.write(f"\n{transcript_text}\n")
    
    print(f"\n✓ Transcription saved to: {output_file}")
    print(f"⏱  Transcription time: {transcribe_time:.1f} seconds ({transcribe_time/60:.1f} minutes)")
    
except Exception as e:
    print(f"\n✗ Error during transcription: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Transcription completed successfully!")
```

## Key Changes:

1. **Separated language and model configurations** - Languages are now independent from models
2. **Both language codes included** - Each language has both `whisper_code` (ISO 639-1) and `mms_code` (ISO 639-3)
3. **Easy configuration at the top**:
   ```python
   SELECTED_LANGUAGE = "kiswahili"
   SELECTED_MODEL = "whisper_small"
   ```

## Usage Examples:

```python
# Kiswahili with Whisper Large
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "whisper_large"

# Kiswahili with MMS
SELECTED_LANGUAGE = "kiswahili"
SELECTED_MODEL = "mms"

# Portuguese with Whisper Small
SELECTED_LANGUAGE = "portuguese"
SELECTED_MODEL = "whisper_small"

# Wolof with MMS (recommended for low-resource languages)
SELECTED_LANGUAGE = "wolof"
SELECTED_MODEL = "mms"
```

The script now correctly handles language code differences and validates your selections before running!


