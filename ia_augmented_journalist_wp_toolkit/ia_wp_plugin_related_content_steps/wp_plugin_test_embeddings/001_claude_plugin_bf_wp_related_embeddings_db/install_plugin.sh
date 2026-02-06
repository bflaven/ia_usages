#!/bin/bash
# Installation script for BF Related Posts via Embeddings plugin
# Usage: ./install_plugin.sh [container-name]

CONTAINER_NAME=${1:-wordpress}
PLUGIN_NAME="bf_wp_related_embeddings_db"
PLUGIN_DIR="/var/www/html/wp-content/plugins/${PLUGIN_NAME}"

echo "========================================="
echo "BF Related Posts Embeddings Installer"
echo "========================================="
echo "Container: ${CONTAINER_NAME}"
echo "Plugin directory: ${PLUGIN_DIR}"
echo ""

# Check if container exists
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Error: Container '${CONTAINER_NAME}' not found or not running"
    echo "Available containers:"
    docker ps --format '{{.Names}}'
    exit 1
fi

echo "✓ Container found"

# Create plugin directory
echo "Creating plugin directory..."
docker exec ${CONTAINER_NAME} mkdir -p ${PLUGIN_DIR}

# Copy plugin files
echo "Copying plugin files..."
docker cp bf_wp_related_embeddings_db.php ${CONTAINER_NAME}:${PLUGIN_DIR}/
docker cp uninstall.php ${CONTAINER_NAME}:${PLUGIN_DIR}/

# Set permissions
echo "Setting permissions..."
docker exec ${CONTAINER_NAME} chown -R www-data:www-data ${PLUGIN_DIR}
docker exec ${CONTAINER_NAME} chmod -R 755 ${PLUGIN_DIR}

# Verify files
echo ""
echo "Verifying installation..."
docker exec ${CONTAINER_NAME} ls -lh ${PLUGIN_DIR}

echo ""
echo "========================================="
echo "✓ Plugin files installed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Go to WordPress Admin → Plugins"
echo "2. Activate 'BF Related Posts via Embeddings (DB)'"
echo "3. Check Settings → Related Embeddings to verify table creation"
echo "4. Import your CSV file"
echo ""
echo "To view debug logs, run:"
echo "  docker logs -f ${CONTAINER_NAME} 2>&1 | grep bf_wp_related_embeddings_db"
echo ""
