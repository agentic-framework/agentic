#!/usr/bin/env python3
"""
Feedback CLI - Command Line Interface for the Agentic Feedback System

This script provides a command-line interface for interacting with the Agentic
feedback system. It allows users to list, view, update, and comment on feedback
items such as issues, improvements, questions, and compliance reports.

Usage:
  ./feedback_cli.py list                      # List all issues
  ./feedback_cli.py get <id>                  # Get details of a specific issue
  ./feedback_cli.py update <id> <status>      # Update the status of an issue
  ./feedback_cli.py comment <id> <comment>    # Add a comment to an issue
  ./feedback_cli.py submit <title> <desc>     # Submit a new issue
"""

import os
import sys
import json
from feedback_system import (
    submit_issue,
    list_feedback,
    get_feedback,
    FeedbackPriority,
    FeedbackStatus
)

# Create a feedback system instance for operations that aren't directly exposed
from feedback_system import FeedbackSystem
feedback_system = FeedbackSystem()

# Use these methods from the instance
update_feedback = feedback_system.update_feedback
add_comment = feedback_system.add_comment

def print_issue(issue_data):
    """Print issue information in a readable format."""
    print("\nIssue ID: {}".format(issue_data.get("id")))
    print("Title: {}".format(issue_data.get("title")))
    print("Status: {}".format(issue_data.get("status")))
    print("Priority: {}".format(issue_data.get("priority")))
    print("Created at: {}".format(issue_data.get("created_at")))
    
    # Print comments if any
    comments = issue_data.get("comments", [])
    if comments:
        print("Comments:")
        for comment in comments:
            print("  - {} ({}): {}".format(
                comment.get("author"),
                comment.get("created_at"),
                comment.get("content")
            ))

def main():
    """Main function to demonstrate the feedback system."""
    if len(sys.argv) < 2:
        print("Usage: ./feedback_cli.py <command> [args]")
        print("Commands: list, get, update, comment, submit")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        # List all issues
        issues = list_feedback(feedback_type="issue")
        print("Found {} issues:".format(len(issues)))
        for issue in issues:
            print_issue(issue)
    
    elif command == "get":
        # Get a specific issue
        if len(sys.argv) < 3:
            print("Usage: ./feedback_cli.py get <issue_id>")
            return
        
        issue_id = sys.argv[2]
        issue_data = get_feedback(issue_id)
        
        if issue_data:
            print_issue(issue_data)
        else:
            print("Issue not found: {}".format(issue_id))
    
    elif command == "update":
        # Update an issue's status
        if len(sys.argv) < 4:
            print("Usage: ./feedback_cli.py update <issue_id> <status>")
            return
        
        issue_id = sys.argv[2]
        new_status = sys.argv[3]
        
        # Validate status
        if new_status not in [FeedbackStatus.NEW, FeedbackStatus.ACKNOWLEDGED, 
                             FeedbackStatus.IN_PROGRESS, FeedbackStatus.RESOLVED, 
                             FeedbackStatus.CLOSED, FeedbackStatus.REJECTED]:
            print("Invalid status: {}".format(new_status))
            print("Valid statuses: new, acknowledged, in_progress, resolved, closed, rejected")
            return
        
        # Update the issue
        success = update_feedback(issue_id, {"status": new_status})
        
        if success:
            print("Issue status updated to '{}'".format(new_status))
            issue_data = get_feedback(issue_id)
            if issue_data:
                print_issue(issue_data)
        else:
            print("Failed to update issue: {}".format(issue_id))
    
    elif command == "comment":
        # Add a comment to an issue
        if len(sys.argv) < 4:
            print("Usage: ./feedback_cli.py comment <issue_id> <comment>")
            return
        
        issue_id = sys.argv[2]
        comment_text = sys.argv[3]
        
        # Add the comment
        success = add_comment(issue_id, comment_text, "AI Agent")
        
        if success:
            print("Comment added to issue: {}".format(issue_id))
            issue_data = get_feedback(issue_id)
            if issue_data:
                print_issue(issue_data)
        else:
            print("Failed to add comment to issue: {}".format(issue_id))
    
    elif command == "submit":
        # Submit a new issue
        if len(sys.argv) < 4:
            print("Usage: ./feedback_cli.py submit <title> <description>")
            return
        
        title = sys.argv[2]
        description = sys.argv[3]
        
        # Submit the issue
        issue_id = submit_issue(
            title=title,
            description=description,
            priority=FeedbackPriority.MEDIUM,
            tags=["cli"]
        )
        
        if issue_id:
            print("Issue submitted with ID: {}".format(issue_id))
            issue_data = get_feedback(issue_id)
            if issue_data:
                print_issue(issue_data)
        else:
            print("Failed to submit issue")
    
    else:
        print("Unknown command: {}".format(command))
        print("Commands: list, get, update, comment, submit")
        print("Run without arguments for usage details")

if __name__ == "__main__":
    main()
