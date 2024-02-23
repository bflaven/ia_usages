# usecase_2_text_classification

**The actual system which relies on Mistral via Ollama (prompt) and will generate a CSV via pandas to retrieve each post tagged with one of the FRANCE24 categories.**

With the help of this recategorization device, it is a POC in particular, it is free and secure since Mistral has replaced ChatGPT.


The following columns for the USECASE_2 CSV are:  

-- **text:** the original message that comes from your csv. Text in FR.

-- **category_predicted:** the category in English guessed by mistral based on my proposal in the prompt

-- **category_decision:** the comment in English of the mistral decision that I included in the prompt


- **Objective:** Posts Categorization to compare with human post categorization. The same categorization that is used to track posts consumed on the production environment.
- **Source:** See ia_llms_usecases/usecase_2_text_classification/data_source
- **Abstract:** usecase_2 posts categorization (usecase_2_text_classification)


