# 004_ia_create_agents.md

## PROMPT_1
As a python expert, can you write a script that enable these two files `013_ia_using_claude_agents_sdk.py`. You can still keep best practises for coding e.g Class and function then show how to launch a test to retrieve from an real example with "keyword" and 
context" defined like below. Follow these guidelines: 

1. Leverage on the variable "BLOG_CREATOR_PROMPT" 
1. {keyword} and {context} are two variables let the user defined it.
e.g. context = "Write a social media post promoting our new eco-friendly water bottles to young adults interested in sustainability"
keyword = "Ecology and Sustainable Development"

2. The CLAUDE_API_KEY is stored inside a .env so be sure to use 

```python
from dotenv import load_dotenv

# Load environment variables
load_dotenv() 
```


```python
BLOG_CREATOR_PROMPT = """
     Given the following information, generate a blog post                   
    Write a full blog post that will rank for the following keywords: {keyword}                 
                    
    Instructions:
    The blog should be properly and beautifully formatted using markdown.
    The blog title should be SEO optimized.
    The blog title, should be crafted with the keyword in mind and should be catchy and engaging. But not overly expressive.
    Generate a title that is concise and direct. Avoid using introductory phrases like 'Exploring' or 'Discover'. For example:

    Incorrect: 'Exploring Gulu: 10 Best Things to Do in Gulu'
    Correct: '10 Best Things to Do in Gulu'

    Incorrect: 'Who is Elon Musk: Exploring the Mind of a Mobile App Alchemist'
    Correct: 'The story of Elon Musk'

    Please provide titles in the correct format.
    Do not include : in the title.
    Each sub-section should have at least 3 paragraphs.
    Each section should have at least three subsections.
    Sub-section headings should be clearly marked.

    Clearly indicate the title, headings, and sub-headings using markdown.
    Each section should cover the specific aspects as outlined.

    For each section, generate detailed content that aligns with the provided subtopics. Ensure that the content is informative and covers the key points.
    Ensure that the content is consistent with the title and subtopics. Do not mention an entity in the title and not write about it in the content.

     Ensure that the content flows logically from one section to another, maintaining coherence and readability.

     Where applicable, include examples, case studies, or insights that can provide a deeper understanding of the topic.

     Always include discussions on ethical considerations, especially in sections dealing with data privacy, bias, and responsible use. Only add this where it is applicable.

     In the final section, provide a forward-looking perspective on the topic and a conclusion.
     Please ensure proper and standard markdown formatting always.

     Make the blog post sound as human and as engaging as possible, add real world examples and make it as informative as possible.
     
     You are a professional blog post writer and SEO expert.
     Each blog post should have atleast 5 sections with 3 sub-sections each.
     Each sub section should have atleast 3 paragraphs.
     Context: {context}
     
     Blog Post: 
"""
```

## OUTPUT
I'll create a Python script that leverages the Claude Agents SDK to generate blog posts using the provided BLOG_CREATOR_PROMPT template. The script will follow best practices with proper class and function organization, and include a test example using the keyword and context variables you specified.

Now I'll create a separate script file for the test file that will demonstrate how to use the ClaudeBlogCreator class:

Now I'll create a README file with instructions on how to use these scripts:

## How to Use the Claude Blog Creator

I've created three files for you:

1. **claude_blog_creator.py** - The main module containing the `ClaudeBlogCreator` class with all the core functionality
2. **013_ia_using_claude_agents_sdk.py** - The example script that demonstrates how to use the module
3. **README.md** - Documentation with setup and usage instructions

### Features Implemented:

- A well-structured Python class `ClaudeBlogCreator` that encapsulates all functionality
- Environment variable loading for the API key using python-dotenv
- Asynchronous API calls using Claude's latest SDK
- Command-line interface with argument parsing
- Functions to save generated content to markdown files
- Customizable model selection
- Error handling
- Clear documentation and examples

### How to Run a Test:

1. Make sure you have a `.env` file with your Claude API key:
   ```
   CLAUDE_API_KEY=your_api_key_here
   ```

2. Install the required dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```

3. Run the example script:
   ```bash
   python 013_ia_using_claude_agents_sdk.py
   ```

   This will use the default keyword and context:
   - Keyword: "Ecology and Sustainable Development"
   - Context: "Write a social media post promoting our new eco-friendly water bottles to young adults interested in sustainability"

4. To specify custom keyword and context:
   ```bash
   python 013_ia_using_claude_agents_sdk.py --keyword "Digital Marketing Trends" --context "Write an informative blog post about emerging digital marketing trends for small businesses in 2025"
   ```

### Code Structure:

The code follows best practices with:
- Clear class and function organization
- Type hints for better code clarity
- Comprehensive documentation
- Error handling
- Default values for optional parameters
- Asynchronous programming for optimal performance

The BLOG_CREATOR_PROMPT is used exactly as provided, with the {keyword} and {context} placeholders properly formatted for string interpolation.

Would you like me to explain any specific part of the implementation in more detail?

