FROM mcr.microsoft.com/devcontainers/python:1-3.13-bullseye

# Install uv - the fast Python package installer
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH for all users
RUN echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> /etc/bash.bashrc
RUN echo 'export PATH="/root/.cargo/bin:$PATH"' >> /etc/bash.bashrc

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspaces/demo_project

# Copy project files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN /root/.cargo/bin/uv sync --dev

# Make sure uv is available for the vscode user
RUN cp /root/.cargo/bin/uv /usr/local/bin/uv
RUN chmod +x /usr/local/bin/uv

# Create vscode user's .local/bin directory and add to PATH
RUN mkdir -p /home/vscode/.local/bin
RUN chown -R vscode:vscode /home/vscode/.local
RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/vscode/.bashrc
