

## PROMPT_1
Based on this article: https://www.datacamp.com/tutorial/semantic-layer-with-dbt, sevceral quesitons: 
- In a dbt project wher do i cerate these two files : metrics.yml,exposures.yml gi ve me the physical path.
- What I have to cut and patste into dbt_project.yml


## PROMPT_2
When I run dbt test, I have this error

[WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.


## PROMPT_3

I have create a sub-folder and put all the files: base_bank_failures.sql, clean_bank_failures.sql, exposures.yml, metrics.yml

- path
/Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/datacamp_project/models/bank_app


- commands
dbt test
dbt build
dbt run --select clean_bank_failures
dbt test --select clean_bank_failures.State

Can you give me the correct commands according to this tree


## PROMPT_4

Can you give me the correct commands according to this code below:
dbt run --select bank_app.base_bank_failures
dbt test --select bank_app.base_bank_failures


dbt run --select bank_app.clean_bank_failures
dbt test --select bank_app.clean_bank_failures.State

- base_bank_failures.sql
```sql
SELECT *
FROM bank_failures
```

- clean_bank_failures.sql
```sql
SELECT
    State,
    COUNT(*) AS total_failures,
    SUM("Assets ($mil.)" ) AS total_assets
FROM
    {{ ref('base_bank_failures') }}
GROUP BY
    State
```

## PROMPT_5
For `dbt test --select bank_app.clean_bank_failures.State`, I got this message: 

06:13:15  The selection criterion 'bank_app.clean_bank_failures.State' does not match any enabled nodes
06:13:15  Nothing to do. Try checking your model configs and model specification args





## PROMPT_5
Enabling exposures in dbt, instead of tableau make a streamlit app that shows elements from the dbt project.


