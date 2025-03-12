# Agent Quick Reference Guide

This document provides a concise reference of essential information for AI agents operating within the Agentic framework. For complete details, refer to [Agent Operation Rules](AGENT_RULES.md).

## Key Directories

```
$HOME/Agentic/
├── agentic/              # Core rules and tools
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
./check_environment.py
./check_environment.py --fix  # Auto-fix issues

# UV Package Manager
./uv_manager.py install       # Install uv
./uv_manager.py install-python 3.11  # Install Python
./uv_manager.py create-venv /path/to/project/.venv --python 3.11  # Create venv
```

### Virtual Environment Management

```bash
# List virtual environments
./venv_manager.py list

# Register a virtual environment
./venv_manager.py add /path/to/venv project-name

# Check virtual environment status
./venv_manager.py check --project-name project-name

# Clean up registry
./venv_manager.py cleanup
```

### Project Management

```bash
# Create a new project
./create_project.py "Project Name" --description "Description"

# Clean up temporary files
./cleanup_manager.py cleanup-tmp
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

## Error Recovery

If you encounter issues:

1. Check environment: `./check_environment.py`
2. Fix common issues: `./check_environment.py --fix`
3. Repair registry: `./venv_manager.py repair`
4. Clean up invalid environments: `./venv_manager.py cleanup`
