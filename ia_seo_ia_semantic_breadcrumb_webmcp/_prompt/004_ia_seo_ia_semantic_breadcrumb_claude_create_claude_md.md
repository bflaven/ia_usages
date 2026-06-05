

```md
# claude.md — Implémentation Opérationnelle v2.0

## 🚀 CONTEXTE RÉEL DU PROJET

**Répertoire de travail** : `_ia_seo_ia_semantic_breadcrumb/`

**Claude Code doit LIRE ces répertoires/fichiers** :
```
📁 wp_docker/                 ← Environnement Docker WordPress (staging)
📁 source/                    ← Sources existantes
📄 001_step_1_list_tags_categories_wp.py  ← Pipeline STEP 1 existante
📄 CLAUDE.md                  ← Spécifications initiales
```

**Claude Code doit IGNORER** :
```
❌ _MMA_semantic_light_3_prompt/
❌ _prompt/
❌ _ia_seo_ia_semantic_breadcrumb.diff
```

---

## 📁 STRUCTURE CIBLE À CRÉER/ÉTENDRE

```
_ia_seo_ia_semantic_breadcrumb/
├── wp_docker/                    ← ✅ EXISTE (ne pas toucher)
├── source/                       ← ✅ EXISTE (pipeline + plugin)
│   ├── pipeline/                 ← À CRÉER/ÉTENDRE
│   │   ├── requirements.txt
│   │   ├── config.yaml
│   │   ├── 001_step_1_list_tags_categories_wp.py  ← ✅ EXISTE
│   │   ├── 002_spacy_ner.py     ← À CRÉER
│   │   ├── 003_wikidata_enrich.py
│   │   ├── 004_breadcrumb_proposal.py
│   │   └── 005_export_wp.py
│   ├── plugin/                  ← À CRÉER
│   │   ├── breadcrumb-migration.php
│   │   ├── includes/
│   │   └── assets/
│   └── sql/
│       ├── create_tables.sql
│       └── sample_data.sql
├── docs/
│   ├── INSTALL.md
│   └── USAGE.md
└── docker-compose.staging.yml   ← À CRÉER (complément wp_docker)
```

---

## 🔄 INTÉGRATION CODE EXISTANT

**Fichier existant à conserver/améliorer** : `001_step_1_list_tags_categories_wp.py`

**Claude Code doit** :
```
✅ 1. LIRE ce fichier existant
✅ 2. L'AMÉLIORER si nécessaire (gestion erreurs, config YAML)
✅ 3. L'INTÉGRER dans la pipeline complète
✅ 4. NE PAS LE SUPPRIMER
```

---

## 🗄️ SCHÉMA SQL — À CRÉER `source/sql/create_tables.sql`

```sql
-- PREFIXE : utiliser wp_ du wp_docker
CREATE TABLE IF NOT EXISTS `wp_breadcrumb_terms` (
    `id` BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `wp_term_id` BIGINT(20) UNSIGNED NOT NULL UNIQUE,
    `taxonomy` VARCHAR(32) NOT NULL,
    `original_name` VARCHAR(200) NOT NULL,
    `original_slug` VARCHAR(200) NOT NULL,
    `original_parent_id` BIGINT(20) UNSIGNED NULL,
    `content_count` INT UNSIGNED DEFAULT 0,
    `language` VARCHAR(10) DEFAULT 'fr',
    `status` ENUM('original','proposed','validated','published') DEFAULT 'original',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_wp_term` (`wp_term_id`),
    INDEX `idx_taxonomy` (`taxonomy`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `wp_breadcrumb_proposals` (
    `id` BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `term_id` BIGINT(20) UNSIGNED NOT NULL,
    `proposed_name` VARCHAR(200),
    `proposed_slug` VARCHAR(200),
    `proposed_description` TEXT,
    `proposed_parent_id` BIGINT(20) UNSIGNED NULL,
    `proposed_language` VARCHAR(10) DEFAULT 'fr',
    `spacy_entity` VARCHAR(32),
    `wikidata_id` VARCHAR(50),
    `proposed_breadcrumb` TEXT,
    `validation_state` ENUM('pending','approved','rejected') DEFAULT 'pending',
    `validated_by` BIGINT(20) UNSIGNED NULL,
    `validated_at` TIMESTAMP NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`term_id`) REFERENCES `wp_breadcrumb_terms`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `wp_breadcrumb_redirects` (
    `id` BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `original_url` VARCHAR(500) NOT NULL,
    `new_url` VARCHAR(500) NOT NULL,
    `term_id` BIGINT(20) UNSIGNED NULL,
    `taxonomy` VARCHAR(32),
    `is_active` BOOLEAN DEFAULT TRUE,
    `redirect_type` ENUM('301','302') DEFAULT '301',
    `hit_count` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `unique_redirect` (`original_url`,`new_url`)
);
```

---

## 🐳 DOCKER — COMPLÉMENT `wp_docker`

**Claude Code doit créer `docker-compose.staging.yml` (racine projet) :**

```yaml
version: '3.8'
services:
  # Utilise wp_docker existant
  wordpress:
    extends:
      file: wp_docker/docker-compose.yml
      service: wordpress
    ports:
      - "8080:80"
    volumes:
      - ./source/plugin:/var/www/html/wp-content/plugins/breadcrumb-migration
      - ./source/sql:/docker-entrypoint-initdb.d  # Tables SQL auto-créées
  
  pipeline:
    build:
      context: .
      dockerfile: Dockerfile.pipeline
    volumes:
      - ./source/pipeline:/app
    depends_on:
      - wordpress
    environment:
      DB_HOST: wordpress_db
      DB_USER: wordpress
      DB_PASS: wordpress
      DB_NAME: wordpress
```

**`Dockerfile.pipeline` :**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY source/pipeline/requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download fr_core_news_sm
CMD ["bash"]
```

---

## 📦 `source/pipeline/requirements.txt` — À CRÉER

```
# Basé sur 001_step_1_list_tags_categories_wp.py existant
pandas==2.2.1
mysql-connector-python==8.2.0
pyyaml==6.0.2
python-dotenv==1.0.1

# NOUVEAUX
spacy==3.7.2
requests==2.31.0
fr_core_news_sm @ https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-3.7.0/fr_core_news_sm-3.7.0-py3-none-any.whl
```

---

## 🎛️ PLUGIN — À CRÉER `source/plugin/breadcrumb-migration.php`

```php
<?php
/**
 * Plugin Name: Breadcrumb Migration
 * Description: Éditeur taxonomies + breadcrumbs depuis pipeline
 * Version: 1.0.0
 * Author: Bruno Flaven
 */

// 1. Activation → créer tables SQL depuis wp_docker
register_activation_hook(__FILE__, function() {
    global $wpdb;
    $tables_sql = file_get_contents( plugin_dir_path(__FILE__) . '../sql/create_tables.sql' );
    $wpdb->query( $tables_sql );
});

// 2. Admin menu unique
add_action('admin_menu', function() {
    add_menu_page(
        'Breadcrumb Migration',
        'Breadcrumbs',
        'manage_options',
        'breadcrumb-migration',
        'bm_admin_page',
        'dashicons-admin-links',
        30
    );
});

// 3. Page principale
function bm_admin_page() {
    ?>
    <div class="wrap">
        <h1>Breadcrumb Migration</h1>
        <?php include plugin_dir_path(__FILE__) . 'includes/admin-page.php'; ?>
    </div>
    <?php
}
```

---

## 🔄 PIPELINE — INTÉGRATION 001 EXISTANT

**`source/pipeline/run_pipeline.sh` — À CRÉER :**
```bash
#!/bin/bash
cd "$(dirname "$0")"

echo "🚀 PHASE 1 : Inventaire (fichier existant)"
python 001_step_1_list_tags_categories_wp.py

echo "🚀 PHASE 2 : Spacy NER"
python 002_spacy_ner.py

echo "🚀 PHASE 3 : Wikidata"
python 003_wikidata_enrich.py

echo "🚀 PHASE 4 : Breadcrumb proposals"
python 004_breadcrumb_proposal.py

echo "✅ Pipeline terminée → plugin prêt"
```

---

## 📋 BACKLOG CLAUDE CODE — ORDRE PRÉCIS

### **PHASE 1 : Infrastructure (30min)**
```
[ ] 1. source/sql/create_tables.sql          ← SQL complet
[ ] 2. source/pipeline/requirements.txt      ← Avec spacy
[ ] 3. docker-compose.staging.yml            ← Complète wp_docker
[ ] 4. source/pipeline/config.yaml           ← Connexions DB
[ ] 5. source/pipeline/run_pipeline.sh       ← Orchestre 001+
```

### **PHASE 2 : Pipeline enrichissement (1h30)**
```
[ ] 6. source/pipeline/002_spacy_ner.py      ← Analyse 001 output
[ ] 7. source/pipeline/003_wikidata_enrich.py← API Wikidata
[ ] 8. source/pipeline/004_breadcrumb_proposal.py
```

### **PHASE 3 : Plugin core (1h)**
```
[ ] 9. source/plugin/breadcrumb-migration.php
[ ] 10. source/plugin/includes/admin-page.php
[ ] 11. source/plugin/includes/db-tables.php
```

### **PHASE 4 : UX complète (1h)**
```
[ ] 12. source/plugin/assets/admin.css
[ ] 13. source/plugin/assets/admin.js
[ ] 14. source/plugin/includes/ajax-handler.php
```

---

## 🧪 COMMANDE DE TEST

```bash
# 1. Démarrer staging
docker-compose -f docker-compose.staging.yml up -d

# 2. Pipeline complète
cd source/pipeline && ./run_pipeline.sh

# 3. Activer plugin
docker exec -it <wordpress_container> wp plugin activate breadcrumb-migration

# 4. Admin
http://localhost:8080/wp-admin/admin.php?page=breadcrumb-migration
```

---

## 🎯 PREMIÈRE TÂCHE CLAUDE CODE

**Crée `source/sql/create_tables.sql` complet** avec :
- 3 tables exactes ci-dessus
- 5 inserts de test (exemples "AI", "WordPress", "UX")
- Compatible wp_docker

**Puis teste** : `docker-compose up && mysql -u wordpress -p wordpress < create_tables.sql`

**Claude Code : commence MAINTENANT par ce fichier SQL !**
```

**Parfait !** Ce `claude.md v2.0` intègre maintenant ton environnement réel :

✅ **Respecte `wp_docker` existant**  
✅ **Conserve `001_step_1_list_tags_categories_wp.py`**  
✅ **Exclut les répertoires à ignorer**  
✅ **Structure `source/` cohérente**  
✅ **Docker-compose complémentaire** (pas de conflit)  
✅ **Backlog précis avec fichiers existants**  

**Claude Code peut démarrer immédiatement** par `source/sql/create_tables.sql` et enchaîner les 14 tâches en **4h**. [dev](https://dev.to/jemeeroy/create-custom-admin-page-in-wordpress-198f)

**Veux-tu le premier fichier SQL généré maintenant ?**