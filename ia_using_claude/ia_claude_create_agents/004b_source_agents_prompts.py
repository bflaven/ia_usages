
# https://github.com/kitsharma/seo-workflow/blob/main/seo-agents.py
# https://github.com/kitsharma/seo-workflow/blob/main/claude_agent_framework.py

"""
Claude SEO Agents Implementation - Specialized agents for different SEO tasks

Path: /claude_seo_agents.py
Purpose: Defines several agent classes, each specializing in a specific SEO function:
         - KeywordResearchAgent: Discovers valuable keywords with intent understanding
         - ContentBriefAgent: Creates content briefs with strategic direction
         - ContentWriterAgent: Generates naturally flowing, SEO-optimized content
         - TechnicalSEOAgent: Identifies and explains technical improvements
         - ContentGapAnalysisAgent: Identifies content opportunities
         - SEOStrategyAgent: Develops comprehensive SEO strategies
"""

from claude_agent_framework import ClaudeAgent, create_system_prompt

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