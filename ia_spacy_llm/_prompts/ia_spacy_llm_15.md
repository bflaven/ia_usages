# ia_spacy_llm_13.md

## PROMPT_1

In a prompt how can you prevent the llm to print out tag like  "```python...```" or  "```javascript...```" in the answer. Modify the prompt below so it does output such tag in the answer.


    prompt = f"""
    Make 10 proposals in {language} for a similar title based on this title_model, and a set of 5 keywords in {language} based on the keywords_model and this content_source. The output must in the language specified {language}.

    - title_model
    ```text
    {title_model}
    ```

    - keywords_model
    ```text
    {keywords_model}
    ```

    - language
    ```text
    {language}
    ```

    ```text
    {content_source}
    ```
    Do not ouput any explanations. Just return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] that contains a set of python object without number but with each keyword between quotes.
    """


## MISTRAL_1


prompt = f"""
Make 10 proposals for a similar title based on this title_model, and a set of 5 keywords based on the keywords_model and this content_source. The output must be in the language specified: {language}.

Title Model: {title_model}

Keywords Model: {keywords_model}

Content Source: {content_source}

Do not output any explanations. Just return the "Title Proposals" in a python object named title_proposals = [] and the "Keywords" in a python object named keywords_combinations = [] that contains a set of python objects, each keyword between quotes.
"""


## PROMPT_2

As an IA expert, can you enhance the prompt below and show a possible output from this prompt to ensure that the ouput format is correct.

prompt = f"""
    Make 10 proposals for a similar title based on this title_model, and a set of 5 keywords based on the keywords_model and this content_source. The output must be in the language specified: {language}.

    Title Model: {title_model}

    Keywords Model: {keywords_model}

    Content Source: {content_source}

    Do not output any explanations. Just return the "Title Proposals" in a python list named title_proposals = [] and the "Keywords" in a python list named keywords_combinations = [] that contains a list of a set of 5 keyword each. Each keyword will be between quotes.
    """


## PROMPT_1

Sure, I'd be happy to help with that. Here's an enhanced version of the prompt and a possible output:

Prompt:


prompt = f"""
Given the title model, keywords model, and content source, your task is to generate 10 similar title proposals and 5 unique keyword combinations. The output should be in the language specified: {language}.

Title Model: {title_model}

Keywords Model: {keywords_model}

Content Source: {content_source}

Please return the output in the following format:

title_proposals = [
    "Proposal 1",
    "Proposal 2",
    ...
    "Proposal 10"
]

keywords_combinations = [
    ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    ...
    ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
]

Ensure that each keyword in the keyword combinations is unique and enclosed in quotes.
"""
Possible Output:


title_proposals = [
    "10 Essential Tips for Mastering Python Programming",
    "Python Programming: A Comprehensive Guide for Beginners",
    "Python Programming Techniques for Data Analysis",
    "Python Programming for Machine Learning: A Practical Approach",
    "Python Programming for Web Development: Building Dynamic Websites",
    "Python Programming for Game Development: Creating Interactive Games",
    "Python Programming for Data Visualization: Creating Beautiful Charts",
    "Python Programming for Automation: Automating Repetitive Tasks",
    "Python Programming for Scientific Computing: Solving Complex Problems",
    "Python Programming for Artificial Intelligence: Building Intelligent Systems"
]

keywords_combinations = [
    ["Python", "Programming", "Data Analysis", "Machine Learning", "Web Development"],
    ["Python", "Programming", "Game Development", "Interactive Games", "Graphics"],
    ["Python", "Programming", "Data Visualization", "Matplotlib", "Seaborn"],
    ["Python", "Programming", "Automation", "Task Scheduler", "Python Scripting"],
    ["Python", "Programming", "Scientific Computing", "NumPy", "SciPy"]
]
In this example, the language model generates 10 title proposals based on the title model, keywords model, and content source. It also generates 5 unique keyword combinations based on the keywords model. The output is formatted as requested, with the title proposals in a Python list named title_proposals and the keyword combinations in a Python list named keywords_combinations. Each keyword in the keyword combinations is unique and enclosed in quotes.


