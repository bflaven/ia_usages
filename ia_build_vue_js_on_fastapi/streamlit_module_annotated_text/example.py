#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# BURN AFTER READING
source activate fmm_fastapi_poc



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs

# BURN AFTER READING
conda env remove -n mistral_integration


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install openai
pip install mistralai
pip install langchain-mistralai
pip install beautifulsoup4

python -m pip install beautifulsoup4
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/streamlit_module_annotated_text/

# launch the file
streamlit run 001_streamlit_no_reruns.py

https://www.youtube.com/watch?v=dPdB7zyGttg

https://discuss.streamlit.io/t/how-to-prevent-the-reloading-of-the-whole-page-when-i-let-the-user-to-perform-an-action/10800/9
https://blog.streamlit.io/introducing-submit-button-and-forms/
https://github.com/tvst/st-annotated-text


"""

import streamlit as st
from annotated_text import annotated_text



"""
# Annotated Text

This app shows off the [Annotated Text component](https://github.com/tvst/st-annotated-text) for
Streamlit.

If you want to try this at home, you'll first need to install it:



```python
pip install st-annotated-text
```


## Basic example

Annotations are just tuples:
"""

with st.echo():
    from annotated_text import annotated_text

    annotated_text(
        "This ",
        ("is", "Verb"),
        " some ",
        ("annotated", "Adj"),
        ("text", "Noun"),
        " for those of ",
        ("you", "Pronoun"),
        " who ",
        ("like", "Verb"),
        " this sort of ",
        ("thing", "Noun"),
        ". ",
        "And here's a ",
        ("word", ""),
        " with a fancy background but no label.",
    )

""

"""
## Nested arguments

You can also pass lists (and lists within lists!) as an argument:
"""


with st.echo():
    my_list = [
        "Hello ",
        [
            "my ",
            ("dear", "Adj"),
            " ",
        ],
        ("world", "Noun"),
        ".",
    ]

    annotated_text(my_list)


""
""

"""
## Customization
"""

"""
### Custom colors

If the annotation tuple has more than 2 items, the 3rd will be used as the background color and the 4th as the foreground color:
"""

with st.echo():
    annotated_text(
        "This ",
        ("is", "Verb", "#8ef"),
        " some ",
        ("annotated", "Adj", "#faa"),
        ("text", "Noun", "#afa"),
        " for those of ",
        ("you", "Pronoun", "#fea"),
        " who ",
        ("like", "Verb", "#8ef"),
        " this sort of ",
        ("thing", "Noun", "#afa"),
        ". "
        "And here's a ",
        ("word", "", "#faf"),
        " with a fancy background but no label.",
    )

""
""

"""
### Custom styles

You can customize a bunch of different styles by overriding the variables
set in the `annotated_text.parameters` module. For example:

```python
from annotated_text import annotated_text, parameters

parameters.SHOW_LABEL_SEPARATOR = False
parameters.BORDER_RADIUS = 0
parameters.PADDING = "0 0.25rem"
```

For more configurable parameters, see the
[parameters.py source file](https://github.com/tvst/st-annotated-text/blob/master/annotated_text/parameters.py).
"""

""
""

"""
### Even more customization

If you want to go beyond the customizations above, you can bring your own CSS!
"""
  
with st.echo():
    from annotated_text import annotated_text, annotation

    annotated_text(
      "Hello ",
      annotation("world!", "noun", font_family="Comic Sans MS", border="2px dashed red"),
    )
