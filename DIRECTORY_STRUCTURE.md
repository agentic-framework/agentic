# Agentic Framework Directory Structure

This document provides a clear explanation of the Agentic framework's directory structure, specifically addressing the distinction between the root Agentic folder and the git-managed repository folder.

## Directory Hierarchy

```
$HOME/
└── Agentic/                  # Root Agentic folder (not under version control)
    ├── agentic/              # Git-managed repository folder (under version control)
    │   ├── README.md         # Framework overview
    │   ├── AGENT_RULES.md    # Comprehensive rules for AI agents
    │   ├── AGENT_QUICK_REFERENCE.md  # Quick reference for AI agents
    │   ├── HUMAN_GUIDE.md    # Guide for human users
    │   ├── DIRECTORY_STRUCTURE.md  # This file
    │   ├── ag                # Main command-line interface
    │   ├── check_environment.py  # Environment verification script (legacy)
    │   ├── venv_manager.py   # Virtual environment management script (legacy)
    │   ├── create_project.py # Project creation script (legacy)
    │   ├── uv_manager.py     # UV package manager script (legacy)
    │   └── cleanup_manager.py  # Cleanup and maintenance script (legacy)
    │
    ├── projects/             # All agent-created projects (not under version control)
    ├── shared/               # Shared resources between projects (not under version control)
    ├── tmp/                  # Temporary files (not under version control)
    ├── logs/                 # Log files (not under version control)
    ├── cache/                # Cache for downloads and other data (not under version control)
    ├── backups/              # Backup files for registry and other critical data (not under version control)
    └── venv_registry.json    # Registry of virtual environments (not under version control)
```

## Key Distinctions

### Root Agentic Folder (`$HOME/Agentic/`)

- **Purpose**: Serves as the container for all Agentic framework components, including the repository, projects, and supporting directories
- **Version Control**: Not under version control
- **Content**: Contains the git repository, project directories, and supporting directories
- **Management**: Managed by the framework's utility scripts
- **Path Reference**: Always referenced as `$HOME/Agentic` in documentation and scripts

### Git-Managed Repository Folder (`$HOME/Agentic/agentic/`)

- **Purpose**: Contains the core framework code, documentation, and utility scripts
- **Version Control**: Under git version control
- **Content**: Contains documentation files and utility scripts
- **Management**: Managed through git commands (pull, push, commit, etc.)
- **Path Reference**: Always referenced as `$HOME/Agentic/agentic` in documentation and scripts

## Important Considerations

### When Using Git Commands

When working with git commands, they should be executed within the git-managed repository folder:

```bash
# Correct
cd $HOME/Agentic/agentic
git pull

# Incorrect
cd $HOME/Agentic
git pull  # This will fail because this directory is not a git repository
```

### When Creating Projects

Projects should always be created in the projects directory, not in the git-managed repository:

```bash
# Correct
$HOME/Agentic/agentic/ag project create "My Project"  # This will create the project in $HOME/Agentic/projects/my-project

# Incorrect
cd $HOME/Agentic/agentic
./ag project create "My Project"  # Don't create projects inside the git repository
```

### When Referencing Paths in Scripts

Scripts should use the correct paths when referencing different parts of the framework:

```python
# Correct
AGENTIC_ROOT = os.path.expanduser("~/Agentic")
AGENTIC_REPO = os.path.join(AGENTIC_ROOT, "agentic")
PROJECTS_DIR = os.path.join(AGENTIC_ROOT, "projects")

# Incorrect
AGENTIC_DIR = os.path.expanduser("~/Agentic/agentic")  # This only points to the repository, not the root
PROJECTS_DIR = os.path.join(AGENTIC_DIR, "projects")  # This would incorrectly point to ~/Agentic/agentic/projects
```

## Visual Representation

```
$HOME/Agentic/                  <-- Root Agentic folder (not git-managed)
│
├── agentic/                    <-- Git repository (git-managed)
│   └── [framework files]
│
└── [other directories]         <-- Not git-managed
```

This clear separation ensures that:

1. The git repository only contains the framework code and documentation
2. User-generated content (projects, logs, etc.) remains separate from the version-controlled code
3. The framework can be updated without affecting user projects
4. Backups and temporary files don't get committed to version control

## Conclusion

Understanding the distinction between the root Agentic folder and the git-managed repository folder is crucial for correctly using the framework. Always be mindful of which directory you're working in, especially when using git commands or creating new projects.
