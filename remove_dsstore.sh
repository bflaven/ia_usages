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

# Set your target GitHub directory
GIT_DIR="/Users/brunoflaven/Documents/03_git/ia_usages"

# Recursively find and delete all ".DS_Store" files
find "$GIT_DIR" -type f -name ".DS_Store" -delete

echo "All .DS_Store files removed from $GIT_DIR and its subdirectories."



