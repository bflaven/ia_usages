# wp_docker

Docker-based WordPress staging environment for testing the Semaphore plugin and related content clustering features.

## Purpose

This directory contains a Docker Compose configuration that creates a local WordPress installation with MySQL and phpMyAdmin. It provides an isolated testing environment for plugin development, allowing you to:

- Test plugin functionality without affecting production sites
- Import production database dumps for realistic testing
- Validate schema markup and breadcrumb generation
- Test tag family CSV imports and semantic clustering
- Debug plugin output in theme sidebar and subfooter

## Stack

- **WordPress**: Latest version
- **MySQL**: Database server for WordPress
- **phpMyAdmin**: Web-based MySQL administration interface

## Usage

### Start the Environment

```bash
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_augmented_journalist_wp_toolkit/wp_docker
docker compose down
docker compose up -d
```

### Access Points

- **WordPress**: [http://localhost:8080](http://localhost:8080)
- **phpMyAdmin**: [http://localhost:8081](http://localhost:8081)

### Stop the Environment

```bash
docker compose down
```

## Configuration

The `docker-compose.yml` file defines:
- WordPress container on port 8080
- MySQL container with persistent volume
- phpMyAdmin container on port 8081
- Network configuration for container communication

## Database Management

Use phpMyAdmin at `localhost:8081` to:
- Import production database dumps
- Update `wp_options` site URLs to `http://localhost:8080`
- Verify tag families table structure
- Check related posts embeddings data
- Monitor plugin database operations

## Testing Workflow

1. Start Docker environment
2. Access WordPress at `localhost:8080`
3. Install/activate Semaphore plugin
4. Import tag families CSV via admin interface
5. Configure related posts embeddings settings
6. Test frontend output in sidebar and subfooter
7. Validate schema markup with Google Rich Results Test
8. Check database changes via phpMyAdmin

## Requirements

- Docker Desktop installed and running
- Available ports 8080 (WordPress) and 8081 (phpMyAdmin)
- Minimum 2GB RAM allocated to Docker

## Notes

- Environment resets between `docker compose down` and `up` unless volumes are configured
- Database credentials defined in `docker-compose.yml`
- Suitable for development and testing only, not production use
