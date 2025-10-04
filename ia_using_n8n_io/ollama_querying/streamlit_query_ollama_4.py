#!/usr/bin/env python3
"""
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_using_n8n_io/ollama_querying/
streamlit run streamlit_query_ollama_4.py

"""

import streamlit as st
import os
from datetime import datetime
import subprocess
import sys

CONFIG_PATH = "config.py"
QUERY_SCRIPT = "query_ollama.py"

# Language mapping and default categories per language
LANG_OPTIONS = {
    "français": {
        "label": "Français",
        "cms_section_keywords_list": """
Sports, Économie / Technologie, Culture, Environnement, France, Europe, Afrique, Amériques, Asie-Pacifique, Moyen-Orient
"""
    },
    "espagnol": {
        "label": "Espagnol",
        "cms_section_keywords_list": """
América Latina, EE.UU. y Canadá, Europa, Francia, Asia-Pacífico, Medio Oriente, África, Medio Ambiente, Cultura, Economía, Ciencia y Tecnologías, Deportes
"""
    },
    "anglais": {
        "label": "Anglais",
        "cms_section_keywords_list": """
France, Africa, Middle East, Americas, Europe, Asia-Pacific, Environment, Business / Tech, Sport, Culture
"""
    }
}

OLLAMA_STATIC_CONFIG = '''# Ollama configuration
OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL
MODEL_NAME = "mistral:7b"              # Model name in Ollama
# MODEL_NAME = "mistral:latest"  
# MODEL_NAME = "phi3.5:3.8b"  
# MODEL_NAME = "neoali/gemma3-8k:4b"  
# MODEL_NAME = "deepseek-r1:latest"
# MODEL_NAME = "embeddinggemma:latest"
# MODEL_NAME = "gemma3:1b"
# MODEL_NAME = "gemma3n:latest"
# MODEL_NAME = "phi3:14b"
# MODEL_NAME = "life4living/ChatGPT:latest"

# Request configuration
STREAM = False  # Set to True for streaming responses

'''

st.title("📝 Ollama Config Editor & Runner")

def read_config(path):
    config = {"lang": "français", "prompt_template": "", "content": "", "output_base": "001a_ner_mistral_f24_fr_focus_mz508039"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        for k in ["lang", "prompt_template", "content", "OUTPUT_FILE"]:
            block = k + " = "
            if block in txt:
                rest = txt.split(block, 1)[1]
                if rest.strip().startswith('"""'):
                    v = rest.split('"""',2)[1]
                else:
                    v = rest.splitlines()[0].split("#")[0].strip().replace('"','')
                if k=="OUTPUT_FILE":
                    v = v.replace(".json","")
                config[k if k!="OUTPUT_FILE" else "output_base"] = v
    except Exception:
        pass
    return config

current = read_config(CONFIG_PATH)

lang = st.selectbox(
    "Select output language:",
    list(LANG_OPTIONS.keys()),
    format_func=lambda x: LANG_OPTIONS[x]['label'],
    index=list(LANG_OPTIONS.keys()).index(current.get("lang", "français"))
)

prompt_template = st.text_area(
    "Edit the prompt template (Jinja-style vars allowed):",
    value=current.get("prompt_template",""),
    height=350
)

content = st.text_area(
    "Paste your article content here:",
    value=current.get("content",""),
    height=250
)

output_base = st.text_input(
    "Output file base name (without .json):",
    value=current.get("output_base", "001a_ner_mistral_f24_fr_focus_mz508039"),
    help="Example: 001a_ner_mistral_f24_fr_focus_mz508039"
)

if st.button("💾 Update config.py"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"config_{timestamp}.py"
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as original:
                with open(backup_path, "w", encoding="utf-8") as backup:
                    backup.write(original.read())

        cms_section_keywords_list = LANG_OPTIONS[lang]["cms_section_keywords_list"]

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(OLLAMA_STATIC_CONFIG)
            config_py = f"""# Language-based CMS categories
FR_cms_section_keywords_list = \"\"\"{LANG_OPTIONS['français']['cms_section_keywords_list'].strip()}\"\"\"
ES_cms_section_keywords_list = \"\"\"{LANG_OPTIONS['espagnol']['cms_section_keywords_list'].strip()}\"\"\"
EN_cms_section_keywords_list = \"\"\"{LANG_OPTIONS['anglais']['cms_section_keywords_list'].strip()}\"\"\"

lang = "{lang}"

match lang:
    case "français":
        cms_section_keywords_list = FR_cms_section_keywords_list
    case "espagnol":
        cms_section_keywords_list = ES_cms_section_keywords_list
    case "anglais":
        cms_section_keywords_list = EN_cms_section_keywords_list
    case _:
        cms_section_keywords_list = FR_cms_section_keywords_list

prompt_template = \"\"\"{prompt_template.strip()}\"\"\"

content = \"\"\"{content.strip()}\"\"\"

OUTPUT_FILE = "{output_base.strip()}.json"
"""
            f.write(config_py)
        st.success(f"Config updated! Old config.py saved as {backup_path}")
    except Exception as e:
        st.error(f"Failed to update config.py: {e}")

st.info("Now you can launch query_ollama.py with the button below.")

if st.button("🚀 Run query_ollama.py"):
    st.write("Launching query_ollama.py, please wait...")
    try:
        result = subprocess.run(
            [sys.executable, QUERY_SCRIPT],
            capture_output=True,
            text=True
        )
        st.subheader("Script Output")
        st.code(result.stdout)
        if result.stderr:
            st.subheader("Errors / Warnings")
            st.code(result.stderr)
        if result.returncode == 0:
            st.success("query_ollama.py executed successfully.")
        else:
            st.error(f"query_ollama.py failed with exit code {result.returncode}.")
    except Exception as e:
        st.error(f"Failed to run query_ollama.py: {e}")



