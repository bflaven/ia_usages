# Claude Blog Generator

This project demonstrates how to use the Anthropic Claude Agents SDK to generate SEO-optimized blog posts.

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install anthropic python-dotenv
```
3. Create a `.env` file in the project root with your Claude API key:
```
CLAUDE_API_KEY=your_api_key_here
```

## Files

- `claude_blog_creator.py`: Main module with the ClaudeBlogCreator class
- `013_ia_using_claude_agents_sdk.py`: Example script showing how to use the module

## Usage

### Command Line Interface

Run the script with command-line arguments:

```bash
python 013_ia_using_claude_agents_sdk.py --keyword "Ecology and Sustainable Development" --context "Write a social media post promoting our new eco-friendly water bottles to young adults interested in sustainability"
```

#### Optional Arguments:

- `--keyword` or `-k`: Main keyword for SEO (default: "Ecology and Sustainable Development")
- `--context` or `-c`: Context for blog creation (default: example context)
- `--model` or `-m`: Claude model to use (default: claude-3-haiku-20240307)
- `--output` or `-o`: Output file name (default: blog_post_[keyword].md)
- `--max-tokens`: Maximum tokens in response (default: 4000)

### Using as a Module

```python
import asyncio
from claude_blog_creator import ClaudeBlogCreator

async def generate_blog():
    # Initialize the blog creator
    blog_creator = ClaudeBlogCreator()
    
    # Optionally set a different model
    # blog_creator.set_model("claude-3-opus-20240229")
    
    # Define your keyword and context
    keyword = "Ecology and Sustainable Development"
    context = "Write a social media post promoting our new eco-friendly water bottles to young adults interested in sustainability"
    
    # Generate the blog post
    blog_post = await blog_creator.create_blog_post(keyword, context)
    
    # Save to file (optional)
    blog_creator.save_blog_post(blog_post, "my_blog_post.md")
    
    return blog_post

# Run the async function
blog_content = asyncio.run(generate_blog())
```

## Notes

- The script uses Claude's capabilities for creative writing and SEO optimization
- The BLOG_CREATOR_PROMPT template can be modified to adjust the formatting and requirements
- Blog posts are saved as Markdown (.md) files by default

## Models

You can select different Claude models based on your needs:
- claude-3-haiku-20240307 (fastest, default)
- claude-3-sonnet-20240229 (balanced)
- claude-3-opus-20240229 (highest quality)