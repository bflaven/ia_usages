"""
Claude Agents SDK Blog Creator Example

This script demonstrates how to use the Claude Agents SDK to generate blog content
based on keywords and context information.
"""

import asyncio
import os
import argparse
from typing import Dict, Any
from dotenv import load_dotenv

# Import the ClaudeBlogCreator class from our module
# Define the ClaudeBlogCreator class in this file
import os
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from anthropic import Anthropic

# Blog creator prompt template
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


class ClaudeBlogCreator:
    """
    A class to interact with Claude AI for generating blog posts.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ClaudeBlogCreator with an API key.
        
        Args:
            api_key: Claude API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("Claude API key is required. Set it via CLAUDE_API_KEY environment variable or pass it directly.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"  # Default model, can be changed
    
    def set_model(self, model_name: str) -> None:
        """
        Set the Claude model to use.
        
        Args:
            model_name: Name of the Claude model to use
        """
        self.model = model_name
    
    async def create_blog_post(self, keyword: str, context: str, max_tokens: int = 4000) -> str:
        """
        Generate a blog post using Claude based on keyword and context.
        
        Args:
            keyword: The main keyword for SEO optimization
            context: Context information for blog creation
            max_tokens: Maximum tokens in the response
            
        Returns:
            Generated blog post as string
        """
        prompt = BLOG_CREATOR_PROMPT.format(keyword=keyword, context=context)
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the blog post text from the response
            blog_content = response.content[0].text if response.content else ""
            return blog_content
            
        except Exception as e:
            print(f"Error generating blog post: {e}")
            return f"Failed to generate blog post: {str(e)}"
    
    def save_blog_post(self, content: str, filename: str) -> str:
        """
        Save the generated blog post to a file.
        
        Args:
            content: Blog post content
            filename: Name of the file to save to
            
        Returns:
            Path to the saved file
        """
        try:
            if not filename.endswith(('.md', '.txt')):
                filename += '.md'
                
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return os.path.abspath(filename)
        
        except Exception as e:
            print(f"Error saving blog post: {e}")
            return ""

# Load environment variables (.env file)
load_dotenv()


async def run_blog_creator(keyword: str, context: str, model: str = None, 
                          output_file: str = None, max_tokens: int = 4000) -> str:
    """
    Run the blog creation process with the given parameters.
    
    Args:
        keyword: Main SEO keyword for the blog
        context: Contextual information about the blog's purpose
        model: Claude model to use (optional)
        output_file: File to save the blog post (optional)
        max_tokens: Maximum tokens for generation
        
    Returns:
        The generated blog post content
    """
    # Initialize the blog creator
    blog_creator = ClaudeBlogCreator()
    
    # Set custom model if provided
    if model:
        blog_creator.set_model(model)
    
    # Generate the blog post
    print(f"Generating blog post for keyword: '{keyword}'")
    print(f"Context: {context}")
    
    blog_post = await blog_creator.create_blog_post(
        keyword=keyword,
        context=context,
        max_tokens=max_tokens
    )
    
    # Save to file if filename is provided
    if output_file:
        saved_path = blog_creator.save_blog_post(blog_post, output_file)
        if saved_path:
            print(f"Blog post saved to: {saved_path}")
    
    return blog_post


async def main():
    """Main function with argument parsing for command-line usage"""
    parser = argparse.ArgumentParser(description="Generate blog posts using Claude AI")
    
    parser.add_argument("--keyword", "-k", type=str, 
                       help="Main SEO keyword for the blog post")
    parser.add_argument("--context", "-c", type=str, 
                       help="Context information for blog creation")
    parser.add_argument("--model", "-m", type=str, 
                       help="Claude model to use (default: claude-3-haiku-20240307)")
    parser.add_argument("--output", "-o", type=str, 
                       help="Output file name for the blog post")
    parser.add_argument("--max-tokens", type=int, default=4000,
                       help="Maximum tokens for response (default: 4000)")
    
    args = parser.parse_args()
    
    # Use default values if arguments are not provided
    keyword = args.keyword or "Ecology and Sustainable Development"
    context = args.context or "Write a social media post promoting our new eco-friendly water bottles to young adults interested in sustainability"
    output = args.output or f"blog_post_{keyword.replace(' ', '_').lower()}.md"
    
    # Run the blog creator
    blog_content = await run_blog_creator(
        keyword=keyword,
        context=context,
        model=args.model,
        output_file=output,
        max_tokens=args.max_tokens
    )
    
    # Display a preview of the generated content
    preview_length = min(300, len(blog_content))
    print("\n--- Blog Post Preview ---")
    print(f"{blog_content[:preview_length]}...")
    print(f"\nFull blog post available in {output}")


if __name__ == "__main__":
    asyncio.run(main())