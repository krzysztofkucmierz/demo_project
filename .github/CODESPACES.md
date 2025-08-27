# GitHub Codespaces Setup Guide

This document explains how to configure GitHub Codespaces for optimal performance with this project.

## Automatic Setup

The project includes a `.devcontainer/` configuration that automatically:

- Uses Microsoft's Python 3.13 Dev Container image
- Installs Docker-in-Docker for running PostgreSQL containers
- Installs `uv` package manager globally via custom Dockerfile
- Sets up development tools (Black, MyPy, Flake8, Ruff, etc.)
- Configures VS Code extensions and settings
- Installs project dependencies after workspace is created
- Sets up port forwarding for FastAPI (port 8000) and PostgreSQL (port 5432)

## DevContainer Configuration

### Current Configuration

The project uses a **Docker-in-Docker approach** with the following setup:

```json
{
  "name": "Demo Project Development Environment",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.13-bullseye",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "moby": true,
      "azureDnsAutoDetection": true,
      "installDockerBuildx": true,
      "version": "latest",
      "dockerDashComposeVersion": "v2"
    }
  },
  "forwardPorts": [8000, 5432],
  "postCreateCommand": "bash setup-codespaces.sh",
  "workspaceFolder": "/workspaces/demo_project"
}
```

### Docker-in-Docker Benefits

The Docker-in-Docker feature provides:

- Full Docker daemon running inside the container
- Support for `docker-compose` commands
- Ability to run PostgreSQL container for development
- Container isolation for database testing
- Docker Buildx for advanced build features

### Custom Dockerfile Benefits

The `.devcontainer/Dockerfile` pre-installs:

- PostgreSQL client and libpq-dev for database connectivity
- `uv` package manager installed globally and available to all users
- System dependencies for Python development

### Development Tools Included

The environment comes with a complete Python development stack:

- **Database**: PostgreSQL via Docker with Alembic migrations
- **Package Management**: uv for fast dependency management
- **Code Quality**: Black, isort, Flake8, MyPy, Ruff
- **Testing**: pytest with coverage reporting
- **Database Migrations**: Alembic for schema versioning
- **API Framework**: FastAPI ready for extension

### VS Code Extensions Included

- **ms-python.python**: Python language support
- **ms-python.black-formatter**: Code formatting with Black
- **ms-python.isort**: Import sorting
- **ms-python.mypy-type-checker**: Static type checking
- **ms-python.flake8**: Code linting
- **charliermarsh.ruff**: Fast Python linter
- **GitHub.copilot**: AI code assistance

## Quick Start Guide

### 1. Open in Codespaces

1. Go to the repository on GitHub
2. Click the **Code** button
3. Select **Open with Codespaces**
4. Choose **New codespace** or select an existing one

### 2. Wait for Setup

The container will automatically:
- Build the Python 3.13 environment with Docker support
- Install system dependencies including Docker daemon
- Run `setup-codespaces.sh` to install project dependencies
- Configure VS Code settings

### 3. Start Development

Once setup is complete:

```bash
# Verify Docker is running
docker --version
docker-compose --version

# Start the database
docker-compose up -d

# Verify database container is running
docker ps

# Run database migrations
uv run alembic upgrade head

# Check migration status
uv run alembic current

# Start the FastAPI application
uv run python -m app.main

# Run tests
uv run pytest
```

## Troubleshooting

### Common Issues

1. **Docker daemon not running**:
   ```bash
   # Check if Docker daemon is running
   sudo systemctl status docker
   
   # Start Docker daemon if needed
   sudo systemctl start docker
   
   # Add user to docker group (then restart terminal)
   sudo usermod -aG docker $USER
   ```

2. **Permission denied for Docker**:
   ```bash
   # This should be handled automatically, but if needed:
   sudo chmod 666 /var/run/docker.sock
   ```

3. **Container build fails**: 
   - Check the build logs in the VS Code terminal
   - Try rebuilding the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

4. **uv not found after setup**:
   - The setup script should handle this automatically
   - If needed, run: `bash setup-codespaces.sh` manually

5. **Extensions not loading**:
   - Reload the window: `Ctrl+Shift+P` → "Developer: Reload Window"
   - Check if extensions are installed in the Extensions panel

6. **Database connection issues**:
   - Ensure Docker daemon is running: `docker ps`
   - Start the database: `docker-compose up -d`
   - Check container logs: `docker-compose logs postgres`

### Manual Setup (if needed)

If the automatic setup fails, you can run the setup manually:

```bash
# Navigate to project directory
cd /workspaces/demo_project

# Ensure Docker is running
sudo systemctl start docker

# Run the setup script
bash setup-codespaces.sh

# Install dependencies
uv sync --extra dev --extra test

# Start the database
docker-compose up -d

# Run migrations
uv run alembic upgrade head
```

### Alembic Commands Reference

```bash
# Check current migration status
uv run alembic current

# View migration history
uv run alembic history

# Create new migration
uv run alembic revision --autogenerate -m "Description"

# Upgrade to latest migration
uv run alembic upgrade head

# Downgrade one revision
uv run alembic downgrade -1
```

### Docker-Specific Troubleshooting

```bash
# Check Docker daemon status
sudo systemctl status docker

# View Docker daemon logs
sudo journalctl -u docker.service

# Restart Docker daemon
sudo systemctl restart docker

# Test Docker installation
docker run hello-world

# Check Docker Compose version
docker-compose --version
```

## Setting Up Prebuilds (Recommended)

To speed up Codespace creation with Docker support, you can enable prebuilds in your repository settings:

### 1. Enable Prebuilds in Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** → **Codespaces**
3. Click **Set up prebuild**
4. Configure the prebuild:
   - **Branch**: `main`
   - **Machine type**: `4-core` (recommended for Docker workloads)
   - **Triggers**: Select "On push" and "On configuration change"

### 2. Prebuild Configuration

Create `.github/dependabot.yml` to keep prebuilds updated:

```yaml
version: 2
updates:
  - package-ecosystem: "devcontainers"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 3. Expected Performance

- **Without prebuilds**: ~3-4 minutes for first setup (Docker adds overhead)
- **With prebuilds**: ~60-90 seconds to start coding

## Advanced Configuration

### Resource Allocation for Docker

Docker-in-Docker requires more resources:
- **Minimum**: 2-core, 8GB RAM
- **Recommended**: 4-core, 16GB RAM for smooth development
- **Heavy workloads**: 8-core for performance testing

### Custom Environment Variables

Add environment variables to your Codespace:

1. Go to **Settings** → **Codespaces**
2. Add secrets under **Repository secrets**:
   - `DATABASE_URL`: Custom database connection string
   - `DEBUG`: Set to `true` for development
   - `DOCKER_BUILDKIT`: Set to `1` for faster builds
   - `COMPOSE_DOCKER_CLI_BUILD`: Set to `1` for Docker Compose v2



