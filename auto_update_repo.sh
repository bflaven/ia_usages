# #!/bin/bash
# =========================================================
# Script: auto_update_repo.sh
# Description: Automate Git repository updates with
#              intelligent commit message generation.
# Author: Bruno Flaven (example)
# =========================================================
# 
# =========================================================
# 
# cd /Users/brunoflaven/Documents/03_git/ia_usages/
# sh auto_update_repo.sh
# 
# =========================================================

# ==== CONFIGURATION ====
REPO_PATH="/Users/brunoflaven/Documents/03_git/ia_usages"

# ==== NAVIGATE TO REPOSITORY ====
cd "$REPO_PATH" || { echo "Error: Cannot access $REPO_PATH"; exit 1; }

# ==== SHOW BASE INFORMATION ====
echo "----------------------------------------"
echo "Current Git Branch and Status"
echo "----------------------------------------"
git branch
git status --short

# ==== STAGE ALL CHANGES ====
git add -A

# ==== CAPTURE GIT STATUS ====
status_output=$(git status --short)

# ==== CHECK IF THERE ARE CHANGES ====
if [ -z "$status_output" ]; then
    echo "No changes detected. Exiting."
    exit 0
fi

# ==== ANALYZE FILE TYPES AND ACTIONS ====
generate_commit_message() {
    # Detect types of modifications
    added=$(echo "$status_output" | grep "^A " | wc -l)
    modified=$(echo "$status_output" | grep "^ M" | wc -l)
    deleted=$(echo "$status_output" | grep "^ D" | wc -l)
    renamed=$(echo "$status_output" | grep "^R" | wc -l)
    untracked=$(echo "$status_output" | grep "^\?\?" | wc -l)

    # Extract filenames for type analysis
    files=$(echo "$status_output" | awk '{print $2}')

    # Detect file type by extension
    python_files=$(echo "$files" | grep -Ei "\.py$" | wc -l)
    js_files=$(echo "$files" | grep -Ei "\.js$" | wc -l)
    php_files=$(echo "$files" | grep -Ei "\.php$" | wc -l)
    md_files=$(echo "$files" | grep -Ei "\.md$|readme" | wc -l)
    text_files=$(echo "$files" | grep -Ei "\.txt$|\.diff$" | wc -l)
    doc_files=$(echo "$files" | grep -Ei "\.pdf$|\.pptx$|\.docx$" | wc -l)
    image_files=$(echo "$files" | grep -Ei "\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$" | wc -l)
    config_files=$(echo "$files" | grep -Ei "\.yml$|\.yaml$|\.json$|\.ini$|\.cfg$" | wc -l)

    # ==== CLASSIFY MESSAGE ====
    if (( renamed > 0 )); then
        echo "rename files or directories"
    elif (( deleted > 0 )); then
        echo "remove unused files"
    elif (( untracked > 0 && modified == 0 )); then
        echo "add new files"
    elif (( modified > 0 && untracked == 0 )); then
        echo "update existing files"
    elif (( untracked > 0 && modified > 0 )); then
        echo "add and update files"
    elif (( md_files > 0 )); then
        echo "update documentation or readme"
    elif (( python_files > 0 )); then
        echo "update Python scripts"
    elif (( js_files > 0 )); then
        echo "update JavaScript files"
    elif (( php_files > 0 )); then
        echo "update PHP code"
    elif (( config_files > 0 )); then
        echo "update configuration files"
    elif (( text_files > 0 )); then
        echo "edit text or diff logs"
    elif (( doc_files > 0 )); then
        echo "update documents or presentations"
    elif (( image_files > 0 )); then
        echo "update images or media assets"
    else
        echo "miscellaneous maintenance update"
    fi
}

# ==== GENERATE THE FINAL COMMIT MESSAGE ====
commit_message=$(generate_commit_message)
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
final_message="Commit: $commit_message ($timestamp)"

# ==== COMMIT AND PUSH ====
git commit -m "$final_message"
git push

# ==== CONFIRMATION ====
echo "----------------------------------------"
echo "Repository successfully updated!"
echo "Commit message used:"
echo "$final_message"
echo "----------------------------------------"


