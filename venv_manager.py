#!/usr/bin/env python3
"""
Virtual Environment Manager

This script provides utilities for managing the virtual environment registry.
It allows adding, removing, and listing virtual environments in the registry.
"""

import json
import os
import sys
import argparse
from datetime import datetime
import pathlib

# Registry file path
REGISTRY_PATH = "/Users/mingli/Agentic/venv_registry.json"

def load_registry():
    """Load the virtual environment registry."""
    try:
        with open(REGISTRY_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create a new registry if it doesn't exist
        registry = {
            "virtual_environments": [],
            "last_updated": datetime.now().isoformat(),
            "registry_version": "1.0.0",
            "metadata": {
                "description": "Registry of active Python virtual environments managed by uv",
                "managed_by": "agentic framework"
            }
        }
        save_registry(registry)
        return registry

def save_registry(registry):
    """Save the virtual environment registry."""
    registry["last_updated"] = datetime.now().isoformat()
    with open(REGISTRY_PATH, 'w') as f:
        json.dump(registry, f, indent=2)

def add_venv(venv_path, project_name, python_version=None, description=None):
    """Add a virtual environment to the registry."""
    registry = load_registry()
    
    # Convert to absolute path
    venv_path = os.path.abspath(os.path.expanduser(venv_path))
    
    # Check if venv exists
    if not os.path.isdir(venv_path):
        print(f"Error: Virtual environment directory not found: {venv_path}")
        return False
    
    # Check if venv is already registered
    for venv in registry["virtual_environments"]:
        if venv["path"] == venv_path:
            print(f"Virtual environment already registered: {venv_path}")
            return False
    
    # Get Python version if not provided
    if not python_version:
        try:
            python_path = os.path.join(venv_path, "bin", "python")
            if os.path.exists(python_path):
                import subprocess
                result = subprocess.run(
                    [python_path, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"],
                    capture_output=True,
                    text=True
                )
                python_version = result.stdout.strip()
        except Exception as e:
            print(f"Warning: Could not determine Python version: {e}")
            python_version = "unknown"
    
    # Add venv to registry
    venv_info = {
        "path": venv_path,
        "project_name": project_name,
        "python_version": python_version,
        "description": description or f"Virtual environment for {project_name}",
        "created_at": datetime.now().isoformat(),
        "last_used": datetime.now().isoformat()
    }
    
    registry["virtual_environments"].append(venv_info)
    save_registry(registry)
    print(f"Added virtual environment: {venv_path}")
    return True

def remove_venv(venv_path=None, project_name=None):
    """Remove a virtual environment from the registry."""
    if not venv_path and not project_name:
        print("Error: Either venv_path or project_name must be provided")
        return False
    
    registry = load_registry()
    
    if venv_path:
        venv_path = os.path.abspath(os.path.expanduser(venv_path))
    
    # Find and remove the venv
    updated_venvs = []
    removed = False
    
    for venv in registry["virtual_environments"]:
        if (venv_path and venv["path"] == venv_path) or (project_name and venv["project_name"] == project_name):
            print(f"Removed virtual environment: {venv['path']} ({venv['project_name']})")
            removed = True
        else:
            updated_venvs.append(venv)
    
    if not removed:
        print("Virtual environment not found in registry")
        return False
    
    registry["virtual_environments"] = updated_venvs
    save_registry(registry)
    return True

def list_venvs(verbose=False):
    """List all registered virtual environments."""
    registry = load_registry()
    
    if not registry["virtual_environments"]:
        print("No virtual environments registered")
        return
    
    print(f"Registered Virtual Environments ({len(registry['virtual_environments'])}):")
    print("-" * 80)
    
    for i, venv in enumerate(registry["virtual_environments"], 1):
        print(f"{i}. {venv['project_name']}")
        print(f"   Path: {venv['path']}")
        print(f"   Python: {venv['python_version']}")
        
        if verbose:
            print(f"   Description: {venv['description']}")
            print(f"   Created: {venv['created_at']}")
            print(f"   Last Used: {venv['last_used']}")
        
        print()

def update_last_used(venv_path):
    """Update the last_used timestamp for a virtual environment."""
    registry = load_registry()
    venv_path = os.path.abspath(os.path.expanduser(venv_path))
    
    for venv in registry["virtual_environments"]:
        if venv["path"] == venv_path:
            venv["last_used"] = datetime.now().isoformat()
            save_registry(registry)
            return True
    
    return False

def check_venv(venv_path=None, project_name=None):
    """Check if a virtual environment is registered."""
    if not venv_path and not project_name:
        print("Error: Either venv_path or project_name must be provided")
        return False
    
    registry = load_registry()
    
    if venv_path:
        venv_path = os.path.abspath(os.path.expanduser(venv_path))
    
    for venv in registry["virtual_environments"]:
        if (venv_path and venv["path"] == venv_path) or (project_name and venv["project_name"] == project_name):
            print(f"Virtual environment found: {venv['path']} ({venv['project_name']})")
            return True
    
    print("Virtual environment not found in registry")
    return False

def cleanup_nonexistent():
    """Remove entries for virtual environments that no longer exist."""
    registry = load_registry()
    original_count = len(registry["virtual_environments"])
    
    updated_venvs = []
    for venv in registry["virtual_environments"]:
        if os.path.isdir(venv["path"]):
            updated_venvs.append(venv)
        else:
            print(f"Removing non-existent virtual environment: {venv['path']} ({venv['project_name']})")
    
    registry["virtual_environments"] = updated_venvs
    save_registry(registry)
    
    removed_count = original_count - len(updated_venvs)
    print(f"Cleanup complete. Removed {removed_count} non-existent virtual environments.")
    return removed_count > 0

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Manage Python virtual environments registry")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a virtual environment to the registry")
    add_parser.add_argument("venv_path", help="Path to the virtual environment")
    add_parser.add_argument("project_name", help="Name of the project")
    add_parser.add_argument("--python-version", help="Python version (detected automatically if not provided)")
    add_parser.add_argument("--description", help="Description of the virtual environment")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a virtual environment from the registry")
    remove_parser.add_argument("--venv-path", help="Path to the virtual environment")
    remove_parser.add_argument("--project-name", help="Name of the project")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all registered virtual environments")
    list_parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed information")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check if a virtual environment is registered")
    check_parser.add_argument("--venv-path", help="Path to the virtual environment")
    check_parser.add_argument("--project-name", help="Name of the project")
    
    # Update last used command
    update_parser = subparsers.add_parser("update-last-used", help="Update the last_used timestamp for a virtual environment")
    update_parser.add_argument("venv_path", help="Path to the virtual environment")
    
    # Cleanup command
    subparsers.add_parser("cleanup", help="Remove entries for virtual environments that no longer exist")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_venv(args.venv_path, args.project_name, args.python_version, args.description)
    elif args.command == "remove":
        remove_venv(args.venv_path, args.project_name)
    elif args.command == "list":
        list_venvs(args.verbose)
    elif args.command == "check":
        check_venv(args.venv_path, args.project_name)
    elif args.command == "update-last-used":
        update_last_used(args.venv_path)
    elif args.command == "cleanup":
        cleanup_nonexistent()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
