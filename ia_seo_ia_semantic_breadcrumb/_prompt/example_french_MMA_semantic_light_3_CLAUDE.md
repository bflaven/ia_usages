# CLAUDE.md — MMA_semantic_light_3

## CONTEXTE

Migration d'un pipeline NLP de traitement et enrichissement de tags éditoriaux vers une architecture propre, testable et multi-services.

Les répertoires sources de référence sont en dehors de MMA_semantic_light_3.
Claude Code travaille **en écriture uniquement dans MMA_semantic_light_3/**.
Les répertoires `_archives/` et `_prompt/` présents dans MMA_semantic_light_3
sont **exclus** — ne pas les lire, ne pas les modifier.

Le pipeline traite des tags thématiques (ThemaTag) issus de médias du groupe
France Médias Monde : France 24 FR, RFI FR, Monte Carlo Doualiya, etc.
Chaque combinaison marque/langue est appelée un **service** (ex. `F24_FR`).

---

## ENVIRONNEMENT TECHNIQUE

- Conda : `tags_treatment`, Python 3.9.13
- Pas de syntaxe Python 3.10+ (pas de `match/case`, pas de `X | Y` pour les types)
- Séparateur CSV : point-virgule (`;`)
- Encodage CSV sources : `utf-8-sig` (gestion BOM)
- Encodage JSON : `utf-8`
- Logs : `logging` standard, jamais de `print()` dans les scripts de pipeline
- Dépendances : `pyyaml`, `requests`, `sentence-transformers`, `scikit-learn`,
  `spacy`, `streamlit`, `pandas`

---

## RÈGLES ABSOLUES AVANT DE CODER

1. **Proposer avant d'écrire** : pour chaque décision d'architecture non
   triviale, présenter les options et attendre validation.

2. **Zéro valeur métier hardcodée** dans les scripts Python. Une chaîne
   de caractères qui est un nom de rubrique, un nom de tag, un chemin de
   fichier, un endpoint API dans un script = bug. Tout passe par les YAML.

3. **Zéro duplication** de constantes entre scripts. Si deux scripts ont
   besoin de la même valeur, elle vit dans un YAML et les deux scripts la
   chargent via `config/loader.py`.

4. **Chaque script est autonome** et exécutable seul via `python step_NNN_...py
   --service F24_FR`. Le `run_pipeline.py` est un orchestrateur optionnel,
   pas un prérequis.

5. **Lint avant livraison** : vérifier avec `python -c "import ast; ast.parse(
   open('fichier.py').read())"` que chaque script est syntaxiquement valide.

---

## NOMENCLATURE DES SCRIPTS

```
step_NNN_PHASE_NOM_COURT.py
```

Liste complète dans l'ordre d'exécution :

```
step_001_COLLECT_api_tags.py
step_002_COLLECT_prepare_stats_call.py
step_003_COLLECT_api_stats.py
step_004_COLLECT_consolidate_tags_stats.py
step_005_ORTHO_spell_check.py
step_006_WIKIDATA_lookup.py
step_007_WIKIDATA_enrichment.py
step_008_CLASS_bucket_b.py
step_009_CLASS_embedding.py
step_010_CLASS_clustering_breadcrumb.py
step_011_PICQ_ingest_csv.py
step_012_PICQ_breadcrumb_merge.py
step_013_PICQ_streamlit_review.py

check_pipeline.py       ← état global de la pipeline
run_pipeline.py         ← orchestrateur optionnel
lint_config.py          ← vérifie l'absence de valeurs hardcodées
```

---

## STRUCTURE DES RÉPERTOIRES

```
MMA_semantic_light_3/
│
├── CLAUDE.md                        ← ce fichier
│
├── config/
│   ├── loader.py                    ← chargement YAML, point d'entrée unique
│   ├── pipeline.yaml                ← paramètres globaux (dry_run, cap_tags)
│   ├── csv_schema.yaml              ← contrat de colonnes des 5 CSV sources
│   ├── F24_FR/
│   │   ├── paths.yaml               ← tous les chemins du service
│   │   ├── taxonomy.yaml            ← ARBO_PRIMAIRE, CANONICAL_C1, C1_STABLE
│   │   ├── editorial_rules.yaml     ← règles slides 3, 6, 7, 8
│   │   └── api.yaml                 ← endpoints Mezzo, timeout, retry
│   ├── RFI_FR/
│   │   └── ...                      ← même structure, contenu différent
│   └── F24_AR/
│       └── ...
│
├── data/
│   └── F24_FR/
│       ├── step_01_collect/
│       │   ├── tags/                ← step_001 output
│       │   ├── stats/               ← step_003 output
│       │   ├── consolidated/        ← step_004 output
│       │   └── consolidated_ortho/  ← step_005 output  ← INPUT step_006
│       ├── step_02_wikidata/
│       │   ├── lookup/              ← step_006 output  ← INPUT step_007
│       │   └── enrichment/          ← step_007 output  ← INPUT step_008
│       ├── step_03_classification/
│       │   ├── bucket_b/            ← step_008 output  ← INPUT step_009
│       │   ├── embedding/           ← step_009 output  ← INPUT step_010
│       │   └── clustering/          ← step_010 output  ← INPUT step_011
│       └── step_04_picq/
│           ├── artefacts/           ← step_011 output  ← INPUT step_012
│           ├── chunks/              ← step_012 output (chunks)
│           └── final/               ← step_012 output final JSON + stats
│
├── source_csv/
│   └── F24_FR/
│       ├── 001_sheet_1_vue_d_ensemble.csv
│       ├── 002_sheet_2_arbo_stable_recommandee.csv
│       ├── 003_sheet_3_sous_rubriques_candidates.csv
│       ├── 004_sheet_4_dossiers_candidates.csv
│       └── 005_sheet_5_mapping_exhaustif.csv    ← sans chiffre de volumétrie
│
├── step_001_COLLECT_api_tags.py
├── step_002_COLLECT_prepare_stats_call.py
├── ...
├── step_013_PICQ_streamlit_review.py
├── check_pipeline.py
├── run_pipeline.py
└── lint_config.py
```

---

## TEMPLATE DOCSTRING — À APPLIQUER À TOUS LES SCRIPTS

```python
"""
step_NNN_PHASE_NOM_COURT.py
===========================
PHASE   : NOM_PHASE
INPUT   : data/{service}/step_XX_.../
OUTPUT  : data/{service}/step_XX_.../
          data/{service}/step_XX_.../_manifest.json
CONFIG  : config/{service}/paths.yaml
          config/pipeline.yaml

DESCRIPTION :
    Texte clair sur ce que fait le script, pourquoi, et ce qu'on obtient.

CAPPING :
    Oui / Non — si Oui, expliquer où dans pipeline.yaml ou api.yaml.

DRY-RUN :
    Oui / Non — si Oui, expliquer ce qui est simulé et ce qui n'est pas écrit.

USAGE :
    python step_NNN_PHASE_NOM_COURT.py --service F24_FR
    python step_NNN_PHASE_NOM_COURT.py --service F24_FR --dry-run
    python step_NNN_PHASE_NOM_COURT.py --service F24_FR --dry-run --cap 50

AUTEUR  : Bruno Flaven — FMM / DEN
VERSION : 3.0 (MMA_semantic_light_3)
PYTHON  : 3.9.x — pas de syntaxe 3.10+
"""
```

---

## MÉCANISME DE CAPPING

Le cap s'applique au **nombre de tags qui entrent dans le step** — les mêmes
N tags traversent toute la pipeline de bout en bout. C'est le seul moyen de
valider le fonctionnement de bout en bout sans attendre le traitement complet.

Règle : si `cap_tags` est défini, le script charge le fichier d'input en
entier mais ne traite que les N premiers tags. Le fichier d'output ne contient
que ces N tags. Les steps suivants héritent automatiquement du cap.

```yaml
# config/pipeline.yaml
dry_run: false
cap_tags: null          # null = production complète, N = test sur N tags
cap_applies_to:         # steps concernés par le cap (API uniquement)
  - step_006            # Wikidata lookup
  - step_007            # Wikidata enrichment
  - step_001            # API Mezzo tags
  - step_002            # API Mezzo prepare stats
  - step_003            # API Mezzo stats
```

Les steps purement locaux (008, 009, 010, 011, 012) héritent du cap via
le fichier d'input — si l'input contient N tags, ils traitent N tags.

---

## MÉCANISME DE DRY-RUN

Un dry-run :
- Lit les fichiers d'input normalement
- Affiche ce qu'il ferait (fichiers à écrire, nombre de tags, endpoints appelés)
- N'appelle aucune API externe
- N'écrit aucun fichier (ni output, ni manifest)
- Se termine avec `log.info("DRY-RUN terminé — aucun fichier écrit.")`

Toujours compatible avec `--cap N` pour simuler un run sur N tags.

---

## MANIFEST PAR STEP

Chaque step écrit un `_manifest.json` dans son répertoire d'output :

```json
{
  "step": "step_006_WIKIDATA_lookup",
  "service": "F24_FR",
  "executed_at": "2026-03-24T16:25:06",
  "status": "OK",
  "input_file": "data/F24_FR/step_01_collect/consolidated_ortho/ortho_FRANCE24_FR_...json",
  "input_tags_total": 4709,
  "input_tags_capped": 50,
  "output_file": "data/F24_FR/step_02_wikidata/lookup/lookup_F24_FR_2026-03-24.json",
  "output_tags": 50,
  "dry_run": false,
  "duration_seconds": 142
}
```

`check_pipeline.py` lit tous les manifests et affiche l'état global.

---

## CHARGEMENT DE LA CONFIGURATION

Un seul point d'entrée pour tous les scripts :

```python
from config.loader import load_config
cfg = load_config("F24_FR")   # remplacer par "RFI_FR" pour un autre service
```

`loader.py` fusionne `pipeline.yaml` + `paths.yaml` + `taxonomy.yaml` +
`editorial_rules.yaml` + `api.yaml` et retourne un dict unique.
Il valide la présence des clés obligatoires et lève une erreur explicite
si une clé manque.

---

## ARGUMENTS CLI STANDARDS

Tous les scripts acceptent les mêmes arguments :

```
--service   SERVICE    Identifiant du service (ex. F24_FR). Obligatoire.
--dry-run              Active le dry-run. Aucun fichier écrit, aucune API appelée.
--cap       N          Limite le traitement aux N premiers tags.
--verbose              Log niveau DEBUG (défaut : INFO).
```

Utiliser `argparse`. Pas de `sys.argv` direct.

---

## FICHIERS DE CONFIGURATION YAML À CRÉER

### config/pipeline.yaml
Paramètres globaux applicables à tous les services et tous les steps.

### config/csv_schema.yaml
Contrat de colonnes pour chacun des 5 CSV sources. Sert à valider les CSV
d'un nouveau service avant de lancer la pipeline.

### config/F24_FR/paths.yaml
Tous les chemins : répertoires d'input/output de chaque step, chemins CSV.
Aucun chemin ne doit apparaître dans les scripts Python.

### config/F24_FR/taxonomy.yaml
- `arbo_primaire` : dict rubrique → liste sous-rubriques
- `c1_stable` : liste des 10 rubriques stables
- `canonical_c1` : dict variantes → forme canonique
- `couche_map` : dict objet_cible_recommande → couche int

### config/F24_FR/editorial_rules.yaml
- `hors_arbo` : liste (slides 3 & 5)
- `a_transformer_en_dossier` : liste (slide 8)
- `tags_promouvoir` : liste (slide 6)
- `tags_secondaires` : liste (slide 7)
- `type_tag_values` : liste des valeurs possibles de type_tag

### config/F24_FR/api.yaml
- Endpoint Mezzo tags
- Endpoint Mezzo stats
- Endpoint Wikidata
- Timeout, retry, délai entre requêtes

---

## ORDRE DE TRAVAIL RECOMMANDÉ POUR CLAUDE CODE

1. Créer la structure de répertoires complète (vide).
2. Créer `config/loader.py` et les 5 fichiers YAML pour F24_FR.
3. Créer `check_pipeline.py` et `lint_config.py`.
4. Migrer les scripts step par step dans l'ordre 001 → 013,
   en appliquant à chaque fois : docstring template, suppression des
   valeurs hardcodées, ajout --cap / --dry-run / --verbose, manifest.
5. Créer `run_pipeline.py` en dernier.
6. Valider la syntaxe de tous les scripts.
7. Produire un `README.md` récapitulatif.

Ne pas passer à l'étape N+1 sans validation de l'étape N.


