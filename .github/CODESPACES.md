# GitHub Codespaces Setup Guide

This document explains how to configure GitHub Codespaces for optimal performance with this project.

## Automatic Setup

The project includes a `.devcontainer/` configuration that automatically:

- Installs Python 3.13
- Installs `uv` package manager
- Sets up development tools (Black, MyPy, Flake8, etc.)
- Configures VS Code extensions and settings
- Installs project dependencies

## Setting Up Prebuilds (Optional)

To speed up Codespace creation, you can enable prebuilds in your repository settings:

### 1. Enable Prebuilds in Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** → **Codespaces**
3. Click **Set up prebuild**
4. Select the branch (usually `main`)
5. Select the devcontainer configuration (`.devcontainer/devcontainer.json`)
6. Choose when to trigger prebuilds:
   - ✅ Configuration changes
   - ✅ On push
   - ✅ On schedule (optional)

### 2. Prebuild Configuration

The prebuild will automatically:

- Build the Docker container
- Install `uv` and Python dependencies
- Set up the development environment

This reduces Codespace startup time from ~3 minutes to ~30 seconds.

## Manual uv Installation

If you need to install `uv` manually in any environment:

```bash
# Run the setup script
./setup-codespaces.sh

# Or install manually
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
```

## Troubleshooting Codespaces

### Common Issues

1. **uv not found**: Run `./setup-codespaces.sh`
2. **Port 8000 not forwarded**: Check VS Code ports panel
3. **Docker not available**: Use GitHub-hosted PostgreSQL or local SQLite for testing

### Checking Setup

```bash
# Verify uv installation
uv --version

# Check Python environment
uv run python --version

# Test project setup
uv run pytest tests/test_main.py -v
```

## Performance Tips

1. **Use prebuilds** for faster startup
2. **Pin to specific regions** closer to your location
3. **Use 4-core machines** for better performance with larger projects
4. **Enable auto-suspend** to save resources when inactive

## Codespaces vs Local Development

| Feature | Local VS Code | GitHub Codespaces |
|---------|---------------|-------------------|
| `uv` availability | ✅ Manual install | ✅ Auto-configured |
| Database | ✅ Docker | ✅ Docker available |
| Performance | ✅ Native speed | ⚠️ Network dependent |
| Setup time | ⚠️ Manual setup | ✅ Instant (with prebuilds) |
| Cost | ✅ Free | 💰 Usage-based |

Both environments are fully supported and work identically once set up.
