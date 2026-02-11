
## 1. INTRO

This repo is a **POC / experiment** around building an offline(ish) speech pipeline for long‑form video:

1. **STEP_1 – Speech‑to‑text (Whisper)**  
   Extract audio from a local `.mp4`, transcribe with Whisper, produce JSON/SRT/TXT.

2. **STEP_2 – Human‑quality translation / rewrite with preserved timecodes**  
   Use a combination of AI and manual editing (Google Translate + human corrections) to get high‑quality French (and potentially Spanish/Russian/Portuguese) while keeping subtitle timing stable.

3. **STEP_3 – Text‑to‑speech (TTS)**  
   Generate a new synthetic voice track per segment, then concatenate to replace the original audio in a video editor (iMovie, etc.).

4. **STEP_4 – Video edit**  
   Replace the original audio track in the `.mp4` with the synthetic track.

This repo deliberately focuses on **steps 1–2** and documents why STEP_3 is not currently solved locally with the attempted open‑source tools.

***

## HUMAN ANSWER

### What was tried for TTS?

Two local TTS approaches were explored and rejected in this POC:

```text
! NOWAY Piper with voice fr as siwis
! NOWAY Coqui tts xtts v2
```

**Piper (French voice “siwis”)**

- Goal: local, free French female voice using Piper + `fr_FR-siwis-medium.onnx`.
- Attempts:
  - CLI binary (`piper_macos_aarch64`) on Apple Silicon (M4 Max).
  - `piper-tts` Python package + direct `PiperVoice` usage.
- Issues:
  - macOS Gatekeeper + architecture problems on the CLI binary (killed, permission issues). [github](https://github.com/rhasspy/piper/issues/480)
  - Python package produced no usable audio even in minimal tests, despite correct model/config and no import errors.
- Conclusion: **not reliable enough on this specific macOS + conda environment** for a reproducible POC.

**Coqui TTS – XTTS v2**

- Goal: higher‑quality multilingual TTS (French/Spanish/Russian/Portuguese) using `tts_models/multilingual/multi-dataset/xtts_v2`. [coqui-tts.readthedocs](https://coqui-tts.readthedocs.io/en/latest/models/xtts.html)
- Attempts:
  - `pip install TTS`, `from TTS.api import TTS`, `TTS("xtts_v2")`.
- Issues:
  - ImportError: `BeamSearchScorer` missing from `transformers` in this env.
  - Upgrading `transformers` + `TTS` did not resolve the mismatch cleanly in the existing `whisper_train` conda environment.
- Conclusion: **XTTS v2 needs a fresh, dedicated environment or container** to be robust; mixing it into an already busy env is brittle.

### Conclusion of the exploration

This POC shows that:

- **Whisper + JSON/SRT/TXT + manual translation is robust and reproducible.**
- Local, open‑source TTS with:
  - Piper + `siwis` **and**
  - Coqui XTTS v2  
  is currently **fragile on macOS Apple Silicon in an existing conda env**. Getting them to run reliably requires either:
  - A dedicated, minimal environment/Docker image, or
  - Accepting a cloud TTS (e.g. ElevenLabs/PlayHT) instead of purely local.

So this repo deliberately **stops before STEP_3** and documents the dead‑ends, leaving TTS as an open, engine‑pluggable step.

***

## Transcription model and files

### Whisper model (STEP_1)

- Transcription is done with **OpenAI Whisper** (Python library) in a local environment.
- Two languages are used:
  - English (original audio)
  - French (Whisper’s own translation mode)

### Ollama model (for experiments around rewriting)

- Local LLM used for initial rewrite experiments:
  ```bash
  mistral:latest
  ```

This model was accessed through **Ollama** for segment‑by‑segment rewriting, but the final chosen approach for French quality is **manual translation + human editing**, not Mistral.

### Transcription outputs

After STEP_1 you get:

```text
# EN (original)
output/001_ia_mistral_ocr_transcript_en.json
output/001_ia_mistral_ocr_transcript_en.srt
output/001_ia_mistral_ocr_transcript_en.txt

# FR (Whisper-translated)
output/001_ia_mistral_ocr_transcript_fr.json
output/001_ia_mistral_ocr_transcript_fr.srt
output/001_ia_mistral_ocr_transcript_fr.txt
```

- `.json` is a **Whisper‑like structure**: `{"text": "...", "segments": [{id, start, end, text}, ...]}`. [community.openai](https://community.openai.com/t/whisper-api-verbose-json-results/93083)
- `.srt` is a standard subtitle file with timecodes and text.
- `.txt` is the plain concatenated transcript.

***

## Scripts in this POC

### 001_ia_whisper_correct_audio_extract_audio_transcribe.py

**STEP_1 – Extract audio + transcribe with Whisper**

- Configuration at the top:
  - `SOURCE_DIR`, `OUTPUT_DIR`, `INPUT_VIDEO_FILENAME`
  - `LANGUAGE`, `MODEL_SIZE`, audio format parameters.
- Flow:
  1. Extract audio from `source/xxx.mp4` using ffmpeg.
  2. Run Whisper transcription on the WAV.
  3. Save:
     - `output/..._transcript_*.json` (with segments + timecodes),
     - `output/..._transcript_*.srt`,
     - `output/..._transcript_*.txt`.

**Purpose:** Provide a reusable, environment‑checked, function‑based pipeline to go from video → audio → text with all the time info needed for later steps.

***

### 002_ia_whisper_correct_audio_translate_transcription.py

**STEP_2 – AI rewrite with timecodes preserved using Ollama (Mistral)**

- Reads a Whisper JSON (`en` or `fr`).
- For each segment:
  - Builds a language‑specific prompt.
  - Calls local Ollama (`mistral:latest`) via HTTP (`/api/generate`).
  - Replaces `segment["text"]` with the rewritten version, keeping `start`/`end` untouched. [ollama](https://ollama.com/library/mistral)
- Rebuilds the global `"text"` field as `join(segments[i]["text"])`.
- Writes:
  - A new JSON (rewritten),
  - SRT/TXT regenerated from the updated JSON.

**Observation:** For French, the quality from `mistral:latest` was not good enough (“catastrophic”) for this use case, so this approach is included as an **experiment**, not the final solution.

***

### 003_ia_whisper_correct_audio_translate_transcription_manual_google.py

**STEP_2 – Manual alignment with Google Translate (option A, deprecated)**

- Idea: work **segment-by-segment** with a template file:
  - Export a template file listing segments like:
    ```text
    ### SEGMENT 0
    ORIGINAL:
    original text…

    EDITED:
    (edit this block with your new text)
    ```
  - Manually edit the `EDITED:` sections using Google Translate + human corrections.
  - Import the edited segments back into the JSON, replacing `segment[i].text` if provided.

**Reason it “sucks” in this POC:**

- The UX of editing a text template file was found too clunky.
- A better solution was to work directly from an **already translated SRT** instead (see the next script).

***

### 004_ia_whisper_correct_audio_translate_transcription_manual_google.py

**STEP_2 – Rebuild Whisper-like JSON from translated SRT (final manual path)**

- This is the **cleanest manual option** that ended up working well.

**Use‑case:**

1. Start from English SRT.
2. Translate SRT to French via Google Translate (copy/paste).
3. Manually correct French translation in the SRT file.
4. Use this script to **convert the translated SRT back into a Whisper‑like JSON** with `start`/`end` timecodes preserved.

**Script behavior:**

- Input: `_003_ia_mistral_ocr_transcript_en_translate_fr.srt` (human‑validated French SRT).
- Parsing:
  - Reads standard SRT blocks: `index`, `start --> end`, `text` (multi‑line). [gist.github](https://gist.github.com/vadimkantorov/8b14c60f79c69c4906571d33a3cae5f1)
  - Converts timestamps `HH:MM:SS,mmm` → seconds (`float`) for `start` and `end`.
  - Joins multi‑line subtitle text with a configurable mode (`join_with_space` by default).
- Output:
  - `_003_ia_mistral_ocr_transcript_en_translate_fr.json` with:
    ```json
    {
      "text": "full French transcript ...",
      "segments": [
        {"id": 0, "start": ..., "end": ..., "text": "..."},
        ...
      ]
    }
    ```
- This **New JSON** becomes the canonical, human‑validated French transcript with Whisper‑style segments, ready for a future TTS step.

***

## Summary of the POC outcome

- **What works well:**
  - STEP_1: Whisper transcription to JSON/SRT/TXT.
  - STEP_2: High‑quality French via:
    - Whisper FR,
    - Manual Google Translate pass,
    - Rebuild of Whisper‑like JSON from SRT.

- **What does not (in this env):**
  - Piper (French voice `siwis`) – CLI and Python both problematic on Apple Silicon + conda.
  - Coqui XTTS v2 – blocked by `transformers`/`BeamSearchScorer` mismatch in the existing `whisper_train` env.

- **What’s left open:**
  - STEP_3 TTS is intentionally not finalized in this repo.  
    The JSON/SRT outputs are designed so that **any TTS engine** (cloud or local) can be plugged in later:
    - Cloud: ElevenLabs, PlayHT.
    - Local: Coqui XTTS v2 in a fresh, minimal env or container.
    - Others: any engine that can take text per segment and output WAV/MP3.

This POC is therefore a **documentation of the path and the dead ends**, plus a solid base for experimenting with different TTS backends without having to redo STEP_1 and STEP_2.



## 2. FINAL ANSWER (IA-oriented)

XTTS v2 in this environment is blocked by a deep dependency clash (`BeamSearchScorer` symbol mismatch in `transformers` vs `TTS`). Fixing that reliably on top of an existing, busy conda env is possible but will be brittle and time‑consuming. [github](https://github.com/coqui-ai/TTS/discussions/3369)

Given how much you’ve already invested, the honest answer is:

- The **TTS step is no longer a “simple” local Python library drop‑in** on this machine/env.
- You have three realistic options that will work without fighting low‑level dependency hell:

***

## Option 1 – Use a cloud TTS (fastest way to finish)

For getting this **one French voiceover** done, the least painful solution is:

- Use **ElevenLabs** or **PlayHT** just for STEP_3:
  - Create free account.
  - Pick a French female voice.
  - Use a small Python script: JSON segments → HTTP TTS → per‑segment MP3/WAV → ffmpeg concat → final track.

You already have the pipeline logic; only the `synth_segment(...)` implementation changes (HTTP instead of Piper/XTTS). Quality is excellent, and you’re done in under an hour.

***

## Option 2 – Use a clean, separate environment / container just for XTTS

XTTS v2 works well in a **fresh, minimal environment**, for example:

- A new conda env:
  - Python 3.10
  - `pip install "transformers==4.36.0" "torch>=2.1" "TTS==0.22.0"` (or matching versions from Coqui docs) [coqui-tts.readthedocs](https://coqui-tts.readthedocs.io/en/latest/models/xtts.html)
- Or a **Docker image** / dedicated venv only used for TTS, not mixed with Whisper, Ollama, etc.

Then:

- Drop a minimal XTTS script in that env that:
  - Accepts a JSON path and output dir,
  - Synthesizes segments,
  - Concats them.

You call this script from outside like:

```bash
conda run -n xtts_env python xtts_step3.py ...
```

This isolates the transformer/torch mess from your main `whisper_train` env.

***

## Option 3 – Use a simpler offline TTS (Piper, but via Docker or Home Assistant image)

Instead of mixing Piper into conda, you can:

- Run Piper TTS via a **Docker container** that exposes an HTTP or CLI interface. [github](https://github.com/agzam/dockerized-piper)
- Your Python script in `whisper_train` calls that local service (HTTP) or shell command, no native libs inside your env.

This path works, but at that point you’re maintaining a container for a single job.

***

Because your Whisper/JSON pipeline is already solid and the blocking factor is only STEP_3, I’d strongly recommend:

- **Use ElevenLabs (or PlayHT) for this project** to get the French track done.
- If you later want a robust, fully local TTS stack, set up a **dedicated XTTS env** from scratch or a Docker container, without mixing it into `whisper_train`.

If you tell me:

- “Let’s finish with ElevenLabs for French now”

I’ll give you a clean STEP_3 script that:

- Reads your Whisper‑like JSON,
- Calls ElevenLabs TTS per segment,
- Concatenates to WAV/MP3 with ffmpeg,

so you can move on and actually use the voiceover in your video editor.











