"""

Prompt: Write me a function in Python that select randomly a unique quote among ten quotes. You can provide your own quotes on Cooking.
Model: TheBloke/Orca-2-7B-GGUF/orca-2-7b.Q2_K.gguf through LM Studio

cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_academy_project/

python interpreter_links_4.py

# PROMPT_1
Can you add each element into a Python's list named "links" :

https://www.perplexity.ai/
https://towardsdatascience.com/extracting-text-from-pdf-files-with-python-a-comprehensive-guide-9fc4003d517
https://github.com/jsvine/pdfplumber
https://source.opennews.org/articles/testing-pdf-data-extraction-chatgpt/
https://github.com/brandonrobertz
https://www.youtube.com/watch?v=wsSqRv-y1r4
https://github.com/dair-ai/Prompt-Engineering-Guide.git
https://www.educative.io/courses/all-you-need-to-know-about-prompt-engineering
https://developers.google.com/machine-learning/resources/intro-llms
https://github.com/amazon-science
https://www.datacamp.com/tutorial/llama-cpp-tutorial
https://continue.dev/
https://github.com/KillianLucas/open-interpreter/#demo
https://docs.openinterpreter.com/introduction


# PROMPT_2
In python, can you iterate through the list and print each link into this code

links = [
    'https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/guides/prompts-intro.md', 
    'https://github.com/dair-ai/Prompt-Engineering-Guide',
    'https://dair.ai/posts/',
    'https://github.com/dair-ai',
    'https://source.opennews.org/guides/',
    'https://maven.com/dair-ai/prompt-engineering-llms',
    'https://platform.openai.com/docs/guides/images/language-specific-tips?context=python',
    'https://www.journalismai.info/programmes/discovery', 
    'https://source.opennews.org/articles/testing-pdf-data-extraction-chatgpt/', 
    'https://github.com/brandonrobertz', 
    'https://source.opennews.org/'
]

In python, how to iterate from a list and create an html output into a file  output.html?



"""

# Add the links into a Python list named "links"
# links = [
#     'https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/guides/prompts-intro.md', 
#     'https://github.com/dair-ai/Prompt-Engineering-Guide',
#     'https://dair.ai/posts/',
#     'https://github.com/dair-ai',
#     'https://source.opennews.org/guides/',
#     'https://maven.com/dair-ai/prompt-engineering-llms',
#     'https://platform.openai.com/docs/guides/images/language-specific-tips?context=python',
#     'https://www.journalismai.info/programmes/discovery', 
#     'https://source.opennews.org/articles/testing-pdf-data-extraction-chatgpt/', 
#     'https://github.com/brandonrobertz', 
#     'https://source.opennews.org/'
# ]

links = ['https://www.perplexity.ai/', 'https://towardsdatascience.co/extracting-text-from-pdf-files-with-python-a-comprehensive-guide-9fc4003d517', 'https://github.com/jsvine/pdfplumber', 'https://source.opennews.org/articles/testing-pdf-data-extraction-chatgpt', 'https://github.com/brandonrobertz', 'https://www.youtube.com/watch?v=wsSqRv-y1r4', 'https://github.com/dair-ai/Prompt-Engineering-Guide.git', 'https://www.educative.io/courses/all-you-need-to-know-about-prompt-engin', 'https://developers.google.com/machine-learning/resources/intro-llms', 'https://github.com/amazon-science', 'https://www.datacamp.com/tutorial/llama-cpp-tutorial', 'https://continue.dev/', 'https://github.com/KillianLucas/open-interpreter/#demo', 'https://docs.openinterpreter.com/introduction']

for link in links:
  # print(link)
  print(f'<li>text<br><a href="{link}" target="_blank" rel="noopener">{link}</a></li>')
  print()


  
"""        
links = []

# Iterate through the text and add each URL to the list
for link in ['https://www.perplexity.ai/', 
'https://towardsdatascience.co/extracting-text-from-pdf-files-with-python-a-comprehensive-guide-9fc4003d517', 
'https://github.com/jsvine/pdfplumber', 
'https://source.opennews.org/articles/testing-pdf-data-extraction-chatgpt', 'https://github.com/brandonrobertz', 
'https://www.youtube.com/watch?v=wsSqRv-y1r4', 
'https://github.com/dair-ai/Prompt-Engineering-Guide.git', 
'https://www.educative.io/courses/all-you-need-to-know-about-prompt-engin', 
'https://developers.google.com/machine-learning/resources/intro-llms', 
'https://github.com/amazon-science', 
'https://www.datacamp.com/tutorial/llama-cpp-tutorial', 
'https://continue.dev/', 
'https://github.com/KillianLucas/open-interpreter/#demo', 
'https://docs.openinterpreter.com/introduction']:
    links.append(link)
    
print(links)
"""