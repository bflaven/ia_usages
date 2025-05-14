# 004_ia_create_agents.md

## PROMPT_1

As a python expert, can you explain how to use a Claude agent named "001_seo_agent_test". This agent is an SEO agent. How can I call this agent "001_seo_agent_test" into the Claude desktop with the help of MCP and then output the result into a local file in directory named "output_filesystem"? Can you write the different scripts required.




## OUTPUT

I'll explain how to use a Claude agent named "001_seo_agent_test" for SEO tasks using MCP (Model Control Protocol) and save the output to your local file system.

To interact with a Claude agent from Python, you'll need to use the Anthropic Python SDK and set up the necessary scripts for calling the agent and handling its responses.

Here's a complete implementation:

```python
import os
import json
import anthropic
from datetime import datetime

def call_seo_agent(prompt, output_dir="output_filesystem"):
    """
    Call the SEO agent and save its response to a file.
    
    Args:
        prompt (str): The prompt to send to the SEO agent
        output_dir (str): Directory to save the output files
    
    Returns:
        str: Path to the saved output file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic(
        # Get API key from environment variable
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    # Construct the system prompt with MCP instructions
    system_prompt = """
    You are agent 001_seo_agent_test, an SEO expert. Analyze the provided content 
    and give detailed SEO recommendations. Be specific about:
    
    1. Keyword optimization opportunities
    2. Content structure improvements
    3. Meta tag recommendations
    4. Internal linking suggestions
    5. Technical SEO considerations
    
    Format your response in clear sections with actionable insights.
    """
    
    try:
        # Call the Claude API with MCP parameters
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",  # Using Claude 3.7 Sonnet
            system=system_prompt,
            max_tokens=4000,
            temperature=0.2,  # Lower temperature for more focused SEO analysis
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response content
        response = message.content[0].text
        
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"seo_analysis_{timestamp}.txt"
        file_path = os.path.join(output_dir, filename)
        
        # Save the response to a file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response)
        
        print(f"SEO analysis saved to {file_path}")
        return file_path
    
    except Exception as e:
        error_file = os.path.join(output_dir, "error_log.txt")
        with open(error_file, "a", encoding="utf-8") as f:
            f.write(f"\n{datetime.now()}: Error - {str(e)}")
        print(f"Error: {str(e)}")
        return None

def main():
    """
    Main function to run the SEO agent.
    """
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set your API key using: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    print("SEO Agent 001_seo_agent_test")
    print("===========================\n")
    
    # Get input from user
    print("Please enter the content you want to analyze for SEO (type 'exit' when done):")
    lines = []
    while True:
        line = input()
        if line.lower() == 'exit':
            break
        lines.append(line)
    
    content = "\n".join(lines)
    
    if not content.strip():
        print("No content provided. Exiting...")
        return
    
    # Call the SEO agent
    output_path = call_seo_agent(content)
    
    if output_path:
        print(f"\nAnalysis complete! Output saved to: {output_path}")
        
        # Ask if user wants to view the results
        view_results = input("\nWould you like to view the results now? (y/n): ")
        if view_results.lower() == 'y':
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    print("\n" + "="*50 + "\n")
                    print(f.read())
                    print("\n" + "="*50)
            except Exception as e:
                print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
```

To use this script:

1. Save it as `seo_agent_caller.py`
2. Set your Anthropic API key as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```
3. Run the script:
   ```bash
   python seo_agent_caller.py
   ```
4. Enter the content you want to analyze
5. Type 'exit' when you're done entering content
6. The script will call the SEO agent and save the output to a file in the `output_filesystem` directory

If you want to use this in a more automated way, you could create a command-line script for batch processing:

```python
import argparse
import os
from seo_agent_caller import call_seo_agent  # Import from the previous file

def process_file(file_path, output_dir):
    """Process a file with the SEO agent"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.strip():
            output_path = call_seo_agent(content, output_dir)
            return output_path
        else:
            print(f"Warning: File {file_path} is empty")
            return None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Run SEO analysis on content files')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('--output-dir', default='output_filesystem', help='Directory to save output files')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input path {args.input} does not exist")
        return
    
    if os.path.isfile(args.input):
        # Process a single file
        output_path = process_file(args.input, args.output_dir)
        if output_path:
            print(f"Analysis saved to: {output_path}")
    elif os.path.isdir(args.input):
        # Process all text files in the directory
        for filename in os.listdir(args.input):
            if filename.endswith('.txt') or filename.endswith('.md') or filename.endswith('.html'):
                file_path = os.path.join(args.input, filename)
                print(f"Processing {file_path}...")
                output_path = process_file(file_path, args.output_dir)
                if output_path:
                    print(f"Analysis saved to: {output_path}\n")

if __name__ == "__main__":
    main()
```

Save this script as `batch_seo_processor.py` and use it like this:

```bash
# Process a single file
python batch_seo_processor.py path/to/content.txt

# Process all text files in a directory
python batch_seo_processor.py path/to/content/directory

# Specify a custom output directory
python batch_seo_processor.py path/to/content.txt --output-dir my_seo_results
```

These scripts provide a complete solution for:
1. Calling the Claude SEO agent with appropriate MCP (system prompt) instructions
2. Saving the output to files in your specified directory
3. Processing either individual files or batches of files
4. Handling errors and edge cases

Remember to install the Anthropic Python SDK first:
```bash
pip install anthropic
```







