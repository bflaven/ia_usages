"""
Claude SEO Agent Framework - Core implementation for SEO automation workflow

Path: /claude_agent_framework.py
Purpose: Provides the foundation for all specialized SEO agents, handling API communication 
         with Anthropic, conversation management, and utility functions.
"""

import os
import json
import datetime
import time
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEFAULT_MODEL = "claude-3-opus-20240229"  # Default to highest capability model

class ClaudeAgent:
    """Base class for all Claude-based SEO agents"""
    
    def __init__(self, name: str, system_prompt: str, model: Optional[str] = None):
        """Initialize a new agent
        
        Args:
            name: Unique identifier for the agent
            system_prompt: System prompt that defines the agent's behavior
            model: Claude model to use (defaults to claude-3-opus-20240229)
        """
        self.name = name
        self.system_prompt = system_prompt
        self.model = model or DEFAULT_MODEL
        self.conversation_history = []
        self.data_store = {}
        
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
    def call_claude(self, user_message: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """Make an API call to Claude
        
        Args:
            user_message: The message to send to Claude
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            The text response from Claude
        """
        # API endpoint for Claude
        api_url = "https://api.anthropic.com/v1/messages"
        
        # Build conversation history for context
        messages = []
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append(msg)
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        
        # Prepare request data
        request_data = {
            "model": self.model,
            "messages": messages,
            "system": self.system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Add the new user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = requests.post(api_url, headers=headers, json=request_data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            response_data = response.json()
            assistant_response = response_data["content"][0]["text"]
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
    
    def save_data(self, key: str, data: Any) -> None:
        """Save data to the agent's data store"""
        self.data_store[key] = data
        
    def get_data(self, key: str) -> Any:
        """Retrieve data from the agent's data store"""
        return self.data_store.get(key)
    
    def clear_conversation(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []


class SEOWorkflow:
    """Orchestrator for the entire SEO workflow"""
    
    def __init__(self):
        """Initialize a new workflow orchestrator"""
        self.agents = {}
        self.workflow_data = {}
        self.execution_log = []
        
    def register_agent(self, agent_name: str, agent_instance: ClaudeAgent) -> None:
        """Register a new agent with the workflow"""
        self.agents[agent_name] = agent_instance
        
    def execute_step(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step using the specified agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not registered")
            
        agent = self.agents[agent_name]
        
        # Format the input data as a structured prompt for the agent
        prompt = self._format_input_for_agent(agent_name, input_data)
        
        # Call the agent
        start_time = time.time()
        response = agent.call_claude(prompt)
        execution_time = time.time() - start_time
        
        # Parse the response into structured data
        output_data = self._parse_agent_response(agent_name, response)
        
        # Log the execution
        self.execution_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "agent": agent_name,
            "execution_time_seconds": execution_time,
            "input_data_keys": list(input_data.keys()),
            "output_data_keys": list(output_data.keys()),
        })
        
        return output_data
    
    def execute_workflow(self, initial_data: Dict[str, Any], workflow_steps: List[str]) -> Dict[str, Any]:
        """Execute the entire workflow with multiple steps"""
        current_data = initial_data.copy()
        
        for step in workflow_steps:
            self.workflow_data[f"input_{step}"] = current_data.copy()
            output_data = self.execute_step(step, current_data)
            current_data.update(output_data)
            self.workflow_data[f"output_{step}"] = output_data.copy()
            
        return current_data
    
    def _format_input_for_agent(self, agent_name: str, input_data: Dict[str, Any]) -> str:
        """Format input data into a prompt string for the specified agent"""
        formatted_input = f"Input data for {agent_name}:\n\n"
        for key, value in input_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                formatted_input += f"{key}: {json.dumps(value, indent=2)}\n\n"
            else:
                formatted_input += f"{key}: {value}\n\n"
        
        formatted_input += "\nPlease process this data according to your function and provide a structured response."
        return formatted_input
    
    def _parse_agent_response(self, agent_name: str, response: str) -> Dict[str, Any]:
        """Parse the agent's text response into structured data"""
        try:
            # Look for JSON-like blocks within the text - Claude is very good at providing 
            # well-structured JSON when asked
            response_lines = response.split('\n')
            json_block = []
            in_json_block = False
            
            for line in response_lines:
                if line.strip() == "```json" or line.strip() == "{":
                    in_json_block = True
                    if line.strip() == "{":
                        json_block.append(line)
                elif line.strip() == "```" and in_json_block:
                    in_json_block = False
                elif in_json_block:
                    json_block.append(line)
            
            if json_block:
                json_text = "\n".join(json_block)
                return json.loads(json_text)
            
            # Fallback: Try to find a JSON object anywhere in the text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
                
            # If no JSON found, create a simple key-value structure
            return {"response_text": response}
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw text
            return {"response_text": response}
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Generate a summary of the workflow execution"""
        total_execution_time = sum(log["execution_time_seconds"] for log in self.execution_log)
        
        return {
            "total_steps_executed": len(self.execution_log),
            "total_execution_time_seconds": total_execution_time,
            "average_step_time_seconds": total_execution_time / len(self.execution_log) if self.execution_log else 0,
            "execution_log": self.execution_log,
        }


# Helper function to create agent system prompts
def create_system_prompt(agent_type: str, agent_description: str, instructions: str) -> str:
    """Create a structured system prompt for a Claude agent"""
    return f"""You are a specialized SEO agent named "{agent_type}".

{agent_description}

INSTRUCTIONS:
{instructions}

IMPORTANT GUIDELINES:
1. Always analyze the input data thoroughly before providing recommendations.
2. Structure your responses in a clear, organized format.
3. When appropriate, return data in JSON format for easy processing.
4. Be specific and actionable in your recommendations.
5. Only include factual information and avoid speculation.
6. If you need more information to make a good recommendation, say so clearly.
7. Provide clear reasoning for all recommendations to aid user understanding.

RESPONSE FORMAT:
When providing structured data, use the following format:

```json
{{
  "analysis": "Brief summary of your analysis",
  "recommendations": ["Recommendation 1", "Recommendation 2", ...],
  "reasoning": "Explanation of your thought process and rationale",
  "data": {{
    // Any structured data you want to return
  }}
}}
```
"""
