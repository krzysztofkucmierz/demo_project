# Demo_project Development Instructions

## Project Architecture

### A standalone Python module

- the module is a standalone component that can be integrated into larger systems
- it provides a REST API for managing reviews
- it uses SQLModel for database operations

### Code Standards

- use SQLModel for database operations
- FastAPI for REST API with dependency injection pattern
- Follow repository pattern for database access
- Use type annotations everywhere

## Integration Points

- Database: PostgreSQL accessed via SQLModel

## Project Conventions

### Patterns
- Use dependency injection for services and repositories
- Repository pattern for database access
- Consistent error handling with HTTP exceptions
- API routes follow RESTful conventions

## Code quality
- use mypy for type checking
- use black for code formatting
- use pytest for testing


## Project Documentation
- General project information: setup and development instructions are in `README.md`
- Requirements are documented in `docs/requirements.md`
- Architecture decisions are documented in `docs/architecture.md`
- API documentation is generated using FastAPI's built-in OpenAPI support

## Development Environment


- The project is set up to run in a GitHub Codespace using a custom development container configuration.
- For details see CODESPACES.md.
- uv package manager is used for dependency management.

### Codespace Configuration
The `.devcontainer/devcontainer.json` file configures the development environment.