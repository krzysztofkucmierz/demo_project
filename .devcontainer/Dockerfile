FROM mcr.microsoft.com/devcontainers/python:1-3.13-bullseye

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv - the fast Python package installer
# Use a more robust installation method
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    uv --version && \
    cp ~/.cargo/bin/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv

# Ensure uv is in PATH for all users
RUN echo 'export PATH="/usr/local/bin:$HOME/.cargo/bin:$PATH"' >> /etc/bash.bashrc

# Create vscode user's .local/bin directory and add to PATH
RUN mkdir -p /home/vscode/.local/bin && \
    chown -R vscode:vscode /home/vscode/.local && \
    echo 'export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"' >> /home/vscode/.bashrc

# Verify uv installation
RUN uv --version
