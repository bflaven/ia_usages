#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name mcp_server_demo python=3.9.13
conda info --envs
source activate mcp_server_demo
conda deactivate

# BURN AFTER READING
source activate mcp_server_demo

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n mcp_server_demo


# install packages with pip
python -m pip install requests python-dotenv

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/000_ia_generate_slides/ia_create_agents


# launch the file
python 012_ia_using_claude_agents_sdk.py




"""
import os
import json
import time
import datetime
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from anthropic import Anthropic  # Using the official Anthropic Python library

# Load environment variables
load_dotenv()

# Constants
DEFAULT_MODEL = "claude-3-haiku-20240307"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Print API key availability (not the actual key)
if CLAUDE_API_KEY:
    print(f"API key loaded successfully: {CLAUDE_API_KEY[:4]}...{CLAUDE_API_KEY[-4:]}")
else:
    print("WARNING: CLAUDE_API_KEY not found in environment variables!")
    CLAUDE_API_KEY = input("Please enter your Claude API key: ")

# Initialize Anthropic client
client = Anthropic(api_key=CLAUDE_API_KEY)

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

class ClaudeAgent:
    """Base class for all Claude-based SEO agents"""
    
    def __init__(self, name: str, system_prompt: str, model: Optional[str] = None):
        """Initialize a new agent
        
        Args:
            name: Unique identifier for the agent
            system_prompt: System prompt that defines the agent's behavior
            model: Claude model to use (defaults to claude-3-haiku-20240307)
        """
        self.name = name
        self.system_prompt = system_prompt
        self.model = model or DEFAULT_MODEL
        self.conversation_history = []
        self.data_store = {}
        
        if not CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY environment variable not set")
        
    def call_claude(self, user_message: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """Make an API call to Claude using the Anthropic SDK
        
        Args:
            user_message: The message to send to Claude
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            The text response from Claude
        """
        # Build conversation history for context
        messages = []
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append(msg)
        
        # Add the new user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Using the Anthropic SDK to make the API call
            response = client.messages.create(
                model=self.model,
                messages=messages,
                system=self.system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract the response text
            assistant_response = response.content[0].text
            
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

class KeywordResearchAgent(ClaudeAgent):
    """Agent specialized in discovering valuable keywords for SEO campaigns"""
    
    def __init__(self, model=None):
        system_prompt = create_system_prompt(
            "Keyword Research Agent",
            "You specialize in discovering valuable keywords for SEO campaigns based on user input, industry trends, search behavior, and underlying search intent.",
            """
            1. Analyze the provided target topic, industry, website, or business objective
            2. Identify primary and secondary keywords that would be valuable targets
            3. Evaluate search volume, competition, difficulty, and user intent for each keyword
            4. Group keywords into semantic clusters and topic clusters
            5. Prioritize keywords based on potential ROI, relevance, intent match, and conversion potential
            6. Consider the full search journey across the marketing funnel
            7. Provide clear reasoning behind keyword selections and groupings
            8. Return a structured analysis with keyword recommendations
            """
        )
        super().__init__("keyword_research", system_prompt, model)


class ContentBriefAgent(ClaudeAgent):
    """Agent specialized in creating comprehensive content briefs"""
    
    def __init__(self, model=None):
        system_prompt = create_system_prompt(
            "Content Brief Agent",
            "You specialize in creating comprehensive content briefs for SEO-optimized articles that address user intent and exceed search engines' expectations.",
            """
            1. Analyze the target keyword and thoroughly understand the underlying search intent
            2. Research top-ranking content for the keyword to identify patterns and gaps
            3. Identify key topics, questions, subtopics, and semantic entities to cover
            4. Suggest compelling title options, meta descriptions, and logical heading structure
            5. Recommend content length, format, media inclusions, and internal linking strategy
            6. Outline specific sections that should be included with rationale for each
            7. Consider E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) factors
            8. Explain how the content should address different phases of the user journey
            9. Return a detailed, structured content brief for writers with clear strategic direction
            """
        )
        super().__init__("content_brief", system_prompt, model)


class ContentWriterAgent(ClaudeAgent):
    """Agent specialized in writing high-quality, SEO-optimized content"""
    
    def __init__(self, model=None):
        system_prompt = create_system_prompt(
            "SEO Content Writer Agent",
            "You specialize in writing high-quality, SEO-optimized content that reads naturally and engages human readers while satisfying search intent.",
            """
            1. Analyze the provided content brief thoroughly
            2. Create engaging, informative content that matches search intent and sounds completely natural
            3. Properly incorporate primary and secondary keywords in a way that flows naturally
            4. Structure content with appropriate headings and subheadings to improve readability
            5. Include relevant examples, data points, stories, and supportive information
            6. Write with a consistent, appropriate tone that matches the target audience
            7. Incorporate elements that enhance E-E-A-T signals throughout the content
            8. Add appropriate transitional elements between sections for improved flow
            9. Return a complete, publishing-ready article that requires minimal editing
            """
        )
        super().__init__("content_writer", system_prompt, model)


class TechnicalSEOAgent(ClaudeAgent):
    """Agent specialized in identifying technical SEO issues"""
    
    def __init__(self, model=None):
        system_prompt = create_system_prompt(
            "Technical SEO Audit Agent",
            "You specialize in identifying technical SEO issues and providing recommendations for fixes with clear explanations of impact and importance.",
            """
            1. Analyze the provided technical data for a website
            2. Identify critical technical SEO issues and prioritize them by impact
            3. Evaluate page speed, mobile-friendliness, and core web vitals
            4. Check for crawlability and indexation problems
            5. Assess structured data implementation and opportunities
            6. Evaluate site architecture and internal linking structure
            7. Examine URL structure, redirects, and status code issues
            8. Analyze international SEO considerations if applicable
            9. Provide detailed explanations of why each issue matters
            10. Include specific implementation guidance for fixing issues
            11. Return a structured analysis with technical recommendations and prioritization
            """
        )
        super().__init__("technical_seo", system_prompt, model)


class ContentGapAnalysisAgent(ClaudeAgent):
    """Agent specialized in identifying content gaps and opportunities"""
    
    def __init__(self, model=None):
        system_prompt = create_system_prompt(
            "Content Gap Analysis Agent",
            "You specialize in identifying content gaps and opportunities by analyzing competitor content and user needs.",
            """
            1. Analyze the current content inventory of the website
            2. Research competitor content for the target keywords and topics
            3. Identify topics, questions, and content types that competitors cover but the client doesn't
            4. Discover unaddressed user needs and questions related to the topic
            5. Evaluate content depth, breadth, and comprehensiveness compared to top-ranking pages
            6. Recommend specific content pieces to create with clear justification
            7. Suggest improvements to existing content based on competitive analysis
            8. Prioritize content opportunities based on potential impact and effort
            9. Return a structured content gap analysis with actionable recommendations
            """
        )
        super().__init__("content_gap_analysis", system_prompt, model)


class SEOStrategyAgent(ClaudeAgent):
    """Agent specialized in developing comprehensive SEO strategies"""
    
    def __init__(self, model=None):
        system_prompt = create_system_prompt(
            "SEO Strategy Agent",
            "You specialize in developing comprehensive SEO strategies tailored to business goals and market conditions.",
            """
            1. Analyze the business goals, target audience, and competitive landscape
            2. Evaluate current SEO performance and identify strengths and weaknesses
            3. Develop a comprehensive SEO strategy aligned with business objectives
            4. Create a prioritized roadmap of tactical SEO initiatives
            5. Recommend specific KPIs and success metrics for the strategy
            6. Consider resources required and potential ROI for recommendations
            7. Include content, technical, and off-page strategic elements
            8. Account for industry trends and search engine algorithm considerations
            9. Return a structured SEO strategy with clear rationale and implementation guidance
            """
        )
        super().__init__("seo_strategy", system_prompt, model)


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
            print(f"\nExecuting step: {step}")
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


# Example usage
if __name__ == "__main__":
    try:
        # Test the API connection first
        print("Testing Claude API connection...")
        test_message = "Hello Claude! This is a test message to verify API connectivity."
        test_response = client.messages.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": test_message}],
            max_tokens=100
        )
        print("✅ API connection successful!")
        print(f"Claude response: {test_response.content[0].text[:100]}...")
        
        # Subject for research - you can change this to any topic you want to research
        subject = "the pope Francis death"
        
        print(f"\nStarting SEO workflow for subject: {subject}")
        
        # Initialize all agents
        keyword_agent = KeywordResearchAgent()
        content_brief_agent = ContentBriefAgent()
        content_writer_agent = ContentWriterAgent()
        technical_seo_agent = TechnicalSEOAgent()
        content_gap_agent = ContentGapAnalysisAgent()
        seo_strategy_agent = SEOStrategyAgent()
        
        # Initialize workflow
        workflow = SEOWorkflow()
        
        # Register all agents with the workflow
        workflow.register_agent("keyword_research", keyword_agent)
        workflow.register_agent("content_brief", content_brief_agent)
        workflow.register_agent("content_writer", content_writer_agent)
        workflow.register_agent("technical_seo", technical_seo_agent)
        workflow.register_agent("content_gap", content_gap_agent)
        workflow.register_agent("seo_strategy", seo_strategy_agent)
        
        # Define initial data
        initial_data = {
            "subject": subject,
            "target_audience": "General public, Catholics, religious news followers",
            "content_type": "News article and explainer",
            "business_objective": "Create authoritative content on recent events",
            "website_data": {
                "domain": "example-news.com",
                "current_ranking": "Page 2 for related terms",
                "competitors": ["cnn.com", "bbc.com", "nytimes.com", "reuters.com"]
            }
        }
        
        # Define full workflow steps - uncomment the steps you want to execute
        # For a quick test, you might want to use fewer steps
        workflow_steps = [
            "keyword_research",          # Step 1: Research keywords
            "content_gap",               # Step 2: Analyze content gaps
            "content_brief",             # Step 3: Create content brief
            "content_writer",            # Step 4: Write the content
            # "technical_seo",           # Optional: Technical SEO audit
            # "seo_strategy"             # Optional: Comprehensive strategy
        ]
        
        # For a quicker test with just basic workflow:
        # workflow_steps = ["keyword_research", "content_brief"]
        
        # Execute the workflow
        print(f"\nExecuting workflow with steps: {', '.join(workflow_steps)}")
        result = workflow.execute_workflow(initial_data, workflow_steps)
        
        # Print summary
        summary = workflow.get_execution_summary()
        print(f"\nWorkflow completed in {summary['total_execution_time_seconds']:.2f} seconds")
        print(f"Steps executed: {summary['total_steps_executed']}")
        
        # Print final results based on which steps were executed
        if "keyword_research" in workflow_steps:
            print("\n--- Keyword Research Results ---")
            if "recommendations" in result:
                for i, rec in enumerate(result["recommendations"][:5], 1):  # Show top 5
                    print(f"{i}. {rec}")
            else:
                print("No structured recommendations found in keyword research")
        
        if "content_brief" in workflow_steps:
            print("\n--- Content Brief Summary ---")
            if "analysis" in result:
                print(result["analysis"])
            else:
                print("No structured analysis found in content brief")
        
        if "content_writer" in workflow_steps:
            print("\n--- Content Preview (first 500 chars) ---")
            if "response_text" in result:
                print(result["response_text"][:500] + "...")
            else:
                print("No content found in writer output")
        
        print("\nWorkflow execution complete!")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTROUBLESHOOTING TIPS:")
        print("1. Make sure you have installed the Anthropic Python SDK: pip install anthropic")
        print("2. Check that your API key is valid and active")
        print("3. Ensure you have access to the Claude model being used (currently using claude-3-haiku-20240307)")
        print("4. If using a .env file, ensure it's formatted correctly: CLAUDE_API_KEY=your_key_here (no quotes)")


        


