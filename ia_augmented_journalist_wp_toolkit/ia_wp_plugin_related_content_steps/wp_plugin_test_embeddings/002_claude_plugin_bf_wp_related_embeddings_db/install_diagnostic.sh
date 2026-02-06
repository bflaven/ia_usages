#!/bin/bash
# Quick Diagnostic Installation Script
# For BF Related Posts via Embeddings Plugin

CONTAINER_NAME=${1:-wordpress}
PLUGIN_DIR="/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db"

echo "========================================="
echo "BF Related Posts - DIAGNOSTIC MODE"
echo "========================================="
echo "Container: ${CONTAINER_NAME}"
echo ""

# Check if container exists
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Error: Container '${CONTAINER_NAME}' not found"
    echo "Available containers:"
    docker ps --format '{{.Names}}'
    exit 1
fi

echo "Step 1: Backing up current plugin file..."
docker exec ${CONTAINER_NAME} cp ${PLUGIN_DIR}/bf_wp_related_embeddings_db.php ${PLUGIN_DIR}/bf_wp_related_embeddings_db.php.backup 2>/dev/null || echo "  (no existing file to backup)"

echo "Step 2: Installing diagnostic version..."
docker cp bf_wp_related_embeddings_db_diagnostic.php ${CONTAINER_NAME}:${PLUGIN_DIR}/bf_wp_related_embeddings_db.php

echo "Step 3: Setting permissions..."
docker exec ${CONTAINER_NAME} chown www-data:www-data ${PLUGIN_DIR}/bf_wp_related_embeddings_db.php

echo ""
echo "========================================="
echo "✓ Diagnostic version installed!"
echo "========================================="
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Open a NEW terminal window and run this command to watch logs:"
echo "   docker logs -f ${CONTAINER_NAME} 2>&1 | grep bf_wp_related_embeddings_db"
echo ""
echo "2. In WordPress Admin:"
echo "   - Go to Plugins"
echo "   - Deactivate the plugin if active"
echo "   - Activate 'BF Related Posts via Embeddings (DB) - DIAGNOSTIC'"
echo ""
echo "3. Watch the logs in the other terminal window"
echo "   You'll see detailed diagnostic information about:"
echo "   - Database connection"
echo "   - Permission checks"
echo "   - Three different table creation attempts"
echo "   - Any error messages"
echo ""
echo "4. Go to Settings → Related Embeddings to see the status"
echo ""
echo "If table creation fails, follow the instructions in DIAGNOSTIC_GUIDE.md"
echo ""
