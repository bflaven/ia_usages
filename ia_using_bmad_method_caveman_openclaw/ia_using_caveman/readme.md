# Using Caveman

Notes and how-to from testing [Caveman](https://github.com/JuliusBrussee/caveman) — a Claude Code plugin that compresses conversational output to save tokens while keeping full technical substance.

## Background: plugins in Claude Code

A Claude Code plugin is one of three things:

- **Skill** — a custom command invoked with `/skill-name`, or a context-aware prompt Claude reaches for automatically when relevant.
- **MCP server** — a connection to an external service/API, giving Claude access to data it wouldn't otherwise have.
- **Hook** — a shell script that runs automatically on an event (before a file edit, after a commit, on session start...).

Source: https://claude.com/plugins · https://code.claude.com/docs/fr/plugins

```bash
# List all installed plugins
claude plugin list

# Update a specific plugin to the latest version
claude plugin update @anthropic/deploy-helper

# Update all plugins
claude plugin update --all

# Remove a plugin
claude plugin remove @anthropic/deploy-helper
```

**Common mistake:** don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside `.claude-plugin/`. Only `plugin.json` goes there — every other directory sits at the plugin's root.

Useful slash commands to know: `/plugin`, `/context`.

## Install Caveman

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

Project: https://github.com/JuliusBrussee/caveman

## Why it's worth it

Caveman is a skill wrapped in a persistent behavioral instruction: same technical content, radically fewer tokens. Articles, filler words, and pleasantries drop out; fragments are fine; technical terms stay exact. It reframes verbosity itself as a cost — tokens are money, and saving them is a skill worth developing, not a shortcut that loses meaning.

## Rough edges

Plugins in this space tend to leave residue. On one session start, a leftover hook from an unrelated tool broke things:

```
SessionStart:startup hook error
Failed with non-blocking status code:

node:internal/modules/cjs/loader:1210
  throw err;
Error: Cannot find module '.../.wolf/hooks/stop.js'
    at Module._resolveFilename (node:internal/modules/cjs/loader:1207:15)
```

That error came from a different, earlier plugin (see below), not Caveman itself — but it's a reminder to check `~/.claude/settings.json`, the plugin cache, and stray config directories whenever a session start hook complains.

## Cleaning up a previous "token saver" plugin (OpenWolf)

Before settling on Caveman, I tried a similarly-pitched plugin called OpenWolf. In practice it added more complexity than it removed. How to fully remove it:

```bash
# where it lives
cd ~/.openwolf/
cd ~/.wolf/

# check contents
ls -la

# remove
rm -R ~/.openwolf
rm -R ~/.wolf

# uninstall / reinstall via npm
openwolf --version
npm uninstall -g openwolf
npm install -g openwolf   # only if reinstalling

# check for leftovers still loaded in Claude Code
# type /context in a session:
#   Memory files · /memory
#     ├ ~/.claude/rules/openwolf.md
#     ├ ~/CLAUDE.md
#     └ ~/.wolf/OPENWOLF.md
# remove any stale references you find there

# clear the Claude Code cache if needed
~/Library/Caches/claude-code
```

Other cleanup reference: https://ctok.ai/en/claude-code-cleanup

## Verdict

Of the "compress my tokens" plugins I've tried, Caveman is the first one that delivers on the promise without adding its own maintenance overhead. It doesn't touch the substance of a technical answer — only the words around it.

## Visual identity note

Concept, in the author's own words:

> Captain Caveman or Fred Flintstone.

A stocky prehistoric figure, single-strap fur tunic, club raised overhead — instantly recognizable, no frills, in the spirit of those two classic cartoon cavemen without reproducing either character directly. Fitting, for a tool whose whole premise is "why use many token when few do trick."

## Sources

- Caveman — GitHub: https://github.com/JuliusBrussee/caveman
- Claude Code plugins overview: https://claude.com/plugins
- Building Claude Code plugins: https://www.datacamp.com/tutorial/how-to-build-claude-code-plugins
- Caveman mode write-up (FR): https://pasqualepillitteri.it/fr/news/847/claude-code-caveman-mode-economie-tokens
