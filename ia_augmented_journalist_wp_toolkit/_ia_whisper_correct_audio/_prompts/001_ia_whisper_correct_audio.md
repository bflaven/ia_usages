
## PROMPT_1
As a python and whisper expert, can you create a python script named `001_ia_whisper_correct_audio.py`that will:

1. Extract the audio from a video and the make the transcription with whisper from an video file named `001_ia_mistral_ocr.mp4` that is stored locally in `source/`. Put this file in a variable so I can update it easily. See MODEL_SIZE for different sizes of the model, put the model and the LANGUAGE in a variable. Put all configuration at the top of the script so I can update it easily.

```python
LANGUAGE = "fr"  # French, English
MODEL_SIZE = "large"  # Options: tiny, base, small, medium, large
```

2. Output at the beginning of the script to check installation and see if all the packages are properly installed. So that indicates that the env is OK. 
3. I want to have a transcription in json file with the timecode, a srt file and text file with only the text.
3. I am using anaconda to manage the python environment. The name of the env is `whisper_train`

FINAL OBJECTIVE: After the speech-to-text operation (STEP_1), the next step will be to have the transcription rewritten in the same language by IA but will preservation of the timecode (STEP_2), then the step will be to create text-to-speech with the same timecodes that will generate a mp3 (STEP_3) and I will replace the IA audio version into an video editing software eg iMovie (STEP_4). I just give you the objective so you can take it into account, I will ask for another but one after the other.


NOTE: Keep in mind that I want to have best practices, cut and paste the script for direct use, use function and DRY principles, make the update easy if I want to add some fields to be parsed and make the script configurable so I can update the parameters easily.


## PROMPT_2

As a python and whisper expert, before coding, can you briefly expose the best way to execute the STEP_2: have the transcription rewritten in the same language by IA but will preservation of the timecode. I have now the transcriptions both in english and in french in json, srt and text. For the french version it has been transalted by Whisper.


## OUTPUT_2

## Best Approach for STEP_2: AI Rewrite Preserving Timecodes

**Core Strategy:** Load JSON → Rewrite each segment's `text` individually → Save updated JSON/SRT/TXT. Timecodes (`start`/`end`) stay untouched.

### Why This Works Perfectly
```
Whisper JSON structure:
{
  "text": "full transcript",
  "segments": [
    {"id": 0, "start": 0.0, "end": 3.2, "text": "segment 1 text"},
    {"id": 1, "start": 3.2, "end": 6.1, "text": "segment 2 text"},
    ...
  ]
}
```
- Rewrite **only** `segments[i]["text"]` 
- Regenerate `result["text"]` by joining rewritten segments
- Timecodes preserved 100%

### Recommended Pipeline (New Script: `002_ia_whisper_rewrite.py`)
```
1. Load JSON (French or English)
2. For each segment → Send to AI: "Rewrite this spoken French text more clearly: [text]"
3. Replace segment["text"] with AI response
4. Regenerate full "text" field
5. Save new JSON/SRT/TXT with same timecodes
```

### AI Provider Choice (Fastest → Cheapest)
| Provider | Model | Latency | Cost | Python lib |
|----------|-------|---------|------|------------|
| **Mistral** | `mistral-large` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | `mistralai` |
| **OpenAI** | `gpt-4o-mini` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | `openai` |
| **Groq** | `llama3.1-70b` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | `groq` |
| **Local** | `llama3.1` | ⭐⭐ | ⭐⭐⭐⭐⭐ | `ollama` |

**Recommendation: Mistral** (since your video is `mistral_ocr.mp4`) - fast, cheap, excellent French.

### Key Implementation Details
```python
# Load
with open("output/001_ia_mistral_ocr_transcript_fr.json") as f:
    data = json.load(f)

# Rewrite each segment (parallelizable)
for seg in data["segments"]:
    prompt = f"Rewrite this French speech more clearly and naturally (keep short): {seg['text']}"
    rewritten = mistral_client.chat(prompt)  # ~1s/segment
    seg["text"] = rewritten

# Regenerate full text
data["text"] = " ".join(seg["text"] for seg in data["segments"])

# Save new files
save_json(data, "002_rewritten_fr.json")
save_srt(data, "002_rewritten_fr.srt")
```

### Batch Processing & Cost
- **100 segments** × 1s = ~2min total
- Mistral cost: ~$0.001 (negligible)
- **Parallel**: Use `asyncio` + `aiohttp` for 10x speed

### Extensibility for STEP_3 (TTS)
New JSON → TTS service (ElevenLabs/PlayHT) with per-segment timing → MP3 with timecodes.

**Ready to code STEP_2?** Pick your AI provider (Mistral recommended) and I'll write the complete script matching your STEP_1 style (config at top, functions, DRY).








