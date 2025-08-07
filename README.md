# Demo Project

A Python application with PostgreSQL database and Alembic migrations for managing review functionality.

## Features

- **Review Management**: Handle review text, sentiment analysis, star ratings, and thumbs-up/thumbs-down feedback
- **PostgreSQL Database**: Robust data storage with SQL database
- **Database Migrations**: Alembic for schema versioning and migrations
- **Development Tools**: Pre-configured with testing, linting, and formatting tools

## Technology Stack

- **Python 3.13+**: Main programming language
- **PostgreSQL 17**: Database engine
- **SQLAlchemy 2.0**: ORM for database operations
- **Alembic**: Database migration tool
- **uv**: Fast Python package manager
- **Docker**: Containerized PostgreSQL database
- **pytest**: Testing framework with coverage reporting

## Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose
- Git

## Project Structure

```text
demo_project/
├── app/                    # Main application code
│   ├── __init__.py
│   └── main.py
├── tests/                  # Test files
│   ├── __init__.py
│   └── test_main.py
├── docker-compose.yml      # PostgreSQL database setup
├── pyproject.toml          # Project configuration and dependencies
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

### 5. Set Up Database Migrations (Optional)

If you plan to use Alembic for database migrations:

```bash
# Initialize Alembic (only needed once)
uv run alembic init migrations

# Create your first migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
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

# Run specific test file
uv run pytest tests/test_main.py
```

### Code Quality Tools

```bash
# Format code with Black
uv run black app tests

# Sort imports with isort
uv run isort app tests

# Lint code with flake8
uv run flake8 app tests

# Type checking with mypy
uv run mypy app
```

## Development Workflow

1. **Make changes** to the code in the `app/` directory
2. **Write tests** in the `tests/` directory
3. **Run tests** to ensure everything works: `uv run pytest`
4. **Format code**: `uv run black app tests`
5. **Check linting**: `uv run flake8 app tests`
6. **Commit changes** with descriptive messages

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
