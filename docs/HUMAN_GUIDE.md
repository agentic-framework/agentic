# Human Guide to the Agentic Framework

This guide is specifically designed for human users of the Agentic framework. It explains how to effectively use the framework and how to instruct AI agents to work with it.

## What is Agentic?

Agentic is a framework that allows AI agents (like Claude, GPT, etc.) to operate on your machine with significant freedom while maintaining security, organization, and best practices. It provides:

- A structured environment for AI agents to work in
- Rules and guidelines for agents to follow
- Utility scripts for common tasks
- Security boundaries to protect your system

## Documentation Structure

The Agentic framework documentation is organized into four main sections:

1. **For Humans**: 
   - This guide (HUMAN_GUIDE.md)
   - The main README.md

2. **For Agents (Comprehensive)**: 
   - [Agent Operation Rules](AGENT_RULES.md) - Detailed rules and guidelines

3. **For Agents (Quick Reference)**: 
   - [Agent Quick Reference Guide](AGENT_QUICK_REFERENCE.md) - Concise summary for common tasks

4. **Development and Maintenance**: 
   - [Lessons Learned](LESSON_LEARNED.md) - Important lessons learned during development and maintenance

As a human user, you should be familiar with this guide and the README, but you don't need to memorize the agent-focused documents. The Lessons Learned document can be particularly useful when you encounter issues with git operations or other development tasks.

## Getting Started

To set up the Agentic framework:

1. Clone the repository to your machine
2. Run `./ag setup all` to fully set up the environment
   - This will install dependencies, create necessary directories, and initialize the registry
   - You can also run specific setup steps:
     ```bash
     # Install dependencies only
     ./ag setup install-dependencies
     
     # Create directories only
     ./ag setup create-directories
     
     # Initialize registry only
     ./ag setup initialize-registry
     ```
   - If you encounter issues with the automated setup (particularly network-related issues), follow the [Manual Setup Guide](MANUAL_SETUP.md) instead
3. Run `./ag env check` to verify the environment is set up correctly
4. Review this guide to understand how to use the framework

## How to Instruct AI Agents

When working with AI agents, you need to instruct them to use the Agentic framework. Here are some effective prompts:

### For Complex Tasks

For tasks that require comprehensive understanding of the framework:

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me with [your task].
```

This instructs the agent to read and understand all the rules and guidelines before proceeding with your task.

### For Simple Tasks

For simpler tasks where the agent doesn't need the full ruleset:

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Focus on the docs/AGENT_QUICK_REFERENCE.md file in the agentic subdirectory. Then help me with [your task].
```

This instructs the agent to use the quick reference guide, which is more concise.

### Task-Specific Examples

#### Creating a New Project

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then create a new Python project called [project name].
```

#### Working with Virtual Environments

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then create a Python [version] virtual environment for [project name].
```

#### Managing Existing Projects

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me update dependencies for [project name].
```

#### Troubleshooting

```
Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me diagnose issues with [project name].
```

## Best Practices for Working with AI Agents

1. **Be Specific**: Clearly state what you want the agent to do. Vague instructions can lead to confusion.

2. **Provide Context**: If you're working on an existing project, provide context about what the project is and what you're trying to achieve.

3. **Set Boundaries**: If there are specific areas of your system you don't want the agent to access, make that clear.

4. **Review Before Executing**: Always review commands or code suggested by the agent before executing them, especially if they involve system changes.

5. **Incremental Tasks**: Break down complex tasks into smaller, incremental steps for better results.

6. **Feedback Loop**: Provide feedback to the agent about what worked and what didn't to help it improve.

7. **Verify Understanding**: Use the rule verification system to ensure the agent has correctly understood the framework rules:
   ```
   ./ag rule verify
   ```
   This will quiz the agent on its understanding of key rules and provide a score.

## Common Use Cases

### Python Project Management

The Agentic framework is particularly well-suited for Python project management:

- Creating new Python projects with proper structure
- Setting up virtual environments
- Managing dependencies
- Running tests
- Packaging and distribution

### Development Workflow

You can use the framework to assist with various stages of development:

- Initial project setup
- Code writing and refactoring
- Testing and debugging
- Documentation
- Deployment

### System Maintenance

The framework includes tools for system maintenance:

- Cleaning up temporary files
- Managing virtual environments
- Monitoring disk usage
- Backing up critical files

## Troubleshooting

If you encounter issues with the Agentic framework:

1. Run `./ag env check` to check for common issues
2. Run `./ag env fix` to automatically fix common issues
3. Check the logs in `$HOME/Agentic/logs/` for more information
4. Ask an AI agent to help diagnose the issue:
   ```
   Read the Agentic framework located at $HOME/Agentic to load your rules and tools. Start by examining the docs/README.md and docs/AGENT_RULES.md files in the agentic subdirectory. Then help me diagnose why [issue description].
   ```

## Security Considerations

The Agentic framework is designed with security in mind, but there are still some considerations:

1. **Review Commands**: Always review commands suggested by AI agents before executing them.

2. **Sensitive Information**: Do not share sensitive information (API keys, passwords, etc.) with AI agents.

3. **System Access**: The framework restricts agents to the `$HOME/Agentic/` directory by default. Be cautious when allowing access outside this area.

4. **Network Access**: Be aware that agents may suggest commands that access the network. Review these carefully.

## Customizing the Framework

You can customize the Agentic framework to suit your needs:

1. **Adding Rules**: You can add or modify rules in the AGENT_RULES.md file.

2. **Custom Commands**: You can create custom commands by developing plugins for the `ag` command-line tool.

3. **Directory Structure**: You can modify the directory structure to suit your workflow.

4. **Project Templates**: You can create custom project templates in the `$HOME/Agentic/shared/templates/` directory.

5. **Custom Home Directory**: You can change the location of the Agentic home directory by setting the `AGHOME` environment variable:

   ```bash
   # Set the AGHOME environment variable
   export AGHOME=/path/to/your/custom/agentic/directory
   
   # Add it to your shell profile for persistence
   echo 'export AGHOME=/path/to/your/custom/agentic/directory' >> ~/.bashrc  # or ~/.zshrc
   
   # Use the ag command with the custom location
   ag env check
   ```
   
   This is useful if you want to:
   - Install the framework on a different drive
   - Use a shared location for multiple users
   - Separate the framework from your home directory

## Contributing

Contributions to improve the Agentic framework are welcome:

1. Fork the repository
2. Make your changes
3. Submit a pull request with a clear description of your changes

## Conclusion

The Agentic framework provides a structured, secure environment for AI agents to operate on your machine. By following the guidelines in this document, you can effectively use AI agents to assist with a wide range of tasks while maintaining control and security.
