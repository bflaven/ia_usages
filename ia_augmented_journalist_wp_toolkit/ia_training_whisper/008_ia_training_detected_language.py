"""
[env]
# Conda Environment
conda create --name whisper_train python=3.10
conda info --envs
source activate whisper_train
conda deactivate


# BURN AFTER READING
source activate whisper_train

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n whisper_train


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
# Install core dependencies
pip install openai-whisper
pip install datasets
pip install transformers
pip install accelerate
pip install evaluate jiwer
pip install torch torchvision torchaudio  # For Mac M1/M2, this gets MPS support

pip install fasttext
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin




# Install PyTorch from conda (better Mac compatibility)
conda install pytorch torchvision torchaudio -c pytorch

# Then install the rest with pip
pip install openai-whisper datasets transformers accelerate evaluate jiwer

# Check Installation
python -c "import whisper; print(whisper.__version__)"
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_training_whisper/

# launch the file
python 008_ia_training_detected_language.py


"""
import fasttext
import numpy as np

print(f"NumPy version: {np.__version__}")

# Load the pre-trained model
model = fasttext.load_model('lid.176.bin')

def detect_language_detailed(text, top_n=5):
    """
    Detect language with detailed analysis
    
    Args:
        text (str): Text to analyze
        top_n (int): Number of top predictions to return
        
    Returns:
        list: List of (language_code, probability) tuples
    """
    # Clean text but preserve content
    text_clean = text.replace('\n', ' ').strip()
    
    # Get top N predictions
    predictions = model.predict(text_clean, k=top_n)
    
    results = []
    for lang, prob in zip(predictions[0], predictions[1]):
        lang_code = lang.replace('__label__', '')
        results.append((lang_code, float(prob)))
    
    return results


def analyze_file(filename):
    """
    Comprehensive file analysis
    """
    try:
        # Read the file with different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        text = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    text = f.read()
                used_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if text is None:
            print("Error: Could not read file with any encoding!")
            return
        
        # File statistics
        print(f"\n{'='*60}")
        print(f"File Analysis: {filename}")
        print(f"{'='*60}")
        print(f"Encoding used: {used_encoding}")
        print(f"Total characters: {len(text)}")
        print(f"Total words: {len(text.split())}")
        print(f"Total lines: {len(text.splitlines())}")
        print(f"{'='*60}\n")
        
        # Show full text if short, otherwise preview
        if len(text) < 500:
            print("FULL TEXT:")
            print(text)
        else:
            print("TEXT PREVIEW (first 500 characters):")
            print(text[:500])
        
        print(f"\n{'='*60}")
        print("LANGUAGE DETECTION RESULTS (Top 5)")
        print(f"{'='*60}")
        
        # Detect languages
        predictions = detect_language_detailed(text, top_n=5)
        
        for i, (lang, prob) in enumerate(predictions, 1):
            print(f"{i}. Language: {lang.upper():5} | Probability: {prob:.10f} | Confidence: {prob*100:6.2f}%")
        
        print(f"{'='*60}\n")
        
        # Warning if top prediction is low confidence
        if predictions[0][1] < 0.5:
            print("⚠️  WARNING: Low confidence detection!")
            print("   Possible reasons:")
            print("   - Text is too short (need more text)")
            print("   - Mixed languages in the document")
            print("   - Lots of proper nouns or technical terms")
            print("   - Text might not be in a well-supported language\n")
        
        return predictions
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# Run analysis
if __name__ == "__main__":
    filename = "MZ71729_good_ha.txt"
    analyze_file(filename)
    








