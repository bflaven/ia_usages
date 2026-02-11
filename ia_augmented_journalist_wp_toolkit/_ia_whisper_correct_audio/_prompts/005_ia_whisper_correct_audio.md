
## PROMPT_1

The previous script sucks, let's try something else. I have translated the .srt from English to French with google. The french version is stored in a file named `_003_ia_mistral_ocr_transcript_en_translate_fr.srt`. This time, you have the time code and the translation, I have checked the translation, it is OK.

Let's code a new that will generetad a transcripition file on a whipser model based on the .srt file, output pit in `_003_ia_mistral_ocr_transcript_en_translate_fr.json`. For the script, create a file named `004_ia_whisper_correct_audio_translate_transcription_manual_google.py`.


FINAL OBJECTIVE: After the speech-to-text operation (STEP_1), the next step will be to have the transcription rewritten in the same language by IA but will preservation of the timecode (STEP_2), then the step will be to create text-to-speech with the same timecodes that will generate a mp3 (STEP_3) and I will replace the IA audio version into an video editing software eg iMovie (STEP_4). I just give you the objective so you can take it into account, I will ask for another but one after the other.


NOTE: Keep in mind that I want to have best practices, cut and paste the script for direct use, use function and DRY principles, make the update easy if I want to add some fields to be parsed and make the script configurable so I can update the parameters easily.


## OUTPUT_1

Here’s a clean, ready-to-use script `004_ia_whisper_correct_audio_translate_transcription_manual_google.py` that parses your **French SRT** and builds a **Whisper-style JSON** transcript at `_003_ia_mistral_ocr_transcript_en_translate_fr.json`. [gist.github](https://gist.github.com/vadimkantorov/8b14c60f79c69c4906571d33a3cae5f1)

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
004_ia_whisper_correct_audio_translate_transcription_manual_google.py

Goal:
- Take a manually translated French SRT file (from Google Translate).
- Parse it and generate a Whisper-style JSON transcript:
    - segments: [{id, start, end, text}, ...]
    - text: full transcript as a single string
- Preserve timecodes from the SRT.
- Output JSON can be used as a "Whisper-like" result for later TTS (STEP_3).

Input:
- _003_ia_mistral_ocr_transcript_en_translate_fr.srt

Output:
- _003_ia_mistral_ocr_transcript_en_translate_fr.json
"""

# =========================
# CONFIGURATION
# =========================

INPUT_SRT = "_003_ia_mistral_ocr_transcript_en_translate_fr.srt"
OUTPUT_JSON = "_003_ia_mistral_ocr_transcript_en_translate_fr.json"

# If your SRT contains multiple lines per subtitle block, set this to:
#   "join_with_space" -> join lines with a space
#   "join_with_newline" -> keep explicit newlines
MULTILINE_JOIN_MODE = "join_with_space"

# =========================
# IMPORTS
# =========================

import json
import re
from pathlib import Path
from typing import List, Dict, Any


# =========================
# UTILITIES
# =========================

def log(msg: str) -> None:
    print(msg, flush=True)


def srt_timestamp_to_seconds(ts: str) -> float:
    """
    Convert SRT timestamp 'HH:MM:SS,mmm' to seconds as float.
    """
    # Example: "00:01:23,456"
    hours, minutes, rest = ts.split(":")
    seconds, millis = rest.split(",")
    h = int(hours)
    m = int(minutes)
    s = int(seconds)
    ms = int(millis)
    return h * 3600 + m * 60 + s + ms / 1000.0


def parse_srt(path: Path) -> List[Dict[str, Any]]:
    """
    Parse a standard SRT file into a list of segments:
    [
      {
        "id": int,
        "start": float (seconds),
        "end": float (seconds),
        "text": str
      },
      ...
    ]
    """
    if not path.exists():
        raise FileNotFoundError(f"SRT file not found: {path}")

    content = path.read_text(encoding="utf-8")

    # Basic SRT block regex:
    #  index
    #  start --> end
    #  text (possibly multiple lines)
    #  blank line
    #
    # This pattern is robust for typical SRT files.[web:45][web:51]
    pattern = re.compile(
        r"""
        (\d+)\s*                          # Subtitle index
        \n
        (\d{2}:\d{2}:\d{2},\d{3})         # start time
        \s-->\s
        (\d{2}:\d{2}:\d{2},\d{3})         # end time
        \n
        (.+?)                             # subtitle text (one or more lines)
        (?=\n{2,}|\Z)                     # until blank line or end of file
        """,
        re.DOTALL | re.VERBOSE,
    )

    segments: List[Dict[str, Any]] = []

    for match in pattern.finditer(content):
        idx_str, start_ts, end_ts, text_block = match.groups()

        start_sec = srt_timestamp_to_seconds(start_ts)
        end_sec = srt_timestamp_to_seconds(end_ts)

        # Handle multiple lines in subtitle text
        lines = [line.strip() for line in text_block.strip().splitlines() if line.strip()]

        if MULTILINE_JOIN_MODE == "join_with_newline":
            text = "\n".join(lines)
        else:
            text = " ".join(lines)

        seg = {
            "id": int(idx_str) - 1,  # 0-based id (Whisper style)[web:50]
            "start": start_sec,
            "end": end_sec,
            "text": text,
        }
        segments.append(seg)

    return segments


def build_whisper_like_json(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a Whisper-like JSON structure from segments:
    {
      "text": "...",
      "segments": [{id, start, end, text}, ...]
      // You can add other fields later if needed
    }[web:50]
    """
    full_text = " ".join(seg["text"] for seg in segments if seg["text"].strip())
    data: Dict[str, Any] = {
        "text": full_text,
        "segments": segments,
    }
    return data


def save_json(data: Dict[str, Any], path: Path) -> None:
    log(f"Saving JSON: {path}")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# =========================
# MAIN
# =========================

def main() -> None:
    srt_path = Path(INPUT_SRT)
    json_path = Path(OUTPUT_JSON)

    log("=== SRT → Whisper-like JSON (FR translation) ===")
    log(f"Input SRT : {srt_path}")
    log(f"Output JSON: {json_path}")
    log(f"Multiline join mode: {MULTILINE_JOIN_MODE}")

    segments = parse_srt(srt_path)
    log(f"Parsed segments: {len(segments)}")

    data = build_whisper_like_json(segments)
    save_json(data, json_path)

    log("\nDone. You now have a Whisper-style JSON built from your French SRT.")
    log("This JSON is ready to be used for STEP_3 (segment-based TTS).")


if __name__ == "__main__":
    main()
```

This script:

- Reads `_003_ia_mistral_ocr_transcript_en_translate_fr.srt`.
- Parses each SRT block: index, time range, text. [stackoverflow](https://stackoverflow.com/questions/67102430/srt-subrip-text-to-json-using-python)
- Converts timestamps to seconds (`start`, `end`).
- Creates `segments` list and `text` field in a **Whisper-like** JSON structure. [github](https://github.com/linto-ai/whisper-timestamped)
- Writes `_003_ia_mistral_ocr_transcript_en_translate_fr.json`.

You can now plug this JSON directly into your future STEP_3 TTS script (loop over `segments`, synthesize per `text`, use `start`/`end` as timing hints).