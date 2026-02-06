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
python 001_ia_training_whisper.py

"""
"""
Whisper Transcription Script for Kiswahili
Environment: whisper_train (Anaconda)
"""

import sys
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================
# PUT YOUR OWN FILES
AUDIO_FILE = "APPELS_ACTU_14-01-26.mp3"
AUDIO_DIR = "source/kiswahili"
LANGUAGE = "sw"  # Kiswahili
MODEL_SIZE = "small"  # Options: tiny, base, small, medium, large

# ============================================================================
# 1. ENVIRONMENT CHECK
# ============================================================================
print("=" * 70)
print("WHISPER ENVIRONMENT CHECK")
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

# Check all required packages
packages_ok = True
packages_ok &= check_package("whisper")
packages_ok &= check_package("torch")
packages_ok &= check_package("transformers")
packages_ok &= check_package("datasets")
packages_ok &= check_package("accelerate")
packages_ok &= check_package("evaluate")
packages_ok &= check_package("jiwer")
packages_ok &= check_package("numpy")

# Check Python version
print(f"\n{'Python version':20} {sys.version.split()[0]}")

# Check conda environment
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

# Check for MPS (Apple Silicon) or CUDA
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
    print("Run: pip install openai-whisper datasets transformers accelerate evaluate jiwer")
    sys.exit(1)

if conda_env != "whisper_train":
    print(f"\n⚠️  WARNING: Current environment is '{conda_env}', expected 'whisper_train'")
    print("Run: conda activate whisper_train")
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        sys.exit(1)

print("\n✅ Environment check passed!\n")

# ============================================================================
# 2. LOAD WHISPER MODEL
# ============================================================================
print("=" * 70)
print("LOADING WHISPER MODEL")
print("=" * 70)

import whisper

# Check if model is cached
cache_dir = Path.home() / '.cache' / 'whisper'
model_file = cache_dir / f'{MODEL_SIZE}.pt'

if model_file.exists():
    print(f"✓ Using cached model: {MODEL_SIZE}")
    print(f"  Location: {model_file}")
    print(f"  Size: {model_file.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"  (No download needed)")
else:
    print(f"⬇ Downloading model: {MODEL_SIZE}")
    print(f"  This will only happen once - model will be cached for future use")
    model_sizes = {
        'tiny': '39 MB',
        'base': '142 MB',
        'small': '461 MB',
        'medium': '1.5 GB',
        'large': '2.9 GB'
    }
    print(f"  Expected size: ~{model_sizes.get(MODEL_SIZE, 'unknown')}")

try:
    model = whisper.load_model(MODEL_SIZE)
    print(f"✓ Model loaded successfully")
    print(f"  Device: {device}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    sys.exit(1)

# ============================================================================
# 3. TRANSCRIBE AUDIO FILE
# ============================================================================
print("\n" + "=" * 70)
print("TRANSCRIPTION")
print("=" * 70)

# Construct full path
audio_path = Path(AUDIO_DIR) / AUDIO_FILE

# Check if file exists
if not audio_path.exists():
    print(f"✗ ERROR: Audio file not found!")
    print(f"  Looking for: {audio_path.absolute()}")
    print(f"\nCurrent directory: {Path.cwd()}")
    print(f"\nMake sure the file exists at: {audio_path}")
    sys.exit(1)

print(f"Audio file: {audio_path}")
print(f"File size: {audio_path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"Language: {LANGUAGE} (Kiswahili)")

# Set FP16 based on device capability
use_fp16 = device == "cuda"  # Only CUDA supports FP16
print(f"Precision: {'FP16' if use_fp16 else 'FP32'}")
print(f"\nTranscribing... (this may take several minutes)")

try:
    result = model.transcribe(
        str(audio_path),
        language=LANGUAGE,
        task="transcribe",
        verbose=True,  # Shows progress
        fp16=use_fp16  # Disable FP16 for CPU/MPS
    )
    
    print("\n" + "=" * 70)
    print("TRANSCRIPTION RESULT")
    print("=" * 70)
    print(result["text"])
    print("=" * 70)
    
    # Save to file
    output_file = audio_path.with_suffix('.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result["text"])
    
    print(f"\n✓ Transcription saved to: {output_file}")
    
    # Show additional info
    if "segments" in result:
        print(f"\nNumber of segments: {len(result['segments'])}")
        print(f"Detected language: {result.get('language', 'N/A')}")
    
except Exception as e:
    print(f"\n✗ Error during transcription: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Transcription completed successfully!")









