#!/usr/bin/env python3
"""
Agentic Framework Discovery Script

This script helps AI agents discover and load the Agentic framework.
It provides information about the framework structure, available tools,
and documentation.
"""

import os
import sys
import json
import argparse
from pathlib import Path

def find_agentic_root():
    """Find the Agentic framework root directory."""
    # First, try the standard location
    standard_path = os.path.expanduser("~/Agentic")
    if os.path.exists(standard_path) and os.path.isdir(standard_path):
        return standard_path
    
    # If not found, try to find it in common locations
    common_locations = [
        os.path.expanduser("~"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Projects"),
        os.path.expanduser("~/Desktop")
    ]
    
    for location in common_locations:
        if os.path.exists(location) and os.path.isdir(location):
            for item in os.listdir(location):
                item_path = os.path.join(location, item)
                if item.lower() == "agentic" and os.path.isdir(item_path):
                    return item_path
    
    # If still not found, return None
    return None

def load_agentic_info(agentic_root, json_output=False):
    """Load the Agentic framework information."""
    info_path = os.path.join(agentic_root, "agentic", ".agentic-info")
    
    if os.path.exists(info_path):
        try:
            with open(info_path, 'r') as f:
                info = json.load(f)
            
            # For JSON output, we'll keep the $HOME placeholder
            # For human-readable output, we'll replace it with the actual home directory
            if not json_output:
                # Replace $HOME with the actual home directory
                home_dir = os.path.expanduser("~")
                for key, value in info.items():
                    if isinstance(value, str):
                        info[key] = value.replace("$HOME", home_dir)
                    elif isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            if isinstance(subvalue, str):
                                info[key][subkey] = subvalue.replace("$HOME", home_dir)
            
            return info
        except Exception as e:
            print(f"Error loading Agentic info: {e}")
            return None
    else:
        # Create a basic info structure
        return {
            "framework_name": "Agentic",
            "version": "Unknown",
            "description": "A framework for managing and operating AI agents with controlled access to a machine",
            "home_directory": agentic_root,
            "documentation": {
                "agent_rules": os.path.join(agentic_root, "agentic", "AGENT_RULES.md"),
                "agent_quick_reference": os.path.join(agentic_root, "agentic", "AGENT_QUICK_REFERENCE.md"),
                "human_guide": os.path.join(agentic_root, "agentic", "HUMAN_GUIDE.md"),
                "readme": os.path.join(agentic_root, "agentic", "README.md")
            },
            "directory_structure": {
                "agentic": os.path.join(agentic_root, "agentic"),
                "projects": os.path.join(agentic_root, "projects"),
                "shared": os.path.join(agentic_root, "shared"),
                "tmp": os.path.join(agentic_root, "tmp"),
                "logs": os.path.join(agentic_root, "logs"),
                "cache": os.path.join(agentic_root, "cache"),
                "backups": os.path.join(agentic_root, "backups")
            },
            "utility_scripts": {
                "check_environment": os.path.join(agentic_root, "agentic", "check_environment.py"),
                "venv_manager": os.path.join(agentic_root, "agentic", "venv_manager.py"),
                "uv_manager": os.path.join(agentic_root, "agentic", "uv_manager.py"),
                "create_project": os.path.join(agentic_root, "agentic", "create_project.py"),
                "cleanup_manager": os.path.join(agentic_root, "agentic", "cleanup_manager.py")
            },
            "registry": {
                "path": os.path.join(agentic_root, "venv_registry.json"),
                "description": "Registry of active Python virtual environments managed by uv"
            }
        }

def check_environment(agentic_root):
    """Check if the Agentic environment is set up correctly."""
    # Check if the agentic directory exists
    agentic_dir = os.path.join(agentic_root, "agentic")
    if not os.path.exists(agentic_dir) or not os.path.isdir(agentic_dir):
        print(f"Error: Agentic directory not found at {agentic_dir}")
        return False
    
    # Check if the required files exist
    required_files = [
        "AGENT_RULES.md",
        "AGENT_QUICK_REFERENCE.md",
        "README.md",
        "check_environment.py"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(agentic_dir, file)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if the required directories exist
    required_dirs = [
        "projects",
        "shared",
        "logs",
        "tmp",
        "cache",
        "backups"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = os.path.join(agentic_root, dir_name)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"Warning: Missing directories: {', '.join(missing_dirs)}")
        print("You can create them using the check_environment.py script.")
    
    return True

def print_framework_info(info):
    """Print information about the Agentic framework."""
    print(f"\n{info['framework_name']} Framework (v{info['version']})")
    print("=" * 50)
    print(f"Description: {info['description']}")
    print(f"Home Directory: {info['home_directory']}")
    
    print("\nDocumentation:")
    for name, path in info['documentation'].items():
        print(f"  - {name.replace('_', ' ').title()}: {path}")
    
    print("\nDirectory Structure:")
    for name, path in info['directory_structure'].items():
        print(f"  - {name.replace('_', ' ').title()}: {path}")
    
    print("\nUtility Scripts:")
    for name, path in info['utility_scripts'].items():
        print(f"  - {name.replace('_', ' ').title()}: {path}")
    
    print("\nRegistry:")
    print(f"  - Path: {info['registry']['path']}")
    print(f"  - Description: {info['registry']['description']}")
    
    if "recommended_entry_prompt" in info:
        print("\nRecommended Entry Prompt:")
        print(f"  {info['recommended_entry_prompt']}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Discover and load the Agentic framework")
    parser.add_argument("--path", help="Path to the Agentic framework root directory")
    parser.add_argument("--json", action="store_true", help="Output information in JSON format")
    parser.add_argument("--check", action="store_true", help="Check if the Agentic environment is set up correctly")
    
    args = parser.parse_args()
    
    # Find the Agentic root directory
    if args.path:
        agentic_root = args.path
    else:
        agentic_root = find_agentic_root()
    
    if not agentic_root:
        print("Error: Could not find the Agentic framework root directory.")
        print("Please specify the path using the --path option.")
        return 1
    
    # Load the Agentic framework information
    info = load_agentic_info(agentic_root, args.json)
    
    if not info:
        print("Error: Could not load Agentic framework information.")
        return 1
    
    # Check the environment if requested
    if args.check:
        if not check_environment(agentic_root):
            return 1
    
    # Output the information
    if args.json:
        # Write the JSON to a file in the current directory
        output_file = os.path.join(os.getcwd(), "agentic_info.json")
        with open(output_file, 'w') as f:
            json.dump(info, f, indent=2)
        print(f"JSON output written to {output_file}")
        
        # Also print the JSON to the terminal
        print(json.dumps(info, indent=2))
    else:
        print_framework_info(info)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
