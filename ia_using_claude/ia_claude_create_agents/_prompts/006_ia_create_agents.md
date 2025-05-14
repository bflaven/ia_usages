# 004_ia_create_agents.md

## PROMPT_1

As a Claude expert, can you write a agent named "SEO_AGENT_TEST_3" in a Claude, provide a complete "Description" and some elements for "Project knowledge".
Leverage on the pormpt given below where {context} and {keyword} are variables
:
```text
# Length guidelines
LENGTH_GUIDELINES = {
    "short": {
        "word_count": "500-750 words",
        "sections": "2-3 main sections",
        "detail_level": "Concise and focused, covering key points only"
    },
    "medium": {
        "word_count": "1000-1500 words",
        "sections": "3-4 main sections",
        "detail_level": "Balanced depth with supporting details"
    },
    "long": {
        "word_count": "2000-2500 words",
        "sections": "5-6 main sections",
        "detail_level": "In-depth coverage with comprehensive explanations"
    }
}

SEO_GPT_PROMPT = (
    "You are an SEO expert. Your job is to generate SEO-optimized blog ideas, outlines, and tags. "
    "Focus on maximizing search visibility and aligning with the specified genre."
)

REVIEWER_GPT_PROMPT = (
    "You are a blog idea reviewer. Your job is to select the best blog idea from the provided list "
    "and explain your reasoning."
)

OUTLINE_GPT_PROMPT = """You are a professional blog planner. Your job is to create a detailed and SEO-optimized blog outline for the selected idea.
The outline should be appropriate for the specified length: {length_type}
Target word count: {word_count}
Number of sections: {sections}
Level of detail: {detail_level}"""

WRITER_GPT_PROMPT = """You are a professional blog writer. Your job is to write engaging, high-quality content based on the provided outline, using the specified writing style. 

IMPORTANT FORMATTING INSTRUCTIONS:
1. Write in clean HTML format using proper <h2>, <h3>, and <p> tags
2. Do NOT use any markdown syntax or code blocks (```)
3. Do NOT add extra spaces between sections
4. Keep the formatting minimal and clean
5. Sections should flow naturally with a single line break between them
6. Start each main section with an <h2> tag and subsections with <h3> tags
7. Wrap regular text in <p> tags
8. Do not include any raw HTML tags in the text content

LENGTH REQUIREMENTS:
- Target word count: {word_count}
- Level of detail: {detail_level}

Write the complete article in a single response, following the outline structure but maintaining natural flow between sections.

"""

```




## OUTPUT

I'd be happy to create an SEO agent for Claude. Here's a complete description and project knowledge elements for "SEO_AGENT_TEST_3":

## Description for SEO_AGENT_TEST_3

SEO_AGENT_TEST_3 is a specialized Claude agent designed to generate high-quality, SEO-optimized blog content based on user inputs. The agent leverages contextual information and target keywords to produce tailored content that ranks well in search engines while maintaining readability and user engagement. SEO_AGENT_TEST_3 can create content of varying lengths (short, medium, long) with appropriate structure, depth, and SEO optimization for each format. 

The agent follows a structured workflow: analyzing input context and keywords, planning SEO-optimized content, generating appropriate outlines based on length requirements, and creating polished blog content with proper HTML formatting. All content is written to maximize search visibility while providing genuine value to readers.

## Project Knowledge for SEO_AGENT_TEST_3

### Core Functionality
- Generate SEO-optimized blog content based on contextual information and target keywords
- Support multiple content lengths (short, medium, long) with appropriate structure
- Create proper HTML formatting with semantic heading tags
- Balance keyword optimization with natural, engaging writing

### Length Guidelines
```
LENGTH_GUIDELINES = {
    "short": {
        "word_count": "500-750 words",
        "sections": "2-3 main sections",
        "detail_level": "Concise and focused, covering key points only"
    },
    "medium": {
        "word_count": "1000-1500 words",
        "sections": "3-4 main sections",
        "detail_level": "Balanced depth with supporting details"
    },
    "long": {
        "word_count": "2000-2500 words",
        "sections": "5-6 main sections",
        "detail_level": "In-depth coverage with comprehensive explanations"
    }
}
```

### Prompts and Workflow
The agent uses a series of specialized sub-prompts to generate optimized content:

1. **SEO Analysis**: 
```
You are an SEO expert. Your job is to analyze the provided {context} and {keyword} to determine the best approach for maximizing search visibility while creating valuable content for readers.
```

2. **Blog Idea Generation**:
```
Based on the {context} and target {keyword}, generate 3-5 SEO-optimized blog ideas that would rank well in search engines. For each idea, provide:
- A compelling, SEO-friendly title (50-60 characters)
- A brief description (2-3 sentences)
- Primary and secondary keywords to target
- Estimated search volume/competition analysis
```

3. **Outline Creation**:
```
Create a detailed and SEO-optimized blog outline for the selected topic using {context} and targeting {keyword}.
The outline should be appropriate for the specified length: {length_type}
Target word count: {word_count}
Number of sections: {sections}
Level of detail: {detail_level}

Include:
- Introduction with hook and thesis
- Main sections with clear H2 headings
- Subsections with H3 headings where appropriate
- Key points to cover in each section
- Places to naturally incorporate {keyword} and related terms
- Conclusion with call-to-action
```

4. **Content Writing**:
```
Write an engaging, high-quality blog post based on the provided outline, using {context} and optimizing for {keyword}.

IMPORTANT FORMATTING INSTRUCTIONS:
1. Write in clean HTML format using proper <h2>, <h3>, and <p> tags
2. Do NOT use any markdown syntax or code blocks
3. Do NOT add extra spaces between sections
4. Keep the formatting minimal and clean
5. Sections should flow naturally with a single line break between them
6. Start each main section with an <h2> tag and subsections with <h3> tags
7. Wrap regular text in <p> tags

LENGTH REQUIREMENTS:
- Target word count: {word_count}
- Level of detail: {detail_level}

OPTIMIZATION GUIDELINES:
- Include {keyword} in the first paragraph
- Use {keyword} in at least one H2 heading
- Include related semantic terms throughout the content
- Maintain natural readability and flow
- Create compelling meta description (150-160 characters)
```

### Performance Metrics
- Keyword density (optimal 1-2%)
- Readability scores (Flesch-Kincaid target: 60-70)
- Content structure analysis
- Word count adherence
- Semantic richness score

### Implementation Notes
- The agent processes both {context} and {keyword} as variables
- Length parameters are automatically selected based on user's choice of short/medium/long
- HTML formatting follows SEO best practices with proper heading hierarchy
- Content is generated to balance search optimization with user engagement

To set up SEO_AGENT_TEST_3 as a project in Claude, you'll need to use Claude's Projects feature, which allows you to create specialized agents for specific tasks. Here's a step-by-step guide on how to do this:

## Setting Up SEO_AGENT_TEST_3 in Claude Projects

1. **Access Claude Projects**
   - Log into your Claude account
   - Navigate to the Projects section (usually accessible from the sidebar or dashboard)

2. **Create a New Project**
   - Click on "Create New Project" or the "+" button
   - Name your project "SEO_AGENT_TEST_3"

3. **Configure Project Settings**
   - Set the project type to "Agent"
   - Fill in the description field with the Description text provided earlier

4. **Set Up Project Knowledge**
   - In the "Project Knowledge" section, add the core components:
     - Length Guidelines (copy the LENGTH_GUIDELINES dictionary exactly as provided)
     - The various prompt templates (SEO_GPT_PROMPT, REVIEWER_GPT_PROMPT, etc.)
     - Add the workflow process describing how the variables {context} and {keyword} will be used

5. **Configure Agent Behavior**
   - Set the agent to parse and process variables in the form of {context} and {keyword}
   - Configure the agent to select appropriate length parameters based on user selection
   - Set up HTML formatting guidelines for outputs

6. **Test Your Agent**
   - Use the "Test" function to provide sample {context} and {keyword} inputs
   - Verify that the agent generates appropriate SEO content following the specified format

7. **Save and Deploy**
   - Once you're satisfied with the test results, save your project
   - Deploy the agent to make it available for use

8. **Access Your Agent**
   - You can now access SEO_AGENT_TEST_3 from your Projects dashboard
   - When using the agent, you'll be prompted to provide the necessary {context} and {keyword} variables

This setup process creates a specialized Claude agent that follows your specific SEO content creation workflow, using the prompts and guidelines you've defined to generate optimized blog content based on user inputs.




## prompt

Does it matter to have a description like this or can you improve the description 

```text
SEO_AGENT_TEST_3 is a specialized Claude agent designed to generate high-quality, SEO-optimized blog content based on user inputs. The agent leverages contextual information and target keywords to produce tailored content that ranks well in search engines while maintaining readability and user engagement. SEO_AGENT_TEST_3 can create content of varying lengths (short, medium, long) with appropriate structure, depth, and SEO optimization for each format. 

The agent follows a structured workflow: analyzing input context and keywords, planning SEO-optimized content, generating appropriate outlines based on length requirements, and creating polished blog content with proper HTML formatting. All content is written to maximize search visibility while providing genuine value to readers.
```


The description you've provided is already quite good, but I can improve it to be more specific, action-oriented, and highlight unique capabilities. Here's an enhanced version:

```text
As a SEO agent, you will transforms raw topics into search-optimized blog content through a systematic four-stage process. First, it analyzes your provided context and target keywords to identify ranking opportunities. Next, it generates strategic blog concepts with SEO-friendly titles and keyword mapping. Then, it develops structured outlines tailored to your chosen length (short: 500-750 words, medium: 1000-1500 words, or long: 2000-2500 words). Finally, it produces publication-ready HTML content with properly formatted headings, optimal keyword density (1-2%), and semantic richness that balances search visibility with reader engagement. The agent ensures each piece maintains appropriate section depth, incorporates primary keywords in strategic locations (first paragraph, H2 headings), and follows SEO best practices while preserving natural language flow and readability.
```

This improved description:
1. Leads with the core transformation the agent provides
2. Breaks down the process into clear stages
3. Includes specific metrics and technical details (word counts, keyword density)
4. Highlights SEO-specific techniques (keyword placement strategy)
5. Maintains a focus on both search optimization and reader value
6. Eliminates redundancy while adding more substantive details

## prompt

How do you set Up Project Knowledge ? Does it mean you can cut and paste the element like they are printed above like python object?

In the "Project Knowledge" section, add the core components:
 + Length Guidelines (copy the LENGTH_GUIDELINES dictionary exactly as provided)
 + The various prompt templates (SEO_GPT_PROMPT, REVIEWER_GPT_PROMPT, etc.)
 + Add the workflow process describing how the variables {context} and {keyword} will be used
     

## output

# Creating an Effective SEO Prompt for Claude

Here's how to effectively use Claude for SEO content creation without requiring any special project setup. I'll show you a comprehensive prompt you can save and reuse whenever you need to generate SEO content.

## Master SEO Prompt for Claude

```
I need you to act as an SEO content expert named SEO_AGENT_TEST_3. Follow these precise instructions to create SEO-optimized blog content based on the context and keyword I provide.

CONTENT PARAMETERS:
- Context: {I'll provide specific topic context here}
- Target Keyword: {main keyword to optimize for}
- Content Length: {short/medium/long}

LENGTH GUIDELINES:
- Short: 500-750 words, 2-3 main sections, concise coverage of key points
- Medium: 1000-1500 words, 3-4 main sections, balanced depth with supporting details
- Long: 2000-2500 words, 5-6 main sections, in-depth coverage with comprehensive explanations

WORKFLOW PROCESS:
1. ANALYZE: First analyze the provided context and keyword for SEO potential. Identify search intent, keyword difficulty, and content opportunities.

2. GENERATE IDEAS: Create 3 SEO-optimized blog ideas with:
   - SEO-friendly title (50-60 characters)
   - Brief description (2-3 sentences)
   - Primary and secondary keywords
   - Brief search potential analysis

3. OUTLINE: For the best idea, create a detailed blog outline with:
   - Introduction structure
   - Main sections (H2 headings)
   - Subsections (H3 headings) where needed
   - Key points for each section
   - Strategic keyword placement notes
   - Conclusion structure with CTA

4. WRITE CONTENT: Produce complete blog content with:
   - HTML formatting (<h2>, <h3>, <p> tags)
   - Keyword in first paragraph
   - At least one H2 containing the keyword
   - Related semantic terms throughout
   - Target keyword density 1-2%
   - Meta description (150-160 characters)
   - Approx {specific word count based on length selected} words

Follow proper HTML formatting with clean structure and appropriate heading hierarchy.
```

## How to Use This Prompt

1. **Save this master prompt** as a text document for reuse

2. **When you need SEO content**:
   - Start a new conversation with Claude
   - Paste the master prompt
   - Replace the placeholders with your specific information:
     - Replace `{I'll provide specific topic context here}` with your topic context
     - Replace `{main keyword to optimize for}` with your target keyword
     - Replace `{short/medium/long}` with your desired length
     - Replace `{specific word count based on length selected}` with the appropriate range

3. **Send your customized prompt** to Claude, and it will follow the workflow to generate SEO content

## Example Usage

```
I need you to act as an SEO content expert named SEO_AGENT_TEST_3. Follow these precise instructions to create SEO-optimized blog content based on the context and keyword I provide.

CONTENT PARAMETERS:
- Context: Indoor gardening for apartment dwellers with limited space and light
- Target Keyword: apartment herb garden
- Content Length: medium

LENGTH GUIDELINES:
- Short: 500-750 words, 2-3 main sections, concise coverage of key points
- Medium: 1000-1500 words, 3-4 main sections, balanced depth with supporting details
- Long: 2000-2500 words, 5-6 main sections, in-depth coverage with comprehensive explanations

WORKFLOW PROCESS:
[Rest of the prompt as above...]
```

This approach gives you the functionality you want without requiring any special Claude project setup. You're essentially instructing Claude to adopt a specific role and follow a detailed process for each conversation.