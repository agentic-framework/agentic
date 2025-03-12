#!/usr/bin/env python3
"""
Feedback System

This module provides a mechanism for AI agents to report issues, suggest improvements,
and provide feedback on the Agentic framework. It helps ensure that AI agents are
correctly following the rules during operation and allows for continuous improvement
of the framework.
"""

import os
import sys
import json
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.expanduser("~/Agentic/logs/feedback.log"), mode='a')
    ]
)
logger = logging.getLogger("feedback_system")

# Create logs directory if it doesn't exist
os.makedirs(os.path.expanduser("~/Agentic/logs"), exist_ok=True)

# Path to the feedback directory
FEEDBACK_DIR = os.path.expanduser("~/Agentic/feedback")

# Create feedback directory if it doesn't exist
os.makedirs(FEEDBACK_DIR, exist_ok=True)

class FeedbackType:
    """Enum-like class for feedback types."""
    ISSUE = "issue"
    IMPROVEMENT = "improvement"
    QUESTION = "question"
    COMPLIANCE = "compliance"
    OTHER = "other"

class FeedbackStatus:
    """Enum-like class for feedback status."""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"

class FeedbackPriority:
    """Enum-like class for feedback priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class FeedbackSystem:
    """Class for managing feedback from AI agents."""
    
    def __init__(self, feedback_dir: str = FEEDBACK_DIR):
        """
        Initialize the feedback system.
        
        Args:
            feedback_dir (str): The directory to store feedback files
        """
        self.feedback_dir = feedback_dir
        
        # Create feedback directory if it doesn't exist
        os.makedirs(self.feedback_dir, exist_ok=True)
        
        # Create subdirectories for different feedback types
        for feedback_type in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                             FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                             FeedbackType.OTHER]:
            os.makedirs(os.path.join(self.feedback_dir, feedback_type), exist_ok=True)
    
    def submit_feedback(self, feedback_type: str, title: str, description: str,
                       priority: str = FeedbackPriority.MEDIUM,
                       tags: Optional[List[str]] = None,
                       context: Optional[Dict[str, Any]] = None) -> str:
        """
        Submit feedback to the system.
        
        Args:
            feedback_type (str): The type of feedback (issue, improvement, question, compliance, other)
            title (str): A short title for the feedback
            description (str): A detailed description of the feedback
            priority (str): The priority of the feedback (low, medium, high, critical)
            tags (Optional[List[str]]): Tags to categorize the feedback
            context (Optional[Dict[str, Any]]): Additional context for the feedback
        
        Returns:
            str: The ID of the submitted feedback
        """
        # Validate feedback type
        if feedback_type not in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                                FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                                FeedbackType.OTHER]:
            logger.warning(f"Invalid feedback type: {feedback_type}, using 'other' instead")
            feedback_type = FeedbackType.OTHER
        
        # Validate priority
        if priority not in [FeedbackPriority.LOW, FeedbackPriority.MEDIUM, 
                           FeedbackPriority.HIGH, FeedbackPriority.CRITICAL]:
            logger.warning(f"Invalid priority: {priority}, using 'medium' instead")
            priority = FeedbackPriority.MEDIUM
        
        # Generate a unique ID for the feedback
        feedback_id = str(uuid.uuid4())
        
        # Create the feedback data
        feedback_data = {
            "id": feedback_id,
            "type": feedback_type,
            "title": title,
            "description": description,
            "priority": priority,
            "tags": tags or [],
            "context": context or {},
            "status": FeedbackStatus.NEW,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "comments": []
        }
        
        # Save the feedback to a file
        feedback_path = os.path.join(self.feedback_dir, feedback_type, f"{feedback_id}.json")
        
        try:
            with open(feedback_path, 'w') as f:
                json.dump(feedback_data, f, indent=2)
            
            logger.info(f"Feedback submitted: {feedback_id} ({feedback_type})")
            return feedback_id
        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
            return ""
    
    def get_feedback(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """
        Get feedback by ID.
        
        Args:
            feedback_id (str): The ID of the feedback to get
        
        Returns:
            Optional[Dict[str, Any]]: The feedback data, or None if not found
        """
        # Search for the feedback in all subdirectories
        for feedback_type in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                             FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                             FeedbackType.OTHER]:
            feedback_path = os.path.join(self.feedback_dir, feedback_type, f"{feedback_id}.json")
            
            if os.path.exists(feedback_path):
                try:
                    with open(feedback_path, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Error reading feedback {feedback_id}: {e}")
                    return None
        
        logger.warning(f"Feedback not found: {feedback_id}")
        return None
    
    def update_feedback(self, feedback_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update feedback by ID.
        
        Args:
            feedback_id (str): The ID of the feedback to update
            updates (Dict[str, Any]): The updates to apply to the feedback
        
        Returns:
            bool: True if the update was successful, False otherwise
        """
        # Get the current feedback data
        feedback_data = self.get_feedback(feedback_id)
        
        if not feedback_data:
            logger.warning(f"Cannot update feedback {feedback_id}: not found")
            return False
        
        # Apply the updates
        for key, value in updates.items():
            if key in ["id", "created_at"]:
                # Don't allow updating these fields
                continue
            
            feedback_data[key] = value
        
        # Update the updated_at timestamp
        feedback_data["updated_at"] = datetime.now().isoformat()
        
        # Save the updated feedback
        feedback_type = feedback_data["type"]
        feedback_path = os.path.join(self.feedback_dir, feedback_type, f"{feedback_id}.json")
        
        try:
            with open(feedback_path, 'w') as f:
                json.dump(feedback_data, f, indent=2)
            
            logger.info(f"Feedback updated: {feedback_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating feedback {feedback_id}: {e}")
            return False
    
    def add_comment(self, feedback_id: str, comment: str, author: str = "AI Agent") -> bool:
        """
        Add a comment to feedback.
        
        Args:
            feedback_id (str): The ID of the feedback to comment on
            comment (str): The comment to add
            author (str): The author of the comment
        
        Returns:
            bool: True if the comment was added successfully, False otherwise
        """
        # Get the current feedback data
        feedback_data = self.get_feedback(feedback_id)
        
        if not feedback_data:
            logger.warning(f"Cannot add comment to feedback {feedback_id}: not found")
            return False
        
        # Create the comment
        comment_data = {
            "id": str(uuid.uuid4()),
            "author": author,
            "content": comment,
            "created_at": datetime.now().isoformat()
        }
        
        # Add the comment to the feedback
        feedback_data["comments"].append(comment_data)
        
        # Update the updated_at timestamp
        feedback_data["updated_at"] = datetime.now().isoformat()
        
        # Save the updated feedback
        feedback_type = feedback_data["type"]
        feedback_path = os.path.join(self.feedback_dir, feedback_type, f"{feedback_id}.json")
        
        try:
            with open(feedback_path, 'w') as f:
                json.dump(feedback_data, f, indent=2)
            
            logger.info(f"Comment added to feedback {feedback_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding comment to feedback {feedback_id}: {e}")
            return False
    
    def list_feedback(self, feedback_type: Optional[str] = None, 
                     status: Optional[str] = None,
                     priority: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """
        List feedback with optional filtering.
        
        Args:
            feedback_type (Optional[str]): Filter by feedback type
            status (Optional[str]): Filter by status
            priority (Optional[str]): Filter by priority
            tags (Optional[List[str]]): Filter by tags (must have all tags)
            limit (int): Maximum number of results to return
        
        Returns:
            List[Dict[str, Any]]: List of feedback data
        """
        results = []
        
        # Determine which directories to search
        if feedback_type:
            if feedback_type in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                                FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                                FeedbackType.OTHER]:
                directories = [os.path.join(self.feedback_dir, feedback_type)]
            else:
                logger.warning(f"Invalid feedback type: {feedback_type}, searching all types")
                directories = [os.path.join(self.feedback_dir, t) for t in 
                              [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                               FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                               FeedbackType.OTHER]]
        else:
            directories = [os.path.join(self.feedback_dir, t) for t in 
                          [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                           FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                           FeedbackType.OTHER]]
        
        # Search for feedback files
        for directory in directories:
            if not os.path.exists(directory):
                continue
            
            for filename in os.listdir(directory):
                if not filename.endswith(".json"):
                    continue
                
                file_path = os.path.join(directory, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        feedback_data = json.load(f)
                    
                    # Apply filters
                    if status and feedback_data.get("status") != status:
                        continue
                    
                    if priority and feedback_data.get("priority") != priority:
                        continue
                    
                    if tags:
                        feedback_tags = feedback_data.get("tags", [])
                        if not all(tag in feedback_tags for tag in tags):
                            continue
                    
                    results.append(feedback_data)
                    
                    # Check if we've reached the limit
                    if len(results) >= limit:
                        break
                except Exception as e:
                    logger.error(f"Error reading feedback file {file_path}: {e}")
            
            # Check if we've reached the limit
            if len(results) >= limit:
                break
        
        # Sort results by created_at (newest first)
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return results[:limit]
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the feedback system.
        
        Returns:
            Dict[str, Any]: Statistics about the feedback system
        """
        stats = {
            "total": 0,
            "by_type": {},
            "by_status": {},
            "by_priority": {}
        }
        
        # Initialize counters
        for feedback_type in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                             FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                             FeedbackType.OTHER]:
            stats["by_type"][feedback_type] = 0
        
        for status in [FeedbackStatus.NEW, FeedbackStatus.ACKNOWLEDGED, 
                      FeedbackStatus.IN_PROGRESS, FeedbackStatus.RESOLVED, 
                      FeedbackStatus.CLOSED, FeedbackStatus.REJECTED]:
            stats["by_status"][status] = 0
        
        for priority in [FeedbackPriority.LOW, FeedbackPriority.MEDIUM, 
                        FeedbackPriority.HIGH, FeedbackPriority.CRITICAL]:
            stats["by_priority"][priority] = 0
        
        # Count feedback
        for feedback_type in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                             FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                             FeedbackType.OTHER]:
            directory = os.path.join(self.feedback_dir, feedback_type)
            
            if not os.path.exists(directory):
                continue
            
            for filename in os.listdir(directory):
                if not filename.endswith(".json"):
                    continue
                
                file_path = os.path.join(directory, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        feedback_data = json.load(f)
                    
                    stats["total"] += 1
                    stats["by_type"][feedback_type] += 1
                    
                    status = feedback_data.get("status", FeedbackStatus.NEW)
                    if status in stats["by_status"]:
                        stats["by_status"][status] += 1
                    
                    priority = feedback_data.get("priority", FeedbackPriority.MEDIUM)
                    if priority in stats["by_priority"]:
                        stats["by_priority"][priority] += 1
                except Exception as e:
                    logger.error(f"Error reading feedback file {file_path}: {e}")
        
        return stats
    
    def export_feedback(self, output_path: str, feedback_type: Optional[str] = None,
                       status: Optional[str] = None) -> bool:
        """
        Export feedback to a JSON file.
        
        Args:
            output_path (str): The path to save the exported feedback
            feedback_type (Optional[str]): Filter by feedback type
            status (Optional[str]): Filter by status
        
        Returns:
            bool: True if the export was successful, False otherwise
        """
        # Get the feedback to export
        feedback_list = self.list_feedback(feedback_type=feedback_type, status=status, limit=1000)
        
        # Create the export data
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total": len(feedback_list),
            "feedback": feedback_list
        }
        
        # Save the export to a file
        try:
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Feedback exported to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting feedback: {e}")
            return False
    
    def import_feedback(self, input_path: str) -> int:
        """
        Import feedback from a JSON file.
        
        Args:
            input_path (str): The path to the JSON file to import
        
        Returns:
            int: The number of feedback items imported
        """
        try:
            with open(input_path, 'r') as f:
                import_data = json.load(f)
            
            feedback_list = import_data.get("feedback", [])
            imported_count = 0
            
            for feedback_data in feedback_list:
                feedback_id = feedback_data.get("id")
                feedback_type = feedback_data.get("type")
                
                if not feedback_id or not feedback_type:
                    logger.warning(f"Skipping feedback without ID or type")
                    continue
                
                # Check if the feedback already exists
                existing_feedback = self.get_feedback(feedback_id)
                if existing_feedback:
                    logger.warning(f"Skipping existing feedback: {feedback_id}")
                    continue
                
                # Save the feedback to a file
                feedback_path = os.path.join(self.feedback_dir, feedback_type, f"{feedback_id}.json")
                
                try:
                    with open(feedback_path, 'w') as f:
                        json.dump(feedback_data, f, indent=2)
                    
                    imported_count += 1
                except Exception as e:
                    logger.error(f"Error importing feedback {feedback_id}: {e}")
            
            logger.info(f"Imported {imported_count} feedback items from {input_path}")
            return imported_count
        except Exception as e:
            logger.error(f"Error importing feedback: {e}")
            return 0
    
    def cleanup_old_feedback(self, days: int = 90, status: Optional[str] = None) -> int:
        """
        Clean up old feedback.
        
        Args:
            days (int): Remove feedback older than this many days
            status (Optional[str]): Only remove feedback with this status
        
        Returns:
            int: The number of feedback items removed
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        removed_count = 0
        
        # Search for old feedback files
        for feedback_type in [FeedbackType.ISSUE, FeedbackType.IMPROVEMENT, 
                             FeedbackType.QUESTION, FeedbackType.COMPLIANCE, 
                             FeedbackType.OTHER]:
            directory = os.path.join(self.feedback_dir, feedback_type)
            
            if not os.path.exists(directory):
                continue
            
            for filename in os.listdir(directory):
                if not filename.endswith(".json"):
                    continue
                
                file_path = os.path.join(directory, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        feedback_data = json.load(f)
                    
                    # Check if the feedback is old enough
                    created_at = feedback_data.get("created_at", "")
                    if not created_at:
                        continue
                    
                    try:
                        created_timestamp = datetime.fromisoformat(created_at).timestamp()
                    except ValueError:
                        continue
                    
                    if created_timestamp > cutoff_date:
                        continue
                    
                    # Check if the feedback has the specified status
                    if status and feedback_data.get("status") != status:
                        continue
                    
                    # Remove the feedback file
                    os.remove(file_path)
                    removed_count += 1
                except Exception as e:
                    logger.error(f"Error cleaning up feedback file {file_path}: {e}")
        
        logger.info(f"Removed {removed_count} old feedback items")
        return removed_count

def submit_issue(title: str, description: str, priority: str = FeedbackPriority.MEDIUM,
               tags: Optional[List[str]] = None, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Submit an issue to the feedback system.
    
    Args:
        title (str): A short title for the issue
        description (str): A detailed description of the issue
        priority (str): The priority of the issue (low, medium, high, critical)
        tags (Optional[List[str]]): Tags to categorize the issue
        context (Optional[Dict[str, Any]]): Additional context for the issue
    
    Returns:
        str: The ID of the submitted issue
    """
    feedback_system = FeedbackSystem()
    return feedback_system.submit_feedback(
        FeedbackType.ISSUE,
        title,
        description,
        priority,
        tags,
        context
    )

def submit_improvement(title: str, description: str, priority: str = FeedbackPriority.MEDIUM,
                     tags: Optional[List[str]] = None, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Submit an improvement suggestion to the feedback system.
    
    Args:
        title (str): A short title for the improvement
        description (str): A detailed description of the improvement
        priority (str): The priority of the improvement (low, medium, high, critical)
        tags (Optional[List[str]]): Tags to categorize the improvement
        context (Optional[Dict[str, Any]]): Additional context for the improvement
    
    Returns:
        str: The ID of the submitted improvement
    """
    feedback_system = FeedbackSystem()
    return feedback_system.submit_feedback(
        FeedbackType.IMPROVEMENT,
        title,
        description,
        priority,
        tags,
        context
    )

def submit_question(title: str, description: str, priority: str = FeedbackPriority.MEDIUM,
                  tags: Optional[List[str]] = None, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Submit a question to the feedback system.
    
    Args:
        title (str): A short title for the question
        description (str): A detailed description of the question
        priority (str): The priority of the question (low, medium, high, critical)
        tags (Optional[List[str]]): Tags to categorize the question
        context (Optional[Dict[str, Any]]): Additional context for the question
    
    Returns:
        str: The ID of the submitted question
    """
    feedback_system = FeedbackSystem()
    return feedback_system.submit_feedback(
        FeedbackType.QUESTION,
        title,
        description,
        priority,
        tags,
        context
    )

def submit_compliance_report(title: str, description: str, priority: str = FeedbackPriority.MEDIUM,
                           tags: Optional[List[str]] = None, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Submit a compliance report to the feedback system.
    
    Args:
        title (str): A short title for the compliance report
        description (str): A detailed description of the compliance report
        priority (str): The priority of the compliance report (low, medium, high, critical)
        tags (Optional[List[str]]): Tags to categorize the compliance report
        context (Optional[Dict[str, Any]]): Additional context for the compliance report
    
    Returns:
        str: The ID of the submitted compliance report
    """
    feedback_system = FeedbackSystem()
    return feedback_system.submit_feedback(
        FeedbackType.COMPLIANCE,
        title,
        description,
        priority,
        tags,
        context
    )

def get_feedback(feedback_id: str) -> Optional[Dict[str, Any]]:
    """
    Get feedback by ID.
    
    Args:
        feedback_id (str): The ID of the feedback to get
    
    Returns:
        Optional[Dict[str, Any]]: The feedback data, or None if not found
    """
    feedback_system = FeedbackSystem()
    return feedback_system.get_feedback(feedback_id)

def list_feedback(feedback_type: Optional[str] = None, status: Optional[str] = None,
                priority: Optional[str] = None, tags: Optional[List[str]] = None,
                limit: int = 100) -> List[Dict[str, Any]]:
    """
    List feedback with optional filtering.
    
    Args:
        feedback_type (Optional[str]): Filter by feedback type
        status (Optional[str]): Filter by status
        priority (Optional[str]): Filter by priority
        tags (Optional[List[str]]): Filter by tags (must have all tags)
        limit (int): Maximum number of results to return
    
    Returns:
        List[Dict[str, Any]]: List of feedback data
    """
    feedback_system = FeedbackSystem()
    return feedback_system.list_feedback(feedback_type, status, priority, tags, limit)

def get_feedback_stats() -> Dict[str, Any]:
    """
    Get statistics about the feedback system.
    
    Returns:
        Dict[str, Any]: Statistics about the feedback system
    """
    feedback_system = FeedbackSystem()
    return feedback_system.get_feedback_stats()

def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agentic Framework Feedback System")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Submit feedback command
    submit_parser = subparsers.add_parser("submit", help="Submit feedback")
    submit_parser.add_argument("--type", required=True, choices=["issue", "improvement", "question", "compliance", "other"],
                             help="The type of feedback")
    submit_parser.add_argument("--title", required=True, help="A short title for the feedback")
    submit_parser.add_argument("--description", required=True, help="A detailed description of the feedback")
    submit_parser.add_argument("--priority", choices=["low", "medium", "high", "critical"],
                             default="medium", help="The priority of the feedback")
    submit_parser.add_argument("--tags", nargs="+", help="Tags to categorize the feedback")
    submit_parser.add_argument("--context", help="Additional context for the feedback (JSON format)")
    
    # Get feedback command
    get_parser = subparsers.add_parser("get", help="Get feedback by ID")
    get_parser.add_argument("id", help="The ID of the feedback to get")
    
    # List feedback command
    list_parser = subparsers.add_parser("list", help="List feedback with optional filtering")
    list_parser.add_argument("--type", choices=["issue", "improvement", "question", "compliance", "other"],
                           help="Filter by feedback type")
    list_parser.add_argument("--status", choices=["new", "acknowledged", "in_progress", "resolved", "closed", "rejected"],
                           help="Filter by status")
    list_parser.add_argument("--priority", choices=["low", "medium", "high", "critical"],
                           help="Filter by priority")
    list_parser.add_argument("--tags", nargs="+", help="Filter by tags (must have all tags)")
    list_parser.add_argument("--limit", type=int, default=100, help="Maximum number of results to return")
    
    # Update feedback command
    update_parser = subparsers.add_parser("update", help="Update feedback by ID")
    update_parser.add_argument("id", help="The ID of the feedback to update")
    update_parser.add_argument("--status", choices=["new", "acknowledged", "in_progress", "resolved", "closed", "rejected"],
                             help="Update the status")
    update_parser.add_argument("--priority", choices=["low", "medium", "high", "critical"],
                             help="Update the priority")
    update_parser.add_argument("--title", help="Update the title")
    update_parser.add_argument("--description", help="Update the description")
    
    # Add comment command
    comment_parser = subparsers.add_parser("comment", help="Add a comment to feedback")
    comment_parser.add_argument("id", help="The ID of the feedback to comment on")
    comment_parser.add_argument("--comment", required=True, help="The comment to add")
    comment_parser.add_argument("--author", default="AI Agent", help="The author of the comment")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get statistics about the feedback system")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export feedback to a JSON file")
    export_parser.add_argument("--output", required=True, help="The path to save the exported feedback")
    export_parser.add_argument("--type", choices=["issue", "improvement", "question", "compliance", "other"],
                             help="Filter by feedback type")
    export_parser.add_argument("--status", choices=["new", "acknowledged", "in_progress", "resolved", "closed", "rejected"],
                             help="Filter by status")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import feedback from a JSON file")
    import_parser.add_argument("--input", required=True, help="The path to the JSON file to import")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old feedback")
    cleanup_parser.add_argument("--days", type=int, default=90, help="Remove feedback older than this many days")
    cleanup_parser.add_argument("--status", choices=["new", "acknowledged", "in_progress", "resolved", "closed", "rejected"],
                              help="Only remove feedback with this status")
    
    args = parser.parse_args()
    
    feedback_system = FeedbackSystem()
    
    if args.command == "submit":
        # Parse context if provided
        context = None
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for context")
                sys.exit(1)
        
        feedback_id = feedback_system.submit_feedback(
            args.type,
            args.title,
            args.description,
            args.priority,
            args.tags,
            context
        )
        
        if feedback_id:
            print(f"Feedback submitted with ID: {feedback_id}")
        else:
            print("Error submitting feedback")
            sys.exit(1)
    elif args.command == "get":
        feedback_data = feedback_system.get_feedback(args.id)
        
        if feedback_data:
            print(json.dumps(feedback_data, indent=2))
        else:
            print(f"Feedback not found: {args.id}")
            sys.exit(1)
    elif args.command == "list":
        feedback_list = feedback_system.list_feedback(
            feedback_type=args.type,
            status=args.status,
            priority=args.priority,
            tags=args.tags,
            limit=args.limit
        )
        
        if feedback_list:
            print(json.dumps(feedback_list, indent=2))
        else:
            print("No feedback found matching the criteria")
    elif args.command == "update":
        updates = {}
        
        if args.status:
            updates["status"] = args.status
        
        if args.priority:
            updates["priority"] = args.priority
        
        if args.title:
            updates["title"] = args.title
        
        if args.description:
            updates["description"] = args.description
        
        if not updates:
            print("Error: No updates specified")
            sys.exit(1)
        
        success = feedback_system.update_feedback(args.id, updates)
        
        if success:
            print(f"Feedback {args.id} updated successfully")
        else:
            print(f"Error updating feedback {args.id}")
            sys.exit(1)
    elif args.command == "comment":
        success = feedback_system.add_comment(args.id, args.comment, args.author)
        
        if success:
            print(f"Comment added to feedback {args.id}")
        else:
            print(f"Error adding comment to feedback {args.id}")
            sys.exit(1)
    elif args.command == "stats":
        stats = feedback_system.get_feedback_stats()
        print(json.dumps(stats, indent=2))
    elif args.command == "export":
        success = feedback_system.export_feedback(args.output, args.type, args.status)
        
        if success:
            print(f"Feedback exported to {args.output}")
        else:
            print("Error exporting feedback")
            sys.exit(1)
    elif args.command == "import":
        imported_count = feedback_system.import_feedback(args.input)
        
        if imported_count > 0:
            print(f"Imported {imported_count} feedback items")
        else:
            print("No feedback items imported")
            sys.exit(1)
    elif args.command == "cleanup":
        removed_count = feedback_system.cleanup_old_feedback(args.days, args.status)
        
        if removed_count > 0:
            print(f"Removed {removed_count} old feedback items")
        else:
            print("No feedback items removed")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
