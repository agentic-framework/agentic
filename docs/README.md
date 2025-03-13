# Agentic

A framework for managing and operating AI agents with controlled access to a machine.

## Overview

This repository contains rules, guidelines, and tools for allowing AI agents to operate on a machine with significant freedom while maintaining security, organization, and best practices.

## Documentation Structure

The documentation is organized into six main sections:

- **For Humans (Overview)**: This README provides an overview of the framework, its features, and basic usage instructions.
- **For Humans (Detailed Guide)**: The [Human Guide](HUMAN_GUIDE.md) provides detailed instructions for human users on how to effectively use the framework and work with AI agents.
- **For Agents (Comprehensive)**: The [Agent Operation Rules](AGENT_RULES.md) document contains detailed rules and guidelines that AI agents should follow when operating on this machine.
- **For Agents (Quick Reference)**: The [Agent Quick Reference Guide](AGENT_QUICK_REFERENCE.md) provides a concise summary of essential information for AI agents, serving as a quick lookup resource for common tasks and rules.
- **Directory Structure**: The [Directory Structure Guide](DIRECTORY_STRUCTURE.md) provides a detailed explanation of the framework's directory structure, specifically addressing the distinction between the root Agentic folder and the git-managed repository folder.
- **Lessons Learned**: The [Lessons Learned](LESSON_LEARNED.md) document records important lessons learned during the development and maintenance of the framework, particularly focusing on git operations and common pitfalls.

## Directory Structure

For a detailed explanation of the directory structure, including the important distinction between the root Agentic folder and the git-managed repository folder, see the [Directory Structure Guide](DIRECTORY_STRUCTURE.md).

```
$HOME/Agentic/
├── agentic/              # Git-managed repository (rules and core tools)
│   ├── docs/             # Documentation files
│   ├── scripts/          # Utility scripts
│   ├── ag                # Main command-line interface
│   └── LICENSE           # License file
├── projects/             # All agent-created projects
├── shared/               # Shared resources
├── tmp/                  # Temporary files
├── logs/                 # Log files
├── cache/                # Cache for downloads and other data
└── backups/              # Backup files for registry and other critical data
```

## Utility Scripts

This repository includes several utility scripts to help agents follow the rules and manage the environment:

### Security Enforcement

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

### Configuration Management

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

### Rule Loading and Verification

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

### Environment Check

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

### Virtual Environment Management

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

### Project Creation

The `scripts/create_project.py` script creates new projects with the standard structure:

```bash
# Create a new project
./scripts/create_project.py "My New Project" --description "A description of the project"

# Create a new project with a specific license
./scripts/create_project.py "My New Project" --license Apache-2.0
```

### UV Package Manager

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

### Cleanup and Maintenance

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

3. Run `./scripts/check_environment.py` to verify the environment is set up correctly
4. Read the [Human Guide](HUMAN_GUIDE.md) for detailed instructions on how to use the framework
5. Use the utility scripts to manage your projects and environments
6. Follow the directory structure and guidelines when creating new projects

For AI agents: Review the [Agent Operation Rules](AGENT_RULES.md) or the [Quick Reference Guide](AGENT_QUICK_REFERENCE.md) to understand how to operate within this framework.

## Using with AI Agents

When working with AI agents (like Claude, GPT, etc.), you can instruct them to use the Agentic framework at the beginning of your conversation. Here are some example prompts to get started:

### Basic Framework Loading

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me with [your task].
```

### Quick Reference Loading

For simpler tasks where the agent doesn't need the full ruleset:

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Focus on the docs/AGENT_QUICK_REFERENCE.md file in the agentic subdirectory. Then help me with [your task].
```

### Creating a New Project

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then create a new Python project called [project name].
```

### Working with Virtual Environments

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then create a Python [version] virtual environment for [project name].
```

### Managing Existing Projects

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me update dependencies for [project name].
```

### Troubleshooting

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me diagnose issues with [project name].
```

These prompts instruct the AI agent to first understand the Agentic framework's rules and available tools before proceeding with your specific task. This ensures that the agent follows the established conventions and uses the provided utility scripts appropriately.

## Contributing

Contributions to improve the rules and guidelines are welcome. Please submit a pull request with your proposed changes.
