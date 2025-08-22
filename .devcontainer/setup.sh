#!/bin/bash
set -e

echo "🚀 Setting up Demo Project development environment..."

# Ensure uv is available in PATH
export PATH="$HOME/.cargo/bin:/usr/local/bin:$PATH"

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ uv version: $(uv --version)"

# Sync dependencies if not already done
if [ -f "pyproject.toml" ] && [ -f "uv.lock" ]; then
    echo "📦 Syncing Python dependencies..."
    uv sync --dev
    echo "✅ Dependencies synced successfully"
else
    echo "⚠️  pyproject.toml or uv.lock not found, skipping dependency sync"
fi

# Install pre-commit hooks if available
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔗 Installing pre-commit hooks..."
    uv run pre-commit install
    echo "✅ Pre-commit hooks installed"
fi

# Make scripts executable
if [ -d "scripts" ]; then
    echo "🔧 Making scripts executable..."
    chmod +x scripts/*.py
fi

echo "🎉 Development environment setup complete!"
echo "💡 You can now use 'uv' commands to manage your Python environment"
echo "💡 Try: 'uv run python -m app.main' to start the FastAPI server"
