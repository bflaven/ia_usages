#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_seo_llm python=3.9.13
conda info --envs
source activate ia_seo_llm
conda deactivate


# BURN AFTER READING
source activate ia_seo_llm

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_seo_llm

# BURN AFTER READING
conda env remove -n ia_seo_llm


# other libraries
python -m pip install spacy 

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_video_editing/



# launch the file
python 003_ia_video_editing_spacy_entitities_cuepoints.py


"""

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
    
    input_file = "source/putin_issues_EN_20241122_013120_013320_CS_8000.json"
    # input_file = "source/germany_scholz_EN_20241122_081318_081504_CS_8000.json"
    
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



    
