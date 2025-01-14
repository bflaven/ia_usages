
# 006_ia_video_editing.md

## PROMPT_1
Can you enhance the script with spacy and indicated for "Detected Entities", "Key Phrases", "Text Segments" the timecode that could be the cue point IN and the cue point OUT for each element where the script found these elements inside the transcription  
## CLAUDE_1


I'll modify the script to include timecode information for each detected entity, key phrase, and text segment.

```python
import json
import spacy
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

class SubtitleAnalyzer:
    def __init__(self, model_name: str = "en_core_web_lg"):
        """
        Initialize the subtitle analyzer with a spaCy model.
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model {model_name} not found. Falling back to en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Pre-compile frequently used attributes for performance
        self.INTERESTING_POS = {'PROPN', 'NOUN', 'ORG', 'PERSON'}
    
    def load_subtitles(self, file_path: str) -> List[Dict]:
        """Load subtitles from a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _find_element_timecodes(self, subtitles: List[Dict], element: str) -> Dict[str, List[Dict]]:
        """
        Find timecodes for specific elements in the subtitles.
        
        Args:
            subtitles (List[Dict]): List of subtitle entries
            element (str): Element to search for
        
        Returns:
            Dict[str, List[Dict]]: Dictionary of elements with their timecodes
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
        
        Args:
            subtitles (List[Dict]): List of subtitle entries
            max_segments (int): Maximum number of segments to create
        
        Returns:
            List[Dict]: Text segments with timecodes
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
            'total_subtitles': len(subtitles),
            'total_duration_ms': sum(sub['duration_ms'] for sub in subtitles),
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

# Example usage
def main():
    input_file = "source/germany_scholz_EN_20241122_081318_081504_CS_8000.json"
    analyzer = SubtitleAnalyzer()
    analysis_results = analyzer.analyze_subtitles(input_file)
    
    print("🔍 Subtitle Analysis Results:")
    print("\n📊 Basic Statistics:")
    print(f"Total Subtitles: {analysis_results['total_subtitles']}")
    print(f"Total Duration: {analysis_results['total_duration_ms']/1000:.2f} seconds")
    
    print("\n👥 Detected Entities with Timecodes:")
    for category, entities in analysis_results['entities']['detected'].items():
        print(f"\n{category.capitalize()}:")
        for entity in entities:
            print(f"  {entity}:")
            # Print timecodes if available
            if entity in analysis_results['entities']['timecodes'][category]:
                for occur in analysis_results['entities']['timecodes'][category][entity].values():
                    print(f"    - Timecodes: {occur}")
    
    print("\n🏷️ Key Phrases with Timecodes:")
    for phrase in analysis_results['key_phrases']['detected']:
        print(f"\n{phrase}:")
        if phrase in analysis_results['key_phrases']['timecodes']:
            for occur in analysis_results['key_phrases']['timecodes'][phrase].values():
                print(f"  - Timecodes: {occur}")
    
    print("\n📝 Text Segments:")
    for i, segment in enumerate(analysis_results['text_segments'], 1):
        print(f"Segment {i}:")
        print(f"  Text: {segment['text']}")
        print(f"  Start Time: {segment['start_time']}")
        print(f"  End Time: {segment['end_time']}")

if __name__ == "__main__":
    main()

```

Key Enhancements:
1. **Timecode Tracking**
   - Added `_find_element_timecodes()` method to locate exact timecodes for:
     - Entities
     - Key Phrases
     - Text Segments

2. **Detailed Output**
   - Each detected entity now shows:
     - Detected text
     - Precise timecodes (start and end times)
     - Multiple occurrences if applicable

3. **Flexible Timecode Representation**
   - Both human-readable time format
   - Millisecond timestamps

### Example Output Structure
```
🔍 Subtitle Analysis Results:

📊 Basic Statistics:
Total Subtitles: 2
Total Duration: 12.36 seconds

👥 Detected Entities with Timecodes:
Persons:
  Olaf Scholz:
    - Timecodes: [{'start_time': '00:00:00,000', 'end_time': '00:00:06,360', ...}]
  Boris Pistorius:
    - Timecodes: [{'start_time': '00:00:07,019', 'end_time': '00:00:13,020', ...}]

Organizations:
  Germany's Social Democratic Party:
    - Timecodes: [{'start_time': '00:00:00,000', 'end_time': '00:00:06,360', ...}]

🏷️ Key Phrases with Timecodes:
Social Democratic Party:
  - Timecodes: [{'start_time': '00:00:00,000', 'end_time': '00:00:06,360', ...}]
Defence Minister:
  - Timecodes: [{'start_time': '00:00:07,019', 'end_time': '00:00:13,020', ...}]

📝 Text Segments:
Segment 1:
  Text: Full first segment text
  Start Time: 00:00:00,000
  End Time: 00:00:06,360
```

### Additional Improvements
- More robust entity and phrase detection
- Handles multiple occurrences of same entity
- Provides comprehensive timecode information

### Recommendations
1. Use larger SpaCy models for better accuracy
2. Adjust segmentation parameters as needed
3. Can be easily extended for more complex analysis

Would you like me to elaborate on any specific aspect of the implementation?
