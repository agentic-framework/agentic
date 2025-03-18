# Agentic GitHub Integration

A plugin for the Agentic framework that provides GitHub integration capabilities through the GitHub CLI (`gh`).

## Overview

This plugin extends the Agentic framework with GitHub integration capabilities, allowing AI agents to interact with GitHub repositories, issues, pull requests, and workflows. It leverages the official GitHub CLI (`gh`) to provide a robust and maintainable implementation.

## Features

- **Repository Management**: Clone, create, fork, and manage repositories
- **Branch Operations**: Create, switch, and merge branches
- **Issue Tracking**: List, create, update, and manage issues
- **Pull Request Workflow**: Create, review, and merge pull requests
- **CI/CD Integration**: Monitor and interact with GitHub Actions workflows

## Installation

```bash
# Clone the repository
git clone git@github.com:agentic-framework/agentic-github.git ~/Agentic/projects/agentic-github

# Navigate to the repository
cd ~/Agentic/projects/agentic-github

# Install in development mode
pip install -e .
```

## Prerequisites

This plugin requires the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install GitHub CLI (macOS example)
brew install gh

# Authenticate with GitHub
gh auth login
```

## Usage

```bash
# Repository operations
ag github clone <repo-url> [--destination <path>]
ag github create <name> [--description "Description"] [--private]
ag github fork <repo-url>

# Branch operations
ag github branch create <branch-name>
ag github branch switch <branch-name>
ag github branch merge <source-branch> [--target <target-branch>]

# Issue operations
ag github issue list [--state open|closed|all] [--assignee <username>]
ag github issue create --title "Issue Title" --body "Description" [--labels bug,enhancement]
ag github issue update <issue-number> --state closed

# Pull request operations
ag github pr create --title "PR Title" --body "Description" --base main --head feature-branch
ag github pr list [--state open|closed|all]
ag github pr review <pr-number> [--approve|--request-changes|--comment] [--body "Review comment"]
ag github pr merge <pr-number> [--method merge|squash|rebase]

# CI/CD operations
ag github workflow list
ag github workflow run <workflow-name> [--ref <branch>]
ag github workflow status <run-id>
```

## Integration with Agentic Framework

This plugin integrates with the Agentic framework by:

1. Following the plugin architecture defined in the framework
2. Registering commands through entry points
3. Maintaining a registry of GitHub repositories
4. Synchronizing with the local issue tracking system

## License

This project is licensed under the MIT License - see the LICENSE file for details.
