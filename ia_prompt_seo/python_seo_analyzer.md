
**Some instructions to manipulate seoanalyze**


```python
"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fmm_fastapi_poc


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
To complete

# manual install
pip install pyseoanalyzer
python -m pip install pyseoanalyzer

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_seo/

# launch the file
python python_seo_analyzer_1.py



"""
```

```bash
# Command-line Usage
# If you run without a sitemap it will start crawling at the homepage.

# MODEL
# seoanalyze http://www.domain.com/
seoanalyze https://flaven.fr/


# Or you can specify the path to a sitmap to seed the urls to scan list.

# MODEL
# seoanalyze http://www.domain.com/ --sitemap path/to/sitemap.xml
seoanalyze https://flaven.fr/ --sitemap /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_seo/sitemap.xml



# HTML output can be generated from the analysis instead of json.

# seoanalyze http://www.domain.com/ --output-format html
seoanalyze https://flaven.fr/ --output-format html




```

