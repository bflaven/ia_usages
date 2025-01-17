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
python 002_ia_video_editing_spacy_entitities.py


"""

import json
import spacy
from typing import List, Dict, Tuple
from collections import Counter

class SubtitleAnalyzer:
    def __init__(self, model_name: str = "en_core_web_lg"):
        """
        Initialize the subtitle analyzer with a spaCy model.
        
        Args:
            model_name (str): SpaCy language model to use. 
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
    
    def combine_subtitles(self, subtitles: List[Dict]) -> str:
        """Combine subtitle texts into a single coherent transcript."""
        return ' '.join(entry['text'] for entry in subtitles)
    
    def segment_text(self, text: str, max_segments: int = 5) -> List[str]:
        """
        Segment text into coherent sections using SpaCy's sentence segmentation.
        
        Args:
            text (str): Input text to segment
            max_segments (int): Maximum number of segments to create
        
        Returns:
            List[str]: Text segments
        """
        # Use SpaCy's sentence segmentation instead of NLTK
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Simple segmentation strategy: divide into roughly equal segments
        segment_size = max(1, len(sentences) // max_segments)
        
        segments = [
            ' '.join(sentences[i:i+segment_size]) 
            for i in range(0, len(sentences), segment_size)
        ]
        
        return segments[:max_segments]
    
    def analyze_subtitles(self, file_path: str) -> Dict:
        """
        Comprehensive analysis of subtitle file using only SpaCy.
        
        Args:
            file_path (str): Path to the subtitle JSON file
        
        Returns:
            Dict: Comprehensive analysis results
        """
        # Load subtitles
        subtitles = self.load_subtitles(file_path)
        
        # Combine subtitle texts
        full_text = self.combine_subtitles(subtitles)
        
        # Process the full text
        doc = self.nlp(full_text)
        
        # Extract entities
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
        
        return {
            'total_subtitles': len(subtitles),
            'total_duration_ms': sum(sub['duration_ms'] for sub in subtitles),
            'entities': entities,
            'key_phrases': significant_phrases,
            'text_segments': self.segment_text(full_text)
        }

# Example usage
def main():
    
    # input_file = "source/germany_scholz_EN_20241122_081318_081504_CS_8000.json"
    input_file = "source/putin_issues_EN_20241122_013120_013320_CS_8000.json"
    

    analyzer = SubtitleAnalyzer()
    analysis_results = analyzer.analyze_subtitles(input_file)
    
    print("🔍 Subtitle Analysis Results:")
    print("\n📊 Basic Statistics:")
    print(f"Total Subtitles: {analysis_results['total_subtitles']}")
    print(f"Total Duration: {analysis_results['total_duration_ms']/1000:.2f} seconds")
    
    print("\n👥 Detected Entities:")
    for category, entities in analysis_results['entities'].items():
        print(f"{category.capitalize()}: {entities}")
    
    print("\n🏷️ Key Phrases:")
    print(analysis_results['key_phrases'])
    
    print("\n📝 Text Segments:")
    for i, segment in enumerate(analysis_results['text_segments'], 1):
        print(f"Segment {i}: {segment}")

if __name__ == "__main__":
    main()






    
