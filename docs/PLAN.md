# Agentic Plan

The Agentic Plan is a comprehensive system designed to manage and organize the agent's work. It includes various tools and components that facilitate the agent's tasks, from tracking work logs to managing projects and schedules.

## First Philosophy

Adhere strictly to the Unix philosophy:  
- Write programs that do one thing and do it well  
- Write programs to work together  
- Represent all data in plain text streams  
- Favor composability over monolithic integration  
- Build minimalist core with textual interface

## Project Structure
The Agentic Plan is organized into several projects, each with its own purpose and functionality.

| Project Name | Description | Function |
|--------------|-------------|----------|
| agentic | Main project with documentation | Provides documents for agent behavior rules, working cycle and meta-methods |
| agentic-core | Command line tool framework | Implements the 'ag' command and manages how it loads sub-tools|
| agentic-log | Agent's work log system | Tracks and manages the agent's activity logs |
| agentic-issue | Issue tracking system | Manages and tracks issues for the agent |
| agentic-note | Agent's notebook | Provides note-taking capabilities for the agent |
| agentic-plan | Work planning tool | Facilitates the agent's work planning and organization |
| agentic-todo | Schedule/calendar system | Manages the agent's todo list and scheduling |
| agentic-search | Local search engine | Provides local search capabilities for the agent |


