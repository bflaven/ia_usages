# Prompt Engineering Course

**1. PROMPTINGGUIDE.AI**
- Summary of the guide at https://www.promptingguide.ai/

**2. GOOGLE.COM**
- Summary of the guide at https://developers.google.com/machine-learning/resources

**3. LEARNPROMPTING.ORG**
- Summary of the guide at 
https://learnprompting.org/docs/intro


## 1. PROMPTINGGUIDE.AI

## Prompt example
Prompt:
Complete the sentence: 
The sky is


Output:
filled with sparkling stars.

When prompting like the above, it's also referred to as zero-shot prompting, i.e., you are directly prompting the model for a response without any examples

## The Instruction
You can design effective prompts for various simple tasks by using commands to instruct the model what you want to achieve, such as "Write", "Classify", "Summarize", "Translate", "Order", etc.

```bash
### Instruction
Translate the text below to Spanish:
Text: "hello!"
```

Extract the name of places in the following text. 
Desired format:
Place: <comma_separated_list_of_company_names>
Input: "Although these developments are encouraging to researchers, much is still a mystery. “We often have a black box between the brain and the effect we see in the periphery,” says Henrique Veiga-Fernandes, a neuroimmunologist at the Champalimaud Centre for the Unknown in Lisbon. “If we want to use it in the therapeutic context, we actually need to understand the mechanism.""


## Prompting Techniques

### 1. Zero-shot Prompting or Direct prompting (Zero-shot)

Direct prompting (also known as Zero-shot) is the simplest type of prompt. It provides no examples to the model, just the instruction. You can also phrase the instruction as a question (model_1), or give the model a "role," as seen in the second example below (model_2).

One-shot prompting shows the model one clear, descriptive example of what you'd like it to imitate.


```bash
# model_1
Prompt: Can you give me a list of ideas for blog posts for tourists visiting
New York City for the first time?



```

```bash
# model_2
Prompt: You are a mighty and powerful prompt-generating robot. You need to
understand my goals and objectives and then design a prompt. The prompt should
include all the relevant information context and data that was provided to you.
You must continue asking questions until you are confident that you can produce
the best prompt for the best outcome. Your final prompt must be optimized for
chat interactions. Start by asking me to describe my goal, then continue with
follow-up questions to design the best prompt.
```



Source: https://developers.google.com/machine-learning/resources/prompt-eng


### 2. Few-shot Prompting

See Prompting with examples (One-, few-, and multi-shot)

```bash
# model_2
Prompt: You are a mighty and powerful prompt-generating robot. You need to
understand my goals and objectives and then design a prompt. The prompt should
include all the relevant information context and data that was provided to you.
You must continue asking questions until you are confident that you can produce
the best prompt for the best outcome. Your final prompt must be optimized for
chat interactions. Start by asking me to describe my goal, then continue with
follow-up questions to design the best prompt.
```


### 3. Chain-of-Thought Prompting

Chain-of-Thought (CoT) prompting enables complex reasoning capabilities through intermediate reasoning steps.

Zero-shot COT Prompting
This is "Let's think step by step" approach to the original prompt.

Automatic Chain-of-Thought (Auto-CoT)
Auto-CoT: Automatic Chain of Thought Prompting in Large Language Models (ICLR 2023)
https://github.com/amazon-science/auto-cot


### 4. Self-Consistency

The idea is to sample multiple, diverse reasoning paths through few-shot CoT, and use the generations to select the most consistent answer. 



```bash
# Prompt:
When I was 6 my sister was half my age. Now
I'm 70 how old is my sister?

# Caution the result is wrong!
# Output:
35

```

```bash
# Prompt:
Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done,
there will be 21 trees. How many trees did the grove workers plant today?
# Output:
A: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted.
So, they must have planted 21 - 15 = 6 trees. The answer is 6.

# Prompt:
Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
# Output:
A: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.

# Prompt:
Q: When I was 6 my sister was half my age. Now I’m 70 how old is my sister?
# Output:
A:
```


Computing for the final answer involves a few steps but for the sake of simplicity, we can see that there is already a majority answer emerging so that would essentially become the final answer.

### 5. Generate Knowledge Prompting

The idea behind the generated knowledge approach is to ask the LLM to generate potentially useful information about a given question/prompt before generating a final response.

For example, say you want to write a small blog post about some animal, like Spirit bears. Before asking the LLM to write the blog post, you can ask it to generate some facts about Spirit bears. This will help the LLM write a more informative blog post. There are two simple ways of going about this.

```bash
# Prompt:
Generate 4 facts about the Kermode bear, then use these facts to write a short blog post using the information:
The Kermode bear, also known as the spirit bear, is a rare subspecies of the American black bear that is found in the coastal regions of British Columbia, Canada. 

# Output:
1. The Kermode bear is a unique subspecies of the American black bear, with approximately 10% of the population having white fur. 

2. The Kermode bear is a symbol of the First Nations people of British Columbia, and is seen as a spirit animal. 

3. The Kermode bear is an important part of the ecosystem, helping to disperse seeds and maintain the balance of the forest. 

4. The Kermode bear is a protected species, and its population is monitored closely by the provincial government.

The Kermode bear is a unique and special animal that is found in the coastal regions of British Columbia, Canada. Approximately 10% of the population of this subspecies of the American black bear have white fur, making them a rare sight. The Kermode bear is a symbol of the First Nations people of British Columbia, and is seen as a spirit animal. It is an important part of the ecosystem, helping to disperse seeds and maintain the balance of the forest. The Kermode bear is a protected species, and its population is monitored closely by the provincial government. It is a beautiful and majestic animal, and it is important that we do our part to protect and conserve this species.
```


### 6. Tree of Thoughts

Tree-of-Thought (ToT) Prompting, a fresh technique borrowing ideas from the Tree-of-Thoughts framework, broadens and enhances the well-established Chain-of-Thought prompting concept, thereby enabling Large Language Models, like ChatGPT, to exhibit superior reasoning abilities. This Tree-of-Thought Prompting technique permits Large Language Models to rectify their errors autonomously while progressively accumulating knowledge.

In one example, a ToT prompt improves ChatGPT 3.5's reasoning ability to answer a question that could previously only be answered by ChatGPT 4.

The existing papers discussing the Tree-of-Thought framework appear to be premised on making multiple calls to an LLM, typically via Python. One of the main advantages of Chain-of-Thought reasoning is that it can be achieved with ChatGPT in a single sentence prompt.

**This led me to ponder: could we improve upon the results of CoT by utilizing a ToT-style prompt?**

```bash
# Prompt:
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking,
then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.
The question is...
```

```bash
# Prompt:
Bob is in the living room.
He walks to the kitchen, carrying a cup.
He puts a ball in the cup and carries the cup to the bedroom.
He turns the cup upside down, then walks to the garden.
He puts the cup down in the garden, then walks to the garage.
Where is the ball?


```


### 7. Retrieval Augmented Generation (RAG)

General-purpose language models can be fine-tuned to achieve several common tasks such as sentiment analysis and named entity recognition. These tasks generally don't require additional background knowledge.

For more complex and knowledge-intensive tasks, it's possible to build a language model-based system that accesses external knowledge sources to complete tasks. This enables more factual consistency, improves reliability of the generated responses, and helps to mitigate the problem of "hallucination".



### 8. Automatic Reasoning and Tool-use

### 9. Automatic Prompt Engineer

### 10. Active-Prompt

### 11. Directional Stimulus Prompting

### 12. ReAct

### 13. Multimodal CoT

### 14. Graph Prompting

## 2. GOOGLE

- <a href="https://developers.google.com/machine-learning/resources">Home</a>

- <a href="https://developers.google.com/machine-learning/resources/intro-llms">Intro to LLMs</a>

- <a href="https://developers.google.com/machine-learning/resources/ml-ai-basics">ML &amp; AI Basics</a>

- <a href="https://developers.google.com/machine-learning/resources/intro-responsible-ai">Intro to Responsible AI</a>

- <a href="https://developers.google.com/machine-learning/resources/safety-gen-ai">Safety &amp; Fairness for Generative Models</a>

- <a href="https://developers.google.com/machine-learning/resources/prompt-eng">Prompt Engineering</a>

- <a href="https://developers.google.com/machine-learning/resources/adv-testing">Adversarial Testing</a>

- <a href="https://developers.google.com/machine-learning/resources/saif">Secure AI Framework</a>





## 4. RESSOURCES

**Other**

ChatGPT Prompt Engineering for Developers
https://www.datacamp.com/courses/chatgpt-prompt-engineering-for-developers

The ChatGPT Prompt Book - LifeArchitect.ai - Rev 6

https://docs.google.com/presentation/d/17b_ocq-GL5lhV_bYSShzUgxL02mtWDoiw9xEroJ5m3Q/edit#slide=id.g1b8e0b333f6_0_257

Prompt-engineering tag on GitHub

https://github.com/topics/prompt-engineering

Use cases from langchain.com

https://python.langchain.com/docs/use_cases

- https://arxiv.org/pdf/2312.16171v1.pdf
- http://pretrain.nlpedia.ai/
- https://github.com/openai/openai-cookbook
- https://learnprompting.org/docs/intro

