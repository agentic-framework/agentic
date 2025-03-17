# Agentic Plan

The Agentic Plan is a streamlined system designed to manage and organize the agent's work. It focuses on core functionality for issue tracking and note-taking, with GitHub integration for professional software engineering practices.

## First Philosophy

Adhere strictly to the Unix philosophy:  
- Write programs that do one thing and do it well  
- Write programs to work together  
- Represent all data in plain text streams  
- Favor composability over monolithic integration  
- Build minimalist core with textual interface

## Project Structure
The Agentic Plan is organized into several core projects, each with its own purpose and functionality.

| Project Name | Description | Function |
|--------------|-------------|----------|
| agentic | Main project with documentation | Provides documents for agent behavior rules, working cycle and meta-methods |
| agentic-core | Command line tool framework | Implements the 'ag' command and manages how it loads sub-tools|
| agentic-issue | Issue tracking system | Manages and tracks issues for the agent |
| agentic-note | Agent's notebook | Provides note-taking capabilities for the agent |
| agentic-github | GitHub integration | Enables interaction with GitHub repositories, issues, and pull requests |

## GitHub Integration

The GitHub integration component (agentic-github) extends the Agentic framework to support professional software engineering workflows through GitHub. This integration enables autonomous agents to follow industry best practices for collaborative development.

### Core Functionality

1. **Repository Management**
   - Clone repositories to the projects directory
   - Create new repositories from local projects
   - Fork existing repositories
   - Manage branches (create, switch, merge)

2. **Issue Tracking**
   - Fetch issues from GitHub repositories
   - Create new issues
   - Update issue status
   - Assign issues to users
   - Synchronize with the local `agentic-issues` plugin

3. **Pull Request Workflow**
   - Create pull requests
   - Review pull requests
   - Merge pull requests
   - Handle code review comments

4. **CI/CD Integration**
   - Monitor GitHub Actions workflow status
   - Trigger workflows
   - Analyze test results and coverage reports

### Command-line Interface Examples

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

### Benefits for Autonomous Agents

This integration enables autonomous agents to:

1. **Follow Industry Best Practices**: Use Git and GitHub workflows that align with professional software engineering practices.
2. **Collaborate with Humans**: Participate in collaborative development through pull requests, code reviews, and issue discussions.
3. **Maintain Project History**: Preserve a complete history of changes and decisions through Git commits and GitHub discussions.
4. **Leverage CI/CD**: Utilize automated testing and deployment pipelines to ensure code quality.
5. **Access Open Source Ecosystem**: Easily incorporate and contribute to open source projects.
