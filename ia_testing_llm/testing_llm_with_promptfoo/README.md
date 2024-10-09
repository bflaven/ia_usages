# testing_llm_with_promptfoo

**Here is a suite to test LLMs using PROMPTFOO. It mainly takes up the tests carried out on MLFlow on an endpoint defined in "Served LLM model" ex: mistral-ollama**


The tool and all information relating to the use of PROMPTFOO are available at:[https://www.promptfoo.dev/](https://www.promptfoo.dev/).


**The file `MODEL_promptfooconfig.yaml` is given as an example of configuration. It must be modified in particular by configuring the `providers` then rename it to `promptfooconfig.yaml` so that it is the configuration file of your PROMPTFOO installation**


## I. QUICK REMINDER


**The main commands to install and launch PROMPTFOO.**


```sh
# Install en local dans un répertoire

# go to path
cd /[your-path]/

# create the directory that will host the PROMPTFOO tests
mkdir 002_promptfoo_running

# get into the directory
cd 002_promptfoo_running


# launch install in the rep
npm install promptfoo@latest
 
# check the install
# promptfoo --version


# launch install globally
npm install -g promptfoo@latest

# init
npx promptfoo init

# eval
npx promptfoo eval

# view results
npx promptfoo view


# uninstall
npm uninstall -g promptfoo

# gain space disk
npm cache clean --force
```

## II. TESTS EN PYTHON


The tests are done in Python. You have to edit the `assert_all_4.py` file. These tests require a specific environment, in my example the environment is named `promptfoo`, it is managed using Anaconda. You can use the Python dev environment management tools like Anaconda, Poetry or Venv.


**The tests actually use the `langdetect` package. See `assert_all_4.py`**


```python
"""
[env]
# Conda Environment
conda create --name promptfoo python=3.9.13
conda info --envs
source activate promptfoo
conda deactivate


# BURN AFTER READING
source activate promptfoo

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n promptfoo

# BURN AFTER READING
conda env remove -n promptfoo


# update conda
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install langdetect
python -m pip install langdetect

"""


# extract from the file assert_all_4.py
# check https://pypi.org/project/langdetect/


from langdetect import detect, LangDetectException


            # add languages to the list if needed
            # langdetect supports 55 languages out of the box (ISO 639-1 codes)
            # https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
            # af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw
        

            # Languages for FMM
            # ar, br, cn, en, es, fa, ff, fr, ha, km, ma, pt, ro, ru, sw, uk, vi

            valid_languages = {"ar", "en", "es", "fa", "fr", "pt", "ro", "ru", "sw", "uk", "vi", "zh-cn"}




```


## III. ADDITIONAL INFORMATION


### 1. INSTALLATION

#### Requirements

- Node.js 18 or newer
- Supported operating systems: macOS, Linux, Windows

#### Installation Methods

##### For Command-Line Usage

###### Using npm (recommended)

Install `promptfoo` globally using npm:

```sh
npm install -g promptfoo
```

Or use `npx` to run `promptfoo` directly without installation:

```sh
npx promptfoo@latest
```

###### Using Homebrew

If you prefer using Homebrew, you can install promptfoo with:

```sh
brew install promptfoo
```

##### For Library Usage

Install `promptfoo` as a library in your project:

```sh
npm install promptfoo
```

#### Verify Installation

To verify that promptfoo is installed correctly, run:

```sh
promptfoo --version
```

This should display the version number of promptfoo.

#### Next Steps

After installation, you can start using promptfoo by running:

```sh
promptfoo init
```

This will create a `promptfooconfig.yaml` placeholder in your current directory.

### 2. CONFIGURE

All PROMPTFOO configuration is defined in the `promptfooconfig.yaml` file.
The 3 essential notions are: `prompts`, `providers`, `tests`.

**Extract from the `promptfooconfig.yaml` file**

```yaml
description: "MLFLOW PROMPTFOO EVAL #1"

# cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_testing_llm/001_promptfoo_running
# npx promptfoo eval

prompts: file://prompts/mig_prompt_1.txt
  

providers:
  - id: ollama:mistral:latest
    config:
      temperature: 0.8
#  - id: openrouter:mistralai/mixtral-8x7b-instruct
#    config:
#      temperature: 0.5
#  - id: openrouter:meta-llama/llama-3.1-8b-instruct
#    config:
#      temperature: 0.5

tests:

    - vars:
        lang: Français
        content: file://articles/fr/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Portuguais
        content: file://articles/pt/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Espagnol
        content: file://articles/es/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Russe
        content: file://articles/ru/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Arabe
        content: file://articles/ar/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: English
        content: file://articles/en/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Persan
        content: file://articles/fa/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Roumain
        content: file://articles/ro/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Swahili
        content: file://articles/sw/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Ukrainien
        content: file://articles/uk/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Vietnamien
        content: file://articles/vi/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Chinois
        content: file://articles/cn/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py
    - vars:
        lang: Khmer
        content: file://articles/km/*.txt
      assert:
        - type: contains-json
          value: file://assert/assert_all.json
        - type: python
          value: file://assert/assert_all_4.py


```

### 3. RUN THE TESTS
You can view the results by running:

```sh
# Lancer les tests
npx promptfoo eval

# For debug
LOG_LEVEL=debug npx promptfoo eval
```

### 4. SEE THE RESULT

You can view the results by running:


```sh
promptfoo view
```


### 5. CONFIGURE OPENAI OR ANY PROVIDER WITH APIKEY

For OpenAI, if testing with an OpenAI model, you'll need to set the OPENAI_API_KEY environment variable (see OpenAI provider docs for more info): To use the OpenAI API, set the OPENAI_API_KEY environment variable, specify via apiKey field in the configuration file or pass the API key as an argument to the constructor. There is two way to do it.

- (i) USING EXPORT
```sh
export OPENAI_API_KEY=your_api_key_here
```

- (ii) USING a `.env`

You can use also `.env` to manage the value for OPENAI_API_KEY. Adds --env-file support to most commands that overrides the default .env. See https://www.promptfoo.dev/docs/usage/command-line/#promptfoo-eval


**More on the command-line `promptfoo eval`**

By default the `eval` command will read the `promptfooconfig.yaml` configuration file in your current directory. But, if you're looking to override certain parameters you can supply optional arguments:

| Option                              | Description                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------- |
| `-a, --assertions <path>`           | Path to assertions file                                                         |
| `-c, --config <paths...>`           | Path to configuration file(s). Automatically loads promptfooconfig.js/json/yaml |
| `--delay <number>`                  | Delay between each test (in milliseconds)                                       |
| `--description <description>`       | Description of the eval run                                                     |
| `--env-file, --env-path <path>`     | Path to .env file                                                               |
| `--filter-failing <path>`           | Path to JSON output file with failing tests                                     |
| `-n, --filter-first-n <number>`     | Only run the first N tests                                                      |
| `--filter-pattern <pattern>`        | Only run tests whose description matches the regex pattern                      |
| `--filter-providers <providers>`    | Only run tests with these providers                                             |
| `--grader <provider>`               | Model that will grade outputs                                                   |
| `-j, --max-concurrency <number>`    | Maximum number of concurrent API calls                                          |
| `--model-outputs <path>`            | Path to JSON containing list of LLM output strings                              |
| `--no-cache`                        | Do not read or write results to disk cache                                      |
| `--no-progress-bar`                 | Do not show progress bar                                                        |
| `--no-table`                        | Do not output table in CLI                                                      |
| `--no-write`                        | Do not write results to promptfoo directory                                     |
| `-o, --output <paths...>`           | Path(s) to output file (csv, txt, json, yaml, yml, html)                        |
| `-p, --prompts <paths...>`          | Paths to prompt files (.txt)                                                    |
| `--prompt-prefix <path>`            | Prefix prepended to every prompt                                                |
| `--prompt-suffix <path>`            | Suffix appended to every prompt                                                 |
| `-r, --providers <name or path...>` | Provider names or paths to custom API caller modules                            |
| `--remote`                          | Force remote inference wherever possible (used for red teams)                   |
| `--repeat <number>`                 | Number of times to run each test                                                |
| `--share`                           | Create a shareable URL                                                          |
| `--suggest-prompts <number>`        | Generate N new prompts and append them to the prompt list                       |
| `--table`                           | Output table in CLI                                                             |
| `--table-cell-max-length <number>`  | Truncate console table cells to this length                                     |
| `-t, --tests <path>`                | Path to CSV with test cases                                                     |
| `--var <key=value>`                 | Set a variable in key=value format                                              |
| `-v, --vars <path>`                 | Path to CSV with test cases (alias for --tests)                                 |
| `--verbose`                         | Show debug logs                                                                 |
| `-w, --watch`                       | Watch for changes in config and re-run                                          |

---

*The `eval` command will return exit code `100` when there is at least 1 test case failure. It will return exit code `1` for any other error. The exit code for failed tests can be overridden with environment variable `PROMPTFOO_FAILED_TEST_EXIT_CODE`.*


### 6.PROMPTFOO: THE OFFICIAL SITE
- Learn more https://www.promptfoo.dev/