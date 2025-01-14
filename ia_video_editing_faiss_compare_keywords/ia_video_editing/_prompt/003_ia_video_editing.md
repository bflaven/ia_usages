
# 003_ia_video_editing.md

## PROMPT_1
As a Python expert, can you write the different sequences and then based on the sequencing, write scripts with python for each sequence that has been defined. 

The objective is to achieve video editing mixing facial recognition techniques and video editing. Let's I have a video with a main subject is "War in Ukraine", I have a provided a directory named "known_personalities" where I stock picture, in jpg format, of the faces I want to identify on the video e.g "Volodymyr Zelensky" is a picture named "face_volodymyr_zelensky.jpg", "Vladimir Putin" is a picture named "face_vladimir_putin.jpg", but it can be also faces for the journalists e.g "face_journalist_1.jpg", "face_journalist_2.jpg"... My objective first is to provide to the editor the cut points (in and out) where the faces are appearing.

## PERPLEXITY_1

Here are the sequences and corresponding Python scripts to achieve video editing with facial recognition for the "War in Ukraine" scenario:

## Sequence 1: Load Known Faces

1. Load known faces from the "known_personalities" directory
2. Encode the known faces for recognition

```python
import face_recognition
import os

def load_known_faces(directory):
    known_faces = {}
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            name = filename.split("_", 1)[1].split(".")[0]
            image = face_recognition.load_image_file(os.path.join(directory, filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_faces[name] = encoding
    return known_faces

known_faces = load_known_faces("known_personalities")
```

## Sequence 2: Process Video and Detect Faces

1. Load the video
2. Process frames at regular intervals
3. Detect and recognize faces in each processed frame
4. Store timestamps and recognized faces

```python
import cv2

def process_video(video_path, known_faces, interval=1):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    face_appearances = {}
    
    for frame_number in range(0, total_frames, int(fps * interval)):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if not ret:
            break
        
        timestamp = frame_number / fps
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
            name = "Unknown"
            if True in matches:
                matched_index = matches.index(True)
                name = list(known_faces.keys())[matched_index]
            
            if name not in face_appearances:
                face_appearances[name] = []
            face_appearances[name].append(timestamp)
    
    video.release()
    return face_appearances

video_path = "war_in_ukraine.mp4"
face_appearances = process_video(video_path, known_faces)
```

## Sequence 3: Generate Cut Points

1. Analyze face appearances to generate in and out points
2. Merge nearby appearances of the same person
3. Create a list of cut points

```python
def generate_cut_points(face_appearances, min_duration=2, max_gap=5):
    cut_points = []
    
    for name, timestamps in face_appearances.items():
        if name == "Unknown":
            continue
        
        appearances = []
        start = timestamps[0]
        prev = start
        
        for t in timestamps[1:]:
            if t - prev > max_gap:
                if prev - start >= min_duration:
                    appearances.append((start, prev))
                start = t
            prev = t
        
        if prev - start >= min_duration:
            appearances.append((start, prev))
        
        cut_points.extend([(name, start, end) for start, end in appearances])
    
    cut_points.sort(key=lambda x: x[1])
    return cut_points

cut_points = generate_cut_points(face_appearances)
```

## Sequence 4: Output Cut Points for Video Editing

1. Format cut points for easy use by video editors
2. Write cut points to a file

```python
def output_cut_points(cut_points, output_file):
    with open(output_file, 'w') as f:
        for name, start, end in cut_points:
            f.write(f"{name}: {start:.2f} - {end:.2f}\n")

output_cut_points(cut_points, "ukraine_war_cut_points.txt")
```

To use these scripts, you would run them in sequence:

1. Load known faces from the "known_personalities" directory
2. Process the "War in Ukraine" video to detect and recognize faces
3. Generate cut points based on face appearances
4. Output the cut points to a file for use by video editors

This approach provides a structured way to identify key personalities in the video and generate cut points for further editing. The video editor can then use these cut points to focus on segments featuring specific individuals, such as Volodymyr Zelensky or Vladimir Putin, or to ensure balanced coverage of different speakers.

Citations:
[1] https://www.edenai.co/post/how-to-use-video-face-detection-api-with-python-in-5-minutes
[2] https://www.codingal.com/coding-for-kids/blog/build-face-recognition-app-with-python/
[3] https://gture.com/live-facial-recognition-system/
[4] https://www.datacamp.com/tutorial/face-detection-python-opencv
[5] https://realpython.com/face-recognition-with-python/
[6] https://pyimagesearch.com/2018/09/24/opencv-face-recognition/
[7] https://www.tripo3d.ai/blog/collect/title--using-python-and-blender-to-automate-video-creation-gku7hg77ylw
[8] https://www.toolify.ai/ai-news/automate-video-editing-with-moviepy-in-python-1200309


