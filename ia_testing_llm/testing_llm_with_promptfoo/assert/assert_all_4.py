#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name promptfoo python=3.9.13
conda info --envs
source activate promptfoo
conda deactivate


# BURN AFTER READING
source activate promptfoo

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n promptfoo

# BURN AFTER READING
conda env remove -n promptfoo


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install langdetect
python -m pip install langdetect

Check https://pypi.org/project/langdetect/

"""
import json
from langdetect import detect, LangDetectException

def get_assert(output, context):
    try:
        # Parse the output as JSON
        output_json = json.loads(output)

        # Check if the output is a list with one dictionary
        if not isinstance(output_json, list) or len(output_json) != 1 or not isinstance(output_json[0], dict):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Output is not a list with one dictionary."
            }

        item = output_json[0]

        # Check the title length
        title = item.get("1", "")
        if not (20 <= len(title) <= 100):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Title length is not between 20 and 100 characters."
            }

        # Check the summary structure
        summary = item.get("2", "")
        if not (2 <= summary.count('.') <= 3):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Summary does not contain 2 to 3 sentences."
            }

        # Check the keywords
        keywords = item.get("3", [])
        if not (isinstance(keywords, list) and len(keywords) == 5):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Keywords are not a list of 5 items."
            }

        # Check the category
        category = item.get("4", "")
        if not category:
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Category is missing."
            }

        # Check the language of the title, summary, and keywords
        try:
            title_lang = detect(title)
            summary_lang = detect(summary)
            keywords_lang = detect(" ".join(keywords))
            # category_lang = detect(category)

        
            # add languages to the list if needed
            # langdetect supports 55 languages out of the box (ISO 639-1 codes)
            # https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
            # af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw
        

            # Languages for FMM
            # ar, br, cn, en, es, fa, ff, fr, ha, km, ma, pt, ro, ru, sw, uk, vi




            valid_languages = {"ar", "en", "es", "fa", "fr", "pt", "ro", "ru", "sw", "uk", "vi", "zh-cn"}
            if (title_lang not in valid_languages 
                or summary_lang not in valid_languages 
                or keywords_lang not in valid_languages 
                # or category_lang not in valid_languages
                ):
                return {
                    "pass": False,
                    "score": 0.0,
                    "reason": "The language of the result is not part of FMM languages and langdetect."
                }

        except LangDetectException as e:
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Language detection error."
            }

        # All checks passed
        return {
            "pass": True,
            "score": 1.0,
            "reason": "All checks passed."
        }

    except json.JSONDecodeError:
        return {
            "pass": False,
            "score": 0.0,
            "reason": "Output is not a valid JSON."
        }
