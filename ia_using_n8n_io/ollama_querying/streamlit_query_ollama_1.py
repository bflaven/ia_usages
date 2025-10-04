# streamlit_query_ollama.py

import streamlit as st
import os
import ast

# Path to your config.py (assumed to be in same directory)
CONFIG_PATH = "config.py"

# Predefined options for categories and languages (edit as needed)
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

# Read current values from config.py for defaults
def read_config_vars(path):
    config_vars = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if line.strip().startswith("#"):
                continue
            # Very basic parsing, customize if you change config.py structure
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
        # Read config.py, update only the selected fields, leave the rest untouched
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
                # Find end of triple-quoted string and replace full block
                new_lines.append(f'content = """\n{content}\n"""\n')
            else:
                new_lines.append(line)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        st.success(f"Config updated! Run your script to use new values.")
    except Exception as e:
        st.error(f"Failed to update config.py: {e}")

st.info("After updating, you can run query_ollama.py with your new settings.")

