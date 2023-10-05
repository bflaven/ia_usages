#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
002_modify_data.py
source Python for GPT query  
QUERY :: In Python, write a function name ExtractEven that extract from only the even item from the following categories list: Nature, Tech, Science, Life, Entertainment, Development, Videos, Cinema, Serial, Literature, Foreign politics, Philosophy.
Then, write a function ExtractOdd that extract from only the odd item from the same list.


[path]
cd //Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_prompts/extras_files/


[file]
python 002_modify_data.py

"""


def ExtractEven(categories):
    even_items = []
    for index, category in enumerate(categories):
        if index % 2 == 0:
            even_items.append(category)
    return even_items


def ExtractOdd(categories):
    odd_items = []
    for index, category in enumerate(categories):
        if index % 2 != 0:
            odd_items.append(category)
    return odd_items


# Example usage
items = [
    'INTRODUCTION',
    'General description for OpenAI platform examples.',
    'Q&A',
    'Answer questions based on existing knowledge.',
    'Grammar correction',
    'Corrects sentences into standard English.',
    'Summarize for a 2nd grader',
    'Translates difficult text into simpler concepts.',
    'Natural language to OpenAI API',
    'Create code to call to the OpenAI API using a natural language instruction.',
    'Text to command',
    'Translate text into programmatic commands.',
    'English to other languages',
    'Translates English text into French, Spanish and Japanese.',
    'Natural language to Stripe API',
    'Create code to call the Stripe API using natural language.',
    'SQL translate',
    'Translate natural language to SQL queries.',
    'Parse unstructured data',
    'Create tables from long form text.',
    'Classification',
    'Classify items into categories via example.',
    'Python to natural language',
    'Explain a piece of Python code in human understandable language.',
    'Movie to Emoji',
    'Convert movie titles into emoji.',
    'Calculate Time Complexity',
    'Find the time complexity of a function.',
    'Translate programming languages',
    'Translate from one programming language to another.',
    'Advanced tweet classifier',
    'Advanced sentiment detection for a piece of text.',
    'Explain code',
    'Explain a complicated piece of code.',
    'Keywords',
    'Extract keywords from a block of text.',
    'Factual answering',
    'Direct the model to provide factual answers and address knowledge gaps.',
    'Ad from product description',
    'Turn a product description into ad copy.',
    'Product name generator',
    'Create product names from examples words.',
    'TL;DR summarization',
    'Summarize text by adding a \'tl;dr:\' to the end of a text passage. It shows that the API understands how to perform a number of tasks with no instructions.',
    'Python bug fixer',
    'Find and fix bugs in source code.',
    'Spreadsheet creator',
    'Create spreadsheets of various kinds of data.',
    'JavaScript helper chatbot',
    'Message-style bot that answers JavaScript questions.',
    'ML/AI language model tutor.',
    'Bot that answers questions about language models',
    'Science fiction book list maker',
    'Create a list of items for a given topic.',
    'Tweet classifier',
    'Basic sentiment detection for a piece of text.',
    'Airport code extractor',
    'Extract airport codes from text.',
    'SQL request',
    'Create simple SQL queries.',
    'Extract contact information',
    'Extract contact information from a block of text.',
    'JavaScript to Python',
    'Convert simple JavaScript expressions into Python.',
    'Friend chat',
    'Emulate a text message conversation.',
    'Mood to color',
    'Turn a text description into a color.',
    'Write a Python docstring',
    'Write a docstring for a Python function.',
    'Analogy maker',
    'Create analogies.',
    'JavaScript one line function',
    'Turn a JavaScript function into a one liner.',
    'Micro horror story creator',
    'Creates two to three sentence short horror stories from a topic input.',
    'Third-person converter',
    'Converts first-person POV to the third-person.',
    'Notes to summary',
    'Turn meeting notes into a summary.',
    'VR fitness idea generator',
    'Create ideas for fitness and virtual reality games.',
    'Essay outline',
    'Generate an outline for a research topic.',
    'Recipe creator (eat at your own risk)',
    'Create a recipe from a list of ingredients.',
    'Chat',
    'Open ended conversation with an AI assistant.',
    'Marv the sarcastic chat bot',
    'Marv is a factual chatbot that is also sarcastic.',
    'Turn by turn directions',
    'Convert natural language to turn-by-turn directions.',
    'Restaurant review creator',
    'Turn a few words into a restaurant review.',
    'Create study notes',
    'Provide a topic and get study notes.',
    'Interview questions',
    'Create interview questions.'
]

even_categories = ExtractEven(items)
# print('Even categories:', even_categories)

odd_categories = ExtractOdd(items)
# print('Odd categories:', odd_categories)

count = len(items)
count_even = len(even_categories)
count_odd = len(odd_categories)

# print('\n--- COUNT')
# print(f'count :: {count}')
# print(f'count_even :: {count_even}')
# print(f'count_odd :: {count_odd}')
# print('\n--- RESULT')
# print(f'even_categories :: {even_categories}')
# print(f'odd_categories :: {odd_categories}')


""" OUTPUT """
MENU_SIDEBAR_USECASE_TITLE_OPTIONS = ['INTRODUCTION', 'Q&A', 'Grammar correction', 'Summarize for a 2nd grader', 'Natural language to OpenAI API', 'Text to command', 'English to other languages', 'Natural language to Stripe API', 'SQL translate', 'Parse unstructured data', 'Classification', 'Python to natural language', 'Movie to Emoji', 'Calculate Time Complexity', 'Translate programming languages', 'Advanced tweet classifier', 'Explain code', 'Keywords', 'Factual answering', 'Ad from product description', 'Product name generator', 'TL;DR summarization', 'Python bug fixer', 'Spreadsheet creator', 'JavaScript helper chatbot', 'ML/AI language model tutor.', 'Science fiction book list maker', 'Tweet classifier', 'Airport code extractor', 'SQL request', 'Extract contact information', 'JavaScript to Python', 'Friend chat', 'Mood to color', 'Write a Python docstring', 'Analogy maker', 'JavaScript one line function', 'Micro horror story creator', 'Third-person converter', 'Notes to summary', 'VR fitness idea generator', 'Essay outline', 'Recipe creator (eat at your own risk)', 'Chat', 'Marv the sarcastic chat bot', 'Turn by turn directions', 'Restaurant review creator', 'Create study notes', 'Interview questions']

MENU_SIDEBAR_USECASE_DESCRIPTION_OPTIONS = ['General description for OpenAI platform examples.', 'Answer questions based on existing knowledge.', 'Corrects sentences into standard English.', 'Translates difficult text into simpler concepts.', 'Create code to call to the OpenAI API using a natural language instruction.', 'Translate text into programmatic commands.', 'Translates English text into French, Spanish and Japanese.', 'Create code to call the Stripe API using natural language.', 'Translate natural language to SQL queries.', 'Create tables from long form text.', 'Classify items into categories via example.', 'Explain a piece of Python code in human understandable language.', 'Convert movie titles into emoji.', 'Find the time complexity of a function.', 'Translate from one programming language to another.', 'Advanced sentiment detection for a piece of text.', 'Explain a complicated piece of code.', 'Extract keywords from a block of text.', 'Direct the model to provide factual answers and address knowledge gaps.', 'Turn a product description into ad copy.', 'Create product names from examples words.', "Summarize text by adding a 'tl;dr:' to the end of a text passage. It shows that the API understands how to perform a number of tasks with no instructions.", 'Find and fix bugs in source code.', 'Create spreadsheets of various kinds of data.', 'Message-style bot that answers JavaScript questions.', 'Bot that answers questions about language models', 'Create a list of items for a given topic.', 'Basic sentiment detection for a piece of text.', 'Extract airport codes from text.', 'Create simple SQL queries.', 'Extract contact information from a block of text.', 'Convert simple JavaScript expressions into Python.', 'Emulate a text message conversation.', 'Turn a text description into a color.', 'Write a docstring for a Python function.', 'Create analogies.', 'Turn a JavaScript function into a one liner.', 'Creates two to three sentence short horror stories from a topic input.', 'Converts first-person POV to the third-person.', 'Turn meeting notes into a summary.', 'Create ideas for fitness and virtual reality games.', 'Generate an outline for a research topic.', 'Create a recipe from a list of ingredients.', 'Open ended conversation with an AI assistant.', 'Marv is a factual chatbot that is also sarcastic.', 'Convert natural language to turn-by-turn directions.', 'Turn a few words into a restaurant review.', 'Provide a topic and get study notes.', 'Create interview questions.']


print('\n--- COUNT')
print(
    f'count for MENU_SIDEBAR_USECASE_TITLE_OPTIONS :: {len(MENU_SIDEBAR_USECASE_TITLE_OPTIONS)}')
print(
    f'count for MENU_SIDEBAR_USECASE_DESCRIPTION_OPTIONS :: {len(MENU_SIDEBAR_USECASE_DESCRIPTION_OPTIONS)}')
























