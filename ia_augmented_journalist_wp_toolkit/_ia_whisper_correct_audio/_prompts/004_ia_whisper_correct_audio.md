
## PROMPT_1

Let's code the script for "Option A – Keep segment alignment manually (recommended)". Create a file named `003_ia_whisper_correct_audio_translate_transcription_manual_google.py`.

FINAL OBJECTIVE: After the speech-to-text operation (STEP_1), the next step will be to have the transcription rewritten in the same language by IA but will preservation of the timecode (STEP_2), then the step will be to create text-to-speech with the same timecodes that will generate a mp3 (STEP_3) and I will replace the IA audio version into an video editing software eg iMovie (STEP_4). I just give you the objective so you can take it into account, I will ask for another but one after the other.


NOTE: Keep in mind that I want to have best practices, cut and paste the script for direct use, use function and DRY principles, make the update easy if I want to add some fields to be parsed and make the script configurable so I can update the parameters easily.


## OUTPUT_1

Below is a complete, copy‑paste‑ready script `003_ia_whisper_correct_audio_translate_transcription_manual_google.py` implementing **Option A (manual segment alignment)**. It generates a template file for manual editing and then rebuilds a **New JSON** + SRT + TXT while preserving timecodes. [community.openai](https://community.openai.com/t/whisper-api-verbose-json-results/93083)

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
003_ia_whisper_correct_audio_translate_transcription_manual_google.py

Goal (STEP_2 - manual variant):
- Export Whisper JSON segments into a human-editable text file
  that you can use with Google Translate / manual rewriting.
- Re-import your edited segments and rebuild a NEW JSON transcript
  while preserving original timecodes (start/end).
- Regenerate SRT and TXT from this NEW JSON.

Workflow:
1) Run with MODE = "export" -> creates a segment template file.
2) Edit that file manually (Google Translate, editorial pass, etc.).
3) Run with MODE = "import" -> apply your edited text to the JSON,
   preserving timecodes, and regenerate SRT/TXT.

Designed to integrate with:
- STEP_1: Whisper transcription (JSON from script 001_*)
- STEP_3: TTS per segment using the NEW JSON.
"""

# =========================
# CONFIGURATION (EASY TO UPDATE)
# =========================

# Language of the transcript you are editing
# Just for naming clarity; not used in logic.
SOURCE_LANGUAGE = "fr"  # "en" or "fr"

# INPUT: original Whisper JSON (from STEP_1)
# Example paths (adjust if needed)
INPUT_JSON_FR = "output/001_ia_mistral_ocr_transcript_fr.json"
INPUT_JSON_EN = "output/001_ia_mistral_ocr_transcript_en.json"

# Which one to use for this run
USE_INPUT_JSON = INPUT_JSON_FR

# OUTPUT: new "manual" JSON + SRT + TXT (after you edit segments)
OUTPUT_JSON = "output/001_ia_mistral_ocr_transcript_fr_manual_new.json"
OUTPUT_SRT = "output/001_ia_mistral_ocr_transcript_fr_manual_new.srt"
OUTPUT_TXT = "output/001_ia_mistral_ocr_transcript_fr_manual_new.txt"

# TEMPLATE FILE for manual editing
SEGMENTS_TEMPLATE = "output/001_ia_mistral_ocr_segments_manual_template.txt"

# MODE:
#   "export" -> create SEGMENTS_TEMPLATE from INPUT_JSON
#   "import" -> read edited SEGMENTS_TEMPLATE and apply to INPUT_JSON, then write OUTPUT_JSON/SRT/TXT
MODE = "export"  # "export" or "import"

# Marker used in the template file
SEGMENT_HEADER_PREFIX = "### SEGMENT "  # followed by segment id
ORIGINAL_PREFIX = "ORIGINAL:"
EDITED_PREFIX = "EDITED:"

# =========================
# IMPORTS
# =========================

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


# =========================
# UTILITIES
# =========================

def log(msg: str) -> None:
    print(msg, flush=True)


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(data: Dict[str, Any], path: Path) -> None:
    log(f"Saving JSON: {path}")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


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

    path.write_text("\n".join(lines), encoding="utf-8")


def save_txt(data: Dict[str, Any], path: Path) -> None:
    log(f"Saving TXT: {path}")
    full_text = data.get("text", "").strip()
    path.write_text(full_text + "\n", encoding="utf-8")


# =========================
# EXPORT: BUILD TEMPLATE FOR MANUAL EDIT
# =========================

def export_segments_template(json_in: Path, template_out: Path) -> None:
    """
    Export segments into a human-editable template file.

    Format:

    ### SEGMENT 0
    ORIGINAL:
    <original text line 1>
    <original text line 2>

    EDITED:
    <your edited text here (can span multiple lines)>

    ### SEGMENT 1
    ORIGINAL:
    ...
    EDITED:
    ...
    """
    log(f"Exporting segments template from: {json_in}")
    data = load_json(json_in)
    segments: List[Dict[str, Any]] = data.get("segments", [])

    lines: List[str] = []
    for seg in segments:
        sid = seg.get("id")
        original_text = seg.get("text", "").strip()

        lines.append(f"{SEGMENT_HEADER_PREFIX}{sid}")
        lines.append(ORIGINAL_PREFIX)
        if original_text:
            lines.append(original_text)
        else:
            lines.append("(empty)")
        lines.append("")  # blank line
        lines.append(EDITED_PREFIX)
        lines.append("(edit this block with your new text)")
        lines.append("")  # blank line between segments

    template_out.parent.mkdir(parents=True, exist_ok=True)
    template_out.write_text("\n".join(lines), encoding="utf-8")
    log(f"Template written: {template_out}")
    log("Now:")
    log("  1) Open this file in your editor.")
    log("  2) For each segment, replace the text under 'EDITED:' with your translated/edited version.")
    log("  3) Keep the '### SEGMENT X', 'ORIGINAL:' and 'EDITED:' markers as they are.")


# =========================
# IMPORT: APPLY EDITED SEGMENTS BACK TO JSON
# =========================

def parse_template_file(template_path: Path) -> Dict[int, str]:
    """
    Parse the edited template file and return mapping: segment_id -> edited_text.
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    content = template_path.read_text(encoding="utf-8").splitlines()
    segments_map: Dict[int, str] = {}

    current_id: int | None = None
    in_original = False
    in_edited = False
    edited_buffer: List[str] = []

    def flush_current():
        nonlocal current_id, edited_buffer
        if current_id is not None:
            text = "\n".join(edited_buffer).strip()
            segments_map[current_id] = text
            edited_buffer = []

    for line in content:
        stripped = line.strip()

        # Start of a new segment
        if stripped.startswith(SEGMENT_HEADER_PREFIX):
            # Flush previous
            flush_current()
            # Parse ID
            sid_str = stripped.replace(SEGMENT_HEADER_PREFIX, "").strip()
            try:
                current_id = int(sid_str)
            except ValueError:
                raise ValueError(f"Invalid segment header line: {line}")
            in_original = False
            in_edited = False
            continue

        # Mode switches
        if stripped == ORIGINAL_PREFIX:
            in_original = True
            in_edited = False
            continue
        if stripped == EDITED_PREFIX:
            in_original = False
            in_edited = True
            continue

        # Accumulate edited text
        if in_edited and current_id is not None:
            # You may leave the default placeholder; we treat it as "no change"
            edited_buffer.append(line)

        # Ignore ORIGINAL text for parsing (it's just context for you)

    # Flush last segment
    flush_current()

    # Clean up placeholders "(edit this block ...)" -> treat as empty / no change
    for sid, txt in list(segments_map.items()):
        if txt.strip().startswith("(edit this block"):
            segments_map[sid] = ""  # means: keep original

    return segments_map


def apply_edited_segments(
    json_in: Path,
    template_path: Path,
    json_out: Path,
    srt_out: Path,
    txt_out: Path,
) -> None:
    log(f"Applying edited segments from: {template_path}")
    data = load_json(json_in)
    segments: List[Dict[str, Any]] = data.get("segments", [])
    edited_map = parse_template_file(template_path)

    updated_texts: List[str] = []

    for seg in segments:
        sid = seg.get("id")
        original_text = seg.get("text", "").strip()
        edited_text = edited_map.get(sid, "")

        # If edited_text is empty, keep original; otherwise, override
        if edited_text and not edited_text.startswith("(edit this block"):
            new_text = edited_text.strip()
        else:
            new_text = original_text

        seg["text"] = new_text
        updated_texts.append(new_text)

    # Rebuild global "text"
    data["text"] = " ".join(t for t in updated_texts if t.strip())

    # Save outputs
    json_out.parent.mkdir(parents=True, exist_ok=True)
    save_json(data, json_out)
    save_srt(data, srt_out)
    save_txt(data, txt_out)

    log("\nManual translation / editing applied successfully.")
    log(f"NEW JSON: {json_out}")
    log(f"NEW SRT : {srt_out}")
    log(f"NEW TXT : {txt_out}")
    log("Timecodes (start/end) were preserved from the original JSON.")


# =========================
# MAIN
# =========================

def main() -> None:
    json_in = Path(USE_INPUT_JSON)
    template_path = Path(SEGMENTS_TEMPLATE)
    json_out = Path(OUTPUT_JSON)
    srt_out = Path(OUTPUT_SRT)
    txt_out = Path(OUTPUT_TXT)

    log(f"Mode: {MODE}")
    log(f"Source language (for info): {SOURCE_LANGUAGE}")
    log(f"Input JSON: {json_in}")

    if MODE.lower() == "export":
        export_segments_template(json_in, template_path)
    elif MODE.lower() == "import":
        apply_edited_segments(json_in, template_path, json_out, srt_out, txt_out)
    else:
        raise ValueError("MODE must be 'export' or 'import'.")


if __name__ == "__main__":
    main()
```

Usage pattern:

1. Set `USE_INPUT_JSON` to the Whisper JSON you want to revise (FR or EN).
2. Set `MODE = "export"` and run:
   ```bash
   python 003_ia_whisper_correct_audio_translate_transcription_manual_google.py
   ```
   This creates `SEGMENTS_TEMPLATE` with `ORIGINAL:` and `EDITED:` blocks per segment.

3. Manually edit `SEGMENTS_TEMPLATE`:
   - For each `### SEGMENT N`, replace the text after `EDITED:` with your Google‑translated + editorial French.
   - Leave markers intact.

4. Set `MODE = "import"` and run again:
   ```bash
   python 003_ia_whisper_correct_audio_translate_transcription_manual_google.py
   ```
   This generates:
   - `OUTPUT_JSON` (New JSON with preserved `start`/`end`),
   - `OUTPUT_SRT`,
   - `OUTPUT_TXT`.

This keeps the pipeline clean for your future STEP_3 TTS script (segment‑based synthesis using the New JSON).