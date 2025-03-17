# Agentic

A framework for managing and operating AI agents with controlled access to a machine.

## Overview

This repository contains rules, guidelines, and tools for allowing AI agents to operate on a machine with significant freedom while maintaining security, organization, and best practices.

## Documentation Structure

The documentation is organized into several main sections:

- **For Humans (Overview)**: This README provides an overview of the framework, its features, and basic usage instructions.
- **For Humans (Detailed Guide)**: The [Human Guide](HUMAN_GUIDE.md) provides detailed instructions for human users on how to effectively use the framework and work with AI agents.
- **For Agents (Comprehensive)**: The [Agent Operation Rules](AGENT_RULES.md) document contains detailed rules and guidelines that AI agents should follow when operating on this machine.
- **For Agents (Quick Reference)**: The [Agent Quick Reference Guide](AGENT_QUICK_REFERENCE.md) provides a concise summary of essential information for AI agents, serving as a quick lookup resource for common tasks and rules.
- **Directory Structure**: The [Directory Structure Guide](DIRECTORY_STRUCTURE.md) provides a detailed explanation of the framework's directory structure, specifically addressing the distinction between the root Agentic folder and the git-managed repository folder.
- **Lessons Learned**: The [Lessons Learned](LESSON_LEARNED.md) document records important lessons learned during the development and maintenance of the framework, particularly focusing on git operations and common pitfalls.
- **Setup Improvements**: The [Setup Improvements](SETUP_IMPROVEMENTS.md) document identifies obstacles encountered during the setup process and suggests improvements to the documentation.
- **Manual Setup**: The [Manual Setup Guide](MANUAL_SETUP.md) provides step-by-step instructions for setting up the environment manually if you encounter issues with the automated setup.
- **Plugin Development**: The [Plugin Development Guide](PLUGIN_DEVELOPMENT.md) explains how to develop plugins for the Agentic framework.

## Installation

There are two main ways to set up the Agentic framework, depending on your needs:

### Option 1: User Installation (Using the Framework)

If you just want to use the Agentic framework without modifying its core functionality:

```bash
# Install the command-line tool
pip install git+https://github.com/agentic-framework/agentic-core.git

# Run the setup command to fully set up the environment
ag setup all

# Verify the environment is set up correctly
ag env check
```

### Option 2: Developer Installation (Contributing to the Framework)

If you want to contribute to the Agentic framework or modify its core functionality:

1. **Create the directory structure**
   ```bash
   # Create the Agentic directory structure
   mkdir -p ~/Agentic/{projects,shared,tmp,logs,cache,backups}
   ```

2. **Clone the repositories**
   ```bash
   # Clone the core repository
   git clone git@github.com:agentic-framework/agentic-core.git ~/Agentic/projects/agentic-core
   
   # Clone the documentation repository
   git clone git@github.com:agentic-framework/agentic.git ~/Agentic/agentic
   
   # Clone plugin repositories (optional)
   git clone git@github.com:agentic-framework/agentic-issues.git ~/Agentic/projects/agentic-issues
   git clone git@github.com:agentic-framework/agentic-notes.git ~/Agentic/projects/agentic-notes
   ```

3. **Create and activate a virtual environment**
   ```bash
   # Create a virtual environment
   python3 -m venv ~/Agentic/.venv
   
   # Activate the virtual environment
   source ~/Agentic/.venv/bin/activate
   ```

4. **Install the packages in development mode**
   ```bash
   # Install the core package
   cd ~/Agentic/projects/agentic-core
   pip install -e .
   
   # Install plugins (optional)
   cd ~/Agentic/projects/agentic-issues
   pip install -e .
   
   cd ~/Agentic/projects/agentic-notes
   pip install -e .
   ```

5. **Register the virtual environment**
   ```bash
   ag venv add ~/Agentic/.venv agentic-core --description "Main virtual environment for Agentic framework"
   ```

6. **Verify the setup**
   ```bash
   # Run environment check
   ag env check
   
   # Fix any issues
   ag env fix
   ```

## Directory Structure

The Agentic framework uses a specific directory structure to organize files and maintain separation between different components:

```
$AGHOME/
├── agentic/              # Git-managed repository (rules and documentation)
│   ├── bin/              # Executable scripts (agx, agx-content)
│   ├── docs/             # Documentation files
│   ├── rules.json        # Structured rules in machine-readable format
│   └── LICENSE           # License file
├── projects/             # All agent-created projects
│   └── agentic-core/     # Core implementation repository
│       └── agentic_info.json  # Framework configuration
├── shared/               # Shared resources
├── tmp/                  # Temporary files
├── logs/                 # Log files
├── cache/                # Cache for downloads and other data
└── backups/              # Backup files for registry and other critical data
```

For a detailed explanation of the directory structure, see the [Directory Structure Guide](DIRECTORY_STRUCTURE.md).

### Customizing the Agentic Home Directory

By default, the Agentic framework uses `~/Agentic` as the home directory. You can customize this location by setting the `AGHOME` environment variable:

```bash
# Set the AGHOME environment variable
export AGHOME=/path/to/your/custom/agentic/directory

# Use the ag command with the custom location
ag env check
```

This allows you to install the Agentic framework in a different location while maintaining all functionality.

## Official Plugins

The Agentic framework can be extended with plugins that add new functionality. Here are the official plugins:

### Issues Management (agentic-issues)

The issues plugin provides issue tracking capabilities for Agentic projects:

```bash
# Installation
git clone git@github.com:agentic-framework/agentic-issues.git ~/Agentic/projects/agentic-issues
cd ~/Agentic/projects/agentic-issues
pip install -e .

# Usage
ag issue list
ag issue submit --title "Issue Title" --description "Description" --priority medium --labels bug,feature
ag issue show <issue-id>
ag issue update <issue-id> --status resolved
ag issue comment <issue-id> "Comment text"
```

### Note Taking (agentic-notes)

The notes plugin provides note-taking capabilities for the Agentic framework:

```bash
# Installation
git clone git@github.com:agentic-framework/agentic-notes.git ~/Agentic/projects/agentic-notes
cd ~/Agentic/projects/agentic-notes
pip install -e .

# Usage
ag note create "Note Title" "Note content" --tags tag1,tag2
ag note list
ag note view <note-id>
ag note update <note-id> --title "New Title" --content "New content"
ag note delete <note-id>
ag note search "query"
```

For information on developing your own plugins, see the [Plugin Development Guide](PLUGIN_DEVELOPMENT.md).

## Core Commands

The Agentic framework provides a set of core commands for managing the environment:

### Security Enforcement

```bash
# Check if a path is allowed
ag security check-path /path/to/check

# Validate a command for execution
ag security validate-command "command to validate"

# Scan a file for potential security violations
ag security scan-file /path/to/file

# Calculate the SHA-256 hash of a file
ag security hash-file /path/to/file

# Verify the integrity of a file
ag security verify-integrity /path/to/file expected-hash
```

### Configuration Management

```bash
# Get a configuration value
ag config get paths.agentic_root

# Set a configuration value
ag config set python.default_python_version 3.12

# List all configuration values
ag config list

# List a specific section
ag config list --section paths

# Check if a path is allowed
ag config check /path/to/check

# Reset configuration to defaults
ag config reset
```

### Rule Loading and Verification

```bash
# Verify an AI agent's understanding of the rules
ag rule verify

# Run verification in non-interactive mode
ag rule verify --non-interactive

# Save verification results to a file
ag rule verify --output /path/to/results.json

# Query specific rules
ag rule query python_environment
ag rule query python_environment --subcategory virtual_environments
ag rule query python_environment --subcategory virtual_environments --key location

# List rule categories
ag rule list

# List utility scripts
ag rule list --utility-scripts
```

### Environment Check

```bash
# Run a complete environment check
ag env check

# Run environment check and automatically fix common issues
ag env fix
```

### Virtual Environment Management

```bash
# List all registered virtual environments
ag venv list

# List with detailed information
ag venv list --verbose

# List with package information
ag venv list --packages

# Add a virtual environment to the registry
ag venv add /path/to/venv project-name

# Add with additional information
ag venv add /path/to/venv project-name --description "Description" --python-version "3.12.9"

# Remove a virtual environment from the registry
ag venv remove --project-name project-name
ag venv remove --venv-path /path/to/venv

# Check if a virtual environment is registered and verify its status
ag venv check --project-name project-name
ag venv check --venv-path /path/to/venv

# Update the package list for a virtual environment
ag venv update-packages --project-name project-name

# Clean up non-existent virtual environments
ag venv cleanup

# Scan for and repair the registry
ag venv repair

# Create a backup of the registry
ag venv backup
```

### Project Creation

```bash
# Create a new project
ag project create "My New Project" --description "A description of the project"

# Create a new project with a specific license
ag project create "My New Project" --license Apache-2.0
```

### UV Package Manager

```bash
# Install uv
ag uv install

# Update uv
ag uv update

# List available Python versions
ag uv list-python

# Install a specific Python version
ag uv install-python 3.11

# Create a virtual environment
ag uv create-venv /path/to/venv --python 3.11

# Create with custom timeout and retries
ag uv create-venv /path/to/venv --python 3.11 --timeout 600 --retries 5

# Install dependencies in a virtual environment
ag uv install-deps /path/to/venv --requirements requirements.txt
ag uv install-deps /path/to/venv --packages numpy pandas matplotlib

# Install a project in editable mode
ag uv install-editable /path/to/venv /path/to/project

# Show information about uv
ag uv info

# Clean the uv cache
ag uv clean-cache
ag uv clean-cache --older-than 30
```

### Cleanup and Maintenance

```bash
# Clean up temporary files older than 7 days
ag cleanup tmp

# Check for orphaned virtual environments
ag cleanup check-orphaned-venvs

# Check the directory structure
ag cleanup check-structure

# Analyze disk usage
ag cleanup disk-usage
```

## Command Wrapper Scripts

The Agentic framework includes wrapper scripts that improve the usability of the `ag` command:

### agx - Command Launcher

The `agx` script is a launcher for the `ag` command that detects the appropriate virtual environment to use:

```bash
# Use the agx script directly
$AGHOME/agentic/bin/agx note list
```

This script makes the `ag` command available from anywhere by creating a symbolic link in `$HOME/bin`.

### agx-content - Content Handler

The `agx-content` script handles large content and special characters in commands:

```bash
# Install the content handler
$AGHOME/agentic/fix_shell_issues.sh
```

This script automatically uses temporary files for large content or content with special characters, solving issues with shell escaping.

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

## Troubleshooting

If you encounter issues during setup or usage, try these steps:

1. **Run the environment check with fix option**
   ```bash
   ag env check --fix
   ```

2. **Check the logs for error messages**
   ```bash
   cat ~/Agentic/logs/agentic.log
   ```

3. **Verify the virtual environment registry**
   ```bash
   ag venv list
   ag venv repair
   ```

4. **Check for missing directories**
   ```bash
   ag cleanup check-structure
   ```

5. **Reinstall the core package**
   ```bash
   pip install --force-reinstall git+https://github.com/agentic-framework/agentic-core.git
   ```

6. **Follow the manual setup guide**
   If automated setup fails, follow the [Manual Setup Guide](MANUAL_SETUP.md) for step-by-step instructions.

## Using with AI Agents

When working with AI agents (like Claude, GPT, etc.), you can instruct them to use the Agentic framework at the beginning of your conversation. Here are some example prompts to get started:

### Basic Framework Loading

```
Read the Agentic framework located at $AGHOME to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me with [your task].
```

### Quick Reference Loading

For simpler tasks where the agent doesn't need the full ruleset:

```
Read the Agentic framework located at $AGHOME to load your rules and tools. Focus on the docs/AGENT_QUICK_REFERENCE.md file in the agentic subdirectory. Then help me with [your task].
```

### Creating a New Project

```
Read the Agentic framework located at $AGHOME to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then create a new Python project called [project name].
```

### Working with Virtual Environments

```
Read the Agentic framework located at $AGHOME to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then create a Python [version] virtual environment for [project name].
```

### Managing Existing Projects

```
Read the Agentic framework located at $AGHOME to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me update dependencies for [project name].
```

### Troubleshooting

```
Read the Agentic framework located at $AGHOME to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me diagnose issues with [project name].
```

These prompts instruct the AI agent to first understand the Agentic framework's rules and available tools before proceeding with your specific task. This ensures that the agent follows the established conventions and uses the provided utility scripts appropriately.

## Contributing

Contributions to improve the rules and guidelines are welcome. Please submit a pull request with your proposed changes.
