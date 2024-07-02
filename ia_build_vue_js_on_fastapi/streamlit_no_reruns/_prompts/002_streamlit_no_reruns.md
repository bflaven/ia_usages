# 002_streamlit_no_reruns.md

## PROMPT_1
As an advanced programmer in Python, using Streamlit, can you write a script that load a .mp4 and .mp3 then show the player, audio player for .mp3, video player for .mp4



## CHATGPT_1

Certainly! Here’s a Streamlit script that loads an `.mp4` video file and an `.mp3` audio file and then displays a video player for the `.mp4` file and an audio player for the `.mp3` file.

First, ensure you have Streamlit installed:
```sh
pip install streamlit
```

Now, you can use the following script:

```python
import streamlit as st

# Title of the app
st.title("Media Player: Video and Audio")

# File uploader for .mp4 and .mp3 files
video_file = st.file_uploader("Upload a .mp4 video file", type=["mp4"])
audio_file = st.file_uploader("Upload a .mp3 audio file", type=["mp3"])

# Display video player if a video file is uploaded
if video_file is not None:
    st.video(video_file)

# Display audio player if an audio file is uploaded
if audio_file is not None:
    st.audio(audio_file)
```

### How to Run the Script
1. Save the script as `app.py`.
2. Open a terminal and navigate to the directory where `app.py` is saved.
3. Run the script with Streamlit:
   ```sh
   streamlit run app.py
   ```
4. This will open a new tab in your web browser with the Streamlit interface, where you can upload and play your video and audio files.

The script uses Streamlit's `file_uploader` to allow users to upload `.mp4` and `.mp3` files and then uses `st.video` and `st.audio` to display the media players for the uploaded files.
