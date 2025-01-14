
# 008_ia_video_editing.md

## PROMPT_1
As Python and Streamlit expert, I got multiple errors,in all tabs, because all the buttons have no different id. Can you fix this e.g "An error occurred while processing the files: There are multiple identical `st.button` widgets with the same generated key."


```python
import streamlit as st
import json
import spacy
from typing import List, Dict, Tuple
from collections import Counter, defaultdict
import base64

class SubtitleAnalyzer:
    def __init__(self, model_name: str = "en_core_web_lg"):
        """
        Initialize the subtitle analyzer with a spaCy model.
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            st.warning(f"Model {model_name} not found. Falling back to en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Pre-compile frequently used attributes for performance
        self.INTERESTING_POS = {'PROPN', 'NOUN', 'ORG', 'PERSON'}
    
    def load_subtitles(self, file_path: str) -> List[Dict]:
        """Load subtitles from a JSON file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle different possible JSON structures
            if isinstance(data, list):
                # If it's already a list of subtitles
                return self._validate_subtitles(data)
            elif isinstance(data, dict):
                # Try to find the subtitles in common keys
                keys_to_check = ['subtitles', 'transcript', 'segments', 'data']
                for key in keys_to_check:
                    if key in data and isinstance(data[key], list):
                        return self._validate_subtitles(data[key])
                
                # If no list found, try to convert the entire dict to a list
                return self._validate_subtitles([data])
            
            raise ValueError("Unable to parse subtitle data")
        
        except json.JSONDecodeError:
            st.error(f"Error decoding JSON file: {file_path}")
            return []
        except Exception as e:
            st.error(f"Unexpected error reading subtitles: {e}")
            return []
    
    def _validate_subtitles(self, subtitles: List[Dict]) -> List[Dict]:
        """
        Validate and standardize subtitle entries.
        Ensures each entry has necessary keys with default values.
        """
        validated_subtitles = []
        for i, subtitle in enumerate(subtitles, 1):
            # Create a standardized subtitle entry
            validated_entry = {
                'text': subtitle.get('text', f'Subtitle {i}'),
                'start_time': subtitle.get('start_time', '00:00:00'),
                'end_time': subtitle.get('end_time', '00:00:00'),
                'start_time_ms': subtitle.get('start_time_ms', i * 1000),
                'end_time_ms': subtitle.get('end_time_ms', (i+1) * 1000),
                'duration_ms': subtitle.get('duration_ms', 1000)
            }
            validated_subtitles.append(validated_entry)
        
        return validated_subtitles
    
    def _find_element_timecodes(self, subtitles: List[Dict], element: str) -> Dict[str, List[Dict]]:
        """
        Find timecodes for specific elements in the subtitles.
        """
        element_timecodes = defaultdict(list)
        
        for subtitle in subtitles:
            text = subtitle['text']
            
            # Process the subtitle text
            doc = self.nlp(text)
            
            # Check entities
            for ent in doc.ents:
                if ent.text.lower() in element.lower():
                    element_timecodes[ent.text].append({
                        'start_time': subtitle['start_time'],
                        'end_time': subtitle['end_time'],
                        'start_time_ms': subtitle['start_time_ms'],
                        'end_time_ms': subtitle['end_time_ms']
                    })
            
            # Check key phrases
            for chunk in doc.noun_chunks:
                if chunk.text.lower() in element.lower():
                    element_timecodes[chunk.text].append({
                        'start_time': subtitle['start_time'],
                        'end_time': subtitle['end_time'],
                        'start_time_ms': subtitle['start_time_ms'],
                        'end_time_ms': subtitle['end_time_ms']
                    })
        
        return dict(element_timecodes)
    
    def combine_subtitles(self, subtitles: List[Dict]) -> str:
        """Combine subtitle texts into a single coherent transcript."""
        return ' '.join(entry['text'] for entry in subtitles)
    
    def segment_text(self, subtitles: List[Dict], max_segments: int = 5) -> List[Dict]:
        """
        Segment text into coherent sections with timecodes.
        """
        full_text = self.combine_subtitles(subtitles)
        doc = self.nlp(full_text)
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Simple segmentation strategy
        segment_size = max(1, len(sentences) // max_segments)
        
        segmented_results = []
        current_segment_start = 0
        
        for i in range(0, len(sentences), segment_size):
            segment_text = ' '.join(sentences[i:i+segment_size])
            
            # Find timecodes for this segment
            segment_subtitles = [
                sub for sub in subtitles 
                if segment_text in sub['text']
            ]
            
            if segment_subtitles:
                segmented_results.append({
                    'text': segment_text,
                    'start_time': segment_subtitles[0]['start_time'],
                    'end_time': segment_subtitles[-1]['end_time'],
                    'start_time_ms': segment_subtitles[0]['start_time_ms'],
                    'end_time_ms': segment_subtitles[-1]['end_time_ms']
                })
        
        return segmented_results[:max_segments]
    
    def analyze_subtitles(self, file_path: str) -> Dict:
        """
        Comprehensive analysis of subtitle file.
        """
        # Load subtitles
        subtitles = self.load_subtitles(file_path)
        
        # Check if subtitles are empty
        if not subtitles:
            return {
                'subtitles': [],
                'total_subtitles': 0,
                'total_duration_ms': 0,
                'entities': {'detected': {}, 'timecodes': {}},
                'key_phrases': {'detected': [], 'timecodes': {}},
                'text_segments': []
            }
        
        full_text = self.combine_subtitles(subtitles)
        
        # Process the full text
        doc = self.nlp(full_text)
        
        # Extract entities with timecodes
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'miscellaneous': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                entities['persons'].append(ent.text)
            elif ent.label_ in ['ORG', 'GPE']:
                entities['organizations'].append(ent.text)
            elif ent.label_ in ['LOC', 'GPE']:
                entities['locations'].append(ent.text)
            else:
                entities['miscellaneous'].append(ent.text)
        
        # Remove duplicates while preserving order
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))
        
        # Extract key phrases
        key_phrases = [
            chunk.text 
            for chunk in doc.noun_chunks 
            if any(token.pos_ in self.INTERESTING_POS for token in chunk)
        ]
        
        # Count and filter key phrases
        phrase_counts = Counter(key_phrases)
        significant_phrases = [
            phrase for phrase, count in phrase_counts.items() 
            if count > 1 and len(phrase.split()) <= 4
        ]
        significant_phrases = list(dict.fromkeys(significant_phrases))
        
        # Find timecodes for detected elements
        entity_timecodes = {}
        for category, items in entities.items():
            entity_timecodes[category] = {
                item: self._find_element_timecodes(subtitles, item)
                for item in items
            }
        
        key_phrase_timecodes = {
            phrase: self._find_element_timecodes(subtitles, phrase)
            for phrase in significant_phrases
        }
        
        # Segment text
        text_segments = self.segment_text(subtitles)
        
        return {
            'subtitles': subtitles,
            'total_subtitles': len(subtitles),
            'total_duration_ms': sum(sub.get('duration_ms', 0) for sub in subtitles),
            'entities': {
                'detected': entities,
                'timecodes': entity_timecodes
            },
            'key_phrases': {
                'detected': significant_phrases,
                'timecodes': key_phrase_timecodes
            },
            'text_segments': text_segments
        }

def create_video_player_with_subtitles(video_path, subtitles=None):
    """
    Create a custom video player with optional subtitle synchronization
    """
    with open(video_path, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
    
    video_html = f"""
    <video 
        id="video-player" 
        controls 
        width="100%" 
        src="data:video/mp4;base64,{video_base64}"
    >
        Your browser does not support the video tag.
    </video>
    <script>
    // Function to seek video to specific time
    function jumpToTime(seconds) {{
        const video = document.getElementById('video-player');
        if (video) {{
            video.currentTime = seconds;
            video.play();
        }}
    }}

    // Custom event listener to handle jumping
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'jumpToTime') {{
            jumpToTime(event.data.time);
        }}
    }});
    </script>
    """
    return video_html

def main():
    st.set_page_config(page_title="Subtitle Video Analyzer", layout="wide")
    st.title("🎥 Subtitle Video Analyzer")

    # Sidebar for file uploads
    with st.sidebar:
        st.header("Upload Files")
        input_json = st.file_uploader("Upload JSON Transcription", type=['json'])
        input_video = st.file_uploader("Upload Video File", type=['mp4'])

    if input_json and input_video:
        # Save uploaded files
        with open("temp_transcript.json", "wb") as f:
            f.write(input_json.getbuffer())
        with open("temp_video.mp4", "wb") as f:
            f.write(input_video.getbuffer())

        # Initialize analyzer
        analyzer = SubtitleAnalyzer()
        
        try:
            # Analyze subtitles
            analysis_results = analyzer.analyze_subtitles("temp_transcript.json")
            
            # Validate analysis results
            if not analysis_results or not analysis_results['subtitles']:
                st.error("Could not parse the subtitle file. Please check the file format.")
                st.stop()

            # Create video player section
            st.header("📽️ Video Player")
            video_html = create_video_player_with_subtitles("temp_video.mp4")
            st.components.v1.html(video_html, height=500)

            # Tabs for different analysis sections
            tab1, tab2, tab3, tab4 = st.tabs([
                "Entities", 
                "Key Phrases", 
                "Text Segments", 
                "Full Statistics"
            ])

            def create_timecode_link(time_ms):
                """Create a Streamlit button that jumps to specific time"""
                return st.button(f"⏩ Jump to {time_ms/1000:.2f}s", 
                                 on_click=lambda: st.components.v1.html(
                                     f"""
                                     <script>
                                     window.parent.postMessage({{
                                         type: 'jumpToTime', 
                                         time: {time_ms/1000}
                                     }}, '*');
                                     </script>
                                     """, 
                                     height=0
                                 )
                )

            with tab1:
                st.subheader("📍 Detected Entities with Timecodes")
                for category, entities in analysis_results['entities']['detected'].items():
                    st.markdown(f"### {category.capitalize()}")
                    for entity in entities:
                        st.markdown(f"#### {entity}")
                        # Display clickable timecodes
                        if category in analysis_results['entities']['timecodes'] and \
                           entity in analysis_results['entities']['timecodes'][category]:
                            for timecode in analysis_results['entities']['timecodes'][category][entity].values():
                                create_timecode_link(timecode[0]['start_time_ms'])
                                st.markdown(
                                    f"📍 Start: {timecode[0]['start_time']} | "
                                    f"End: {timecode[0]['end_time']}"
                                )

            with tab2:
                st.subheader("🏷️ Key Phrases with Timecodes")
                for phrase in analysis_results['key_phrases']['detected']:
                    st.markdown(f"### {phrase}")
                    if phrase in analysis_results['key_phrases']['timecodes']:
                        for timecode in analysis_results['key_phrases']['timecodes'][phrase].values():
                            create_timecode_link(timecode[0]['start_time_ms'])
                            st.markdown(
                                f"📍 Start: {timecode[0]['start_time']} | "
                                f"End: {timecode[0]['end_time']}"
                            )

            with tab3:
                st.subheader("📝 Text Segments")
                for i, segment in enumerate(analysis_results['text_segments'], 1):
                    st.markdown(f"### Segment {i}")
                    st.markdown(f"**Text:** {segment['text']}")
                    create_timecode_link(segment['start_time_ms'])
                    st.markdown(
                        f"**Start Time:** {segment['start_time']} | "
                        f"**End Time:** {segment['end_time']}"
                    )

            with tab4:
                st.subheader("📊 Full Statistics")
                st.write(f"Total Subtitles: {analysis_results['total_subtitles']}")
                st.write(f"Total Duration: {analysis_results['total_duration_ms']/1000:.2f} seconds")

        except Exception as e:
            st.error(f"An error occurred while processing the files: {e}")
            import traceback
            st.error(traceback.format_exc())

if __name__ == "__main__":
    main()
```
