## PROMPT_1

As a python and whisper expert, can you provide simple steps for a newbie to train whisper-small locally on a mac to improve:

1. The quality of the transcription for a specific language e.g Kiswahili
2. The quality of the entities recognition for based on a list of keywords stored in json file including persons, localisations… etc for a specific language e.g Kiswahili
3. I am using anaconda to manage the python environment.

## OUTPUT_1


I'll give you practical steps for both training Whisper and handling entity recognition. Note that Whisper doesn't natively do entity recognition - that requires a separate approach.

## Prerequisites Setup

```bash
# Create conda environment
conda create -n whisper-train python=3.10
conda activate whisper-train

# Install core dependencies
pip install openai-whisper
pip install datasets
pip install transformers
pip install accelerate
pip install evaluate jiwer
pip install torch torchvision torchaudio  # For Mac M1/M2, this gets MPS support
```

## 1. Fine-tuning Whisper for Kiswahili

### Step 1: Prepare Your Dataset

You need paired audio-transcription data. Structure:

```
kiswahili_data/
├── audio/
│   ├── audio_001.wav
│   ├── audio_002.wav
│   └── ...
└── transcripts.json
```

**transcripts.json format:**
```json
[
  {
    "audio_path": "audio/audio_001.wav",
    "text": "Habari za asubuhi kutoka Dar es Salaam"
  },
  {
    "audio_path": "audio/audio_002.wav", 
    "text": "Rais wa Tanzania amesema..."
  }
]
```

### Step 2: Create Training Script

Save as `train_whisper.py`:

```python
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import Dataset, Audio
import json

# Check if Mac has MPS (Apple Silicon)
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# Load model and processor
model_name = "openai/whisper-small"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)
model.to(device)

# Force language to Kiswahili
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
    language="sw", task="transcribe"
)

# Load your data
with open("kiswahili_data/transcripts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Create dataset
dataset = Dataset.from_dict({
    "audio": [item["audio_path"] for item in data],
    "text": [item["text"] for item in data]
})

# Cast audio column
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

# Split dataset
dataset = dataset.train_test_split(test_size=0.1)

def prepare_dataset(batch):
    # Load and resample audio
    audio = batch["audio"]
    
    # Compute input features
    batch["input_features"] = processor(
        audio["array"], 
        sampling_rate=audio["sampling_rate"]
    ).input_features[0]
    
    # Encode target text
    batch["labels"] = processor.tokenizer(batch["text"]).input_ids
    
    return batch

# Prepare datasets
dataset = dataset.map(prepare_dataset, remove_columns=dataset.column_names["train"])

# Training arguments (adjusted for Mac)
training_args = Seq2SeqTrainingArguments(
    output_dir="./whisper-small-kiswahili",
    per_device_train_batch_size=4,  # Reduce if memory issues
    gradient_accumulation_steps=2,
    learning_rate=1e-5,
    warmup_steps=50,
    num_train_epochs=3,
    evaluation_strategy="steps",
    eval_steps=100,
    save_steps=100,
    logging_steps=25,
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,
    push_to_hub=False,
    use_cpu=True if device == "cpu" else False,  # Force CPU if no MPS
    fp16=False,  # Mac doesn't support fp16
)

# Data collator
from dataclasses import dataclass
from typing import Any, Dict, List, Union

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")
        
        label_features = [{"input_ids": feature["labels"]} for feature in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")
        
        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )
        
        batch["labels"] = labels
        return batch

data_collator = DataCollatorSpeechSeq2SeqWithPadding(processor=processor)

# Metric
import evaluate
wer_metric = evaluate.load("wer")

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids
    
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
    
    pred_str = processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)
    
    wer = wer_metric.compute(predictions=pred_str, references=label_str)
    return {"wer": wer}

# Trainer
trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    tokenizer=processor.feature_extractor,
)

# Train
trainer.train()

# Save
model.save_pretrained("./whisper-small-kiswahili-final")
processor.save_pretrained("./whisper-small-kiswahili-final")
```

### Step 3: Run Training

```bash
python train_whisper.py
```

**Mac-specific notes:**
- Training will be **slow** on Mac (even M-series)
- Reduce `per_device_train_batch_size` to 2 or 1 if you get memory errors
- Consider using smaller dataset for initial testing (100-500 samples)

## 2. Entity Recognition with Keywords

Whisper doesn't do NER, so we need post-processing:

### Create Entity Enhancement Script

Save as `enhance_entities.py`:

```python
import json
import re
from typing import List, Dict
import whisper

class EntityEnhancer:
    def __init__(self, entities_file: str):
        """Load entities from JSON file"""
        with open(entities_file, 'r', encoding='utf-8') as f:
            self.entities = json.load(f)
        
        # Build case-insensitive patterns
        self.patterns = {}
        for category, terms in self.entities.items():
            self.patterns[category] = [
                (term, re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE))
                for term in terms
            ]
    
    def enhance_transcription(self, text: str) -> Dict:
        """Find and correct entities in transcription"""
        enhanced_text = text
        found_entities = {category: [] for category in self.entities.keys()}
        
        # Find and correct entities
        for category, patterns in self.patterns.items():
            for correct_term, pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    # Replace with correct capitalization/spelling
                    enhanced_text = enhanced_text[:match.start()] + \
                                  correct_term + \
                                  enhanced_text[match.end():]
                    
                    if correct_term not in found_entities[category]:
                        found_entities[category].append(correct_term)
        
        return {
            "original": text,
            "enhanced": enhanced_text,
            "entities": found_entities
        }

# Example usage
if __name__ == "__main__":
    # Load fine-tuned model
    model = whisper.load_model("whisper-small-kiswahili-final")
    
    # Load entity enhancer
    enhancer = EntityEnhancer("entities_kiswahili.json")
    
    # Transcribe
    result = model.transcribe("test_audio.wav", language="sw")
    
    # Enhance
    enhanced = enhancer.enhance_transcription(result["text"])
    
    print(f"Original: {enhanced['original']}")
    print(f"Enhanced: {enhanced['enhanced']}")
    print(f"Entities: {json.dumps(enhanced['entities'], indent=2, ensure_ascii=False)}")
```

### Entity Dictionary Format

**entities_kiswahili.json:**
```json
{
  "persons": [
    "William Ruto",
    "Samia Suluhu Hassan",
    "Paul Kagame",
    "Uhuru Kenyatta"
  ],
  "locations": [
    "Dar es Salaam",
    "Nairobi",
    "Kampala",
    "Kigali",
    "Dodoma",
    "Mombasa"
  ],
  "organizations": [
    "Umoja wa Afrika",
    "Jumuiya ya Afrika Mashariki",
    "Bunge la Kenya"
  ]
}
```

## 3. Complete Pipeline

**full_pipeline.py:**
```python
import whisper
from enhance_entities import EntityEnhancer

# Load your fine-tuned model
model = whisper.load_model("./whisper-small-kiswahili-final")

# Load entity enhancer
enhancer = EntityEnhancer("entities_kiswahili.json")

def transcribe_with_entities(audio_file: str):
    # Transcribe
    result = model.transcribe(
        audio_file,
        language="sw",
        task="transcribe"
    )
    
    # Enhance with entities
    enhanced = enhancer.enhance_transcription(result["text"])
    
    return {
        "transcription": enhanced["enhanced"],
        "entities": enhanced["entities"],
        "segments": result.get("segments", [])
    }

# Use it
result = transcribe_with_entities("my_audio.wav")
print(result)
```

## Quick Start (Minimal Training Data)

If you have **limited data** (< 100 hours):

```bash
# Just use base Whisper + entity enhancement
python -c "
import whisper
model = whisper.load_model('small')
result = model.transcribe('audio.wav', language='sw')
print(result['text'])
"
```

Then apply entity enhancement separately - this might be sufficient for your needs without fine-tuning.

## Reality Check

- **Fine-tuning requires**: 10+ hours of Kiswahili audio with accurate transcripts
- **On Mac**: Training is slow; consider using Colab with GPU for actual training
- **Entity recognition**: The keyword matching approach is practical and works well for known entities

Need help with a specific part?