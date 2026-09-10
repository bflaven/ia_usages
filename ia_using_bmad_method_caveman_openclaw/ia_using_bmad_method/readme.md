# Using the BMad Method

Notes and how-to from testing the [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) — an AI-driven planning and development framework that runs as a set of agents/skills inside Claude Code.

## What it is

The BMad Method ("Build More Architect Dreams") is a framework module that walks a project from idea to implementation through specialized AI agents, guided workflows, and adaptive planning. If you're already comfortable with an AI coding assistant (Claude, Cursor, GitHub Copilot), you're ready to start.

- Docs: https://docs.bmad-method.org/
- Getting started: https://docs.bmad-method.org/tutorials/getting-started/
- Blog / guides: https://bmadcode.com/
- Community: https://discord.gg/gk8jAdXWmj

## Prerequisites

```
Node.js v20.12+
Python 3.10+
uv
```

`uv` is the recommended Python package/project manager for running BMAD's Python scripts (`uv run <script>`). BMAD installs fine without it, but the ecosystem is moving toward it.

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
which uv
uv --version
```

You can also manage the Python side with conda instead:

```bash
conda create --name bmad_method python=3.13
conda info --envs
source activate bmad_method
conda deactivate
```

## Install

```bash
npx bmad-method install
```

This installs the core module, shared scripts, configuration, and — for Claude Code — 46 skills dropped into `.claude/skills`. Once installed, ask the help skill what to do first:

```
bmad-help what should I do first?
```

## Core commands (inside Claude Code)

```
*help                       # list commands for the current agent
BMad:agents:analyst         # Mary — business analyst / brainstorming
BMad:agents:pm              # John — product manager (PRD)
BMad:agents:architect       # Winston — system architect
BMad:agents:po              # product owner
BMad:agents:sm              # Bob — scrum master
BMad:agents:qa              # QA
BMad:tasks:shard-doc        # split a doc into a directory of pieces (aka "md-tree")
```

**Tip:** start a new session (or clear the current one) for each agent — it reduces context overlap between personas.

## Workflow in practice

1. **Brainstorm** with the analyst agent. It pushes on you with an elicitation format that's worth stealing even outside the tool:

   > "As the `<role>`, what I want is ___, what I fear is ___, what I'd demand is ___."

   Run it once per stakeholder — a journalist and an editor rarely land on the same answer, which is the point of asking before writing any code.

2. **Produce artifacts**: `brief.md` → `prd.md` → `architecture.md`. A PRD (Product Requirements Document) states the *what* and *why*, never the *how*. The PM turns it into epics; the scrum master turns epics into stories.

3. **Shard the docs.** Running the shard-doc command on `prd.md` creates a `prd/` directory with one file per epic/story; the same on `architecture.md` creates an `architecture/` directory with the technical breakdown. From there, stories can be pushed into a tracker (Jira, [Linear](https://linear.app/integrations/claude)).

4. **Develop** story by story with the dev agent, review with QA.

## Vocabulary

- **Greenfield** — a new project, no existing constraints to work around.
- **Brownfield** — an existing system, technical debt included; most real-world work falls here, and it's where BMad's upfront reflection pays off the most.
- **Elicitation technique** — a structured way to pull requirements, beliefs, or preferences out of a stakeholder through direct interaction.
- **Moonshot** — an ambitious, high-risk/high-reward goal (from the Apollo 11 program).

## What actually worked

- The brainstorming phase is where the tool earns its keep — measurable gains in both the productivity of the creative process and the depth you can reach with an agent pushing back on you.
- Personas aren't decoration: talking to "Mary" or "John" instead of a generic assistant keeps a stable mental model as you switch between roles.
- The method doesn't automate execution — it structures the thinking that comes before it, then hands the actual build back to your coding assistant.

## Rough edges

- The one thing it can't give you is the idea itself — brainstorming support only goes so far if you show up with nothing.
- Real risk of overload: FOMO, infobesity, more agent proposals than one person can triage in a day.
- Applied outside software (tested here on a non-dev "screenwriting" brainstorming project with custom personas), the same core mechanics hold up — the framework isn't inherently developer-only.

## Test case used for these notes

Brief: a web app letting a journalist grow and manage a keyword corpus locally, exportable as JSON, ultimately shared across newsrooms via an API endpoint.

## Visual identity note

Concept, in the author's own words:

> be mad icon but not angry more a smile icon. It also evokes me the MadMag.com boy. The boy from Mad Magazine is named Alfred E. Neuman. He is the magazine's mascot and is known for his distinctive smile and the catchphrase "What, me worry?"

"Be mad" read as a smile rather than anger — a fitting attitude for a method that pushes you to stay unbothered by not-knowing and brainstorm anyway. (Reference mood boards, not reproduced here for rights reasons: a generic smiling-face icon, and the Mad Magazine mascot's gap-toothed grin.)

## Sources

- BMad Method — GitHub: https://github.com/bmad-code-org/BMAD-METHOD
- The Official BMad-Method Masterclass (video): https://www.youtube.com/watch?v=LorEJPrALcg
- Installing & Configuring the BMAD Method (video): https://www.youtube.com/watch?v=IpbtzVbYtsk
- BMad Code YouTube channel: https://www.youtube.com/@BMadCode
- French write-up: https://www.sfeir.dev/ia/bmad-method-comment-revolutionner-le-developpement-avec-lia-agentique/
