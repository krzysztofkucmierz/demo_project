# GitHub Codespaces Setup Guide

This document explains how to configure GitHub Codespaces for optimal performance with this project.

## Automatic Setup

The project includes a `.devcontainer/` configuration that automatically:

- Uses Microsoft's Python 3.13 Dev Container image
- Installs `uv` package manager globally via custom Dockerfile
- Sets up development tools (Black, MyPy, Flake8, Ruff, etc.)
- Configures VS Code extensions and settings
- Installs project dependencies after workspace is created
- Sets up port forwarding for FastAPI on port 8000

## DevContainer Configuration

### Current Configuration

The project uses a **custom Dockerfile approach** with the following setup:

```json
{
  "name": "Demo Project Development Environment",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.13-bullseye",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [8000],
  "postCreateCommand": "bash setup-codespaces.sh",
  "workspaceFolder": "/workspaces/demo_project"
}
```

### Custom Dockerfile Benefits

The `.devcontainer/Dockerfile` pre-installs:

- PostgreSQL client and libpq-dev for database connectivity
- `uv` package manager installed globally and available to all users
- System dependencies for Python development

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
- Build the Python 3.13 environment
- Install system dependencies
- Run `setup-codespaces.sh` to install project dependencies
- Configure VS Code settings

### 3. Start Development

Once setup is complete:

```bash
# Start the database
docker-compose up -d

# Run database migrations
uv run alembic upgrade head

# Start the FastAPI application
uv run python -m app.main

# Run tests
uv run pytest
```

## Troubleshooting

### Common Issues

1. **Container build fails**: 
   - Check the build logs in the VS Code terminal
   - Try rebuilding the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

2. **uv not found after setup**:
   - The setup script should handle this automatically
   - If needed, run: `bash setup-codespaces.sh` manually

3. **Extensions not loading**:
   - Reload the window: `Ctrl+Shift+P` → "Developer: Reload Window"
   - Check if extensions are installed in the Extensions panel

4. **Database connection issues**:
   - Ensure Docker is running: `docker-compose up -d`
   - Check if PostgreSQL container is running: `docker ps`

### Manual Setup (if needed)

If the automatic setup fails, you can run the setup manually:

```bash
# Navigate to project directory
cd /workspaces/demo_project

# Run the setup script
bash setup-codespaces.sh

# Install dependencies
uv sync --extra dev --extra test

# Start the database
docker-compose up -d

# Run migrations
uv run alembic upgrade head
```

## Setting Up Prebuilds (Recommended)

To speed up Codespace creation, you can enable prebuilds in your repository settings:

### 1. Enable Prebuilds in Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** → **Codespaces**
3. Click **Set up prebuild**
4. Configure the prebuild:
   - **Branch**: `main`
   - **Machine type**: `2-core` (sufficient for this project)
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

- **Without prebuilds**: ~2-3 minutes for first setup
- **With prebuilds**: ~30-60 seconds to start coding

## Advanced Configuration

### Custom Environment Variables

Add environment variables to your Codespace:

1. Go to **Settings** → **Codespaces**
2. Add secrets under **Repository secrets**:
   - `DATABASE_URL`: Custom database connection string
   - `DEBUG`: Set to `true` for development

### Resource Allocation

For heavy development work, consider upgrading machine type:
- **2-core**: Standard development (recommended)
- **4-core**: Heavy testing or multiple services
- **8-core**: Performance testing or large datasets

## Tips for Optimal Performance

1. **Use prebuilds** to reduce startup time
2. **Pin specific image versions** in devcontainer.json for consistency
3. **Enable auto-suspend** to save compute credits when idle
4. **Use VS Code settings sync** to maintain your preferences across Codespaces
5. **Install only necessary extensions** to keep container lightweight

## Support

For issues specific to GitHub Codespaces:
- Check [GitHub Codespaces documentation](https://docs.github.com/en/codespaces)
- Report issues in the repository's Issues tab
- For general Codespaces support, contact GitHub Support
