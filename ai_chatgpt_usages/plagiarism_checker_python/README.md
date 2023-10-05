# plagiarism_checker_python


## Usage
A very simple plagiarism checker in python, show result in Streamlit, both work with text or code. Required (.txt) sources. The file `plagiarism_checker_python_4.py` is the most complete version, the others are just WIPs.

The plagiarism checker parses the files (.txt) in one directory e.g. `./source papers` or `./source codes` and then gave a percentage of plagiarism in it and a call to action. Fire the person or not :)

__It inspires from this code [https://github.com/Kalebu/Plagiarism-checker-Python](https://github.com/Kalebu/Plagiarism-checker-Python)__

```python
# VALUES
file_output = 'output/plagiarism_checker_python_4_result.csv'
path_text = "./source_papers"
path_code = "./source_codes"
```


## Abstract
The idea naturally came as a result of using GPT chat [https://chat.openai.com/](https://chat.openai.com/) Indeed the massive use of GPT chat or any other form of AI device necessarily brings its corollary of control which comes down to the following question: is it a human who wrote all or part of the text or code that I have under the eyes ?

For sure, I suppose that many algorithms are already in use in many sectors: reading and summarizing legal documents, profiling individuals in marketing and tracking, reading and checking course materials and students materials in a training, reading and automatic summary for scenarios in TV production, verification of copy-writing in PR or writing press release in the communication sector, automatic reading of CVs and cover letters in the HRD sector… if it is not the case, it will become soon!

The IA’s examples list for usages is endless and indeed, this “monitoring” task will become a recurring task for a P.O, a product manager or in all sorts of job. So, for my personal use, I have a made a quick and dirty plagiarism checker with Python, Streamlit and Scikit-learn.




## How-to
```bash
# plagiarism_checker_python env
conda create --name plagiarism_checker_python python=3.10.9
conda info --envs
source activate plagiarism_checker_python
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

# example to remove for a clean place
conda env remove -n unstructured_data_python_parsing
conda env remove -n streamlit-custom

# to export requirements
pip freeze > requirements_plagiarism_checker_python.txt

# to install
pip install -r requirements_plagiarism_checker_python.txt

# get a project from github named bard_ai_chatgpt_usages
git clone https://github.com/bflaven/bard_ai_chatgpt_usages.git bard_ai_chatgpt_usages

```


## Source for texts
Feel free to change the sources...

[https://www.utc.edu/library/help/tutorials/plagiarism/examples-of-plagiarism](https://www.utc.edu/library/help/tutorials/plagiarism/examples-of-plagiarism)



## Other sources from projects for plagiarism checker in python

- **kalebu_plagiarism_checker_python**
[https://github.com/Kalebu/Plagiarism-checker-Python](https://github.com/Kalebu/Plagiarism-checker-Python)



- **Python-Plagiarism-Checker by Copyleaks**
[https://github.com/Copyleaks/Python-Plagiarism-Checker](https://github.com/Copyleaks/Python-Plagiarism-Checker)
	+ [https://pypi.org/project/copyleaks/](https://pypi.org/project/copyleaks/)
	+ [https://api.copyleaks.com/](https://api.copyleaks.com/)

- **secretsquirrel_plagiarismchecker**
[https://github.com/secretsquirrel/PlagiarismChecker](https://github.com/secretsquirrel/PlagiarismChecker)


- **alphasaur666_plagiarismchecker**
[https://github.com/alphasaur666/PlagiarismChecker](https://github.com/alphasaur666/PlagiarismChecker)


- **wazzabeee_plagiarism_checker**
[https://github.com/Wazzabeee/plagiarism_checker](https://github.com/Wazzabeee/plagiarism_checker)


- **me_badsha_plagiarism_checker**
[https://github.com/me-badsha/Plagiarism-checker](https://github.com/me-badsha/Plagiarism-checker)

- **Repositories Python plagiarism-checker on github.com**
[https://github.com/search?l=Python&q=plagiarism-checker&type=Repositories](https://github.com/search?l=Python&q=plagiarism-checker&type=Repositories)
