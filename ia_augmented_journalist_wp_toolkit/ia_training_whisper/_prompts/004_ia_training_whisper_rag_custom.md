## PROMPT_1

As a python and whisper expert, can you write a python script that

1. load whisper and make the transcription from an audio file named `APPELS_ACTU_14-01-26.mp3` that is stored locally in `source/kiswahili/`. Put this file in a variable so I can update it easily.
2. Output at the beginning of the script to check installation and see if all the packages are properly installed. So that indicates that the env is OK.
3. I am using anaconda to manage the python environment. The name of the env is `whisper_train`





## OUTPUT_1


```python
#!/usr/bin/env python3
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
print(f"\nTranscribing... (this may take several minutes)")

try:
    result = model.transcribe(
        str(audio_path),
        language=LANGUAGE,
        task="transcribe",
        verbose=True  # Shows progress
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
```

## What's New

The enhanced script now:

1. **Checks for cached models** before loading
2. **Shows cache location and size** if model already exists
3. **Displays expected download size** for first-time downloads
4. **Confirms "No download needed"** for subsequent runs

## Sample Output (First Run)

```
======================================================================
LOADING WHISPER MODEL
======================================================================
⬇ Downloading model: small
  This will only happen once - model will be cached for future use
  Expected size: ~461 MB
✓ Model loaded successfully
  Device: mps
```

## Sample Output (Subsequent Runs)

```
======================================================================
LOADING WHISPER MODEL
======================================================================
✓ Using cached model: small
  Location: /Users/bruno/.cache/whisper/small.pt
  Size: 461.2 MB
  (No download needed)
✓ Model loaded successfully
  Device: mps
```

Save this as `transcribe_kiswahili.py` and run with:

```bash
conda activate whisper_train
python transcribe_kiswahili.py
```

Perfect for your workflow - fast subsequent runs! 🚀