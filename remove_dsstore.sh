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
# sh remove_dsstore.sh
# 
# =========================================================

#!/bin/bash
# Set your GitHub project directory
# TARGET_DIR="/Users/brunoflaven/Documents/03_git/ia_usages"
TARGET_DIR="/Users/brunoflaven/Documents/03_git/ia_usages/ia_augmented_journalist_wp_toolkit"

# Navigate to the target directory
cd "$TARGET_DIR"

# Recursively find and delete all .DS_Store files
# find . -name ".DS_Store" -type f -delete
find . -type f \( -name ".DS_Store" -o -name "._.DS_Store" \) -delete

echo "All .DS_Store files removed from $TARGET_DIR and its subdirectories."



