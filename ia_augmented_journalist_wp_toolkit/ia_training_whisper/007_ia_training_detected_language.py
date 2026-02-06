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
python 007_ia_training_detected_language.py


"""
import fasttext
import numpy as np

print(f"NumPy version: {np.__version__}")

# Load the pre-trained model
model = fasttext.load_model('lid.176.bin')

def detect_language(text):
    """
    Detect language from text using fasttext
    
    Args:
        text (str): Text to analyze
        
    Returns:
        tuple: (language_code, probability)
    """
    # Remove newlines and extra spaces
    text = text.replace('\n', ' ').strip()
    
    # Predict language (returns top prediction by default)
    predictions = model.predict(text, k=1)  # k=1 for top prediction
    
    # Extract language code (remove '__label__' prefix)
    detected_language = predictions[0][0].replace('__label__', '')
    
    # Get probability
    language_probability = float(predictions[1][0])
    
    return detected_language, language_probability


# Example usage
if __name__ == "__main__":
    # Test with different languages
    test_texts = {
        "pt": "Olá, como você está? Este é um teste em português brasileiro.",
        "zh": "你好,这是一个简体中文测试。",
        "ha": "Sannu, yaya kake? Wannan gwaji ne a Hausa.",
        "vi": "Xin chào, đây là một bài kiểm tra tiếng Việt.",
        "sw": "Habari, hii ni jaribio la Kiswahili.",
        "km": "សួស្តី នេះគឺជាការធ្វើតេស្តភាសាខ្មែរ។",
        "fr": "Bonjour, ceci est un test en français."
    }
    
    for expected_lang, text in test_texts.items():
        detected_language, language_probability = detect_language(text)
        print(f"Expected: {expected_lang} | Detected: {detected_language} | Probability: {language_probability:.10f}")


        






