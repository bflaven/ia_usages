
For the comamnd `dbt seed --show-all-deprecations --no-partial-parse`, I got this error.


```bash
dbt seed --show-all-deprecations --no-partial-parse
04:32:25  Running with dbt=1.10.13
04:32:25  Registered adapter: duckdb=1.10.0
04:32:26  [WARNING][MissingArgumentsPropertyInGenericTestDeprecation]: Deprecated
functionality
Found top-level arguments to test `accepted_values`. Arguments to generic tests
should be nested under the `arguments` property.`
04:32:26  [WARNING][MissingArgumentsPropertyInGenericTestDeprecation]: Deprecated
functionality
Found top-level arguments to test `accepted_values`. Arguments to generic tests
should be nested under the `arguments` property.`
04:32:26  [WARNING][MissingArgumentsPropertyInGenericTestDeprecation]: Deprecated
functionality
Found top-level arguments to test `accepted_values`. Arguments to generic tests
should be nested under the `arguments` property.`
04:32:26  [WARNING][MissingArgumentsPropertyInGenericTestDeprecation]: Deprecated
functionality
Found top-level arguments to test `relationships`. Arguments to generic tests
should be nested under the `arguments` property.`
04:32:26  Encountered an error:
Parsing Error
  Invalid metrics config given in FilePath(searched_path='models', relative_path='semantic/metrics.yml', modification_time=1762871826.0206685, project_root='/Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/taxonomy_semantic') @ metrics: {'name': 'tags_by_entity_type', 'label': 'Tags Grouped by Entity Type', 'description': 'Tag count segmented by NER entity type (PER, ORG, GPE, etc.)', 'type': 'simple', 'type_params': {'measure': 'total_tags'}, 'dimensions': ['entity_type']} - at path []: Additional properties are not allowed ('dimensions' was unexpected)
04:32:26  [WARNING][DeprecationsSummary]: Deprecated functionality
Summary of encountered deprecations:
- MissingArgumentsPropertyInGenericTestDeprecation: 4 occurrences
```

