
Test made on Version is 1.23.0 fine
```text
Android, apache, Alain Devalpo
```


## PROMPT_2

I am not ok with the evolutions in the plugin `breadcrumb-migration` Version v1.21.0 but I want a better UX. 

1. In the tab `Proposals`, I want to see the result in `bm-card__body` with a set of `<div class="bm-card bm-state--[status]"></div>` in order to have a list with detailed status for each tag searched. Remember what I say on the previous "I want to be able to search with the help of textarea bm-bulk-keywords because it will enable me to bulk search and have a list with detailed status for each tag searched. You can do it above bm-filter-sections and create a new section and give a title. Maybe this search can be driven as a form by the 2 buttons "Reset" and "Filter" already existing. Think simple in terms of UX."

- example of tag searched list
```text
agentic browsers, Atlas, Comet, dbt, DuckDB, GDPR, Google Chrome, innovation theater, late-stage capitalism, natural search, OpenAI, organizational pathologies, personal data, privacy, surveillance
```

2. I made a mistake, I was talking about the tab `Bulk Description`. So, when I click on the checkbox of each tag/row, I want tp have a dynamic list of the tags selected like in the tab `Bulk Assign` inside the textarea named `bm-check-selected-keywords` e.g "Selected keywords — comma-separated list of checked keywords, copy & paste ready" because it will enable me to bulk check the status for each tag.
Put this new div on top only above `widefat striped bm-bulk-desc-table` and under `bm-bulk-desc-filters`


- example of tag searched list
```text
agentic browsers, Atlas, Comet, dbt
```

3. CAUTION: Use as much as possible native look and feel from WP, avoid floating, ugly that deserves the UX and the intuitive understanding of a beginner user.

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.







## PROMPT_1


I am fine with the evolutions in the plugin `breadcrumb-migration` Version v1.21.0 but I want a better UX. 

1. In the tab `Proposals`, I want to be able to search with the help of textarea bm-bulk-keywords because it will enable me to bulk search and have a list with detailed status for each tag searched. You can do it above bm-filter-sections and create a new section and give a title. Maybe this search can be driven as a form by the 2 buttons "Reset" and "Filter" already existing. Think simple in terms of UX.

- example of tag searched list
```text
agentic browsers, Atlas, Comet, dbt, DuckDB, GDPR, Google Chrome, innovation theater, late-stage capitalism, natural search, OpenAI, organizational pathologies, personal data, privacy, surveillance
```

2. In the tab `Bulk Description`, when I click on the checkbox of each tag/row, I want tp have a dynamic list of the tags selected like in the tab `Bulk Assign` inside the textarea named `bm-check-selected-keywords` e.g "Selected keywords — comma-separated list of checked keywords, copy & paste ready" because it will enable me to bulk check the status for each tag.
Put this new div on top only above `widefat striped bm-bulk-desc-table` and under `bm-bulk-desc-filters`


- example of tag searched list
```text
agentic browsers, Atlas, Comet, dbt
```

3. CAUTION: Use as much as possible native look and feel from WP, avoid floating, ugly that deserves the UX and the intuitive understanding of a beginner user.

Note: Before coding, summarize in bullet points that you understand from the given instructions. Update the readme in the changelog in the readme and the version of the plugin when I validate the changes asked.









