Create a `.gitignore` for a wp plugin that avoir to launch important info and php file and append this below. Make so I just have to cut and paste


```text

# Claude Code local settings — never commit
.claude/

# OpenWolf (deprecated) — never commit
.wolf/

# Environment secrets
.env
.env.local
.env.*.local

# Node
node_modules/
npm-debug.log*

# Build output
dist/

# Memory output files (generated, not source)
memory/*.md
memory/*.png

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Editor directories
.idea/
.vscode/
*.swp
*.swo
```




