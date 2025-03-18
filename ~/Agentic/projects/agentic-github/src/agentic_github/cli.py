"""
Command-line interface for the GitHub integration plugin.

This module provides the command-line interface for the GitHub integration plugin,
allowing users to interact with GitHub repositories, issues, pull requests, and
workflows through the `ag github` command.
"""

import argparse
import os
import sys
from typing import Dict, List, Optional

from agentic_github.github_manager import GitHubManager


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="GitHub integration for the Agentic framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
          # Clone a repository
          ag github clone https://github.com/username/repo.git
          
          # Create a new repository
          ag github create repo-name --description "Description" --private
          
          # List issues
          ag github issue list --state open
          
          # Create a pull request
          ag github pr create --title "PR Title" --body "Description" --base main --head feature-branch
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Repository commands
    clone_parser = subparsers.add_parser("clone", help="Clone a repository")
    clone_parser.add_argument("url", help="Repository URL")
    clone_parser.add_argument("--destination", help="Destination path")
    
    create_parser = subparsers.add_parser("create", help="Create a repository")
    create_parser.add_argument("name", help="Repository name")
    create_parser.add_argument("--description", help="Repository description")
    create_parser.add_argument("--private", action="store_true", help="Create a private repository")
    
    fork_parser = subparsers.add_parser("fork", help="Fork a repository")
    fork_parser.add_argument("url", help="Repository URL")
    
    # Branch commands
    branch_parser = subparsers.add_parser("branch", help="Branch operations")
    branch_subparsers = branch_parser.add_subparsers(dest="branch_command", help="Branch command to execute")
    
    branch_create_parser = branch_subparsers.add_parser("create", help="Create a branch")
    branch_create_parser.add_argument("name", help="Branch name")
    branch_create_parser.add_argument("--repo", help="Repository name")
    
    branch_switch_parser = branch_subparsers.add_parser("switch", help="Switch to a branch")
    branch_switch_parser.add_argument("name", help="Branch name")
    branch_switch_parser.add_argument("--repo", help="Repository name")
    
    branch_merge_parser = branch_subparsers.add_parser("merge", help="Merge a branch")
    branch_merge_parser.add_argument("source", help="Source branch")
    branch_merge_parser.add_argument("--target", help="Target branch")
    branch_merge_parser.add_argument("--repo", help="Repository name")
    
    # Issue commands
    issue_parser = subparsers.add_parser("issue", help="Issue operations")
    issue_subparsers = issue_parser.add_subparsers(dest="issue_command", help="Issue command to execute")
    
    issue_list_parser = issue_subparsers.add_parser("list", help="List issues")
    issue_list_parser.add_argument("--state", choices=["open", "closed", "all"], default="open", help="Issue state")
    issue_list_parser.add_argument("--assignee", help="Assignee username")
    issue_list_parser.add_argument("--repo", help="Repository name")
    
    issue_create_parser = issue_subparsers.add_parser("create", help="Create an issue")
    issue_create_parser.add_argument("--title", required=True, help="Issue title")
    issue_create_parser.add_argument("--body", required=True, help="Issue body")
    issue_create_parser.add_argument("--labels", help="Comma-separated list of labels")
    issue_create_parser.add_argument("--repo", help="Repository name")
    
    issue_view_parser = issue_subparsers.add_parser("view", help="View an issue")
    issue_view_parser.add_argument("number", help="Issue number")
    issue_view_parser.add_argument("--repo", help="Repository name")
    
    issue_update_parser = issue_subparsers.add_parser("update", help="Update an issue")
    issue_update_parser.add_argument("number", help="Issue number")
    issue_update_parser.add_argument("--state", choices=["open", "closed"], required=True, help="New issue state")
    issue_update_parser.add_argument("--repo", help="Repository name")
    
    # Pull request commands
    pr_parser = subparsers.add_parser("pr", help="Pull request operations")
    pr_subparsers = pr_parser.add_subparsers(dest="pr_command", help="Pull request command to execute")
    
    pr_list_parser = pr_subparsers.add_parser("list", help="List pull requests")
    pr_list_parser.add_argument("--state", choices=["open", "closed", "merged", "all"], default="open", help="Pull request state")
    pr_list_parser.add_argument("--repo", help="Repository name")
    
    pr_create_parser = pr_subparsers.add_parser("create", help="Create a pull request")
    pr_create_parser.add_argument("--title", required=True, help="Pull request title")
    pr_create_parser.add_argument("--body", required=True, help="Pull request body")
    pr_create_parser.add_argument("--base", required=True, help="Base branch")
    pr_create_parser.add_argument("--head", required=True, help="Head branch")
    pr_create_parser.add_argument("--repo", help="Repository name")
    
    pr_view_parser = pr_subparsers.add_parser("view", help="View a pull request")
    pr_view_parser.add_argument("number", help="Pull request number")
    pr_view_parser.add_argument("--repo", help="Repository name")
    
    pr_review_parser = pr_subparsers.add_parser("review", help="Review a pull request")
    pr_review_parser.add_argument("number", help="Pull request number")
    pr_review_parser.add_argument("--action", choices=["approve", "request-changes", "comment"], required=True, help="Review action")
    pr_review_parser.add_argument("--body", help="Review body")
    pr_review_parser.add_argument("--repo", help="Repository name")
    
    pr_merge_parser = pr_subparsers.add_parser("merge", help="Merge a pull request")
    pr_merge_parser.add_argument("number", help="Pull request number")
    pr_merge_parser.add_argument("--method", choices=["merge", "squash", "rebase"], default="merge", help="Merge method")
    pr_merge_parser.add_argument("--repo", help="Repository name")
    
    # Workflow commands
    workflow_parser = subparsers.add_parser("workflow", help="Workflow operations")
    workflow_subparsers = workflow_parser.add_subparsers(dest="workflow_command", help="Workflow command to execute")
    
    workflow_list_parser = workflow_subparsers.add_parser("list", help="List workflows")
    workflow_list_parser.add_argument("--repo", help="Repository name")
    
    workflow_run_parser = workflow_subparsers.add_parser("run", help="Run a workflow")
    workflow_run_parser.add_argument("name", help="Workflow name")
    workflow_run_parser.add_argument("--ref", help="Branch or tag name")
    workflow_run_parser.add_argument("--repo", help="Repository name")
    
    workflow_status_parser = workflow_subparsers.add_parser("status", help="Get workflow status")
    workflow_status_parser.add_argument("run_id", help="Run ID")
    workflow_status_parser.add_argument("--repo", help="Repository name")
    
    # Sync commands
    sync_parser = subparsers.add_parser("sync", help="Synchronization operations")
    sync_subparsers = sync_parser.add_subparsers(dest="sync_command", help="Sync command to execute")
    
    sync_issues_parser = sync_subparsers.add_parser("issues", help="Synchronize GitHub issues with local issues")
    sync_issues_parser.add_argument("repo", help="Repository name")
    
    return parser


def process_command(args: argparse.Namespace) -> int:
    """
    Process the command with the given arguments.
    
    Args:
        args: The parsed command-line arguments.
        
    Returns:
        The exit code (0 for success, non-zero for failure).
    """
    if not args.command:
        create_parser().print_help()
        return 1
    
    try:
        github_manager = GitHubManager()
        
        # Repository commands
        if args.command == "clone":
            destination = github_manager.clone_repository(args.url, args.destination)
            print(f"Repository cloned to {destination}")
            return 0
        
        elif args.command == "create":
            repo_url = github_manager.create_repository(args.name, args.description, args.private)
            print(f"Repository created: {repo_url}")
            return 0
        
        elif args.command == "fork":
            forked_url = github_manager.fork_repository(args.url)
            print(f"Repository forked: {forked_url}")
            return 0
        
        # Branch commands
        elif args.command == "branch":
            if not args.branch_command:
                create_parser().parse_args(["branch", "--help"])
                return 1
            
            if args.branch_command == "create":
                github_manager.create_branch(args.name, args.repo)
                print(f"Branch '{args.name}' created")
                return 0
            
            elif args.branch_command == "switch":
                github_manager.switch_branch(args.name, args.repo)
                print(f"Switched to branch '{args.name}'")
                return 0
            
            elif args.branch_command == "merge":
                github_manager.merge_branch(args.source, args.target, args.repo)
                print(f"Branch '{args.source}' merged")
                return 0
        
        # Issue commands
        elif args.command == "issue":
            if not args.issue_command:
                create_parser().parse_args(["issue", "--help"])
                return 1
            
            if args.issue_command == "list":
                issues = github_manager.list_issues(args.state, args.assignee, args.repo)
                if not issues:
                    print("No issues found")
                else:
                    print(f"Found {len(issues)} issues:")
                    for issue in issues:
                        print(f"#{issue['number']} {issue['title']} ({issue['state']})")
                return 0
            
            elif args.issue_command == "create":
                labels = args.labels.split(",") if args.labels else None
                issue = github_manager.create_issue(args.title, args.body, labels, args.repo)
                print(f"Issue created: #{issue['number']} {issue['title']}")
                print(f"URL: {issue['url']}")
                return 0
            
            elif args.issue_command == "view":
                issue = github_manager.get_issue(args.number, args.repo)
                print(f"#{issue['number']} {issue['title']} ({issue['state']})")
                print(f"URL: {issue['url']}")
                print("\n" + issue['body'])
                return 0
            
            elif args.issue_command == "update":
                issue = github_manager.update_issue(args.number, args.state, args.repo)
                print(f"Issue updated: #{issue['number']} {issue['title']} ({issue['state']})")
                return 0
        
        # Pull request commands
        elif args.command == "pr":
            if not args.pr_command:
                create_parser().parse_args(["pr", "--help"])
                return 1
            
            if args.pr_command == "list":
                prs = github_manager.list_pull_requests(args.state, args.repo)
                if not prs:
                    print("No pull requests found")
                else:
                    print(f"Found {len(prs)} pull requests:")
                    for pr in prs:
                        print(f"#{pr['number']} {pr['title']} ({pr['state']})")
                return 0
            
            elif args.pr_command == "create":
                pr = github_manager.create_pull_request(args.title, args.body, args.base, args.head, args.repo)
                print(f"Pull request created: #{pr['number']} {pr['title']}")
                print(f"URL: {pr['url']}")
                return 0
            
            elif args.pr_command == "view":
                pr = github_manager.get_pull_request(args.number, args.repo)
                print(f"#{pr['number']} {pr['title']} ({pr['state']})")
                print(f"URL: {pr['url']}")
                print(f"Base: {pr['baseRefName']} <- Head: {pr['headRefName']}")
                print("\n" + pr['body'])
                return 0
            
            elif args.pr_command == "review":
                github_manager.review_pull_request(args.number, args.action, args.body, args.repo)
                print(f"Pull request #{args.number} reviewed with action: {args.action}")
                return 0
            
            elif args.pr_command == "merge":
                github_manager.merge_pull_request(args.number, args.method, args.repo)
                print(f"Pull request #{args.number} merged with method: {args.method}")
                return 0
        
        # Workflow commands
        elif args.command == "workflow":
            if not args.workflow_command:
                create_parser().parse_args(["workflow", "--help"])
                return 1
            
            if args.workflow_command == "list":
                workflows = github_manager.list_workflows(args.repo)
                if not workflows:
                    print("No workflows found")
                else:
                    print(f"Found {len(workflows)} workflows:")
                    for workflow in workflows:
                        print(f"{workflow['name']} ({workflow['state']})")
                return 0
            
            elif args.workflow_command == "run":
                run_id = github_manager.run_workflow(args.name, args.ref, args.repo)
                print(f"Workflow '{args.name}' started with run ID: {run_id}")
                return 0
            
            elif args.workflow_command == "status":
                status = github_manager.get_workflow_status(args.run_id, args.repo)
                print(f"Workflow run {args.run_id}:")
                print(f"Status: {status['status']}")
                print(f"Conclusion: {status['conclusion']}")
                print(f"Created at: {status['createdAt']}")
                print(f"Updated at: {status['updatedAt']}")
                return 0
        
        # Sync commands
        elif args.command == "sync":
            if not args.sync_command:
                create_parser().parse_args(["sync", "--help"])
                return 1
            
            if args.sync_command == "issues":
                github_manager.sync_issues_with_local(args.repo)
                print(f"Issues synchronized for repository: {args.repo}")
                return 0
        
        print(f"Unknown command: {args.command}")
        return 1
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """
    Main entry point for the standalone CLI.
    
    Returns:
        The exit code (0 for success, non-zero for failure).
    """
    parser = create_parser()
    args = parser.parse_args()
    return process_command(args)


def github_command() -> int:
    """
    Entry point for the 'ag github' command.
    
    This function follows the command interface for agentic-core plugins:
    1. Takes no arguments (it parses sys.argv directly)
    2. Returns an integer exit code (0 for success, non-zero for failure)
    3. Handles its own argument parsing
    
    Returns:
        The exit code (0 for success, non-zero for failure).
    """
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    return process_command(args)


if __name__ == "__main__":
    sys.exit(main())
