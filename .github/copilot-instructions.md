# Demo_project Development Instructions

## Project Architecture

### A standalone Python module

- the module is a standalone component that can be integrated into larger systems
- it provides a REST API for managing reviews
- it uses SQLModel for database operations


## Key Workflows

- TODO

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

### Project Documentation
- Requirements are documented in `docs/requirements.md`
- Architecture decisions are documented in `docs/architecture.md`
- API documentation is generated using FastAPI's built-in OpenAPI support

