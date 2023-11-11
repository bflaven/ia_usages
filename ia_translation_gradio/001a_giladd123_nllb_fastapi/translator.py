import ctranslate2
import transformers
# from lang_list import lang_list
from lang_list import lang_list
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline



class translator:
    def __init__(self):
        """
        Initialize the translator class with the model and tokenizer directories.
        """
        self.lang_list = lang_list

    def translate(self, src_lang, tgt_lang, input_text):
        """
        Translate the input text from the source language to the target language.
        """
        checkpoint = 'facebook/nllb-200-distilled-600M'
        # checkpoint = 'facebook/nllb-200-1.3B'
        # checkpoint = 'facebook/nllb-200-3.3B'
        # checkpoint = 'facebook/nllb-200-distilled-1.3B'

        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)

        
        translation_pipeline = pipeline('translation', 
                                        model=model, 
                                        tokenizer=tokenizer, 
                                        src_lang=src_lang, 
                                        tgt_lang=tgt_lang, 
                                        max_length = 400)


        output = translation_pipeline(input_text)
        # print(output[0]['translation_text'])

        return output

    def validate_inputs(self, src_lang, tgt_lang):
        """
        Validate the source and target languages.
        """
        invalid_languages = []
        if src_lang not in self.lang_list:
            invalid_languages.append(src_lang)

        if tgt_lang not in self.lang_list:
            invalid_languages.append(tgt_lang)

        return invalid_languages

    def check_langs_not_equal(self, src_lang, tgt_lang):
        """
        Check if the source and target languages are not the same.
        """

        if src_lang == tgt_lang:
            return False
        return True
