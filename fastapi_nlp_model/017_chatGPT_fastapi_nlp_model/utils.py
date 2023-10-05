

from typing import Optional
import spacy
from itertools import chain
from nltk.corpus import wordnet
from gtts import gTTS 

# python -m spacy validate
# nlp = spacy.load("en_core_web_sm")
# nlp = spacy.load("en_core_web_lg")

# pip install nltk
# python -m spacy download en_core_web_sm 

def similarity_(text_1 : str , text_2 : str,nlp=nlp) -> float:
    text_1 = nlp(text_1)
    text_2 = nlp(text_2)
    score = text_1.similarity(text_2)
    return score

def tokenize_(text : str , nlp=nlp):
    doc = nlp(text)
    doc_ = doc.to_json()
    return doc_

def synonyms_(text : str ):
    try:
        synonyms_ = wordnet.synsets(text)
        lemmas = list(set(chain.from_iterable([word.lemma_names() for word in synonyms_])))
        return lemmas
    except:
        return []
    

def antonyms_(text : str ):
    try:
        antonyms_ = wordnet.synsets(text)
        lemmas = list(set([lm.antonyms()[0].name() for syn in antonyms_ for lm in syn.lemmas() if lm.antonyms()]))
        return lemmas
    except:
        return []

def text_to_speech_(text : str , language : Optional[str] = 'en'):
    try:
        aud = gTTS(text=text, lang=language, slow=False)
    except:
        aud = gTTS(text=text, lang='en', slow=False)
    else:
        pass
    return aud

if __name__== '__main__':
   print(synonyms_('mad'))