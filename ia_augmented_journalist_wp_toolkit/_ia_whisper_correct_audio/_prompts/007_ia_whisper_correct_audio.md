
## INPUT
Let's go for local and free: Coqui XTTS v2 instead of Piper.
1. Give commands to uninstall piper and remove models
2. Give commands to install Coqui XTTS v2

## OUTPUT
1) Uninstall Piper (package + clean models)

In your `whisper_train` env:

```bash
conda activate whisper_train

# Uninstall Python packages (both names, if present)
pip uninstall -y piper-tts piper
```

Optionally confirm nothing remains:

```bash
pip show piper-tts
pip show piper
```

Remove the Piper models directory from your project (just deletes files, does not touch conda):

```bash
cd "/Users/brunoflaven/Documents/01_work/blog_articles/_ia_whisper_correct_audio"

rm -rf piper
```

You now have a clean project (no Piper binary, no models).

2) Install Coqui TTS with XTTS v2

Still in `whisper_train`:

```bash
conda activate whisper_train

# Install Coqui TTS (includes XTTS v2 support)
pip install TTS
```

Check it’s installed:

```bash
python -c "from TTS.api import TTS; print(TTS)"
```

This gives you the `TTS` API, which you’ll use like:

```python
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")  # downloads model on first run[web:113][web:115]
tts.tts_to_file(
    text="Bonjour, ceci est un test XTTS v2.",
    file_path="output/test_xtts_fr.wav",
    language="fr",
    speaker="female",  # or default; you can refine later
)
```

Once this works, we can write a new STEP_3 script that:

- Loads your Whisper‑like JSON,
- Calls `tts.tts_to_file` per segment (FR, female voice),
- Concatenates all WAVs with ffmpeg into one WAV/MP3.




