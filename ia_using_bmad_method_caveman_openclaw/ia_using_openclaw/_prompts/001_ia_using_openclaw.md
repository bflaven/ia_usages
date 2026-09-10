Voici une lecture complète d'OpenClaw depuis la page officielle — c'est un projet vraiment récent et impressionnant. Je te prépare un guide structuré PO-friendly.

---

## OpenClaw — ce que c'est en 30 secondes

OpenClaw est un assistant AI open-source qui **tourne sur ta machine** (Mac, Windows, Linux) et avec lequel tu communiques via WhatsApp, Telegram, Discord, iMessage ou Slack — les apps que tu utilises déjà. Il a accès à ton système de fichiers, ton navigateur, et peut exécuter des commandes shell. Sa puissance vient des **Skills** : des plugins que la communauté crée, et que OpenClaw peut même écrire lui-même.

---

## 1 — Commandes simples : exemples concrets

Tu envoies un message texte comme à un collègue. OpenClaw fait le reste.

```
"Summarize my last 10 emails and tell me what needs a reply today"
→ Il lit ta boîte Gmail et te donne un résumé structuré.

"Schedule a call with Pierre tomorrow at 3pm, 30 minutes, send him the invite"
→ Il crée l'événement Google Calendar et envoie l'email.

"Check if flaven.fr is up and tell me the load time"
→ Il lance une requête HTTP et te répond avec le status.

"Write a tweet about AI coordination in newsrooms, post it"
→ Il rédige, te montre le draft, attend ta validation, publie.

"Remind me in 2 hours to review the MMA pipeline script"
→ Il pose un timer et te ping dans 2h sur Telegram.

"What's the weather in Paris this week? Should I bike to work Monday?"
→ Réponse contextualisée avec ta routine mémorisée.
```

Le pattern : **verbe + objet + contexte**. Pas de syntaxe spéciale, pas de commandes.

---

## 2 — Les deux processus complexes

Voici les deux pipelines en un coup d'œil :*(Clique sur chaque étape pour approfondir)*

---

## PROCESS_1 — Blog publishing : les commandes concrètes

**Étape 1 — Idea & brief**
```
"I want to write a blog post about AI coordination tools in newsrooms.
Target: product managers. Tone: practical, no jargon. ~800 words."
```
OpenClaw mémorise ça comme contexte pour toute la suite.

**Étape 2 — Write post**
```
"Write the draft now. Use my preferred structure:
hook → problem → solution → example → CTA.
Save it as draft-ai-newsrooms.md"
```
Il écrit, sauvegarde le fichier sur ta machine. Tu lis, tu corriges directement dans le chat.

**Étape 3 — Generate image**
```
"Generate a default featured image for this post.
Style: clean editorial, navy and white, no text on image.
Use DALL-E. Save as featured-ai-newsrooms.png"
```
Pour ça, OpenClaw doit avoir le skill image generation installé (DALL-E via API ou Flux via un skill communautaire).

**Étape 4 — Publish**
```
"Publish the post to my WordPress blog.
Category: AI & Tools. Tags: AI, newsroom, product management.
Featured image: the PNG we just generated. Status: draft first, I'll review."
```
Il appelle l'API WordPress REST en background. Tu reçois le lien de preview.

---

## PROCESS_2 — Video production : les commandes + les pré-requis

C'est le process le plus complexe. Il requiert des **skills supplémentaires** et potentiellement des outils externes. Voici comment l'aborder.

**Étape 1 — Script**
```
"From the blog post draft-ai-newsrooms.md,
write a video walkthrough script. Format: scene by scene.
Each scene: visual description + narrator text. Max 3 minutes total."
```

**Étape 2 — Screen capture** ← le point d'attention
```
"Record a screen capture of me navigating openclaw.ai.
Use the browser skill. Capture 1080p. Save as walkthrough-raw.mp4"
```
OpenClaw peut piloter le navigateur nativement. Pour la vidéo, il peut déclencher un outil comme `ffmpeg` ou une app de capture installée sur ton Mac (`screencapture` CLI, OBS via script). C'est là que tu commences à construire un **skill personnalisé** si ça n'existe pas encore en communauté.

**Étape 3 — Thumbnail**
```
"Create a YouTube thumbnail for this video.
Title overlay: 'OpenClaw : ton assistant IA personnel'
Style: bold text, dark background, my face placeholder.
Size: 1280x720. Save as thumbnail-yt.png"
```

**Étape 4 — YouTube upload**
```
"Upload walkthrough-raw.mp4 to YouTube.
Title: 'OpenClaw : automatiser sa veille et son blog en 2026'
Description: use the blog post intro, adapted for YouTube.
Thumbnail: thumbnail-yt.png. Visibility: unlisted for now."
```
Pour ça il faut le skill YouTube (via l'API YouTube Data v3, credentials OAuth à configurer une fois).

---

## Le modèle mental PO pour monter en complexité

Pense OpenClaw comme une **équipe de sous-traitants** que tu manages via chat :

| Niveau | Ce que tu fais | Exemple |
|---|---|---|
| **Simple** | Une instruction, un résultat | "Summarize my emails" |
| **Séquentiel** | Tu enchaînes les étapes toi-même | Process 1 ci-dessus |
| **Pipeline automatisé** | Tu demandes à Claw d'enchaîner les étapes seul | "Do the full blog process end to end, show me each output before continuing" |
| **Skill custom** | Tu demandes à Claw d'écrire son propre skill | "Build a skill that does Process 1 in one command" |

Le dernier niveau est la vraie puissance : OpenClaw peut écrire ses propres skills, ce qui veut dire que tu lui décris ton process une fois, et il se programme lui-même pour le reproduire en une commande.

**Pour commencer concrètement :**

```bash
# Installation (tu l'as déjà fait puisque Xcode CLI est ok)
curl -fsSL https://openclaw.ai/install.sh | bash

# Onboarding (choix du LLM, connexion chat app)
openclaw onboard

# Puis depuis Telegram/WhatsApp :
"Hello! What skills do you have installed?"
```

La documentation complète est sur [docs.openclaw.ai](https://docs.openclaw.ai/getting-started) et les skills communautaires sur [clawhub.ai](https://clawhub.ai).