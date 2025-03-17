# Agentic Framework Plugins Guide

This guide provides detailed information about the official plugins available for the Agentic framework, focusing on the issues and notes plugins.

## Overview

The Agentic framework can be extended with plugins that add new functionality through the `ag` command. Plugins are implemented as Python packages that register entry points in the `agentic.commands` group, allowing them to be discovered and loaded by the `ag` command.

## Available Plugins

### Issues Management (agentic-issues)

The issues plugin provides issue tracking capabilities for Agentic projects, allowing you to create, list, view, update, and comment on issues.

#### Installation

```bash
# Clone the repository
git clone git@github.com:agentic-framework/agentic-issues.git ~/Agentic/projects/agentic-issues

# Navigate to the repository
cd ~/Agentic/projects/agentic-issues

# Install in development mode
pip install -e .
```

#### Usage

```bash
# List issues for the current project
ag issue list

# List issues with specific status
ag issue list --status open
ag issue list --status resolved

# List issues for a specific project
ag issue list --project project-name

# Show details of a specific issue
ag issue show <issue-id>

# Submit a new issue
ag issue submit --title "Issue Title" --description "Issue Description" --priority medium --labels bug,feature

# Update an existing issue
ag issue update <issue-id> --status resolved --priority low

# Add a comment to an issue
ag issue comment <issue-id> "Comment text"
```

#### Features

- **Project-based organization**: Issues are organized by project, making it easy to track issues for specific projects.
- **Status tracking**: Issues can have different statuses (open, in-progress, resolved, etc.) to track their progress.
- **Priority levels**: Issues can be assigned priority levels (low, medium, high, critical) to indicate their importance.
- **Labels**: Issues can be tagged with labels to categorize them (bug, feature, documentation, etc.).
- **Comments**: Users can add comments to issues to provide updates or additional information.
- **JSON storage**: Issues are stored in JSON files in the project directory, making them easy to version control and share.

#### Data Storage

Issues are stored in a JSON file in the project directory:

```
project-name/
└── .agentic/
    └── issues/
        └── issues.json
```

### Note Taking (agentic-notes)

The notes plugin provides note-taking capabilities for the Agentic framework, allowing you to create, list, view, update, delete, and search notes.

#### Installation

```bash
# Clone the repository
git clone git@github.com:agentic-framework/agentic-notes.git ~/Agentic/projects/agentic-notes

# Navigate to the repository
cd ~/Agentic/projects/agentic-notes

# Install in development mode
pip install -e .
```

#### Usage

```bash
# Create a new note
ag note create "Note Title" "Note content goes here" --tags tag1,tag2

# List all notes
ag note list

# List notes with a specific tag
ag note list --tag tag1

# View a note
ag note view <note-id>

# Update a note
ag note update <note-id> --title "New Title" --content "New content" --tags tag1,tag3

# Delete a note
ag note delete <note-id>

# Search notes
ag note search "query"
```

#### Features

- **Rich text content**: Notes can contain rich text content, including Markdown formatting.
- **Tagging**: Notes can be tagged with multiple tags for easy organization and filtering.
- **Full-text search**: Notes can be searched by title, content, or tags.
- **Timestamps**: Notes include creation and update timestamps for tracking changes.
- **JSON storage**: Notes are stored in JSON files in the shared directory, making them accessible across projects.

#### Data Storage

Notes are stored in a JSON file in the shared directory:

```
$AGHOME/
└── shared/
    └── notes/
        └── notes.json
```

## Developing Plugins

For information on developing your own plugins for the Agentic framework, see the [Plugin Development Guide](PLUGIN_DEVELOPMENT.md).

## Troubleshooting

### Plugin Not Found

If a plugin is not found when running `ag <plugin-name>`, check:

1. Is the plugin installed in the current environment?
   ```bash
   pip list | grep agentic
   ```

2. Are the entry points correctly registered?
   ```bash
   python -c "import importlib.metadata; print(importlib.metadata.entry_points(group='agentic.commands'))"
   ```

3. Is the plugin command function implemented correctly?
   ```bash
   ag --debug <plugin-name>
   ```

### Command Not Working

If a plugin command is not working correctly, check:

1. Are you using the correct syntax?
   ```bash
   ag <plugin-name> --help
   ```

2. Are there any error messages in the logs?
   ```bash
   cat ~/Agentic/logs/agentic.log
   ```

3. Is the plugin data file accessible and valid?
   ```bash
   # For issues
   cat <project-dir>/.agentic/issues/issues.json
   
   # For notes
   cat ~/Agentic/shared/notes/notes.json
   ```

## Best Practices

### Issues Management

- **Use descriptive titles**: Make issue titles clear and descriptive to help others understand the issue at a glance.
- **Provide detailed descriptions**: Include all relevant information in the issue description, such as steps to reproduce, expected behavior, and actual behavior.
- **Use appropriate priority levels**: Reserve high and critical priorities for issues that truly need immediate attention.
- **Use labels consistently**: Establish a consistent set of labels for your projects and use them consistently.
- **Keep issues updated**: Update issue status and add comments as progress is made.

### Note Taking

- **Organize with tags**: Use tags to organize notes by topic, project, or status.
- **Use Markdown formatting**: Take advantage of Markdown formatting to make notes more readable and structured.
- **Include code snippets**: Use code blocks for code snippets to make them easy to read and copy.
- **Link related notes**: Reference related notes by ID or title to create a network of connected information.
- **Regular cleanup**: Periodically review and clean up old or outdated notes.

## Conclusion

The issues and notes plugins provide essential functionality for managing projects and capturing information in the Agentic framework. By following the installation and usage instructions in this guide, you can effectively use these plugins to enhance your workflow.
