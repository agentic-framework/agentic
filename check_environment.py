#!/usr/bin/env python3
"""
Environment Checker

This script checks if the current environment is set up correctly according to the agent rules.
It verifies the installation of uv, the directory structure, and the registry file.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Base directories
AGENTIC_DIR = "/Users/mingli/Agentic"
TMP_DIR = os.path.join(AGENTIC_DIR, "tmp")
PROJECTS_DIR = os.path.join(AGENTIC_DIR, "projects")
SHARED_DIR = os.path.join(AGENTIC_DIR, "shared")
REGISTRY_PATH = os.path.join(AGENTIC_DIR, "venv_registry.json")

def print_status(message, status, details=None):
    """Print a status message with color coding."""
    if status:
        status_str = "\033[92m✓\033[0m"  # Green checkmark
    else:
        status_str = "\033[91m✗\033[0m"  # Red X
    
    print(f"{status_str} {message}")
    
    if details and not status:
        print(f"  \033[93m{details}\033[0m")  # Yellow details

def check_uv_installation():
    """Check if uv is installed and get its version."""
    uv_path = shutil.which("uv")
    
    if uv_path:
        try:
            result = subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            version = result.stdout.strip()
            print_status(f"uv is installed (version {version})", True)
            return True
        except subprocess.CalledProcessError:
            print_status("uv is installed but failed to get version", False, "Try running 'uv --version' manually")
            return False
    else:
        print_status("uv is not installed", False, "Install uv using './uv_manager.py install'")
        return False

def check_directory_structure():
    """Check if the required directory structure exists."""
    directories = [
        (AGENTIC_DIR, "Agentic root directory"),
        (TMP_DIR, "Temporary files directory"),
        (PROJECTS_DIR, "Projects directory"),
        (SHARED_DIR, "Shared resources directory")
    ]
    
    all_exist = True
    
    for dir_path, description in directories:
        exists = os.path.exists(dir_path) and os.path.isdir(dir_path)
        print_status(f"{description}: {dir_path}", exists)
        
        if not exists:
            all_exist = False
    
    return all_exist

def check_registry_file():
    """Check if the registry file exists and is valid."""
    if not os.path.exists(REGISTRY_PATH):
        print_status(f"Virtual environment registry: {REGISTRY_PATH}", False, "Registry file does not exist")
        return False
    
    try:
        with open(REGISTRY_PATH, 'r') as f:
            registry = json.load(f)
        
        if "virtual_environments" in registry:
            venv_count = len(registry["virtual_environments"])
            print_status(f"Virtual environment registry: {REGISTRY_PATH} ({venv_count} environments)", True)
            return True
        else:
            print_status(f"Virtual environment registry: {REGISTRY_PATH}", False, "Registry file is missing required fields")
            return False
    except json.JSONDecodeError:
        print_status(f"Virtual environment registry: {REGISTRY_PATH}", False, "Registry file is not valid JSON")
        return False
    except Exception as e:
        print_status(f"Virtual environment registry: {REGISTRY_PATH}", False, f"Error reading registry file: {e}")
        return False

def check_utility_scripts():
    """Check if the utility scripts exist and are executable."""
    scripts = [
        "venv_manager.py",
        "create_project.py",
        "uv_manager.py",
        "cleanup_manager.py"
    ]
    
    all_exist = True
    
    for script in scripts:
        script_path = os.path.join(AGENTIC_DIR, "agentic", script)
        exists = os.path.exists(script_path)
        executable = exists and os.access(script_path, os.X_OK)
        
        if exists and executable:
            print_status(f"Utility script: {script}", True)
        elif exists:
            print_status(f"Utility script: {script}", False, "Script exists but is not executable. Run 'chmod +x {script}'")
            all_exist = False
        else:
            print_status(f"Utility script: {script}", False, "Script does not exist")
            all_exist = False
    
    return all_exist

def check_python_installations():
    """Check Python installations managed by uv."""
    if not shutil.which("uv"):
        print_status("Python installations", False, "uv is not installed")
        return False
    
    try:
        result = subprocess.run(
            ["uv", "python", "list"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            python_versions = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            
            if python_versions:
                print_status(f"Python installations: {len(python_versions)} version(s) available", True)
                for version in python_versions:
                    print(f"  - {version}")
                return True
            else:
                print_status("Python installations", False, "No Python versions installed with uv")
                return False
        else:
            print_status("Python installations", False, "Failed to list Python versions")
            return False
    except Exception as e:
        print_status("Python installations", False, f"Error checking Python installations: {e}")
        return False

def main():
    """Main function to check the environment."""
    print("\n\033[1mAgentic Environment Check\033[0m\n")
    
    print("\033[1m1. UV Installation\033[0m")
    uv_ok = check_uv_installation()
    print()
    
    print("\033[1m2. Directory Structure\033[0m")
    dirs_ok = check_directory_structure()
    print()
    
    print("\033[1m3. Registry File\033[0m")
    registry_ok = check_registry_file()
    print()
    
    print("\033[1m4. Utility Scripts\033[0m")
    scripts_ok = check_utility_scripts()
    print()
    
    print("\033[1m5. Python Installations\033[0m")
    python_ok = check_python_installations()
    print()
    
    # Summary
    print("\033[1mSummary\033[0m")
    all_ok = uv_ok and dirs_ok and registry_ok and scripts_ok and python_ok
    
    if all_ok:
        print("\033[92mEnvironment is set up correctly according to the agent rules.\033[0m")
    else:
        print("\033[91mEnvironment has issues that need to be addressed.\033[0m")
        
        if not uv_ok:
            print("- Install uv using './uv_manager.py install'")
        
        if not dirs_ok:
            print("- Create missing directories using './cleanup_manager.py check-structure'")
        
        if not registry_ok:
            print("- Create or fix the registry file")
        
        if not scripts_ok:
            print("- Ensure all utility scripts exist and are executable")
        
        if not python_ok:
            print("- Install Python using './uv_manager.py install-python'")

if __name__ == "__main__":
    main()
