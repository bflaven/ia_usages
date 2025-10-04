#!/usr/bin/env python3
"""
Script to request locally installed Mistral 7B model via Ollama
All configurable variables are externalized in config.py for easy updating.

cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_using_n8n_io/ollama_querying/
streamlit run streamlit_query_ollama_3.py

"""

import streamlit as st
import os
from datetime import datetime
import subprocess
import sys

CONFIG_PATH = "config.py"
QUERY_SCRIPT = "query_ollama.py"

SECTION_KEYWORDS_OPTIONS = [
    "Sports",
    "Économie / Technologie",
    "Culture",
    "Environnement",
    "France",
    "Europe",
    "Afrique",
    "Amériques",
    "Asie-Pacifique",
    "Moyen-Orient",
]
LANG_OPTIONS = ["français", "espagnol", "anglais"]

st.title("📝 Ollama Config Editor")

def read_config_vars(path):
    config_vars = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if line.strip().startswith("#"):
                continue
            if "cms_section_keywords_list" in line:
                start = line.find('"""')+3
                end = line.rfind('"""')
                if start > 2 and end > start:
                    cats = line[start:end].replace("\n", "").split(",")
                    config_vars["cms_section_keywords_list"] = [c.strip() for c in cats if c.strip()]
            elif line.startswith("lang"):
                config_vars["lang"] = line.split("=")[1].replace('"',"").replace("'","").strip()
            elif line.startswith("content"):
                start = line.find('"""')+3
                end = line.rfind('"""')
                if start > 2 and end > start:
                    config_vars["content"] = line[start:end].strip()
    except Exception as e:
        st.error(f"Error reading config.py: {e}")
    return config_vars

current = read_config_vars(CONFIG_PATH)
default_cats = current.get("cms_section_keywords_list", SECTION_KEYWORDS_OPTIONS)
default_lang = current.get("lang", LANG_OPTIONS[0])
default_content = current.get("content", "")

st.subheader("Categories")
cms_section_keywords_list = st.multiselect(
    "Select categories (comma-delimited list will be saved):",
    SECTION_KEYWORDS_OPTIONS,
    default=default_cats,
)

st.subheader("Language")
lang = st.selectbox("Select output language:", LANG_OPTIONS, index=LANG_OPTIONS.index(default_lang) if default_lang in LANG_OPTIONS else 0)

st.subheader("Content")
content = st.text_area("Paste your article content here:", value=default_content, height=300)

if st.button("💾 Update config.py"):
    try:
        # Backup current config.py with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"config_{timestamp}.py"
        with open(CONFIG_PATH, "r", encoding="utf-8") as original:
            with open(backup_path, "w", encoding="utf-8") as backup:
                backup.write(original.read())
        # Update config.py with new values
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.strip().startswith("cms_section_keywords_list"):
                cat_string = ", ".join(cms_section_keywords_list)
                new_value = f'cms_section_keywords_list = """\n{cat_string}\n"""\n'
                new_lines.append(new_value)
            elif line.strip().startswith("lang"):
                new_lines.append(f'lang = "{lang}"\n')
            elif line.strip().startswith("content"):
                new_lines.append(f'content = """\n{content}\n"""\n')
            else:
                new_lines.append(line)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        st.success(f"Config updated! Old config.py saved as {backup_path}")
    except Exception as e:
        st.error(f"Failed to update config.py: {e}")

st.info("After updating, you can now launch query_ollama.py with the button below.")

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
