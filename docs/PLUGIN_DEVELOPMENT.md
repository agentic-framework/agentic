# Plugin Development Guide

This guide explains how to develop plugins for the Agentic framework. Plugins extend the functionality of the `ag` command by adding new subcommands.

## Overview

The Agentic framework uses a plugin mechanism based on Python's entry points system. This allows developers to create new commands that can be accessed through the `ag` command-line interface. For example, the `agentic-note` plugin adds a `note` subcommand that can be accessed via `ag note`.

## Plugin Architecture

The plugin architecture consists of three main components:

1. **Command Function**: A Python function that implements the command logic
2. **Entry Point Registration**: Registration of the command function as an entry point
3. **Plugin Discovery**: The mechanism by which the `ag` command discovers and loads plugins

## Creating a Plugin

Follow these steps to create a new plugin for the Agentic framework:

### 1. Create a New Project

Start by creating a new project using the `ag project create` command:

```bash
ag project create "agentic-myplugin" --description "Description of your plugin"
```

This will create a new project with the standard directory structure.

### 2. Implement the Command Function

Create a module that implements your command functionality. The command function must follow this interface:

1. Take no arguments (it will parse `sys.argv` directly)
2. Return an integer exit code (0 for success, non-zero for failure)
3. Handle its own argument parsing

Here's an example implementation:

```python
# src/agentic_myplugin/cli.py

import argparse
import sys

def create_parser():
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="My Plugin - Description of your plugin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
          # Example command
          ag myplugin subcommand --option value
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add subcommands here
    example_parser = subparsers.add_parser("example", help="Example subcommand")
    example_parser.add_argument("--option", help="Example option")
    
    return parser

def process_command(args):
    """Process the command with the given arguments."""
    if not args.command:
        create_parser().print_help()
        return 1
    
    # Implement command logic here
    if args.command == "example":
        print(f"Example command executed with option: {args.option}")
        return 0
    
    return 1

def main():
    """Main entry point for the standalone CLI."""
    parser = create_parser()
    args = parser.parse_args()
    return process_command(args)

def myplugin_command():
    """
    Entry point for the 'ag myplugin' command.
    
    This function follows the command interface for agentic-core plugins:
    1. Takes no arguments (it parses sys.argv directly)
    2. Returns an integer exit code (0 for success, non-zero for failure)
    3. Handles its own argument parsing
    """
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    return process_command(args)

if __name__ == "__main__":
    sys.exit(main())
```

### 3. Register the Entry Point

In your `pyproject.toml` file, register your command function as an entry point in the `agentic.commands` group:

```toml
[project.scripts]
ag-myplugin = "agentic_myplugin.cli:main"

[project.entry-points."agentic.commands"]
myplugin = "agentic_myplugin.cli:myplugin_command"
```

This registers:
- A standalone command `ag-myplugin` that can be used directly
- A plugin command `myplugin` that can be accessed via `ag myplugin`

### 4. Install Your Plugin

Install your plugin in development mode:

```bash
cd /path/to/your/plugin
source .venv/bin/activate
uv pip install -e .
```

### 5. Test Your Plugin

Test your plugin using both the standalone command and the `ag` command:

```bash
# Test the standalone command
ag-myplugin example --option value

# Test the plugin command
ag myplugin example --option value
```

## How the Plugin Mechanism Works

### Entry Points

The Agentic framework uses Python's entry points system to discover and load plugins. Entry points are defined in the `pyproject.toml` file and provide a way to register functions that can be discovered and called by other packages.

The `agentic-core` package looks for entry points in the `agentic.commands` group. Each entry point in this group is registered as a subcommand of the `ag` command.

### Plugin Discovery

When the `ag` command is run, it performs the following steps:

1. Parses the first argument as the command name
2. Checks if the command exists in the built-in commands
3. If not, it discovers and loads all entry points in the `agentic.commands` group
4. If the command matches an entry point name, it calls the corresponding function

The discovery process is implemented in the `discover_plugins` function in the `agentic_core.cli` module:

```python
def discover_plugins():
    """Discover and load all agentic command plugins."""
    commands = {}

    # Find all entry points in the 'agentic.commands' group
    try:
        entry_points = importlib.metadata.entry_points(group='agentic.commands')
        
        for entry_point in entry_points:
            try:
                # Load the command function
                command_func = entry_point.load()
                commands[entry_point.name] = command_func
            except Exception as e:
                print(f"Error loading command {entry_point.name}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error discovering plugins: {e}", file=sys.stderr)

    return commands
```

### Command Execution

When a plugin command is executed, the `ag` command:

1. Removes the command name from `sys.argv`
2. Calls the plugin's command function
3. Returns the exit code from the command function

This allows the plugin to handle its own argument parsing and execution.

## Best Practices

### Command Structure

- Use a consistent command structure with subcommands
- Provide clear help text and examples
- Follow the Unix philosophy: do one thing and do it well

### Error Handling

- Return appropriate exit codes (0 for success, non-zero for failure)
- Provide clear error messages
- Handle exceptions gracefully

### Documentation

- Document your plugin's commands and options
- Provide examples of common use cases
- Update the README.md and create a usage.md file

### Testing

- Write tests for your plugin's functionality
- Test both the standalone command and the `ag` command
- Test error cases and edge cases

## Example Plugins

Here are some examples of plugins in the Agentic framework:

- **agentic-note**: Provides note-taking capabilities
- **agentic-log**: Tracks and manages activity logs
- **agentic-issue**: Manages and tracks issues
- **agentic-plan**: Facilitates work planning and organization
- **agentic-todo**: Manages todo lists and scheduling

## Troubleshooting

### Plugin Not Found

If your plugin is not found when running `ag myplugin`, check:

1. Is your plugin installed in the current environment?
2. Is the entry point correctly registered in `pyproject.toml`?
3. Does the entry point function exist and follow the command interface?

### Command Not Working

If your plugin command is not working correctly, check:

1. Are you handling argument parsing correctly?
2. Are you returning the correct exit codes?
3. Are there any exceptions being raised?

## Conclusion

The plugin mechanism in the Agentic framework provides a flexible way to extend the functionality of the `ag` command. By following this guide, you can create your own plugins that integrate seamlessly with the Agentic framework.
