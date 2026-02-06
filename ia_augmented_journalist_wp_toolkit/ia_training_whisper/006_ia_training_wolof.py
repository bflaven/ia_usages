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
python 006_ia_training_wolof.py


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
LANGUAGE = "wol"  
AUDIO_FILE = "info_foot_en_wolof.mp3"
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








