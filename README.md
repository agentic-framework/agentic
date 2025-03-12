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
├── tmp/                  # Temporary files
├── logs/                 # Log files
├── cache/                # Cache for downloads and other data
└── backups/              # Backup files for registry and other critical data
```

## Utility Scripts

This repository includes several utility scripts to help agents follow the rules and manage the environment:

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

## Key Features

The Agentic framework includes several key features to ensure robustness and reliability:

### Error Handling and Recovery

- Robust error handling with detailed logging
- Automatic retry mechanisms for failed operations
- Verification steps to ensure operations complete successfully
- Recovery mechanisms for corrupted files and interrupted operations

### Network Resilience

- Configurable timeout settings for network operations
- Retry logic with exponential backoff
- Graceful handling of network failures

### Caching and Optimization

- Caching system for downloaded files and packages
- Parallel installation options for faster dependency resolution
- Cache management commands to clean up old cache files

### Logging and Monitoring

- Comprehensive logging system with configurable levels
- Log rotation and management
- Activity tracking and monitoring

### Backup and Restoration

- Automatic backup of critical files
- Registry backup and restoration mechanisms
- Recovery procedures for common failure scenarios

## Getting Started

To work with this framework:

1. Clone this repository
2. Run `./check_environment.py --fix` to set up the environment
3. Review the [Agent Operation Rules](AGENT_RULES.md)
4. Use the utility scripts to manage your projects and environments
5. Follow the directory structure and guidelines when creating new projects

## Using with AI Agents

When working with AI agents (like Claude, GPT, etc.), you can instruct them to use the Agentic framework at the beginning of your conversation. Here are some example prompts to get started:

### Basic Framework Loading

```
Read Agentic folders to load your rules and tools, and help me with [your task].
```

### Creating a New Project

```
Read Agentic folders to load your rules and tools, and create a new Python project called [project name].
```

### Working with Virtual Environments

```
Read Agentic folders to load your rules and tools, and create a Python [version] virtual environment for [project name].
```

### Managing Existing Projects

```
Read Agentic folders to load your rules and tools, and help me update dependencies for [project name].
```

### Troubleshooting

```
Read Agentic folders to load your rules and tools, and help me diagnose issues with [project name].
```

These prompts instruct the AI agent to first understand the Agentic framework's rules and available tools before proceeding with your specific task. This ensures that the agent follows the established conventions and uses the provided utility scripts appropriately.

## Contributing

Contributions to improve the rules and guidelines are welcome. Please submit a pull request with your proposed changes.
