
# 008_ia_testing_llm.md






## PROMPT_1

As a Python and Promptfoo expert, writes, in pyhton, some assertions that test the relevance of the output in term of content.


## MSITRAL_1




Certainly! When testing the relevance of the output in terms of content, you typically want to ensure that the output meets certain criteria or contains specific information. Here are some examples of assertions in Python that can help you verify the relevance of the output:

1. **Checking for Specific Keywords**:
   ```python
   def test_output_contains_keywords(output, keywords):
       for keyword in keywords:
           assert keyword in output, f"Keyword '{keyword}' not found in output"

   # Example usage
   output = "The quick brown fox jumps over the lazy dog."
   keywords = ["quick", "fox", "dog"]
   test_output_contains_keywords(output, keywords)
   ```

2. **Checking for Minimum Length**:
   ```python
   def test_output_minimum_length(output, min_length):
       assert len(output) >= min_length, f"Output length is less than {min_length}"

   # Example usage
   output = "The quick brown fox jumps over the lazy dog."
   min_length = 10
   test_output_minimum_length(output, min_length)
   ```

3. **Checking for Specific Patterns (e.g., Email Address)**:
   ```python
   import re

   def test_output_contains_email(output):
       email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
       assert re.search(email_pattern, output), "No email address found in output"

   # Example usage
   output = "Contact us at support@example.com for assistance."
   test_output_contains_email(output)
   ```

4. **Checking for Specific Data Types**:
   ```python
   def test_output_contains_number(output):
       assert any(char.isdigit() for char in output), "No number found in output"

   # Example usage
   output = "The quick brown fox jumps over the lazy dog 123."
   test_output_contains_number(output)
   ```

5. **Checking for Specific Phrases**:
   ```python
   def test_output_contains_phrase(output, phrase):
       assert phrase in output, f"Phrase '{phrase}' not found in output"

   # Example usage
   output = "The quick brown fox jumps over the lazy dog."
   phrase = "jumps over"
   test_output_contains_phrase(output, phrase)
   ```

6. **Checking for Specific Format (e.g., Date)**:
   ```python
   import re

   def test_output_contains_date(output):
       date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
       assert re.search(date_pattern, output), "No date found in output"

   # Example usage
   output = "The event is scheduled for 2023-10-15."
   test_output_contains_date(output)
   ```

These assertions can be used in your test cases to ensure that the output meets the expected criteria in terms of content relevance.


## PROMPT_1


As a Python and Promptfoo expert, extends, in python, the assertions below with a test on the keywords relevance in the output.


```json

"3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition"],

 "3": ["Rassemblement national", "Nouveau front populaire", "Patrons", "Économie française", "Incertitude"],


 

```



```python
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
```

## MISTRAL_1
To extend the provided assertions with a test on the relevance of the keywords in the output, we can add a function that checks if the keywords are relevant to the context. For simplicity, let's assume that the context is provided as a list of relevant keywords, and we will check if the keywords in the output are a subset of the context keywords.

Here's the extended code:

```python
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

        # Check the relevance of the keywords
        context_keywords = context.get("3", [])
        if not set(keywords).issubset(set(context_keywords)):
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Keywords are not relevant to the context."
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

            # Languages for FMM
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

# Example usage
output = '''
[
    {
        "1": "PSG Wins Ligue des Champions",
        "2": "PSG secured a historic win in the Ligue des Champions. The team, led by Luis Enrique, dominated the competition. Football fans worldwide celebrated the victory.",
        "3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition"],
        "4": "Sports"
    }
]
'''

context = {
    "3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"]
}

result = get_assert(output, context)
print(result)
```

In this extended code, the `get_assert` function now includes a check for the relevance of the keywords. It compares the keywords in the output with the context keywords and ensures that the output keywords are a subset of the context keywords. If the keywords are not relevant, the function returns a failure message.

## MISTRAL_3
As a Python and Promptfoo expert, extends, in python, some assertions for this test in order to add some cases for languages: "fr", "en", "es"...

For instance for the language "fr", the test has to compare with this good_keywords_list = ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"]


```python
    # Check the keywords
    keywords = item.get("3", [])
    if not (isinstance(keywords, list) and len(keywords) == 5):
        return {
            "pass": False,
            "score": 0.0,
            "reason": "Keywords are not a list of 5 items."
        }
```


## MISTRAL_3

To extend the assertions to handle different languages and their respective good keyword lists, you can create a mapping of languages to their corresponding good keyword lists. Then, based on the detected language of the keywords, you can check the relevance of the keywords against the appropriate list.

Here's the extended code:

```python
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

            # Languages for FMM
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

            # Mapping of languages to their good keyword lists
            good_keywords_lists = {
                "fr": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"],
                "en": ["PSG", "Champions League", "Luis Enrique", "Football", "Competition", "Victory", "Celebration"],
                "es": ["PSG", "Liga de Campeones", "Luis Enrique", "Fútbol", "Competencia", "Victoria", "Celebración"],
                # Add more languages and their good keyword lists as needed
            }

            # Get the good keyword list for the detected language
            good_keywords_list = good_keywords_lists.get(keywords_lang, [])
            if not set(keywords).issubset(set(good_keywords_list)):
                return {
                    "pass": False,
                    "score": 0.0,
                    "reason": "Keywords are not relevant to the context."
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

# Example usage
output = '''
[
    {
        "1": "PSG Wins Ligue des Champions",
        "2": "PSG secured a historic win in the Ligue des Champions. The team, led by Luis Enrique, dominated the competition. Football fans worldwide celebrated the victory.",
        "3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition"],
        "4": "Sports"
    }
]
'''

context = {
    "3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"]
}

result = get_assert(output, context)
print(result)
```

In this extended code, we have added a mapping of languages to their respective good keyword lists. The function detects the language of the keywords and then checks the relevance of the keywords against the appropriate list based on the detected language. If the keywords are not relevant, the function returns a failure message.


Make the case according to the language, as there are 2 articles in french, it enables to load the 2 lists and 1 for "en" then one for "es"
# Mapping of languages to their good keyword lists
            good_keywords_lists = {
                "fr": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"],
                "fr": ["Rassemblement national", "Nouveau front populaire", "Patrons", "Économie française", "Incertitude"],
                # "en": ["PSG", "Champions League", "Luis Enrique", "Football", "Competition", "Victory", "Celebration"],
                # "es": ["PSG", "Liga de Campeones", "Luis Enrique", "Fútbol", "Competencia", "Victoria", "Celebración"],
                # Add more languages and their good keyword lists as needed
            }

            # Get the good keyword list for the detected language
            good_keywords_list = good_keywords_lists.get(keywords_lang, [])
            if not set(keywords).issubset(set(good_keywords_list)):
                return {
                    "pass": False,
                    "score": 0.0,
                    "reason": "Keywords are not relevant to the context."
                }


## MISTRAL_5


To handle multiple articles in the same language and ensure that the keywords are checked against the appropriate list, you can modify the `good_keywords_lists` mapping to include multiple lists for each language. Then, you can iterate through these lists to check if the keywords are relevant to any of the contexts.

Here's the updated code:

```python
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

            # Languages for FMM
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

            # Mapping of languages to their good keyword lists
            good_keywords_lists = {
                "fr": [
                    ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"],
                    ["Rassemblement national", "Nouveau front populaire", "Patrons", "Économie française", "Incertitude"]
                ],
                "en": [["PSG", "Champions League", "Luis Enrique", "Football", "Competition", "Victory", "Celebration"]],
                "es": [["PSG", "Liga de Campeones", "Luis Enrique", "Fútbol", "Competencia", "Victoria", "Celebración"]],
                # Add more languages and their good keyword lists as needed
            }

            # Get the good keyword lists for the detected language
            good_keywords_lists_for_lang = good_keywords_lists.get(keywords_lang, [])
            is_relevant = any(set(keywords).issubset(set(good_keywords_list)) for good_keywords_list in good_keywords_lists_for_lang)

            if not is_relevant:
                return {
                    "pass": False,
                    "score": 0.0,
                    "reason": "Keywords are not relevant to the context."
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

# Example usage
output = '''
[
    {
        "1": "PSG Wins Ligue des Champions",
        "2": "PSG secured a historic win in the Ligue des Champions. The team, led by Luis Enrique, dominated the competition. Football fans worldwide celebrated the victory.",
        "3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition"],
        "4": "Sports"
    }
]
'''

context = {
    "3": ["PSG", "Ligue des champions", "Luis Enrique", "Football", "Compétition", "Victory", "Celebration"]
}

result = get_assert(output, context)
print(result)
```

In this updated code, the `good_keywords_lists` mapping now includes multiple lists for each language. The function iterates through these lists to check if the keywords are relevant to any of the contexts. If the keywords are not relevant to any of the contexts, the function returns a failure message.

## MISTRAL_6

As a Python and Promptfoo expert, extends, in python, some assertions with "llm-rubric". llm-rubric is promptfoo's general-purpose grader for "LLM as a judge" evaluation.

```yaml
assert:
  - type: llm-rubric
    # Specify the criteria for grading the LLM output:
    value: Is not apologetic and provides a clear, concise answer
```



