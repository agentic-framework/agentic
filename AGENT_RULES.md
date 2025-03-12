# Agent Operation Rules

This document outlines the rules and guidelines for agents operating on this machine. These rules are designed to maintain a clean, organized, and secure environment while allowing agents to have significant operational freedom.

## Table of Contents

1. [Python Environment Management](#python-environment-management)
2. [Directory Structure](#directory-structure)
3. [Project Management](#project-management)
4. [Git and Version Control](#git-and-version-control)
5. [Agent Operation Guidelines](#agent-operation-guidelines)
6. [Security Considerations](#security-considerations)
7. [Logging and Monitoring](#logging-and-monitoring)
8. [Error Handling](#error-handling)

## Python Environment Management

### Python Installation

- Python is managed exclusively using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.
- Do not use pip, conda, or other package managers directly.
- Default Python version should be the latest stable release unless a specific version is required for compatibility.

### Virtual Environments

- All Python projects must use isolated virtual environments.
- Virtual environments should be created using uv:
  ```bash
  uv venv /path/to/project/.venv
  ```
- Virtual environment directories should be named `.venv` and located within the project directory.
- Virtual environments must not be committed to version control (already in .gitignore).
- When activating a virtual environment, use:
  ```bash
  source /path/to/project/.venv/bin/activate
  ```

### Package Management

- Use uv for all package installations:
  ```bash
  uv pip install <package>
  ```
- All projects must include a `requirements.txt` or `pyproject.toml` file listing dependencies.
- For development dependencies, use a separate `requirements-dev.txt` file or appropriate section in `pyproject.toml`.
- Lock files (`uv.lock`) should be committed to version control for applications but not for libraries.

### Environment Cleanup

- Regularly clean unused virtual environments.
- Maintain a list of active virtual environments in `$HOME/Agentic/venv_registry.json`.
- Update the registry when creating or removing virtual environments.

## Directory Structure

### Root Organization

- All agent-created projects should be organized under `$HOME/Agentic/projects/`.
- Shared resources should be placed in `$HOME/Agentic/shared/`.
- Temporary files should be stored in `$HOME/Agentic/tmp/` and cleaned regularly.

### Project Structure

- Each project should have its own directory with a descriptive name.
- Project names should use kebab-case (e.g., `my-project-name`).
- Standard project structure:
  ```
  project-name/
  ├── .venv/                 # Virtual environment (not in version control)
  ├── src/                   # Source code
  ├── tests/                 # Test files
  ├── docs/                  # Documentation
  ├── data/                  # Data files (if applicable)
  ├── notebooks/             # Jupyter notebooks (if applicable)
  ├── .gitignore             # Git ignore file
  ├── README.md              # Project documentation
  ├── LICENSE                # License file
  └── pyproject.toml         # Project configuration
  ```

### Naming Conventions

- Use descriptive names for all files and directories.
- Python modules and packages should use snake_case.
- Classes should use PascalCase.
- Functions and variables should use snake_case.
- Constants should use UPPER_SNAKE_CASE.

## Project Management

### Project Initialization

- All new projects should be initialized with a README.md file describing the project.
- Include a LICENSE file with appropriate licensing information.
- Set up proper .gitignore file for the project type.

### Documentation

- All projects must include basic documentation in the README.md file.
- Code should be documented with docstrings following the Google style guide.
- Complex projects should include additional documentation in the docs/ directory.

### Testing

- All projects should include tests in the tests/ directory.
- Use pytest for testing Python code.
- Aim for reasonable test coverage for critical functionality.

## Git and Version Control

### Repository Structure

- Each project should have its own git repository.
- Use .gitignore to exclude appropriate files (virtual environments, cache files, etc.).

### Commit Messages

- Follow conventional commits format: `type(scope): description`
- Types include: feat, fix, docs, style, refactor, test, chore
- Keep commit messages clear and descriptive.
- Reference issue numbers when applicable.

### Branching Strategy

- Main branch should always be stable.
- Use feature branches for development.
- Branch naming convention: `type/description` (e.g., `feature/add-login`, `fix/memory-leak`).

## Agent Operation Guidelines

### Permissions

- The `$HOME/Agentic/` folder is the area agents can fully control, used for shared tools and rules for different projects.
- Agents have permission to create, modify, and delete files within the `$HOME/Agentic/` directory.
- Outside the Agentic folder are projects managed by humans; agent actions need to be approved before taking.
- Agents should not modify system files or configurations outside their designated areas.
- Agents should not install global packages or modify global configurations without explicit permission.
- Always use `$HOME` instead of specific user paths (like "/Users/username/") to keep rules and scripts universal across different environments.

### Resource Usage

- Monitor and limit CPU and memory usage to avoid impacting system performance.
- Clean up resources after tasks are completed.
- Limit concurrent operations to avoid overloading the system.

### Tool Usage

- Prefer using established tools and libraries over creating custom solutions when appropriate.
- Document all tools and dependencies used in projects.
- Keep tools and dependencies updated to secure versions.

## Security Considerations

### Access Control

- Agents should operate with the minimum privileges necessary to complete their tasks.
- Do not store or expose sensitive information (API keys, passwords, etc.) in code or version control.
- Use environment variables or secure storage for sensitive information.

### Data Handling

- Do not process sensitive user data without explicit permission.
- Anonymize or pseudonymize data when possible.
- Delete temporary data after use.

### Network Security

- Limit network requests to trusted domains.
- Use secure connections (HTTPS, SSH) for all network communications.
- Document all external services and APIs used by projects.

## Logging and Monitoring

### Logging

- Implement appropriate logging in all projects.
- Log files should be stored in a designated logs/ directory.
- Do not log sensitive information.
- Use structured logging when possible.

### Monitoring

- All agent activities should be recorded in an activity log.
- Monitor resource usage and performance.
- Set up alerts for unusual behavior or errors.

## Error Handling

### Error Reporting

- Implement proper error handling in all code.
- Catch and log exceptions appropriately.
- Provide meaningful error messages.

### Recovery

- Implement graceful degradation when possible.
- Design systems to recover from failures automatically when appropriate.
- Document known failure modes and recovery procedures.

---

These rules are subject to change and improvement. Agents should check for updates regularly and adapt their behavior accordingly.
