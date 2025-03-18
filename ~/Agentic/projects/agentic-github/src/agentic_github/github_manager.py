"""
GitHub Manager module for the Agentic framework.

This module provides the core functionality for interacting with GitHub through
the GitHub CLI (gh). It handles repository management, branch operations, issue
tracking, pull request workflow, and CI/CD integration.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml


class GitHubManager:
    """
    Manager class for GitHub operations using the GitHub CLI (gh).
    """

    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize the GitHub manager.

        Args:
            registry_path: Path to the GitHub registry file. If None, uses the default path.
        """
        self.agentic_root = os.path.expanduser("~/Agentic")
        self.projects_dir = os.path.join(self.agentic_root, "projects")
        
        if registry_path is None:
            self.registry_path = os.path.join(self.agentic_root, "shared", "github_registry.json")
        else:
            self.registry_path = registry_path
        
        self._ensure_registry_exists()
        self._check_gh_cli()
    
    def _ensure_registry_exists(self) -> None:
        """Ensure the GitHub registry file exists."""
        registry_dir = os.path.dirname(self.registry_path)
        os.makedirs(registry_dir, exist_ok=True)
        
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, "w") as f:
                json.dump({
                    "repositories": [],
                    "last_updated": "",
                    "registry_version": "1.0.0",
                    "metadata": {
                        "description": "Registry of GitHub repositories managed by the Agentic framework",
                        "managed_by": "agentic-github"
                    }
                }, f, indent=2)
    
    def _check_gh_cli(self) -> None:
        """Check if the GitHub CLI is installed and authenticated."""
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"GitHub CLI detected: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("GitHub CLI (gh) not found. Please install it and authenticate.", file=sys.stderr)
            print("Installation instructions: https://github.com/cli/cli#installation", file=sys.stderr)
            print("After installation, run: gh auth login", file=sys.stderr)
            sys.exit(1)
        
        # Check authentication
        try:
            subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                check=True
            )
        except subprocess.CalledProcessError:
            print("GitHub CLI is not authenticated. Please run: gh auth login", file=sys.stderr)
            sys.exit(1)
    
    def _run_gh_command(self, args: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        """
        Run a GitHub CLI command.

        Args:
            args: List of command arguments.
            cwd: Current working directory for the command.

        Returns:
            The completed process object.
        """
        try:
            return subprocess.run(
                ["gh"] + args,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
        except subprocess.CalledProcessError as e:
            print(f"Error executing GitHub CLI command: {e}", file=sys.stderr)
            print(f"Command output: {e.stdout}", file=sys.stderr)
            print(f"Command error: {e.stderr}", file=sys.stderr)
            raise
    
    def _load_registry(self) -> Dict:
        """Load the GitHub registry."""
        with open(self.registry_path, "r") as f:
            return json.load(f)
    
    def _save_registry(self, registry: Dict) -> None:
        """Save the GitHub registry."""
        with open(self.registry_path, "w") as f:
            json.dump(registry, f, indent=2)
    
    def _get_repo_path(self, repo_name: str) -> Optional[str]:
        """
        Get the local path for a repository.

        Args:
            repo_name: The repository name.

        Returns:
            The local path if found, None otherwise.
        """
        registry = self._load_registry()
        for repo in registry["repositories"]:
            if repo["name"] == repo_name:
                return repo["local_path"]
        return None
    
    # Repository operations
    
    def clone_repository(self, repo_url: str, destination: Optional[str] = None) -> str:
        """
        Clone a GitHub repository.

        Args:
            repo_url: The repository URL.
            destination: The destination path. If None, uses the repository name.

        Returns:
            The local path of the cloned repository.
        """
        # Extract repo name from URL
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        
        if destination is None:
            destination = os.path.join(self.projects_dir, repo_name)
        
        # Clone the repository
        self._run_gh_command(["repo", "clone", repo_url, destination])
        
        # Add to registry
        registry = self._load_registry()
        
        # Check if already in registry
        for repo in registry["repositories"]:
            if repo["name"] == repo_name:
                repo["local_path"] = destination
                repo["url"] = repo_url
                self._save_registry(registry)
                return destination
        
        # Add new entry
        registry["repositories"].append({
            "name": repo_name,
            "url": repo_url,
            "local_path": destination,
            "added_at": "",  # TODO: Add timestamp
            "default_branch": "main"  # Assume main, will be updated later
        })
        
        self._save_registry(registry)
        return destination
    
    def create_repository(self, name: str, description: Optional[str] = None, private: bool = False) -> str:
        """
        Create a new GitHub repository.

        Args:
            name: The repository name.
            description: The repository description.
            private: Whether the repository should be private.

        Returns:
            The URL of the created repository.
        """
        args = ["repo", "create", name]
        
        if description:
            args.extend(["--description", description])
        
        if private:
            args.append("--private")
        else:
            args.append("--public")
        
        result = self._run_gh_command(args)
        
        # Extract the repository URL from the output
        for line in result.stdout.splitlines():
            if line.startswith("https://"):
                repo_url = line.strip()
                break
        else:
            raise ValueError("Could not extract repository URL from output")
        
        # Add to registry
        registry = self._load_registry()
        registry["repositories"].append({
            "name": name,
            "url": repo_url,
            "local_path": os.path.join(self.projects_dir, name),
            "added_at": "",  # TODO: Add timestamp
            "default_branch": "main"
        })
        
        self._save_registry(registry)
        return repo_url
    
    def fork_repository(self, repo_url: str) -> str:
        """
        Fork a GitHub repository.

        Args:
            repo_url: The repository URL.

        Returns:
            The URL of the forked repository.
        """
        result = self._run_gh_command(["repo", "fork", repo_url])
        
        # Extract the repository URL from the output
        for line in result.stdout.splitlines():
            if line.startswith("https://"):
                forked_url = line.strip()
                break
        else:
            raise ValueError("Could not extract forked repository URL from output")
        
        # Extract repo name from URL
        repo_name = forked_url.split("/")[-1].replace(".git", "")
        
        # Add to registry
        registry = self._load_registry()
        registry["repositories"].append({
            "name": repo_name,
            "url": forked_url,
            "local_path": os.path.join(self.projects_dir, repo_name),
            "added_at": "",  # TODO: Add timestamp
            "default_branch": "main",
            "forked_from": repo_url
        })
        
        self._save_registry(registry)
        return forked_url
    
    # Branch operations
    
    def create_branch(self, branch_name: str, repo_name: Optional[str] = None) -> None:
        """
        Create a new branch.

        Args:
            branch_name: The branch name.
            repo_name: The repository name. If None, uses the current directory.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        # Use git directly for branch creation
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )
    
    def switch_branch(self, branch_name: str, repo_name: Optional[str] = None) -> None:
        """
        Switch to a branch.

        Args:
            branch_name: The branch name.
            repo_name: The repository name. If None, uses the current directory.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        # Use git directly for branch switching
        subprocess.run(
            ["git", "checkout", branch_name],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )
    
    def merge_branch(self, source_branch: str, target_branch: Optional[str] = None, repo_name: Optional[str] = None) -> None:
        """
        Merge a branch.

        Args:
            source_branch: The source branch.
            target_branch: The target branch. If None, uses the current branch.
            repo_name: The repository name. If None, uses the current directory.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        if target_branch:
            # First switch to target branch
            subprocess.run(
                ["git", "checkout", target_branch],
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
        
        # Then merge source branch
        subprocess.run(
            ["git", "merge", source_branch],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )
    
    # Issue operations
    
    def list_issues(self, state: str = "open", assignee: Optional[str] = None, repo_name: Optional[str] = None) -> List[Dict]:
        """
        List issues.

        Args:
            state: The issue state (open, closed, all).
            assignee: The assignee username.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            A list of issues.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = ["issue", "list", "--state", state, "--json", "number,title,state,assignees,labels,url"]
        
        if assignee:
            args.extend(["--assignee", assignee])
        
        result = self._run_gh_command(args, cwd=cwd)
        return json.loads(result.stdout)
    
    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None, repo_name: Optional[str] = None) -> Dict:
        """
        Create an issue.

        Args:
            title: The issue title.
            body: The issue body.
            labels: The issue labels.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The created issue.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = ["issue", "create", "--title", title, "--body", body]
        
        if labels:
            args.extend(["--label", ",".join(labels)])
        
        result = self._run_gh_command(args, cwd=cwd)
        
        # Extract the issue URL from the output
        for line in result.stdout.splitlines():
            if line.startswith("https://"):
                issue_url = line.strip()
                break
        else:
            raise ValueError("Could not extract issue URL from output")
        
        # Get the issue details
        issue_number = issue_url.split("/")[-1]
        return self.get_issue(issue_number, repo_name)
    
    def get_issue(self, issue_number: str, repo_name: Optional[str] = None) -> Dict:
        """
        Get an issue.

        Args:
            issue_number: The issue number.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The issue.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        result = self._run_gh_command(
            ["issue", "view", issue_number, "--json", "number,title,state,assignees,labels,url,body"],
            cwd=cwd
        )
        return json.loads(result.stdout)
    
    def update_issue(self, issue_number: str, state: Optional[str] = None, repo_name: Optional[str] = None) -> Dict:
        """
        Update an issue.

        Args:
            issue_number: The issue number.
            state: The new state (closed, open).
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The updated issue.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        if state == "closed":
            self._run_gh_command(["issue", "close", issue_number], cwd=cwd)
        elif state == "open":
            self._run_gh_command(["issue", "reopen", issue_number], cwd=cwd)
        
        return self.get_issue(issue_number, repo_name)
    
    # Pull request operations
    
    def list_pull_requests(self, state: str = "open", repo_name: Optional[str] = None) -> List[Dict]:
        """
        List pull requests.

        Args:
            state: The pull request state (open, closed, merged, all).
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            A list of pull requests.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = ["pr", "list", "--state", state, "--json", "number,title,state,headRefName,baseRefName,url"]
        
        result = self._run_gh_command(args, cwd=cwd)
        return json.loads(result.stdout)
    
    def create_pull_request(
        self,
        title: str,
        body: str,
        base: str,
        head: str,
        repo_name: Optional[str] = None
    ) -> Dict:
        """
        Create a pull request.

        Args:
            title: The pull request title.
            body: The pull request body.
            base: The base branch.
            head: The head branch.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The created pull request.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = [
            "pr", "create",
            "--title", title,
            "--body", body,
            "--base", base,
            "--head", head
        ]
        
        result = self._run_gh_command(args, cwd=cwd)
        
        # Extract the PR URL from the output
        for line in result.stdout.splitlines():
            if line.startswith("https://"):
                pr_url = line.strip()
                break
        else:
            raise ValueError("Could not extract pull request URL from output")
        
        # Get the PR details
        pr_number = pr_url.split("/")[-1]
        return self.get_pull_request(pr_number, repo_name)
    
    def get_pull_request(self, pr_number: str, repo_name: Optional[str] = None) -> Dict:
        """
        Get a pull request.

        Args:
            pr_number: The pull request number.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The pull request.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        result = self._run_gh_command(
            ["pr", "view", pr_number, "--json", "number,title,state,headRefName,baseRefName,url,body"],
            cwd=cwd
        )
        return json.loads(result.stdout)
    
    def review_pull_request(
        self,
        pr_number: str,
        action: str,
        body: Optional[str] = None,
        repo_name: Optional[str] = None
    ) -> None:
        """
        Review a pull request.

        Args:
            pr_number: The pull request number.
            action: The review action (approve, request-changes, comment).
            body: The review body.
            repo_name: The repository name. If None, uses the current directory.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = ["pr", "review", pr_number]
        
        if action == "approve":
            args.append("--approve")
        elif action == "request-changes":
            args.append("--request-changes")
        elif action == "comment":
            args.append("--comment")
        
        if body:
            args.extend(["--body", body])
        
        self._run_gh_command(args, cwd=cwd)
    
    def merge_pull_request(
        self,
        pr_number: str,
        method: str = "merge",
        repo_name: Optional[str] = None
    ) -> None:
        """
        Merge a pull request.

        Args:
            pr_number: The pull request number.
            method: The merge method (merge, squash, rebase).
            repo_name: The repository name. If None, uses the current directory.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = ["pr", "merge", pr_number, f"--{method}"]
        
        self._run_gh_command(args, cwd=cwd)
    
    # CI/CD operations
    
    def list_workflows(self, repo_name: Optional[str] = None) -> List[Dict]:
        """
        List workflows.

        Args:
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            A list of workflows.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        result = self._run_gh_command(["workflow", "list", "--json", "id,name,state,path"], cwd=cwd)
        return json.loads(result.stdout)
    
    def run_workflow(self, workflow_name: str, ref: Optional[str] = None, repo_name: Optional[str] = None) -> str:
        """
        Run a workflow.

        Args:
            workflow_name: The workflow name.
            ref: The branch or tag name.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The run ID.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        args = ["workflow", "run", workflow_name]
        
        if ref:
            args.extend(["--ref", ref])
        
        result = self._run_gh_command(args, cwd=cwd)
        
        # Extract the run ID from the output
        for line in result.stdout.splitlines():
            if "Run ID" in line:
                run_id = line.split("Run ID")[-1].strip()
                break
        else:
            raise ValueError("Could not extract run ID from output")
        
        return run_id
    
    def get_workflow_status(self, run_id: str, repo_name: Optional[str] = None) -> Dict:
        """
        Get workflow status.

        Args:
            run_id: The run ID.
            repo_name: The repository name. If None, uses the current directory.

        Returns:
            The workflow status.
        """
        cwd = None
        if repo_name:
            cwd = self._get_repo_path(repo_name)
            if not cwd:
                raise ValueError(f"Repository {repo_name} not found in registry")
        
        result = self._run_gh_command(["run", "view", run_id, "--json", "status,conclusion,createdAt,updatedAt"], cwd=cwd)
        return json.loads(result.stdout)
    
    # Integration with agentic-issues
    
    def sync_issues_with_local(self, repo_name: str) -> None:
        """
        Synchronize GitHub issues with local issues.

        Args:
            repo_name: The repository name.
        """
        # This is a placeholder for integration with agentic-issues
        # The actual implementation would depend on the agentic-issues API
        pass
