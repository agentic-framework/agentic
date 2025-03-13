# Agentic Framework Consolidated Documentation

This document provides a comprehensive overview of the Agentic framework by consolidating information from various documentation files. It serves as a central reference point to ensure all relevant information is considered when performing tasks.

## Table of Contents

1. [Framework Overview](#framework-overview)
2. [Directory Structure](#directory-structure)
3. [Python Environment Management](#python-environment-management)
4. [Project Management](#project-management)
5. [Security Considerations](#security-considerations)
6. [Utility Scripts](#utility-scripts)
7. [Agent Operation Guidelines](#agent-operation-guidelines)
8. [Error Handling and Recovery](#error-handling-and-recovery)
9. [Logging and Monitoring](#logging-and-monitoring)
10. [Caching and Optimization](#caching-and-optimization)
11. [Backup and Recovery](#backup-and-recovery)
12. [Getting Started](#getting-started)

## Framework Overview

The Agentic framework is designed for managing and operating AI agents with controlled access to a machine. It provides rules, guidelines, and tools that allow AI agents to operate with significant freedom while maintaining security, organization, and best practices.

Key features of the framework include:

- **Structured Rules**: Rules are stored in a machine-readable format (rules.json) that can be programmatically accessed and verified.
- **Security Enforcement**: Technical mechanisms ensure AI agents operate only within their designated areas.
- **Centralized Configuration**: A configuration system provides consistent access to settings across the framework.
- **Utility Scripts**: A set of scripts for common tasks like environment checking, virtual environment management, and project creation.
- **Error Handling and Recovery**: Robust error handling with detailed logging and recovery mechanisms.
- **Logging and Monitoring**: Comprehensive logging system with configurable levels and log rotation.

## Directory Structure

The Agentic framework has a specific directory structure that separates the git-managed repository from user-generated content:

```
$HOME/
└── Agentic/                  # Root Agentic folder (not under version control)
    ├── agentic/              # Git-managed repository folder (under version control)
    │   ├── docs/             # Documentation files
    │   │   ├── README.md     # Framework overview
    │   │   ├── AGENT_RULES.md  # Comprehensive rules for AI agents
    │   │   ├── AGENT_QUICK_REFERENCE.md  # Quick reference for AI agents
    │   │   ├── HUMAN_GUIDE.md  # Guide for human users
    │   │   ├── DIRECTORY_STRUCTURE.md  # Directory structure documentation
    │   │   ├── LESSON_LEARNED.md  # Lessons learned during development
    │   │   └── CONSOLIDATED_DOCS.md  # This file
    │   ├── scripts/          # Utility scripts
    │   │   ├── check_environment.py  # Environment verification script
    │   │   ├── venv_manager.py  # Virtual environment management script
    │   │   ├── create_project.py  # Project creation script
    │   │   ├── uv_manager.py  # UV package manager script
    │   │   └── cleanup_manager.py  # Cleanup and maintenance script
    │   ├── ag                # Main command-line interface
    │   ├── LICENSE           # License file
    │   ├── rules.json        # Structured rules in machine-readable format
    │   └── agentic_info.json # Framework configuration
    │
    ├── projects/             # All agent-created projects (not under version control)
    ├── shared/               # Shared resources between projects (not under version control)
    ├── tmp/                  # Temporary files (not under version control)
    ├── logs/                 # Log files (not under version control)
    ├── cache/                # Cache for downloads and other data (not under version control)
    ├── backups/              # Backup files for registry and other critical data (not under version control)
    └── venv_registry.json    # Registry of virtual environments (not under version control)
```

### Key Distinctions

#### Root Agentic Folder (`$HOME/Agentic/`)

- **Purpose**: Serves as the container for all Agentic framework components
- **Version Control**: Not under version control
- **Content**: Contains the git repository, project directories, and supporting directories
- **Management**: Managed by the framework's utility scripts
- **Path Reference**: Always referenced as `$HOME/Agentic` in documentation and scripts

#### Git-Managed Repository Folder (`$HOME/Agentic/agentic/`)

- **Purpose**: Contains the core framework code, documentation, and utility scripts
- **Version Control**: Under git version control
- **Content**: Organized into `docs/` (documentation files) and `scripts/` (utility scripts) directories
- **Management**: Managed through git commands (pull, push, commit, etc.)
- **Path Reference**: Always referenced as `$HOME/Agentic/agentic` in documentation and scripts

### Important Considerations

When using git commands, they should be executed within the git-managed repository folder:

```bash
# Correct
cd $HOME/Agentic/agentic
git pull

# Incorrect
cd $HOME/Agentic
git pull  # This will fail because this directory is not a git repository
```

When creating projects, they should always be created in the projects directory, not in the git-managed repository:

```bash
# Correct
$HOME/Agentic/agentic/ag project create "My Project"  # This will create the project in $HOME/Agentic/projects/my-project

# Incorrect
cd $HOME/Agentic/agentic
./ag project create "My Project"  # Don't create projects inside the git repository
```

When referencing paths in scripts, use the correct paths:

```python
# Correct
AGENTIC_ROOT = os.path.expanduser("~/Agentic")
AGENTIC_REPO = os.path.join(AGENTIC_ROOT, "agentic")
PROJECTS_DIR = os.path.join(AGENTIC_ROOT, "projects")

# Incorrect
AGENTIC_DIR = os.path.expanduser("~/Agentic/agentic")  # This only points to the repository, not the root
PROJECTS_DIR = os.path.join(AGENTIC_DIR, "projects")  # This would incorrectly point to ~/Agentic/agentic/projects
```

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
  ./ag uv install-editable /path/to/venv /path/to/project
  ```

### Environment Cleanup

- Regularly clean unused virtual environments.
- Maintain a list of active virtual environments in `$HOME/Agentic/venv_registry.json`.
- Update the registry when creating or removing virtual environments.
- Periodically run `./ag venv cleanup` to remove invalid or non-existent environments from the registry.
- Use `./ag venv repair` to scan for and register untracked environments.

## Project Management

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
  ├── logs/                  # Log files
  ├── .gitignore             # Git ignore file
  ├── README.md              # Project documentation
  ├── LICENSE                # License file
  └── pyproject.toml         # Project configuration
  ```

### Project Initialization

- All new projects should be initialized with a README.md file describing the project.
- Include a LICENSE file with appropriate licensing information.
- Set up proper .gitignore file for the project type.
- Use the `./ag project create` command to create new projects with the standard structure.

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

### Naming Conventions

- Use descriptive names for all files and directories.
- Python modules and packages should use snake_case.
- Classes should use PascalCase.
- Functions and variables should use snake_case.
- Constants should use UPPER_SNAKE_CASE.

## Security Considerations

### Access Control

- The `$HOME/Agentic/` folder is the area agents can fully control, used for shared tools and rules for different projects.
- Agents have permission to create, modify, and delete files within the `$HOME/Agentic/` directory.
- Outside the Agentic folder are projects managed by humans; agent actions need to be approved before taking.
- Agents should not modify system files or configurations outside their designated areas.
- Agents should not install global packages or modify global configurations without explicit permission.
- Always use `$HOME` instead of specific user paths (like "/Users/username/") to keep rules and scripts universal across different environments.

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

## Utility Scripts

The Agentic framework includes several utility scripts to help agents follow the rules and manage the environment:

### Security Enforcement (`scripts/security.py`)

The `scripts/security.py` script provides technical enforcement mechanisms to ensure AI agents operate only within their designated areas:

```bash
# Check if a path is allowed
./scripts/security.py check-path /path/to/check

# Validate a command for execution
./scripts/security.py validate-command "command to validate"

# Scan a file for potential security violations
./scripts/security.py scan-file /path/to/file

# Calculate the SHA-256 hash of a file
./scripts/security.py hash-file /path/to/file

# Verify the integrity of a file
./scripts/security.py verify-integrity /path/to/file expected-hash
```

This script enforces security boundaries, validates operations, and logs security events. It helps prevent AI agents from accessing or modifying files outside their designated areas.

### Configuration Management (`scripts/config.py`)

The `scripts/config.py` script provides a centralized configuration system for the Agentic framework:

```bash
# Get a configuration value
./scripts/config.py get paths.agentic_root

# Set a configuration value
./scripts/config.py set python.default_python_version 3.12

# List all configuration values
./scripts/config.py list

# List a specific section
./scripts/config.py list --section paths

# Check if a path is allowed
./scripts/config.py check /path/to/check

# Reset configuration to defaults
./scripts/config.py reset
```

This script provides a standardized API for accessing configuration values and handles path variability across different installations. All other scripts in the framework use this configuration system to ensure consistency.

### Rule Loading and Verification (`scripts/rule_loader.py`)

The `scripts/rule_loader.py` script provides utilities for loading, verifying, and querying the Agentic framework rules:

```bash
# Verify an AI agent's understanding of the rules
./scripts/rule_loader.py verify

# Run verification in non-interactive mode
./scripts/rule_loader.py verify --non-interactive

# Save verification results to a file
./scripts/rule_loader.py verify --output /path/to/results.json

# Query specific rules
./scripts/rule_loader.py query python_environment
./scripts/rule_loader.py query python_environment --subcategory virtual_environments
./scripts/rule_loader.py query python_environment --subcategory virtual_environments --key location

# List rule categories
./scripts/rule_loader.py list

# List utility scripts
./scripts/rule_loader.py list --utility-scripts
```

This script uses a structured rules file (`rules.json`) that contains all the framework rules in a machine-readable format, enabling programmatic access and verification.

### Environment Check (`scripts/check_environment.py`)

The `scripts/check_environment.py` script verifies that the environment is set up correctly:

```bash
# Run a complete environment check
./scripts/check_environment.py

# Run environment check and automatically fix common issues
./scripts/check_environment.py --fix
```

This script checks:
- UV installation
- Directory structure
- Registry file
- Utility scripts
- Python installations
- Virtual environments
- Disk space

### Virtual Environment Management (`scripts/venv_manager.py`)

The `scripts/venv_manager.py` script helps manage Python virtual environments:

```bash
# List all registered virtual environments
./scripts/venv_manager.py list

# List with detailed information
./scripts/venv_manager.py list --verbose

# List with package information
./scripts/venv_manager.py list --packages

# Add a virtual environment to the registry
./scripts/venv_manager.py add /path/to/venv project-name

# Add with additional information
./scripts/venv_manager.py add /path/to/venv project-name --description "Description" --python-version "3.12.9"

# Remove a virtual environment from the registry
./scripts/venv_manager.py remove --project-name project-name
./scripts/venv_manager.py remove --venv-path /path/to/venv

# Check if a virtual environment is registered and verify its status
./scripts/venv_manager.py check --project-name project-name
./scripts/venv_manager.py check --venv-path /path/to/venv

# Update the package list for a virtual environment
./scripts/venv_manager.py update-packages --project-name project-name

# Clean up non-existent virtual environments
./scripts/venv_manager.py cleanup

# Scan for and repair the registry
./scripts/venv_manager.py repair

# Create a backup of the registry
./scripts/venv_manager.py backup
```

### Project Creation (`scripts/create_project.py`)

The `scripts/create_project.py` script creates new projects with the standard structure:

```bash
# Create a new project
./scripts/create_project.py "My New Project" --description "A description of the project"

# Create a new project with a specific license
./scripts/create_project.py "My New Project" --license Apache-2.0
```

### UV Package Manager (`scripts/uv_manager.py`)

The `scripts/uv_manager.py` script helps with installing and managing uv:

```bash
# Install uv
./scripts/uv_manager.py install

# Update uv
./scripts/uv_manager.py update

# List available Python versions
./scripts/uv_manager.py list-python

# Install a specific Python version
./scripts/uv_manager.py install-python 3.11

# Create a virtual environment
./scripts/uv_manager.py create-venv /path/to/venv --python 3.11

# Create with custom timeout and retries
./scripts/uv_manager.py create-venv /path/to/venv --python 3.11 --timeout 600 --retries 5

# Install dependencies in a virtual environment
./scripts/uv_manager.py install-deps /path/to/venv --requirements requirements.txt
./scripts/uv_manager.py install-deps /path/to/venv --packages numpy pandas matplotlib

# Install a project in editable mode
./scripts/uv_manager.py install-editable /path/to/venv /path/to/project

# Show information about uv
./scripts/uv_manager.py info

# Clean the uv cache
./scripts/uv_manager.py clean-cache
./scripts/uv_manager.py clean-cache --older-than 30
```

### Cleanup and Maintenance (`scripts/cleanup_manager.py`)

The `scripts/cleanup_manager.py` script helps with cleaning up temporary files and maintaining the directory structure:

```bash
# Clean up temporary files older than 7 days
./scripts/cleanup_manager.py cleanup-tmp

# Check for orphaned virtual environments
./scripts/cleanup_manager.py check-orphaned-venvs

# Check the directory structure
./scripts/cleanup_manager.py check-structure

# Analyze disk usage
./scripts/cleanup_manager.py disk-usage
```

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

## Error Handling and Recovery

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

## Caching and Optimization

### Cache Management

- Use the designated cache directory (`$HOME/Agentic/cache/`) for all cached data.
- Organize cache files in subdirectories by purpose or application.
- Include cache invalidation mechanisms to prevent stale data.
- Regularly clean up old cache files using `./ag uv clean-cache`.
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
- Use `./ag venv backup` to create registry backups.
- Limit the number of backup files to prevent excessive disk usage.

### Recovery Procedures

- Document recovery procedures for common failure scenarios.
- Implement automatic recovery mechanisms where possible.
- Verify the integrity of restored files after recovery.
- Test recovery procedures periodically.
- Use `./ag env fix` to automatically repair common issues.

## Getting Started

To work with this framework:

1. Clone this repository
2. Run the setup script to fully set up the environment:
   ```bash
   ./scripts/setup_agentic.sh
   ```
   This script will:
   - Install required dependencies (uv)
   - Create all necessary directories
   - Initialize the virtual environment registry
   - Make utility scripts executable

   You can also run specific setup steps:
   ```bash
   # Install dependencies only
   ./scripts/setup_agentic.sh --install-dependencies
   
   # Create directories only
   ./scripts/setup_agentic.sh --create-directories
   
   # Initialize registry only
   ./scripts/setup_agentic.sh --initialize-registry
   ```

   If you encounter issues with the automated setup script (particularly network-related issues when installing dependencies), you can follow the [Manual Setup Guide](MANUAL_SETUP.md) to set up the environment manually.

3. Run `./ag env check` to verify the environment is set up correctly
4. Read the [Human Guide](HUMAN_GUIDE.md) for detailed instructions on how to use the framework
5. Use the `ag` command to manage your projects and environments
6. Follow the directory structure and guidelines when creating new projects

For AI agents: Review the [Agent Operation Rules](AGENT_RULES.md) or the [Quick Reference Guide](AGENT_QUICK_REFERENCE.md) to understand how to operate within this framework.

## Cross-References

This consolidated document includes information from the following files:

- [README.md](README.md) - Framework overview and basic usage instructions
- [AGENT_RULES.md](AGENT_RULES.md) - Comprehensive rules for AI agents
- [AGENT_QUICK_REFERENCE.md](AGENT_QUICK_REFERENCE.md) - Quick reference for AI agents
- [HUMAN_GUIDE.md](HUMAN_GUIDE.md) - Detailed instructions for human users
- [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - Explanation of the directory structure
- [MANUAL_SETUP.md](MANUAL_SETUP.md) - Step-by-step instructions for manual setup
- [LESSON_LEARNED.md](LESSON_LEARNED.md) - Important lessons learned during development and maintenance

When performing tasks, refer to this consolidated document to ensure all relevant information is considered.
