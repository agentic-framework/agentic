# Agent Quick Reference Guide

This document provides a concise reference of essential information for AI agents operating within the Agentic framework. For complete details, refer to [Agent Operation Rules](AGENT_RULES.md).

> **Important**: All rules are available in a structured, machine-readable format in the `rules.json` file. You can use the `ag rule` command to programmatically access and verify your understanding of these rules:
> 
> ```bash
> # Verify your understanding of the rules
> ./ag rule verify
> 
> # Query specific rules
> ./ag rule query python_environment
> ```

## Key Directories

```
$HOME/Agentic/
├── agentic/              # Core rules and tools
│   ├── docs/             # Documentation files
│   ├── scripts/          # Utility scripts
│   ├── ag                # Main command-line interface
│   └── LICENSE           # License file
├── projects/             # All agent-created projects
├── shared/               # Shared resources
├── tmp/                  # Temporary files
├── logs/                 # Log files
├── cache/                # Cache files
└── backups/              # Backup files
```

## Essential Commands

### Environment Management

```bash
# Check environment setup
./ag env check
./ag env fix  # Auto-fix issues

# UV Package Manager
./ag uv install       # Install uv
./ag uv install-python 3.11  # Install Python
./ag venv create /path/to/project/.venv --python 3.11  # Create venv
```

### Virtual Environment Management

```bash
# List virtual environments
./ag venv list

# Create a virtual environment
./ag venv create /path/to/venv project-name

# Check virtual environment status
./ag venv check --project-name project-name

# Clean up registry
./ag venv cleanup
```

### Project Management

```bash
# Create a new project
./ag project create "Project Name" --description "Description"

# List existing projects
./ag project list

# Clean up temporary files
./ag cleanup tmp
```

## Standard Project Structure

```
project-name/
├── .venv/                 # Virtual environment
├── src/                   # Source code
├── tests/                 # Test files
├── docs/                  # Documentation
├── data/                  # Data files
├── notebooks/             # Jupyter notebooks
├── logs/                  # Log files
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── LICENSE                # License file
└── pyproject.toml         # Project configuration
```

## Naming Conventions

- **Project directories**: kebab-case (e.g., `my-project-name`)
- **Python modules/packages**: snake_case
- **Classes**: PascalCase
- **Functions/variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE

## Critical Rules

1. **Python Management**:
   - Use uv exclusively for Python package management
   - Always use virtual environments for projects
   - Register all virtual environments

2. **Directory Usage**:
   - Create all projects under `$HOME/Agentic/projects/`
   - Use appropriate directories for logs, cache, etc.

3. **Security**:
   - Do not modify system files outside designated areas
   - Do not store sensitive information in code
   - Use secure connections for network operations

4. **Error Handling**:
   - Implement proper error handling in all code
   - Log errors appropriately
   - Use retry mechanisms for transient failures

5. **Resource Management**:
   - Clean up resources after tasks
   - Monitor and limit CPU/memory usage
   - Regularly clean cache and temporary files

## Common Patterns

### Creating a New Python Project

```bash
# 1. Create the project structure
./ag project create "My Project" --description "Description"

# 2. Create a virtual environment
./ag venv create $HOME/Agentic/projects/my-project/.venv --python 3.11

# 3. Install dependencies
./ag uv install-deps $HOME/Agentic/projects/my-project/.venv --packages numpy pandas
```

### Working with Existing Projects

```bash
# 1. Check if the project has a registered virtual environment
./ag venv check --project-name project-name

# 2. Update package list
./ag venv update-packages --project-name project-name

# 3. Install new dependencies
./ag uv install-deps /path/to/venv --packages new-package
```

## Error Recovery

If you encounter issues:

1. Check environment: `./ag env check`
2. Fix common issues: `./ag env fix`
3. Repair registry: `./ag venv repair`
4. Clean up invalid environments: `./ag venv cleanup`

## Environment Variables

The Agentic framework uses the following environment variables:

- `AGHOME`: Custom location for the Agentic home directory (default: `~/Agentic`)
  ```bash
  # Example: Using a custom Agentic home directory
  export AGHOME=/path/to/custom/agentic
  ag env check
  ```
