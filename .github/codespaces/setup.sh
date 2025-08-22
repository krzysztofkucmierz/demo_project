#!/bin/bash
# Codespaces prebuild script to install uv

set -e

echo "🚀 Installing uv for Codespaces..."

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
export PATH="$HOME/.cargo/bin:$PATH"

# Verify installation
uv --version

echo "✅ uv installed successfully in Codespaces!"

# Sync dependencies
if [ -f "pyproject.toml" ]; then
    echo "📦 Syncing Python dependencies..."
    uv sync --dev
    echo "✅ Dependencies synced!"
fi
