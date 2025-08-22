#!/bin/bash
# Quick setup script for GitHub Codespaces or any environment missing uv

set -e

echo "🚀 Demo Project - Quick Setup for Codespaces"
echo "============================================="

# Make sure we're in the right directory
cd /workspaces/demo_project 2>/dev/null || cd $(dirname "$0")

# Check if uv is already installed
if command -v uv &> /dev/null; then
    echo "✅ uv is already installed: $(uv --version)"
else
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Add to bashrc for future sessions
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
    
    echo "✅ uv installed: $(uv --version)"
fi

# Install system dependencies if needed (PostgreSQL client)
if ! command -v psql &> /dev/null; then
    echo "📦 Installing PostgreSQL client..."
    sudo apt-get update && sudo apt-get install -y postgresql-client libpq-dev
fi

# Install Python dependencies
if [ -f "pyproject.toml" ]; then
    echo "📚 Installing Python dependencies..."
    uv sync --dev
    echo "✅ Dependencies installed successfully!"
else
    echo "⚠️  pyproject.toml not found - make sure you're in the project root"
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker is available"
    if [ -f "docker-compose.yml" ]; then
        echo "💡 To start the database, run: docker-compose up -d"
    fi
else
    echo "⚠️  Docker not found - database setup will be manual"
fi

echo ""
echo "🎉 Setup complete! You can now use:"
echo "   📦 uv run python -m app.main    # Start the FastAPI server"
echo "   🧪 uv run pytest               # Run tests"
echo "   🔧 uv run alembic upgrade head  # Run database migrations"
echo ""
echo "💡 If you're in Codespaces, the FastAPI server (port 8000) will be automatically forwarded"
