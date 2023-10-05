#!/usr/bin/python
# -*- coding: utf-8 -*-

import spacy
from spacy.language import Language

from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from .punctuation import TOKENIZER_PREFIXES, TOKENIZER_INFIXES
from .punctuation import TOKENIZER_SUFFIXES
from .stop_words import STOP_WORDS
from .syntax_iterators import SYNTAX_ITERATORS


class CustomEnglishDefaults(Language.Defaults):
    tokenizer_exceptions = TOKENIZER_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    infixes = TOKENIZER_INFIXES
    suffixes = TOKENIZER_SUFFIXES
    syntax_iterators = SYNTAX_ITERATORS
    stop_words = STOP_WORDS


@spacy.registry.languages("custom_en")
class CustomEnglish(Language):
    lang = "custom_en"
    Defaults = CustomEnglishDefaults
    
    
    
