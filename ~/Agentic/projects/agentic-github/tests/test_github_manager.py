"""
Tests for the GitHub Manager module.

This module contains tests for the GitHubManager class, which provides
the core functionality for interacting with GitHub through the GitHub CLI.
"""

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

from agentic_github.github_manager import GitHubManager


class TestGitHubManager(unittest.TestCase):
    """Test cases for the GitHubManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary registry file for testing
        self.temp_registry_path = os.path.join(os.path.dirname(__file__), "test_registry.json")
        
        # Mock the subprocess.run function
        self.patcher = patch("subprocess.run")
        self.mock_run = self.patcher.start()
        
        # Set up a mock return value for subprocess.run
        self.mock_process = MagicMock()
        self.mock_process.stdout = ""
        self.mock_process.returncode = 0
        self.mock_run.return_value = self.mock_process
        
        # Create the GitHubManager instance with the test registry
        self.github_manager = GitHubManager(registry_path=self.temp_registry_path)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Stop the patcher
        self.patcher.stop()
        
        # Remove the temporary registry file
        if os.path.exists(self.temp_registry_path):
            os.remove(self.temp_registry_path)
    
    def test_ensure_registry_exists(self):
        """Test that the registry file is created if it doesn't exist."""
        # The registry file should have been created in setUp
        self.assertTrue(os.path.exists(self.temp_registry_path))
        
        # Check the content of the registry file
        with open(self.temp_registry_path, "r") as f:
            registry = json.load(f)
        
        self.assertIn("repositories", registry)
        self.assertIn("registry_version", registry)
        self.assertIn("metadata", registry)
    
    def test_check_gh_cli(self):
        """Test that the GitHub CLI check works."""
        # The check should have been performed in setUp
        # Verify that subprocess.run was called with the correct arguments
        self.mock_run.assert_any_call(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        
        self.mock_run.assert_any_call(
            ["gh", "auth", "status"],
            capture_output=True,
            check=True
        )
    
    def test_clone_repository(self):
        """Test cloning a repository."""
        # Set up the mock return value
        self.mock_process.stdout = "Repository cloned successfully"
        
        # Call the method
        result = self.github_manager.clone_repository("https://github.com/username/repo.git")
        
        # Verify that subprocess.run was called with the correct arguments
        self.mock_run.assert_any_call(
            ["gh", "repo", "clone", "https://github.com/username/repo.git", os.path.join(self.github_manager.projects_dir, "repo")],
            capture_output=True,
            text=True,
            check=True,
            cwd=None
        )
        
        # Verify that the repository was added to the registry
        with open(self.temp_registry_path, "r") as f:
            registry = json.load(f)
        
        self.assertEqual(len(registry["repositories"]), 1)
        self.assertEqual(registry["repositories"][0]["name"], "repo")
        self.assertEqual(registry["repositories"][0]["url"], "https://github.com/username/repo.git")
        
        # Verify the return value
        self.assertEqual(result, os.path.join(self.github_manager.projects_dir, "repo"))
    
    def test_create_repository(self):
        """Test creating a repository."""
        # Set up the mock return value
        self.mock_process.stdout = "https://github.com/username/new-repo.git"
        
        # Call the method
        result = self.github_manager.create_repository("new-repo", "Test repository", True)
        
        # Verify that subprocess.run was called with the correct arguments
        self.mock_run.assert_called_with(
            ["gh", "repo", "create", "new-repo", "--description", "Test repository", "--private"],
            capture_output=True,
            text=True,
            check=True,
            cwd=None
        )
        
        # Verify that the repository was added to the registry
        with open(self.temp_registry_path, "r") as f:
            registry = json.load(f)
        
        self.assertEqual(len(registry["repositories"]), 1)
        self.assertEqual(registry["repositories"][0]["name"], "new-repo")
        self.assertEqual(registry["repositories"][0]["url"], "https://github.com/username/new-repo.git")
        
        # Verify the return value
        self.assertEqual(result, "https://github.com/username/new-repo.git")
    
    def test_list_issues(self):
        """Test listing issues."""
        # Set up the mock return value
        self.mock_process.stdout = json.dumps([
            {
                "number": 1,
                "title": "Test issue",
                "state": "open",
                "assignees": [],
                "labels": [],
                "url": "https://github.com/username/repo/issues/1"
            }
        ])
        
        # Call the method
        result = self.github_manager.list_issues()
        
        # Verify that subprocess.run was called with the correct arguments
        self.mock_run.assert_called_with(
            ["gh", "issue", "list", "--state", "open", "--json", "number,title,state,assignees,labels,url"],
            capture_output=True,
            text=True,
            check=True,
            cwd=None
        )
        
        # Verify the return value
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["number"], 1)
        self.assertEqual(result[0]["title"], "Test issue")
        self.assertEqual(result[0]["state"], "open")
    
    def test_create_pull_request(self):
        """Test creating a pull request."""
        # Set up the mock return value
        self.mock_process.stdout = "https://github.com/username/repo/pull/1"
        
        # Mock the get_pull_request method
        self.github_manager.get_pull_request = MagicMock(return_value={
            "number": 1,
            "title": "Test PR",
            "state": "open",
            "headRefName": "feature-branch",
            "baseRefName": "main",
            "url": "https://github.com/username/repo/pull/1",
            "body": "Test body"
        })
        
        # Call the method
        result = self.github_manager.create_pull_request(
            "Test PR",
            "Test body",
            "main",
            "feature-branch"
        )
        
        # Verify that subprocess.run was called with the correct arguments
        self.mock_run.assert_called_with(
            ["gh", "pr", "create", "--title", "Test PR", "--body", "Test body", "--base", "main", "--head", "feature-branch"],
            capture_output=True,
            text=True,
            check=True,
            cwd=None
        )
        
        # Verify that get_pull_request was called
        self.github_manager.get_pull_request.assert_called_with("1", None)
        
        # Verify the return value
        self.assertEqual(result["number"], 1)
        self.assertEqual(result["title"], "Test PR")
        self.assertEqual(result["state"], "open")
        self.assertEqual(result["headRefName"], "feature-branch")
        self.assertEqual(result["baseRefName"], "main")


if __name__ == "__main__":
    unittest.main()
