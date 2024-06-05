# w11_prompts_explained.md

## prompt_1 summary_length
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: Input: {source} Produce a {summary_length} sentences length summary of the text. Captures the main ideas and key points of the text. Summary Does not include verbatim sentences from the original text.
```


## prompt_2 text_translate
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: user input: {source} convert it into {target_lang} language output must contain only the translated text
```

## prompt_3 extract_patterns
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: user input: {source} extract following patterns from it: {patterns} output must be in this format:pattern_name: pattern_values...
```

## prompt_4 text_replace
Expliquer en francais ce que fait ce prompt:

```text
Given the original text: user input: {source} And the replacement rule: replacement rule: {replacement_rules}__________________________Replace words in the original text according to the replacement rules provided. Apply the rules to modify the text. Only provide the output that has the modified text with replacements nothing else. Replace words even when sentence does not make sense. make sure all mentioned words must be replaced replace word even if change the meaning of the sentence or does not make sense output format: word_to_replace: replacement_word
```


## prompt_5 detect_ner
Expliquer en francais ce que fait ce prompt:

```text
Given the input text:user input: {source} perform NER detection on it. NER TAGS: FAC;  CARDINAL;  NUMBER;  DEMONYM;  QUANTITY;  TITLE;  PHONE_NUMBER;  NATIONAL;  JOB;  PERSON;  LOC;  NORP;  TIME;  CITY;  EMAIL;  GPE;  LANGUAGE;  PRODUCT;  ZIP_CODE;  ADDRESS;  MONEY;  ORDINAL;  DATE;  EVENT;  CRIMINAL_CHARGE;  STATE_OR_PROVINCE;  RELIGION;  DURATION;  URL;  WORK_OF_ART;  PERCENT;  CAUSE_OF_DEATH;  COUNTRY;  ORG;  LAW;  NAME;  COUNTRY;  RELIGION;  TIME answer must be in the format tag:value
```

## prompt_6 text_summarize
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: Input: {source} Produce a {summary_length} sentences length summary of the text. Captures the main ideas and key points of the text. Summary Does not include verbatim sentences from the original text.
```

## prompt_7 text_qna
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: Input: {source} Answer the following question:  {question} The answer should be relevant and concise; without any additional information. Ensure that the answer directly addresses the question.
```


## prompt_8 text_intent
Expliquer en francais ce que fait ce prompt: 

```text
Given the input sentence: user input: {source} Identify the intent of the text. If no clear intent can be determined from the input; return None. If the output intent contains multiple words; separate them with comma. output must be in this format -> Intent: intent1; intent2; ...
detect_spam, Given the input text; perform spam detection on it  {source} num_classes: {num_classes} You must not provide any other information than the format {format_answer}
```

## prompt_9 text_spellcheck
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: user input: {source} output must be in this format: misspelled_word:corrected_word ... output must not contain any other information than the format
```

## prompt_10 text_srl
Expliquer en francais ce que fait ce prompt: 

```text
Given the input sentence: user input: {source} __________________________ Perform Semantic Role Labeling (SRL) on the input sentence to identify the predicate; agent; and theme. - Predicate: The action or state described by the verb. - Agent: The entity performing the action. - Theme: The entity that is affected by the action. Ensure the output follows this format: - Predicate: [predicate] - Agent: [agent] - Theme: [theme] If any component is not present or cannot be identified; return None for that component.
```

## prompt_11 detect_pos
Expliquer en francais ce que fait ce prompt: 

```text
Given the input text: user input: {source} perform POS detection on it. POS TAGS:noun;  verb;  adjective;  adverb;  pronoun;  preposition;  conjunction;  interjection;  determiner;  cardinal;  foreign;  number;  date;  time;  ordinal;  money;  percent;  symbol;  punctuation;  emoticon;  hashtag;  email;  url;  mention;  phone;  ip;  cashtag;  entity;  answer must be in the format tag:value
```

## prompt_12 text_emojis
Expliquer en francais ce que fait ce prompt: 
```text
Given the input text: user input: {source} Identify the emojis in the text and replace them with their text representation. output must be the updated text with emojis replaced by their text representation. output must not contain any other information than the updated text.
```

## prompt_13 text_idioms
Expliquer en francais ce que fait ce prompt: 
```text
Given the input sentence: user input: {source} __________________________ Identify and extract any idioms present in the sentence. Output must only contain the extracted idioms. Output must not contain any bullet points. If there is more than one idiom found; return both in new lines. If no idiom is found; return None. output must be in this format: extracted idioms ... output must not contain any other information than the extracted idioms.
```


## prompt_13 text_anomaly
Expliquer en francais ce que fait ce prompt: 

```text
Given the input sentence: user input: {source} Detect any anomalies or outliers in the text. output only the detected anomalies and do not provide any other information do not use bullet points or any other formatting output must be in this format: detected anomalies ... output must not contain any other information than the detected anomalies.
```


## prompt_14 text_coreference
Expliquer en francais ce que fait ce prompt: 
```text
Given the input paragraph: user input: {source} __________________________ Perform coreference resolution to identify what each pronoun in the paragraph is referring to. Output must only contain the resolved references for each pronoun; without any additional context. Output must not contain any bullet points. If no referent is found for a pronoun; return 'None'. Output must be in this format: Pronoun: Referent ... output must not contain another information.
```
 