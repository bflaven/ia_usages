{% macro levenshtein(string1, string2) %}
    editdist3({{ string1 }}, {{ string2 }})
{% endmacro %}