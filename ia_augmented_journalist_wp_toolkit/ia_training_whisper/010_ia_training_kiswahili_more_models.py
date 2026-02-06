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
python 010_ia_training_kiswahili_more_models.py
"""

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

# CRITICAL: Upgrade PyTorch to 2.6+ (security requirement)
pip install --upgrade torch torchvision torchaudio

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
# Install PyTorch 2.6+ FIRST (required for security)
pip install --upgrade torch>=2.6.0 torchvision torchaudio

# Install core dependencies
pip install openai-whisper
pip install datasets
pip install transformers>=4.50.0
pip install accelerate
pip install evaluate jiwer

# For Mac M1/M2 - use conda for better compatibility
conda install pytorch torchvision torchaudio -c pytorch

# Check Installation
python -c "import whisper; print(whisper.__version__)"
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import transformers; print('Transformers:', transformers.__version__)"

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_training_whisper/

# launch the file
python 010_ia_training_kiswahili_more_models.py
"""

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

# CRITICAL: Upgrade PyTorch to 2.6+ (security requirement)
pip install --upgrade torch torchvision torchaudio

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
# Install PyTorch 2.6+ FIRST (required for security)
pip install --upgrade torch>=2.6.0 torchvision torchaudio

# Install core dependencies
pip install openai-whisper
pip install datasets
pip install transformers>=4.50.0
pip install accelerate
pip install evaluate jiwer
pip install protobuf  # CRITICAL: Required for some tokenizers

# For Mac M1/M2 - use conda for better compatibility
conda install pytorch torchvision torchaudio -c pytorch

# Check Installation
python -c "import whisper; print(whisper.__version__)"
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import transformers; print('Transformers:', transformers.__version__)"
python -c "import google.protobuf; print('Protobuf:', google.protobuf.__version__)"

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_training_whisper/

# launch the file
python 010_ia_training_kiswahili_more_models.py
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
        'target_language': 'kiswahili',
        'fallback_processor': 'openai/whisper-small'  # Fallback if tokenizer missing
    },
    'whisper_swahili_large': {
        'type': 'whisper_hf',
        'model_name': 'RafatK/Whisper_Largev2-Swahili-Decodis_Comb_FT',
        'display_name': 'Whisper Large V2 Swahili (Fine-tuned)',
        'requires_lang': False,  # Already trained for Swahili
        'target_language': 'kiswahili',
        'fallback_processor': 'openai/whisper-large-v2'  # Fallback if tokenizer missing
    },
}

# ============================================================================
# SELECT YOUR CONFIGURATION HERE
# ============================================================================

# Choose language: kiswahili, portuguese, chinese, hausa, vietnamese, wolof
SELECTED_LANGUAGE = "kiswahili"

# Choose model from MODEL_CONFIGS keys above
SELECTED_MODEL = "whisper_swahili_large"

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
    # Check for protobuf (required for some tokenizers)
    try:
        import google.protobuf
        print(f"✓ {'protobuf':20} {google.protobuf.__version__}")
    except ImportError:
        print(f"✗ {'protobuf':20} NOT INSTALLED")
        print("  REQUIRED for HuggingFace tokenizers!")
        packages_ok = False

packages_ok &= check_package("torch")

print(f"\n{'Python version':20} {sys.version.split()[0]}")
conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda env')
print(f"{'Conda environment':20} {conda_env}")

# Check PyTorch version
import torch
torch_version = torch.__version__.split('+')[0]  # Remove +cu118 suffix if present
torch_major, torch_minor = map(int, torch_version.split('.')[:2])

print(f"{'PyTorch version':20} {torch.__version__}")

# CRITICAL: Check if PyTorch is >= 2.6
if torch_major < 2 or (torch_major == 2 and torch_minor < 6):
    print("\n" + "=" * 70)
    print("⚠️  CRITICAL: PyTorch version too old!")
    print("=" * 70)
    print(f"Your PyTorch version: {torch.__version__}")
    print(f"Required: 2.6.0 or higher")
    print("\nThis is required due to security vulnerability CVE-2025-32434")
    print("\nTo upgrade PyTorch, run:")
    print("  pip install --upgrade torch>=2.6.0 torchvision torchaudio")
    print("\nOr with conda:")
    print("  conda install pytorch torchvision torchaudio -c pytorch")
    print("=" * 70)
    sys.exit(1)

# Check for MPS/CUDA
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
        print("Run: pip install transformers accelerate protobuf")
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
        processor = None  # Whisper doesn't use processor
        
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
        processor = None  # Pipeline handles processing
    
    elif MODEL_TYPE == 'whisper_hf':
        # Load HuggingFace Whisper model
        from transformers import (
            AutoModelForSpeechSeq2Seq, 
            AutoProcessor,
            pipeline
        )
        
        model_name = model_config['model_name']
        print(f"Loading HuggingFace model: {model_name}")
        print("(First run will download the model)")
        
        # Determine torch dtype based on device
        if device == "cuda":
            torch_dtype = torch.float16
            device_map = "auto"
        else:
            torch_dtype = torch.float32
            device_map = None
        
        # Load model with proper configuration
        print("  Loading model...")
        model_hf = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,  # Use safetensors format (safer)
            device_map=device_map
        )
        
        # Load processor with fallback
        print("  Loading processor...")
        processor = None
        try:
            processor = AutoProcessor.from_pretrained(model_name)
            print("  ✓ Using model's own processor")
        except Exception as e:
            print(f"  ⚠️  Model's processor failed: {str(e)[:100]}...")
            
            # Try fallback processor if specified
            if 'fallback_processor' in model_config:
                fallback_name = model_config['fallback_processor']
                print(f"  → Trying fallback processor: {fallback_name}")
                try:
                    processor = AutoProcessor.from_pretrained(fallback_name)
                    print(f"  ✓ Using fallback processor from {fallback_name}")
                except Exception as e2:
                    print(f"  ✗ Fallback processor also failed: {str(e2)[:100]}...")
                    raise RuntimeError(
                        f"Could not load processor for {model_name}. "
                        f"The model may have incomplete tokenizer configuration. "
                        f"Original error: {e}"
                    )
            else:
                raise
        
        # Create pipeline with chunk_length_s for long audio
        print("  Creating pipeline...")
        model = pipeline(
            "automatic-speech-recognition",
            model=model_hf,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device if device != "mps" else "cpu",  # MPS not fully supported in pipeline
            chunk_length_s=30,  # Process audio in 30-second chunks
            stride_length_s=5,  # 5-second overlap between chunks
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

# Get audio duration for info
try:
    import subprocess
    import json
    ffprobe_cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', str(audio_path)
    ]
    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        info = json.loads(result.stdout)
        duration = float(info['format']['duration'])
        print(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
except:
    pass  # ffprobe not available, skip duration info

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
            # For fine-tuned models, still set task to transcribe
            generate_kwargs["task"] = "transcribe"
        
        # CRITICAL FIX: Always enable timestamps for long audio (>30 seconds)
        # This allows the model to handle long-form transcription properly
        print("  Using long-form transcription (with timestamps)...")
        
        result = model(
            str(audio_path),
            generate_kwargs=generate_kwargs,
            return_timestamps=True  # CRITICAL: Enable for long audio
        )
        
        # Extract text from result
        # When timestamps are enabled, result structure is different
        if isinstance(result, dict) and "text" in result:
            transcript_text = result["text"]
        elif isinstance(result, dict) and "chunks" in result:
            # Combine all chunks
            transcript_text = " ".join([chunk["text"] for chunk in result["chunks"]])
        else:
            transcript_text = str(result)
    
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
        f.write(f"Device: {device}\n")
        f.write(f"\n{transcript_text}\n")
    
    print(f"\n✓ Transcription saved to: {output_file}")
    print(f"⏱  Transcription time: {transcribe_time:.1f} seconds ({transcribe_time/60:.1f} minutes)")
    
except Exception as e:
    print(f"\n✗ Error during transcription: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Transcription completed successfully!")

