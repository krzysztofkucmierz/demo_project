# Module Architecture Documentation Generator

---
mode: ask
---

Generate a comprehensive `architecture.md` documentation file for the specified module. Focus on providing a detailed architectural overview that helps developers understand the module's design, functionality, and integration points.
If the architecture is already documented for the module, update the existing file with new information or improvements if applicable.

## Required Sections

### 0. Module Metadata
Include the following metadata at the top of the document:
- **Module Name**: The name of the module (e.g., `review`)
- **Key Functionality**: A brief description of the module's primary responsibilities (e.g  ., "Automated review management system")
- **Special Considerations**: Any unique aspects or constraints of the module if applicable (e.g., "High computational requirements for AI processing, requires integration with external AI services")
- **Last Updated**: Date of the last update to this document


### 1. Module Overview
Provide a concise description of this module's purpose, responsibilities, and role within the overall Science Net application. Explain why this module exists as a separate component.

### 2. Key Components
Document the main components within this module, organized by file:

- `models.py`: Describe the database models, relationships, and key fields
- `schemas.py`: Document the Pydantic models used for API I/O
- `repository.py`: Explain the database operations and query patterns
- `routers.py`: Detail the API endpoints, their purpose, and parameters
- `service.py`: Describe the business logic and operations
- `dependencies.py`: Document the dependency injection providers

### 3. Data Flow
Illustrate the typical data flows through this module, from API request to database operations and response. Include:

- Request handling path
- Data transformation steps
- Database interactions
- Response formation

### 4. Integration Points
Identify how this module interacts with:

- Other modules in the application
- External services
- Shared utilities and helpers

### 5. Authentication and Authorization
Document the security mechanisms implemented in this module:

- Permission requirements for different operations
- Role-based access controls
- Security validation steps

### 6. Error Handling
Describe the error handling strategy:

- Module-specific exceptions
- Error response patterns
- Validation approaches

### 7. Performance Considerations
Note any performance optimizations or potential bottlenecks:

- Query optimization techniques
- Caching strategies (if applicable)
- Areas that may need performance attention

### 8. Testing Strategy
Outline how the module should be tested:

- Key test scenarios
- Mock requirements
- Integration test considerations

## Formatting Guidelines
- Use clear, concise Markdown formatting
- Include code examples for important patterns
- Use headings and subheadings for organization
- Add diagrams or flowcharts in mermaid when helpful

