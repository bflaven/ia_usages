# claude.md — Implémentation Opérationnelle

## 🚀 OBJECTIF CLAUDE CODE

Développer **en 4 phases séquentielles** un projet complet de **migration de breadcrumbs WordPress** avec pipeline Python + plugin WordPress.

**Claude Code doit produire** :
- **Pipeline Python** d'analyse/enrichissement,
- **Plugin WordPress** d'édition/validation,
- **Tables SQL** séparées,
- **Fichiers prêts à déployer**.

---

## 📁 STRUCTURE DE FICHIERS À CRÉER

```
breadcrumb-migration/
├── pipeline/
│   ├── requirements.txt
│   ├── config.yaml
│   ├── 01_inventory.py
│   ├── 02_spacy_ner.py
│   ├── 03_wikidata_enrich.py
│   ├── 04_breadcrumb_proposal.py
│   ├── 05_export_wp.py
│   └── run_pipeline.sh
├── plugin/
│   ├── breadcrumb-migration.php
│   ├── includes/
│   │   ├── admin-page.php
│   │   ├── db-tables.php
│   │   ├── ajax-handler.php
│   │   └── breadcrumb-simulator.php
│   ├── assets/
│   │   ├── admin.css
│   │   └── admin.js
│   └── languages/
│       └── breadcrumb-migration-fr_FR.mo
├── sql/
│   ├── create_tables.sql
│   └── sample_data.sql
├── docker/
│   └── docker-compose.staging.yml
└── docs/
    ├── INSTALL.md
    └── USAGE.md
```

---

## 🗄️ SCHÉMA SQL — À CRÉER EN PREMIER

**Claude Code doit générer `sql/create_tables.sql` :**

```sql
-- Table principale : copie des termes originaux
CREATE TABLE wp_breadcrumb_terms (
    id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    wp_term_id BIGINT(20) UNSIGNED NOT NULL,
    taxonomy VARCHAR(32) NOT NULL,
    original_name VARCHAR(200) NOT NULL,
    original_slug VARCHAR(200) NOT NULL,
    original_parent_id BIGINT(20) UNSIGNED NULL,
    content_count INT UNSIGNED DEFAULT 0,
    language VARCHAR(10) DEFAULT 'fr',
    status ENUM('original', 'proposed', 'validated', 'published') DEFAULT 'original',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_wp_term (wp_term_id),
    INDEX idx_taxonomy (taxonomy),
    INDEX idx_status (status)
);

-- Table des propositions enrichies
CREATE TABLE wp_breadcrumb_proposals (
    id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    term_id BIGINT(20) UNSIGNED NOT NULL,
    proposed_name VARCHAR(200),
    proposed_slug VARCHAR(200),
    proposed_description TEXT,
    proposed_parent_id BIGINT(20) UNSIGNED NULL,
    proposed_language VARCHAR(10) DEFAULT 'fr',
    spacy_entity VARCHAR(32),
    wikidata_id VARCHAR(50),
    proposed_breadcrumb TEXT,
    validation_state ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    validated_by BIGINT(20) UNSIGNED NULL,
    validated_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (term_id) REFERENCES wp_breadcrumb_terms(id),
    INDEX idx_term (term_id),
    INDEX idx_validation (validation_state)
);

-- Table des redirections
CREATE TABLE wp_breadcrumb_redirects (
    id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    original_url VARCHAR(500) NOT NULL,
    new_url VARCHAR(500) NOT NULL,
    term_id BIGINT(20) UNSIGNED NULL,
    taxonomy VARCHAR(32),
    is_active BOOLEAN DEFAULT TRUE,
    redirect_type ENUM('301', '302') DEFAULT '301',
    hit_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 PHASE 1 — PIPELINE PYTHON (PRIORITÉ 1)

**Claude Code doit créer ces 6 scripts dans `pipeline/` :**

### 1. `requirements.txt`
```
spacy==3.7.2
pandas==2.2.1
requests==2.31.0
pyyaml==6.0.1
mysql-connector-python==8.2.0
python-dotenv==1.0.0
fr_core_news_sm @ https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-3.7.0/fr_core_news_sm-3.7.0-py3-none-any.whl
```

### 2. `config.yaml`
```yaml
database:
  host: "localhost"
  user: "wordpress"
  password: "password"
  database: "wordpress"
  wp_prefix: "wp_"

wikidata:
  base_url: "https://www.wikidata.org/w/api.php"
  search_limit: 3

spacy:
  model: "fr_core_news_sm"
  entity_types: ["PERSON", "ORG", "GPE", "LOC", "PRODUCT", "EVENT"]
```

### 3. `01_inventory.py` — Lister taxonomies
```python
# Récupère toutes les categories et post_tag
# Export CSV + insertion wp_breadcrumb_terms
```

### 4. `02_spacy_ner.py` — Analyse NER
```python
# Pour chaque terme, extraire entité Spacy
# Mettre à jour wp_breadcrumb_terms.spacy_entity
```

### 5. `03_wikidata_enrich.py` — Recherche Wikidata
```python
# Pour chaque terme, chercher sur Wikidata
# Stocker meilleur candidat dans wp_breadcrumb_terms
```

### 6. `05_export_wp.py` — Préparer plugin
```python
# Générer propositions dans wp_breadcrumb_proposals
# Créer structure breadcrumb
```

---

## 🎛️ PHASE 2 — PLUGIN WORDPRESS (PRIORITÉ 2)

**Claude Code doit créer `plugin/breadcrumb-migration.php` :**

```php
<?php
/*
Plugin Name: Breadcrumb Migration
Description: Éditeur de taxonomies et breadcrumbs
Version: 1.0.0
*/

// 1. Activation : créer tables SQL
register_activation_hook(__FILE__, 'bm_create_tables');

// 2. Menu admin unique
add_action('admin_menu', 'bm_admin_menu');
function bm_admin_menu() {
    add_menu_page(
        'Breadcrumb Migration',
        'Breadcrumb Migration',
        'manage_options',
        'breadcrumb-migration',
        'bm_admin_page',
        'dashicons-admin-links'
    );
}

// 3. Page admin principale
function bm_admin_page() {
    include plugin_dir_path(__FILE__) . 'includes/admin-page.php';
}

// 4. AJAX handlers
add_action('wp_ajax_bm_validate_proposal', 'bm_ajax_validate');
add_action('wp_ajax_bm_simulate_breadcrumb', 'bm_ajax_simulate');
```

### Interface Admin (UX Mapping)
**Tableau 2 colonnes** :
```
| ORIGINAL                          | PROPOSÉ / VALIDÉ                   |
|-----------------------------------|------------------------------------|
| ID: 123                           | ID: 123                           |
| Nom: ux-experience-utilisateur    | Nom: UX User Experience           |
| Slug: ux-experience-utilisateur   | Slug: ux-user-experience ✓        |
| Parent: -                         | Parent: AI (ID: 45) ✓             |
| Nb posts: 12                      | Nb posts: 12                      |
| Spacy: ORG                        | Spacy: ORG ✓                      |
| Wikidata: -                       | Wikidata: Q123 ✓                  |
|                                   |                                    |
| [SIMULER] [VALIDER] [REJETER]     | [ÉDITER] [PUBLIER]                |
```

---

## 🎨 ASSETS — À GÉNÉRER

### `assets/admin.css`
```css
/* Design mapping responsive 2 colonnes */
/* Boutons validation colorés */
/* Prévisualisation breadcrumb cliquable */
```

### `assets/admin.js`
```javascript
// AJAX pour simulation
// Drag & drop mapping
// Validation en temps réel
// Prévisualisation live
```

---

## 🧪 PHASE 3 — TESTS & DOCKER

**Claude Code doit créer `docker/docker-compose.staging.yml` :**

```yaml
version: '3.8'
services:
  wordpress:
    image: wordpress:6.5
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - ./plugin:/var/www/html/wp-content/plugins/breadcrumb-migration
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
  pipeline:
    build: .
    volumes:
      - ./pipeline:/app
    depends_on:
      - db
```

---

## 📋 BACKLOG CLAUDE CODE — ORDRE EXACT

### ✅ **PHASE 1 : Pipeline (2h)**
```
[ ] 1. sql/create_tables.sql
[ ] 2. pipeline/requirements.txt
[ ] 3. pipeline/config.yaml  
[ ] 4. pipeline/01_inventory.py
[ ] 5. pipeline/run_pipeline.sh
[ ] 6. docker/docker-compose.staging.yml
```

### ✅ **PHASE 2 : Plugin Core (3h)**
```
[ ] 7. plugin/breadcrumb-migration.php
[ ] 8. plugin/includes/db-tables.php
[ ] 9. plugin/includes/admin-page.php
[ ] 10. assets/admin.css
```

### ✅ **PHASE 3 : UX & AJAX (2h)**
```
[ ] 11. assets/admin.js
[ ] 12. plugin/includes/ajax-handler.php
[ ] 13. plugin/includes/breadcrumb-simulator.php
```

### ✅ **PHASE 4 : Enrichissement (2h)**
```
[ ] 14. pipeline/02_spacy_ner.py
[ ] 15. pipeline/03_wikidata_enrich.py
[ ] 16. pipeline/04_breadcrumb_proposal.py
```

### ✅ **PHASE 5 : Publication (1h)**
```
[ ] 17. docs/INSTALL.md
[ ] 18. docs/USAGE.md
[ ] 19. Tests sur Docker staging
```

---

## 🎯 CRITÈRES D'ACCEPTATION PAR FICHIER

| Fichier | Critères |
|---------|----------|
| `create_tables.sql` | 3 tables créées, clés étrangères, index |
| `01_inventory.py` | Liste 100% taxonomies, export CSV |
| `breadcrumb-migration.php` | Menu admin visible `/wp-admin/admin.php?page=breadcrumb-migration` |
| `admin-page.php` | Tableau 2 colonnes, boutons fonctionnels |
| `admin.js` | AJAX simulation breadcrumb live |
| `02_spacy_ner.py` | 80% termes analysés avec entité |
| `03_wikidata_enrich.py` | Recherche API, stockage meilleur candidat |

---

## 🚀 COMMANDE DE DÉPLOIEMENT

```bash
# 1. Staging
docker-compose -f docker/docker-compose.staging.yml up -d

# 2. Pipeline
cd pipeline && ./run_pipeline.sh

# 3. Plugin
wp plugin activate breadcrumb-migration

# 4. Admin
https://localhost:8080/wp-admin/admin.php?page=breadcrumb-migration
```

---

## 📞 INSTRUCTIONS CLAUDE CODE

**Commence par PHASE 1** et produis **un fichier à la fois**.

**Pour chaque fichier** :
```
1. Écris le code complet et fonctionnel
2. Explique son rôle (2 lignes)
3. Donne la commande de test
4. Passe au suivant
```

**NE PAS** :
- Modifier les tables WordPress originales
- Publier sans validation manuelle
- Oublier les redirections 301
- Créer de code incomplet

**DOIT FONCTIONNER** :
- Sur WordPress 6.5+
- Avec MySQL 8.0
- Python 3.11+
- Docker Compose 2.0+

**PREMIER FICHIER À CRÉER** : `sql/create_tables.sql`
