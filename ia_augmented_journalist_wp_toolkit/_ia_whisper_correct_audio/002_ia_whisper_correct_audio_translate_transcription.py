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
python 002_ia_whisper_correct_audio_translate_transcription.py

ollama pull mistral:latest
ollama serve

"""

"""
002_ia_whisper_correct_audio_translate_transcription.py

STEP_2:
- Load Whisper JSON transcript (EN or FR)
- Rewrite each segment with Ollama (mistral:latest) in the SAME language
- Preserve timecodes exactly (start/end unchanged)
- Regenerate JSON, SRT, TXT

Designed to be chained after STEP_1 and before TTS (STEP_3).
"""

# =========================
# CONFIGURATION (EASY TO UPDATE)
# =========================

# Choose which language transcript to rewrite
# Options: "en" or "fr"
SOURCE_LANGUAGE = "fr"

# Input transcript basenames (from STEP_1)
INPUT_BASE_EN = "output/001_ia_mistral_ocr_transcript_en"
INPUT_BASE_FR = "output/001_ia_mistral_ocr_transcript_fr"

# Output suffix to distinguish rewritten files
OUTPUT_SUFFIX = "_rewritten"

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral:latest"

# Prompt templates per language
PROMPT_TEMPLATE_FR = (
    "Tu es un expert de la langue française.\n"
    "Réécris ce texte de transcription orale en français plus clair, fluide et naturel, "
    "en conservant le sens et le ton, sans ajouter d'informations.\n"
    "Garde une longueur similaire (pas de paragraphe très long) et ne réponds que par le texte réécrit.\n\n"
    "Texte à réécrire:\n\"\"\"\n{segment_text}\n\"\"\""
)

PROMPT_TEMPLATE_EN = (
    "You are an expert in English writing.\n"
    "Rewrite this spoken English transcript to be clearer, more fluent and natural, "
    "preserving meaning and tone, without adding new information.\n"
    "Keep a similar length (no very long paragraph) and respond only with the rewritten text.\n\n"
    "Text to rewrite:\n\"\"\"\n{segment_text}\n\"\"\""
)

# Max characters per segment sent to the model (safety)
MAX_SEGMENT_CHARS = 800

# =========================
# IMPORTS
# =========================

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

import requests  # for Ollama HTTP API[web:21]


# =========================
# UTILITIES
# =========================

def log(msg: str) -> None:
    print(msg)
    sys.stdout.flush()


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"JSON transcript not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], path: Path) -> None:
    log(f"Saving JSON: {path}")
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def format_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    secs = ms // 1000
    ms %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def save_srt(data: Dict[str, Any], path: Path) -> None:
    log(f"Saving SRT: {path}")
    segments: List[Dict[str, Any]] = data.get("segments", [])
    lines: List[str] = []

    for idx, seg in enumerate(segments, start=1):
        start_ts = format_timestamp(float(seg["start"]))
        end_ts = format_timestamp(float(seg["end"]))
        text = seg.get("text", "").strip()
        if not text:
            continue

        lines.append(str(idx))
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(text)
        lines.append("")

    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def save_txt(data: Dict[str, Any], path: Path) -> None:
    log(f"Saving TXT: {path}")
    full_text = data.get("text", "").strip()
    with path.open("w", encoding="utf-8") as f:
        f.write(full_text + "\n")


# =========================
# OLLAMA CLIENT
# =========================

def build_prompt(segment_text: str, language: str) -> str:
    segment_text = segment_text.strip()
    if len(segment_text) > MAX_SEGMENT_CHARS:
        segment_text = segment_text[:MAX_SEGMENT_CHARS] + "..."
    if language == "fr":
        return PROMPT_TEMPLATE_FR.format(segment_text=segment_text)
    else:
        return PROMPT_TEMPLATE_EN.format(segment_text=segment_text)


def call_ollama(prompt: str) -> str:
    """
    Call Ollama /api/generate with mistral:latest and return the generated text.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    # Standard Ollama /api/generate returns { "model": ..., "created_at": ..., "response": "...", ... }[web:20][web:21]
    rewritten = data.get("response", "").strip()
    return rewritten


# =========================
# CORE LOGIC
# =========================

def rewrite_segments(data: Dict[str, Any], language: str) -> Dict[str, Any]:
    """
    Iterate over segments, rewrite each segment['text'] via Ollama,
    keep start/end intact, and regenerate data['text'].
    """
    segments: List[Dict[str, Any]] = data.get("segments", [])
    rewritten_texts: List[str] = []

    log(f"Total segments to rewrite: {len(segments)}")

    for i, seg in enumerate(segments):
        original_text = seg.get("text", "").strip()

        if not original_text:
            rewritten = ""
            log(f"Segment {i} is empty, skipping rewrite.")
        else:
            log(f"Rewriting segment {i}/{len(segments)-1}...")
            prompt = build_prompt(original_text, language=language)
            rewritten = call_ollama(prompt)
            log(f"Segment {i} rewritten.")

        seg["text"] = rewritten
        rewritten_texts.append(rewritten)

    # Rebuild global "text" field as a simple join of segment texts
    data["text"] = " ".join(t for t in rewritten_texts if t.strip())
    return data


def get_io_paths() -> Dict[str, Path]:
    """
    Resolve input/output paths based on SOURCE_LANGUAGE and basenames.
    """
    if SOURCE_LANGUAGE == "fr":
        base_in = Path(INPUT_BASE_FR)
    elif SOURCE_LANGUAGE == "en":
        base_in = Path(INPUT_BASE_EN)
    else:
        raise ValueError(f"Unsupported SOURCE_LANGUAGE: {SOURCE_LANGUAGE}")

    base_out = Path(str(base_in) + OUTPUT_SUFFIX)

    return {
        "json_in": base_in.with_suffix(".json"),
        "srt_in": base_in.with_suffix(".srt"),   # not strictly needed but kept for reference
        "txt_in": base_in.with_suffix(".txt"),   # not strictly needed but kept for reference
        "json_out": base_out.with_suffix(".json"),
        "srt_out": base_out.with_suffix(".srt"),
        "txt_out": base_out.with_suffix(".txt"),
    }


# =========================
# MAIN
# =========================

def main() -> None:
    log("=== STEP_2: AI REWRITE WITH OLLAMA (MISTRAL) ===")
    log(f"Source language: {SOURCE_LANGUAGE}")
    log(f"Ollama model: {OLLAMA_MODEL}")
    paths = get_io_paths()

    log("Input / Output paths:")
    for k, v in paths.items():
        log(f"  {k}: {v}")
    log("==============================================")

    # 1. Load JSON from STEP_1
    data = load_json(paths["json_in"])

    # 2–4. Rewrite segments then rebuild full text
    data = rewrite_segments(data, language=SOURCE_LANGUAGE)

    # 5. Save updated JSON, SRT, TXT (same timecodes preserved)
    save_json(data, paths["json_out"])
    save_srt(data, paths["srt_out"])
    save_txt(data, paths["txt_out"])

    log("\n✅ STEP_2 COMPLETE (rewritten transcript with preserved timecodes)")
    log("Generated files:")
    log(f"  JSON: {paths['json_out']}")
    log(f"  SRT : {paths['srt_out']}")
    log(f"  TXT : {paths['txt_out']}")
    log("\nReady for STEP_3 (TTS using these segments and timecodes).")


if __name__ == "__main__":
    main()





