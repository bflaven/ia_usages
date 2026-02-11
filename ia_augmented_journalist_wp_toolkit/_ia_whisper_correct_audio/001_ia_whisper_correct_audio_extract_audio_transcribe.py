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

pip install moviepy


# Check Installation
python -c "import whisper; print(whisper.__version__)"
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_whisper_correct_audio

# launch the file
python 001_ia_whisper_correct_audio_extract_audio_transcribe.py

"""


"""
001_ia_whisper_correct_audio_extract_audio_transcribe.py

STEP_1: Extract audio from video -> Whisper transcription -> JSON/SRT/TXT output
Designed for easy extension to STEP_2 (AI rewrite preserving timecodes)
"""

# =========================
# CONFIGURATION (EASY TO UPDATE)
# =========================
CONDA_ENV_NAME = "whisper_train"
SOURCE_DIR = "source"
INPUT_VIDEO_FILENAME = "001_ia_mistral_ocr.mp4"  # Change here
OUTPUT_DIR = "output"
AUDIO_FILENAME = "001_ia_mistral_ocr_audio.wav"

# LANGUAGE = "fr"  # French
LANGUAGE = "en"  # English
MODEL_SIZE = "large"  # tiny, base, small, medium, large
TRANSCRIPT_BASENAME = "001_ia_mistral_ocr_transcript"

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# =========================
# IMPORTS
# =========================
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List
import whisper

# =========================
# UTILITIES
# =========================
def log(msg: str) -> None:
    """Simple logging with flush for progress tracking."""
    print(msg)
    sys.stdout.flush()

def ensure_directory(path: str | Path) -> None:
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_paths() -> Dict[str, Path]:
    """Build all paths from config."""
    source_dir = Path(SOURCE_DIR)
    output_dir = Path(OUTPUT_DIR)
    
    return {
        "source_dir": source_dir,
        "output_dir": output_dir,
        "input_video": source_dir / INPUT_VIDEO_FILENAME,
        "audio_file": output_dir / AUDIO_FILENAME,
        "transcript_json": output_dir / f"{TRANSCRIPT_BASENAME}.json",
        "transcript_srt": output_dir / f"{TRANSCRIPT_BASENAME}.srt",
        "transcript_txt": output_dir / f"{TRANSCRIPT_BASENAME}.txt",
    }

# =========================
# ENVIRONMENT CHECK
# =========================
def check_environment() -> None:
    """Verify key dependencies are installed."""
    log("=== ENVIRONMENT CHECK ===")
    log(f"Python version: {sys.version.split()[0]}")
    log(f"Expected conda env: {CONDA_ENV_NAME}")
    
    # Check whisper
    try:
        import whisper  # noqa: F401
        log(" - whisper: OK")
    except ImportError:
        log(" - whisper: MISSING (pip install -U openai-whisper)")
    
    # Check ffmpeg
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    log(" - ffmpeg: OK" if result.returncode == 0 else " - ffmpeg: MISSING (brew install ffmpeg)")
    
    log("=========================\n")

# =========================
# AUDIO EXTRACTION (FFMPEG)
# =========================
def extract_audio_from_video(video_path: Path, audio_path: Path) -> None:
    """Extract audio from video using FFmpeg (no MoviePy dependency)."""
    log(f"Extracting audio: {video_path}")
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn",  # no video
        "-acodec", "pcm_s16le",
        "-ar", str(AUDIO_SAMPLE_RATE),
        "-ac", str(AUDIO_CHANNELS),
        "-y",  # overwrite
        str(audio_path),
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{result.stderr}")
    
    log(f"Audio saved: {audio_path}")

# =========================
# WHISPER TRANSCRIPTION
# =========================
def load_whisper_model(model_size: str) -> Any:
    """Load specified Whisper model."""
    log(f"Loading Whisper {model_size}...")
    model = whisper.load_model(model_size)
    log("Model loaded successfully.")
    return model

def transcribe_audio(model: Any, audio_path: Path, language: str) -> Dict[str, Any]:
    """Transcribe audio with timestamps."""
    log(f"Transcribing: {audio_path}")
    result = model.transcribe(
        str(audio_path),
        language=language,
        verbose=False,
    )
    log("Transcription complete.")
    return result

# =========================
# OUTPUT FORMATS
# =========================
def save_json(result: Dict[str, Any], json_path: Path) -> None:
    """Save full transcription (with segments/timecodes) as JSON."""
    log(f"Saving JSON: {json_path}")
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    ms = int(round(seconds * 1000))
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    secs = ms // 1000
    ms %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

def save_srt(result: Dict[str, Any], srt_path: Path) -> None:
    """Generate SRT file from Whisper segments."""
    log(f"Saving SRT: {srt_path}")
    segments: List[Dict[str, Any]] = result.get("segments", [])
    
    lines = []
    for idx, seg in enumerate(segments, 1):
        start_ts = format_timestamp(seg["start"])
        end_ts = format_timestamp(seg["end"])
        text = seg.get("text", "").strip()
        
        if not text:
            continue
            
        lines.extend([str(idx), f"{start_ts} --> {end_ts}", text, ""])
    
    with srt_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def save_txt(result: Dict[str, Any], txt_path: Path) -> None:
    """Save plain text only."""
    log(f"Saving TXT: {txt_path}")
    text = result.get("text", "").strip()
    with txt_path.open("w", encoding="utf-8") as f:
        f.write(text + "\n")

# =========================
# MAIN PIPELINE
# =========================
def main() -> None:
    check_environment()
    
    paths = get_paths()
    ensure_directory(paths["source_dir"])
    ensure_directory(paths["output_dir"])
    
    log("=== PATHS ===")
    for name, path in paths.items():
        log(f"{name}: {path}")
    log("==============\n")
    
    # STEP 1: Extract audio
    extract_audio_from_video(paths["input_video"], paths["audio_file"])
    
    # STEP 2: Transcribe
    model = load_whisper_model(MODEL_SIZE)
    result = transcribe_audio(model, paths["audio_file"], LANGUAGE)
    
    # STEP 3: Save outputs
    save_json(result, paths["transcript_json"])
    save_srt(result, paths["transcript_srt"])
    save_txt(result, paths["transcript_txt"])
    
    log("\n✅ STEP_1 COMPLETE!")
    log("Outputs created:")
    log(f"  📄 JSON: {paths['transcript_json']}")
    log(f"  🎬 SRT:  {paths['transcript_srt']}")
    log(f"  📝 TXT:  {paths['transcript_txt']}")
    log("\nReady for STEP_2 (AI rewrite with preserved timecodes)")

if __name__ == "__main__":
    main()



