
## PROMPT_1
As a python expert, can you write a script name "server.py" containing an SEO expert with a prompt that enable to use Claude desktop with the help of MCP and then output the result into a local file in directory named "output_filesystem"? Can you write the different scripts required.

**server.py**
```python
from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server named "SEO_Agent"
mcp = FastMCP("SEO_Agent")
```

**seo agent**
```python
# Construct the system prompt with MCP instructions
    system_prompt = """
    As a SEO expert. Analyze the provided content 
    and give detailed SEO recommendations. Be specific about:
    
    1. Keyword optimization opportunities
    2. Content structure improvements
    3. Meta tag recommendations
    4. Internal linking suggestions
    5. Technical SEO considerations
    
    Format your response in clear sections with actionable insights.
    """
```

## OUTPUT_1


I'd be happy to help you create a Python script that sets up an SEO expert agent using Claude via MCP (Machine Conversation Protocol), which will output results to a local filesystem. Let me write the necessary scripts for you.

I've created the necessary scripts for an SEO expert agent that leverages Claude via MCP (Machine Conversation Protocol) and saves results to a local filesystem. Here's what each file does:

1. **server.py**: The main server script that:
   - Sets up a FastMCP server named "SEO_Agent"
   - Creates a Claude-powered SEO expert agent with a specialized prompt
   - Includes a custom tool to save analysis to files
   - Defines input and output handlers to process requests and save responses

2. **client.py**: A client script that:
   - Sends content to the SEO agent for analysis
   - Can read content from files or direct text input
   - Displays the results and shows where they're saved

3. **requirements.txt**: Lists all required Python packages

4. **README.md**: Instructions for setup and usage

To use this system:

1. Install the requirements: `pip install -r requirements.txt`
2. Set your Anthropic API key as an environment variable
3. Start the server: `python server.py`
4. Use the client to send content: `python client.py your-file.html` or `python client.py --text "Your content here"`

The SEO agent will analyze the content and provide recommendations in five key areas:
- Keyword optimization
- Content structure
- Meta tag recommendations
- Internal linking suggestions
- Technical SEO considerations

All analysis results will be saved to the "output_filesystem" directory with timestamped filenames.

Would you like me to explain any specific part of the implementation in more detail?


```python
#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP
from mcp.server.handlers import InputHandler, OutputHandler
from mcp.agents.claude import ClaudeAgent
from mcp.tools import Tool
import os
import time
import json
from datetime import datetime

# Create output directory if it doesn't exist
output_dir = "output_filesystem"
os.makedirs(output_dir, exist_ok=True)

# Define the SEO Expert agent
class SEOExpert(ClaudeAgent):
    def __init__(self):
        # System prompt for the SEO agent
        system_prompt = """
        As a SEO expert, analyze the provided content 
        and give detailed SEO recommendations. Be specific about:
        
        1. Keyword optimization opportunities
        2. Content structure improvements
        3. Meta tag recommendations
        4. Internal linking suggestions
        5. Technical SEO considerations
        
        Format your response in clear sections with actionable insights.
        """
        
        # Initialize the ClaudeAgent with our system prompt
        super().__init__(
            system=system_prompt,
            model="claude-3-7-sonnet-20250219",  # Using Claude 3.7 Sonnet
        )

# Save output to filesystem tool
class SaveToFileSystem(Tool):
    name = "save_to_filesystem"
    description = "Saves the SEO analysis to a file in the output_filesystem directory"
    
    def __init__(self):
        super().__init__()
    
    async def __call__(self, content):
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/seo_analysis_{timestamp}.txt"
        
        # Write content to file
        with open(filename, "w") as f:
            f.write(content)
        
        return f"SEO analysis saved to {filename}"

# Input handler that processes user content for SEO analysis
class SEOInputHandler(InputHandler):
    async def __call__(self, message):
        if message.get("content"):
            # Log the incoming request
            print(f"Received content for SEO analysis: {message['content'][:50]}...")
            
            # Forward the message to the agent
            return message
        else:
            return {"content": "Please provide content for SEO analysis."}

# Output handler that saves responses to filesystem
class SEOOutputHandler(OutputHandler):
    async def __call__(self, message):
        # Get the content from the message
        content = message.get("content", "")
        
        # Save to filesystem
        save_tool = SaveToFileSystem()
        file_path = await save_tool(content)
        
        # Add file path info to the message
        message["file_info"] = file_path
        
        return message

# Create an MCP server named "SEO_Agent"
mcp = FastMCP("SEO_Agent")

# Register the agent and handlers
seo_expert = SEOExpert()
mcp.add_agent(seo_expert)
mcp.add_input_handler(SEOInputHandler())
mcp.add_output_handler(SEOOutputHandler())

if __name__ == "__main__":
    print("Starting SEO Agent server...")
    print(f"Results will be saved to the '{output_dir}' directory")
    mcp.run(host="0.0.0.0", port=8000)
```