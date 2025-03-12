# Agentic Framework: Consolidated Documentation

This document provides a comprehensive overview of the Agentic framework, combining all rules, guidelines, and information from the various documentation files.

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Python Environment Management](#python-environment-management)
4. [Project Management](#project-management)
5. [Git and Version Control](#git-and-version-control)
6. [Agent Operation Guidelines](#agent-operation-guidelines)
7. [Security Considerations](#security-considerations)
8. [Logging and Monitoring](#logging-and-monitoring)
9. [Error Handling](#error-handling)
10. [Caching and Optimization](#caching-and-optimization)
11. [Backup and Recovery](#backup-and-recovery)
12. [Utility Scripts](#utility-scripts)
13. [Common Patterns and Examples](#common-patterns-and-examples)
14. [Troubleshooting](#troubleshooting)

## Overview

The Agentic framework is designed to provide a structured environment for AI agents (like Claude, GPT, etc.) to operate on a machine with significant freedom while maintaining security, organization, and best practices. It includes:

- A structured directory hierarchy for organizing projects and resources
- Rules and guidelines for agents to follow
- Utility scripts for common tasks
- Security boundaries to protect the system

## Directory Structure

### Root Organization

All files and directories related to the Agentic framework are organized under the `$HOME/Agentic/` directory:

```
$HOME/Agentic/
├── agentic/              # This repository (rules and core tools)
├── projects/             # All agent-created projects
├── shared/               # Shared resources between projects
├── tmp/                  # Temporary files
├── logs/                 # Log files
├── cache/                # Cache for downloads and other data
└── backups/              # Backup files for registry and other critical data
```

### Project Structure

Each project should have its own directory with a descriptive name following kebab-case (e.g., `my-project-name`). The standard project structure is:

```
project-name/
├── .venv/                 # Virtual environment (not in version control)
├── src/                   # Source code
├── tests/                 # Test files
├── docs/                  # Documentation
├── data/                  # Data files (if applicable)
├── notebooks/             # Jupyter notebooks (if applicable)
├── logs/                  # Log files
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── LICENSE                # License file
└── pyproject.toml         # Project configuration
```

### Naming Conventions

- Project directories: kebab-case (e.g., `my-project-name`)
- Python modules/packages: snake_case
- Classes: PascalCase
- Functions/variables: snake_case
- Constants: UPPER_SNAKE_CASE

## Python Environment Management

### Python Installation

- Python is managed exclusively using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.
- Do not use pip, conda, or other package managers directly.
- Default Python version should be the latest stable release unless a specific version is required for compatibility.
- Python installations should be verified after installation to ensure they are working correctly.

### Virtual Environments

- All Python projects must use isolated virtual environments.
- Virtual environments should be created using uv:
  ```bash
  uv venv /path/to/project/.venv
  ```
- For more control over the creation process, use additional options:
  ```bash
  uv venv /path/to/project/.venv --python 3.12 --timeout 600 --retries 5
  ```
- Virtual environment directories should be named `.venv` and located within the project directory.
- Virtual environments must not be committed to version control (already in .gitignore).
- When activating a virtual environment, use:
  ```bash
  source /path/to/project/.venv/bin/activate
  ```
- All virtual environments must be registered in the central registry.

### Package Management

- Use uv for all package installations:
  ```bash
  uv pip install <package>
  ```
- For faster installations, use parallel mode:
  ```bash
  uv pip install <package> --parallel
  ```
- All projects must include a `requirements.txt` or `pyproject.toml` file listing dependencies.
- For development dependencies, use a separate `requirements-dev.txt` file or appropriate section in `pyproject.toml`.
- Lock files (`uv.lock`) should be committed to version control for applications but not for libraries.
- When installing a project in editable mode, use:
  ```bash
  uv_manager.py install-editable /path/to/venv /path/to/project
  ```

### Environment Cleanup

- Regularly clean unused virtual environments.
- Maintain a list of active virtual environments in `$HOME/Agentic/venv_registry.json`.
- Update the registry when creating or removing virtual environments.
- Periodically run `venv_manager.py cleanup` to remove invalid or non-existent environments from the registry.
- Use `venv_manager.py repair` to scan for and register untracked environments.

## Project Management

### Project Initialization

- All new projects should be initialized with a README.md file describing the project.
- Include a LICENSE file with appropriate licensing information.
- Set up proper .gitignore file for the project type.
- Use the `create_project.py` script to create new projects with the standard structure:
  ```bash
  ./create_project.py "My New Project" --description "A description of the project"
  ```

### Documentation

- All projects must include basic documentation in the README.md file.
- Code should be documented with docstrings following the Google style guide.
- Complex projects should include additional documentation in the docs/ directory.
- Document all configuration options and environment variables.

### Testing

- All projects should include tests in the tests/ directory.
- Use pytest for testing Python code.
- Aim for reasonable test coverage for critical functionality.
- Include tests for error handling and edge cases.

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
- Use parallel operations judiciously, considering system resources.

### Tool Usage

- Prefer using established tools and libraries over creating custom solutions when appropriate.
- Document all tools and dependencies used in projects.
- Keep tools and dependencies updated to secure versions.
- Use the provided utility scripts for common tasks.

## Security Considerations

### Access Control

- Agents should operate with the minimum privileges necessary to complete their tasks.
- Do not store or expose sensitive information (API keys, passwords, etc.) in code or version control.
- Use environment variables or secure storage for sensitive information.

### Data Handling

- Do not process sensitive user data without explicit permission.
- Anonymize or pseudonymize data when possible.
- Delete temporary data after use.
- Regularly clean cache directories to avoid accumulating sensitive data.

### Network Security

- Limit network requests to trusted domains.
- Use secure connections (HTTPS, SSH) for all network communications.
- Document all external services and APIs used by projects.
- Implement proper timeout and retry mechanisms for network operations.

## Logging and Monitoring

### Logging

- Implement appropriate logging in all projects.
- Log files should be stored in a designated logs/ directory.
- Do not log sensitive information.
- Use structured logging when possible.
- Configure appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- Implement log rotation to prevent log files from growing too large.

### Monitoring

- All agent activities should be recorded in an activity log.
- Monitor resource usage and performance.
- Set up alerts for unusual behavior or errors.
- Regularly check the status of virtual environments and Python installations.

## Error Handling

### Error Reporting

- Implement proper error handling in all code.
- Catch and log exceptions appropriately.
- Provide meaningful error messages.
- Include context information in error messages.
- Use appropriate error types and hierarchies.
- Log stack traces for debugging purposes.

### Recovery

- Implement graceful degradation when possible.
- Design systems to recover from failures automatically when appropriate.
- Document known failure modes and recovery procedures.
- Implement retry mechanisms with exponential backoff for transient failures.
- Verify operations after recovery to ensure consistency.

## Caching and Optimization

### Cache Management

- Use the designated cache directory (`$HOME/Agentic/cache/`) for all cached data.
- Organize cache files in subdirectories by purpose or application.
- Include cache invalidation mechanisms to prevent stale data.
- Regularly clean up old cache files using `uv_manager.py clean-cache`.
- Document cache structure and purpose.

### Performance Optimization

- Use parallel processing when appropriate for CPU-intensive tasks.
- Enable parallel installation for faster dependency resolution.
- Implement appropriate timeouts for network operations.
- Monitor and optimize resource usage.
- Use appropriate data structures and algorithms for performance-critical code.

## Backup and Recovery

### Backup Procedures

- Regularly back up critical files to the `$HOME/Agentic/backups/` directory.
- Use timestamped filenames for backups to maintain version history.
- Implement automatic backup before critical operations.
- Use `venv_manager.py backup` to create registry backups.
- Limit the number of backup files to prevent excessive disk usage.

### Recovery Procedures

- Document recovery procedures for common failure scenarios.
- Implement automatic recovery mechanisms where possible.
- Verify the integrity of restored files after recovery.
- Test recovery procedures periodically.
- Use `check_environment.py --fix` to automatically repair common issues.

## Utility Scripts

The Agentic framework includes several utility scripts to help agents follow the rules and manage the environment:

### Environment Check

The `check_environment.py` script verifies that the environment is set up correctly:

```bash
# Run a complete environment check
./check_environment.py

# Run environment check and automatically fix common issues
./check_environment.py --fix
```

This script checks:
- UV installation
- Directory structure
- Registry file
- Utility scripts
- Python installations
- Virtual environments
- Disk space

### Virtual Environment Management

The `venv_manager.py` script helps manage Python virtual environments:

```bash
# List all registered virtual environments
./venv_manager.py list

# List with detailed information
./venv_manager.py list --verbose

# List with package information
./venv_manager.py list --packages

# Add a virtual environment to the registry
./venv_manager.py add /path/to/venv project-name

# Add with additional information
./venv_manager.py add /path/to/venv project-name --description "Description" --python-version "3.12.9"

# Remove a virtual environment from the registry
./venv_manager.py remove --project-name project-name
./venv_manager.py remove --venv-path /path/to/venv

# Check if a virtual environment is registered and verify its status
./venv_manager.py check --project-name project-name
./venv_manager.py check --venv-path /path/to/venv

# Update the package list for a virtual environment
./venv_manager.py update-packages --project-name project-name

# Clean up non-existent virtual environments
./venv_manager.py cleanup

# Scan for and repair the registry
./venv_manager.py repair

# Create a backup of the registry
./venv_manager.py backup
```

### Project Creation

The `create_project.py` script creates new projects with the standard structure:

```bash
# Create a new project
./create_project.py "My New Project" --description "A description of the project"

# Create a new project with a specific license
./create_project.py "My New Project" --license Apache-2.0
```

### UV Package Manager

The `uv_manager.py` script helps with installing and managing uv:

```bash
# Install uv
./uv_manager.py install

# Update uv
./uv_manager.py update

# List available Python versions
./uv_manager.py list-python

# Install a specific Python version
./uv_manager.py install-python 3.11

# Create a virtual environment
./uv_manager.py create-venv /path/to/venv --python 3.11

# Create with custom timeout and retries
./uv_manager.py create-venv /path/to/venv --python 3.11 --timeout 600 --retries 5

# Install dependencies in a virtual environment
./uv_manager.py install-deps /path/to/venv --requirements requirements.txt
./uv_manager.py install-deps /path/to/venv --packages numpy pandas matplotlib

# Install a project in editable mode
./uv_manager.py install-editable /path/to/venv /path/to/project

# Show information about uv
./uv_manager.py info

# Clean the uv cache
./uv_manager.py clean-cache
./uv_manager.py clean-cache --older-than 30
```

### Cleanup and Maintenance

The `cleanup_manager.py` script helps with cleaning up temporary files and maintaining the directory structure:

```bash
# Clean up temporary files older than 7 days
./cleanup_manager.py cleanup-tmp

# Check for orphaned virtual environments
./cleanup_manager.py check-orphaned-venvs

# Check the directory structure
./cleanup_manager.py check-structure

# Analyze disk usage
./cleanup_manager.py disk-usage
```

## Common Patterns and Examples

### Creating a New Python Project

```bash
# 1. Create the project structure
./create_project.py "My Project" --description "Description"

# 2. Create a virtual environment
./uv_manager.py create-venv $HOME/Agentic/projects/my-project/.venv --python 3.11

# 3. Register the virtual environment
./venv_manager.py add $HOME/Agentic/projects/my-project/.venv my-project

# 4. Install dependencies
./uv_manager.py install-deps $HOME/Agentic/projects/my-project/.venv --packages numpy pandas
```

### Working with Existing Projects

```bash
# 1. Check if the project has a registered virtual environment
./venv_manager.py check --project-name project-name

# 2. Update package list
./venv_manager.py update-packages --project-name project-name

# 3. Install new dependencies
./uv_manager.py install-deps /path/to/venv --packages new-package
```

## Troubleshooting

If you encounter issues with the Agentic framework:

1. Run `./check_environment.py` to check for common issues
2. Run `./check_environment.py --fix` to automatically fix common issues
3. Check the logs in `$HOME/Agentic/logs/` for more information
4. Use the utility scripts to diagnose and fix specific issues:
   - `./venv_manager.py repair` to scan for and register untracked environments
   - `./venv_manager.py cleanup` to remove invalid or non-existent environments
   - `./cleanup_manager.py check-structure` to verify the directory structure
