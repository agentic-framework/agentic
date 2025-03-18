# GitHub Integration Usage Guide

This guide explains how to use the GitHub integration plugin for the Agentic framework.

## Prerequisites

Before using the GitHub integration, you need to:

1. Install the GitHub CLI (`gh`):
   ```bash
   # macOS
   brew install gh
   
   # Linux
   # See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
   
   # Windows
   # See https://github.com/cli/cli#installation
   ```

2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

3. Install the agentic-github plugin:
   ```bash
   cd ~/Agentic/projects/agentic-github
   pip install -e .
   ```

## Repository Operations

### Clone a Repository

Clone a GitHub repository to the Agentic projects directory:

```bash
ag github clone https://github.com/username/repo.git
```

You can specify a custom destination:

```bash
ag github clone https://github.com/username/repo.git --destination ~/Agentic/projects/custom-name
```

### Create a Repository

Create a new GitHub repository:

```bash
ag github create repo-name --description "Repository description" --private
```

### Fork a Repository

Fork an existing GitHub repository:

```bash
ag github fork https://github.com/username/repo.git
```

## Branch Operations

### Create a Branch

Create a new branch in a repository:

```bash
ag github branch create feature-branch --repo repo-name
```

### Switch to a Branch

Switch to an existing branch:

```bash
ag github branch switch feature-branch --repo repo-name
```

### Merge a Branch

Merge a branch into another branch:

```bash
ag github branch merge feature-branch --target main --repo repo-name
```

## Issue Operations

### List Issues

List issues in a repository:

```bash
ag github issue list --state open --repo repo-name
```

You can filter by state (`open`, `closed`, `all`) and assignee:

```bash
ag github issue list --state open --assignee username --repo repo-name
```

### Create an Issue

Create a new issue:

```bash
ag github issue create --title "Issue title" --body "Issue description" --labels bug,enhancement --repo repo-name
```

### View an Issue

View details of an issue:

```bash
ag github issue view 123 --repo repo-name
```

### Update an Issue

Update the state of an issue:

```bash
ag github issue update 123 --state closed --repo repo-name
```

## Pull Request Operations

### List Pull Requests

List pull requests in a repository:

```bash
ag github pr list --state open --repo repo-name
```

You can filter by state (`open`, `closed`, `merged`, `all`):

```bash
ag github pr list --state all --repo repo-name
```

### Create a Pull Request

Create a new pull request:

```bash
ag github pr create --title "PR title" --body "PR description" --base main --head feature-branch --repo repo-name
```

### View a Pull Request

View details of a pull request:

```bash
ag github pr view 123 --repo repo-name
```

### Review a Pull Request

Review a pull request:

```bash
ag github pr review 123 --action approve --body "LGTM!" --repo repo-name
```

Available actions: `approve`, `request-changes`, `comment`

### Merge a Pull Request

Merge a pull request:

```bash
ag github pr merge 123 --method squash --repo repo-name
```

Available methods: `merge`, `squash`, `rebase`

## Workflow Operations

### List Workflows

List GitHub Actions workflows in a repository:

```bash
ag github workflow list --repo repo-name
```

### Run a Workflow

Run a GitHub Actions workflow:

```bash
ag github workflow run workflow-name --ref main --repo repo-name
```

### Check Workflow Status

Check the status of a workflow run:

```bash
ag github workflow status run-id --repo repo-name
```

## Synchronization Operations

### Synchronize Issues

Synchronize GitHub issues with local issues:

```bash
ag github sync issues repo-name
```

## Integration with Agentic Framework

The GitHub integration plugin integrates with the Agentic framework by:

1. Following the plugin architecture defined in the framework
2. Registering commands through entry points
3. Maintaining a registry of GitHub repositories
4. Synchronizing with the local issue tracking system

## Troubleshooting

### GitHub CLI Not Found

If you see an error like:

```
GitHub CLI (gh) not found. Please install it and authenticate.
```

Follow the installation instructions at https://github.com/cli/cli#installation and then run `gh auth login`.

### Authentication Issues

If you see an error like:

```
GitHub CLI is not authenticated. Please run: gh auth login
```

Run `gh auth login` to authenticate with GitHub.

### Repository Not Found

If you see an error like:

```
Repository repo-name not found in registry
```

Make sure the repository is cloned or created using the GitHub integration plugin.
