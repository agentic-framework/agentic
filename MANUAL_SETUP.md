# Manual Setup Guide for Agentic Framework

This guide provides step-by-step instructions for manually setting up the Agentic framework environment. This can be useful if the automated setup script (`setup_agentic.sh`) encounters issues, particularly with network connectivity when trying to install dependencies.

## Prerequisites

- A Unix-like operating system (macOS, Linux)
- Basic command-line knowledge

## Manual Setup Steps

### 1. Create the Directory Structure

First, create the necessary directory structure for the Agentic framework:

```bash
mkdir -p $HOME/Agentic/projects $HOME/Agentic/shared $HOME/Agentic/tmp $HOME/Agentic/logs $HOME/Agentic/cache $HOME/Agentic/backups
```

This creates:
- `$HOME/Agentic/projects`: For all agent-created projects
- `$HOME/Agentic/shared`: For shared resources between projects
- `$HOME/Agentic/tmp`: For temporary files
- `$HOME/Agentic/logs`: For log files
- `$HOME/Agentic/cache`: For cache files
- `$HOME/Agentic/backups`: For backup files

### 2. Initialize the Virtual Environment Registry

Create the virtual environment registry file:

```bash
cat > $HOME/Agentic/venv_registry.json << EOF
{
  "virtual_environments": [],
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "registry_version": "1.0.0",
  "metadata": {
    "description": "Registry of active Python virtual environments managed by uv",
    "managed_by": "agentic framework",
    "created_by": "manual setup"
  }
}
EOF
```

### 3. Make Utility Scripts Executable

Make all the utility scripts executable:

```bash
chmod +x $HOME/Agentic/agentic/*.py $HOME/Agentic/agentic/*.sh
```

### 4. Verify the Setup

Run the `check_environment.py` script to verify the setup:

```bash
cd $HOME/Agentic/agentic
./check_environment.py
```

This will show you what's working and what still needs to be addressed.

## Optional: Installing UV Package Manager

If you want to install the UV package manager (required for Python environment management in the Agentic framework), you can try:

```bash
cd $HOME/Agentic/agentic
./uv_manager.py install
```

If this fails due to network issues, you can install UV manually following the instructions at [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv).

## Optional: Installing Python

After installing UV, you can install Python:

```bash
cd $HOME/Agentic/agentic
./uv_manager.py install-python 3.11  # or your preferred version
```

## Optional: Creating Virtual Environments

To create a virtual environment for a project:

```bash
cd $HOME/Agentic/agentic
./uv_manager.py create-venv $HOME/Agentic/projects/your-project/.venv
./venv_manager.py add $HOME/Agentic/projects/your-project/.venv your-project
```

## Troubleshooting

### Logs Directory Missing

If you encounter an error like:

```
FileNotFoundError: [Errno 2] No such file or directory: '/Users/username/Agentic/logs/rule_loader.log'
```

This indicates that the logs directory is missing. Create it with:

```bash
mkdir -p $HOME/Agentic/logs
```

### Network Issues

If you encounter network issues when trying to install UV or Python, you might be behind a firewall or have connectivity problems. In this case, the manual setup described in this document should at least allow you to use the basic functionality of the Agentic framework.

## Conclusion

This manual setup provides the basic structure needed for the Agentic framework to function. While some advanced features that depend on UV and Python might not be available without those components, the basic framework structure is in place and can be used for organizing projects and following the Agentic guidelines.
