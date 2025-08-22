# Demo Project

A Python application with PostgreSQL database and SQLModel ORM for managing review systems.

## Features

- **Review Management System**: Complete database schema for managing reviews with multiple rating types
- **Three-Entity Model**: Reviewers, ReviewedObjects, and Reviews with proper relationships
- **Flexible Rating System**: Support for star ratings (0-5), thumbs ratings (up/down), and text reviews
- **PostgreSQL Database**: Robust data storage with JSONB support for metadata
- **SQLModel ORM**: Modern type-safe ORM built on SQLAlchemy and Pydantic
- **Database Migrations**: Alembic for schema versioning and migrations
- **Repository Pattern**: Clean data access layer with comprehensive CRUD operations
- **Comprehensive Testing**: Full test suite with SQLite compatibility for unit tests
- **Development Tools**: Pre-configured with testing, linting, formatting, and type checking

## Technology Stack

- **Python 3.13+**: Main programming language
- **PostgreSQL 17**: Database engine with JSONB support
- **SQLModel 0.0.24**: Modern ORM combining SQLAlchemy and Pydantic
- **SQLAlchemy 2.0**: Underlying ORM framework
- **Alembic**: Database migration tool
- **FastAPI**: API framework (ready for extension)
- **uv**: Fast Python package manager
- **Docker**: Containerized PostgreSQL database
- **pytest**: Testing framework with coverage reporting
- **Black**: Code formatting
- **MyPy**: Static type checking

## Prerequisites

### Local Development
- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose
- Git

### Dev Container (Recommended)
- Visual Studio Code with Dev Containers extension
- Docker Desktop
- Git

> **💡 Pro tip**: Use the Dev Container for the best development experience. Everything is pre-configured!

## Project Structure

```text
demo_project/
├── .devcontainer/         # Development container configuration
│   ├── devcontainer.json  # VS Code Dev Container config with Python 3.13
│   └── Dockerfile         # Custom container with uv and PostgreSQL client
├── .github/              # GitHub workflows and Codespaces config
│   ├── copilot-instructions.md
│   └── CODESPACES.md     # GitHub Codespaces setup guide
├── app/                  # Main application code
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # SQLModel database models
│   ├── database.py      # Database connection and session management
│   └── repositories.py # Repository pattern for data access
├── migrations/          # Alembic database migrations
│   ├── env.py
│   └── versions/
│       └── 87e9b654863c_create_initial_schema_for_review_.py
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_main.py
│   └── test_review_schema.py  # Comprehensive database schema tests
├── docs/                # Documentation
│   └── requirements.md
├── scripts/             # Utility scripts
│   └── populate_db.py
├── docker-compose.yml   # PostgreSQL database setup
├── pyproject.toml       # Project configuration and dependencies
├── alembic.ini         # Alembic configuration
├── setup-codespaces.sh # Automated setup script for Codespaces
├── README.md
└── .gitignore
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/krzysztofkucmierz/demo_project.git
cd demo_project
```

### 2. Set Up Python Environment

Create and activate a virtual environment using uv:

```bash
# Create virtual environment
uv venv

# Activate virtual environment (Linux/Mac)
source .venv/bin/activate

# On Windows
# .venv\Scripts\activate
```

### 3. Install Dependencies

Install the project with all dependencies:

```bash
# Install production dependencies
uv sync

# Install with development dependencies (recommended)
uv sync --extra dev --extra test
```

### 4. Start the Database

Start the PostgreSQL database using Docker:

```bash
docker-compose up -d
```

The database will be available on `localhost:5431` with:

- **Database**: `demo_project`
- **Username**: `user`
- **Password**: `password`

### 5. Run Database Migrations

The database schema is already set up with Alembic migrations:

```bash
# Apply the existing migration to set up the review schema
uv run alembic upgrade head
```

The migration creates the complete review management schema including:

- `reviewers` table with unique username/email constraints
- `reviewed_objects` table with JSONB metadata support
- `reviews` table with multiple rating types and constraints

## Dev Container & GitHub Codespaces Support

This project is fully configured to work with VS Code Dev Containers and GitHub Codespaces out of the box.

### DevContainer Features

The `.devcontainer/` configuration includes:

- **Base Image**: Microsoft's official Python 3.13 Dev Container image
- **Docker-in-Docker**: Full Docker daemon with compose support for running PostgreSQL
- **Pre-installed Tools**: 
  - `uv` package manager (installed globally)
  - PostgreSQL client and libpq-dev
  - Git and GitHub CLI
  - Docker and Docker Compose v2
- **VS Code Extensions**: 
  - Python language support
  - Code formatters (Black, isort)
  - Linters (Flake8, MyPy, Ruff)
  - GitHub Copilot
- **Automatic Setup**: 
  - Runs `setup-codespaces.sh` after container creation
  - Installs all project dependencies
  - Configures development environment
- **Port Forwarding**: FastAPI (8000) and PostgreSQL (5432)

### GitHub Codespaces Quick Start

When you open the project in Codespaces, it will automatically:

1. Build the development container with Python 3.13 and Docker support
2. Install `uv` package manager and system dependencies including Docker daemon
3. Run the setup script to install project dependencies
4. Configure VS Code with recommended extensions and settings
5. Set up port forwarding for FastAPI (port 8000) and PostgreSQL (port 5432)

**Steps to get started:**

1. Click the "Code" button on GitHub and select "Open with Codespaces"
2. Wait for the environment to build (first time takes ~3-4 minutes with Docker support)
3. Verify Docker is working: `docker --version && docker-compose --version`
4. Start the database: `docker-compose up -d`
5. Run migrations: `uv run alembic upgrade head`
6. Start the application: `uv run python -m app.main`

**💡 Pro tip**: See [`.github/CODESPACES.md`](.github/CODESPACES.md) for advanced configuration and prebuild setup!

### Manual uv Installation in Codespaces

If for some reason `uv` is not available, you can install it manually:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Verify installation
uv --version

# Install dependencies
uv sync --dev
```

## Running the Application

### Run the Main Application

```bash
uv run python -m app.main
```

### Run Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=app --cov-report=html

# Run specific test file for database schema
uv run pytest tests/test_review_schema.py -v

# Run with type checking and linting
uv run pytest && uv run mypy app tests && uv run flake8 app tests
```

### Database Operations

```bash
# Test database connection and schema
uv run python -c "
from app.database import engine
from app.models import SQLModel
from sqlmodel import Session

# Test connection
with Session(engine) as session:
    print('✓ Database connection successful')
    
# Check tables exist
print('✓ Database schema ready')
"

# Access database console
docker exec -it postgres_demo_project psql -U user -d demo_project
```

### Code Quality Tools

```bash
# Format code with Black (line length 79)
uv run black app tests --line-length 79

# Sort imports with isort
uv run isort app tests

# Lint code with flake8
uv run flake8 app tests

# Type checking with mypy
uv run mypy app tests

# Run all quality checks
uv run black app tests --line-length 79 && uv run isort app tests && uv run flake8 app tests && uv run mypy app tests
```

## Development Workflow

1. **Make changes** to the code in the `app/` directory
2. **Write tests** in the `tests/` directory for any new functionality
3. **Run tests** to ensure everything works: `uv run pytest -v`
4. **Run database tests** specifically: `uv run pytest tests/test_review_schema.py -v`
5. **Format code**: `uv run black app tests --line-length 79`
6. **Check linting**: `uv run flake8 app tests`
7. **Type checking**: `uv run mypy app tests`
8. **Run migrations** if schema changes: `uv run alembic upgrade head`
9. **Commit changes** with descriptive messages

### Creating New Migrations

When you modify the database models:

```bash
# Generate a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file in migrations/versions/

# Apply the migration
uv run alembic upgrade head
```

## Environment Variables

Create a `.env` file in the project root for environment-specific configuration:

```bash
# Database configuration
DATABASE_URL=postgresql://user:password@localhost:5431/demo_project

# Application settings
DEBUG=True
LOG_LEVEL=INFO
```

## Database Management

### Stop the Database

```bash
docker-compose down
```

### Reset the Database

```bash
# Stop and remove containers with data
docker-compose down -v

# Start fresh
docker-compose up -d
```

### Access Database Console

```bash
# Using docker exec
docker exec -it postgres_demo_project psql -U user -d demo_project

# Or using psql directly (if installed)
psql -h localhost -p 5431 -U user -d demo_project
```

## Troubleshooting

### Common Issues

1. **Port 5431 already in use**: Change the port in `docker-compose.yml`
2. **Permission denied on Docker**: Add your user to the docker group or use `sudo`
3. **uv not found**: Install uv following the [official documentation](https://docs.astral.sh/uv/getting-started/installation/)

### Getting Help

- Check the [uv documentation](https://docs.astral.sh/uv/)
- Review PostgreSQL logs: `docker-compose logs db`
- Run tests to verify setup: `uv run pytest -v`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `uv run pytest`
5. Format your code: `uv run black app tests`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
