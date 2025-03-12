# Agentic

A framework for managing and operating AI agents with controlled access to a machine.

## Overview

This repository contains rules, guidelines, and tools for allowing AI agents to operate on a machine with significant freedom while maintaining security, organization, and best practices.

## Agent Rules

The [Agent Operation Rules](AGENT_RULES.md) document outlines the comprehensive set of rules and guidelines that agents must follow when operating on this machine. These rules cover:

- Python environment management using uv
- Directory structure and organization
- Project management practices
- Git and version control standards
- Security considerations
- And more

## Directory Structure

```
$HOME/Agentic/
├── agentic/              # This repository (rules and core tools)
├── projects/             # All agent-created projects
├── shared/               # Shared resources between projects
└── tmp/                  # Temporary files
```

## Utility Scripts

This repository includes several utility scripts to help agents follow the rules and manage the environment:

### Environment Check

The `check_environment.py` script verifies that the environment is set up correctly:

```bash
# Run a complete environment check
./check_environment.py
```

This script checks:
- UV installation
- Directory structure
- Registry file
- Utility scripts
- Python installations

### Virtual Environment Management

The `venv_manager.py` script helps manage Python virtual environments:

```bash
# List all registered virtual environments
./venv_manager.py list

# Add a virtual environment to the registry
./venv_manager.py add /path/to/venv project-name

# Remove a virtual environment from the registry
./venv_manager.py remove --project-name project-name

# Check if a virtual environment is registered
./venv_manager.py check --project-name project-name
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

## Getting Started

To work with this framework:

1. Clone this repository
2. Review the [Agent Operation Rules](AGENT_RULES.md)
3. Use the utility scripts to set up the environment
4. Follow the directory structure and guidelines when creating new projects

## Contributing

Contributions to improve the rules and guidelines are welcome. Please submit a pull request with your proposed changes.
