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

The security commands provide technical enforcement mechanisms to ensure AI agents operate only within their designated areas:

```bash
# Check if a path is allowed
./ag security check-path /path/to/check

# Validate a command for execution
./ag security validate-command "command to validate"

# Scan a file for potential security violations
./ag security scan-file /path/to/file

# Calculate the SHA-256 hash of a file
./ag security hash-file /path/to/file

# Verify the integrity of a file
./ag security verify-integrity /path/to/file expected-hash
```

This script enforces security boundaries, validates operations, and logs security events. It helps prevent AI agents from accessing or modifying files outside their designated areas.

### Configuration Management

The config commands provide a centralized configuration system for the Agentic framework:

```bash
# Get a configuration value
./ag config get paths.agentic_root

# Set a configuration value
./ag config set python.default_python_version 3.12

# List all configuration values
./ag config list

# List a specific section
./ag config list --section paths

# Check if a path is allowed
./ag config check /path/to/check

# Reset configuration to defaults
./ag config reset
```

This script provides a standardized API for accessing configuration values and handles path variability across different installations. All other scripts in the framework use this configuration system to ensure consistency.

### Rule Loading and Verification

The rule commands provide utilities for loading, verifying, and querying the Agentic framework rules:

```bash
# Verify an AI agent's understanding of the rules
./ag rule verify

# Run verification in non-interactive mode
./ag rule verify --non-interactive

# Save verification results to a file
./ag rule verify --output /path/to/results.json

# Query specific rules
./ag rule query python_environment
./ag rule query python_environment --subcategory virtual_environments
./ag rule query python_environment --subcategory virtual_environments --key location

# List rule categories
./ag rule list

# List utility scripts
./ag rule list --utility-scripts
```

This script uses a structured rules file (`rules.json`) that contains all the framework rules in a machine-readable format, enabling programmatic access and verification.

### Environment Check

The env commands verify that the environment is set up correctly:

```bash
# Run a complete environment check
./ag env check

# Run environment check and automatically fix common issues
./ag env fix
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

The venv commands help manage Python virtual environments:

```bash
# List all registered virtual environments
./ag venv list

# List with detailed information
./ag venv list --verbose

# List with package information
./ag venv list --packages

# Add a virtual environment to the registry
./ag venv add /path/to/venv project-name

# Add with additional information
./ag venv add /path/to/venv project-name --description "Description" --python-version "3.12.9"

# Remove a virtual environment from the registry
./ag venv remove --project-name project-name
./ag venv remove --venv-path /path/to/venv

# Check if a virtual environment is registered and verify its status
./ag venv check --project-name project-name
./ag venv check --venv-path /path/to/venv

# Update the package list for a virtual environment
./ag venv update-packages --project-name project-name

# Clean up non-existent virtual environments
./ag venv cleanup

# Scan for and repair the registry
./ag venv repair

# Create a backup of the registry
./ag venv backup
```

### Project Creation

The project commands create new projects with the standard structure:

```bash
# Create a new project
./ag project create "My New Project" --description "A description of the project"

# Create a new project with a specific license
./ag project create "My New Project" --license Apache-2.0
```

### UV Package Manager

The uv commands help with installing and managing uv:

```bash
# Install uv
./ag uv install

# Update uv
./ag uv update

# List available Python versions
./ag uv list-python

# Install a specific Python version
./ag uv install-python 3.11

# Create a virtual environment
./ag uv create-venv /path/to/venv --python 3.11

# Create with custom timeout and retries
./ag uv create-venv /path/to/venv --python 3.11 --timeout 600 --retries 5

# Install dependencies in a virtual environment
./ag uv install-deps /path/to/venv --requirements requirements.txt
./ag uv install-deps /path/to/venv --packages numpy pandas matplotlib

# Install a project in editable mode
./ag uv install-editable /path/to/venv /path/to/project

# Show information about uv
./ag uv info

# Clean the uv cache
./ag uv clean-cache
./ag uv clean-cache --older-than 30
```

### Cleanup and Maintenance

The cleanup commands help with cleaning up temporary files and maintaining the directory structure:

```bash
# Clean up temporary files older than 7 days
./ag cleanup tmp

# Check for orphaned virtual environments
./ag cleanup check-orphaned-venvs

# Check the directory structure
./ag cleanup check-structure

# Analyze disk usage
./ag cleanup disk-usage
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

3. Run `./ag env check` to verify the environment is set up correctly
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
