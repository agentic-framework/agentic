#!/usr/bin/env python3
"""
UV Manager

This script helps with installing and managing uv, the Python package manager
specified in the agent rules. It provides commands to install, update, and
manage Python installations with uv.
"""

import os
import sys
import subprocess
import argparse
import platform
import shutil
from pathlib import Path

def run_command(command, capture_output=True):
    """Run a shell command and return the output."""
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                capture_output=True
            )
            return result.stdout.strip()
        else:
            # For commands where we want to see the output in real-time
            subprocess.run(
                command,
                shell=True,
                check=True
            )
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        if capture_output:
            print(f"Error message: {e.stderr}")
        return None

def is_uv_installed():
    """Check if uv is installed."""
    return shutil.which("uv") is not None

def get_uv_version():
    """Get the installed uv version."""
    if not is_uv_installed():
        return None
    
    result = run_command("uv --version")
    return result

def install_uv():
    """Install uv using the official installation script."""
    if is_uv_installed():
        print(f"uv is already installed (version {get_uv_version()})")
        return True
    
    print("Installing uv...")
    
    # Use the official installation script
    result = run_command("curl -sSf https://astral.sh/uv/install.sh | sh", capture_output=False)
    
    if result is None:
        print("Failed to install uv.")
        return False
    
    # Check if uv is now in the PATH
    if not is_uv_installed():
        print("\nuv was installed but is not in your PATH.")
        print("You may need to restart your terminal or add the installation directory to your PATH.")
        
        # Try to find the installation directory
        home_dir = Path.home()
        possible_paths = [
            home_dir / ".cargo" / "bin",
            home_dir / ".local" / "bin"
        ]
        
        for path in possible_paths:
            if (path / "uv").exists():
                print(f"\nFound uv at: {path / 'uv'}")
                print(f"Add this directory to your PATH: {path}")
                break
        
        return False
    
    print(f"uv installed successfully (version {get_uv_version()})")
    return True

def update_uv():
    """Update uv to the latest version."""
    if not is_uv_installed():
        print("uv is not installed. Installing...")
        return install_uv()
    
    current_version = get_uv_version()
    print(f"Current uv version: {current_version}")
    print("Updating uv...")
    
    # Use the official installation script to update
    result = run_command("curl -sSf https://astral.sh/uv/install.sh | sh", capture_output=False)
    
    if result is None:
        print("Failed to update uv.")
        return False
    
    new_version = get_uv_version()
    if new_version == current_version:
        print("uv is already at the latest version.")
    else:
        print(f"uv updated successfully: {current_version} -> {new_version}")
    
    return True

def list_python_versions():
    """List Python versions available through uv."""
    if not is_uv_installed():
        print("uv is not installed. Please install it first.")
        return False
    
    print("Available Python versions:")
    run_command("uv python list", capture_output=False)
    return True

def install_python(version=None):
    """Install a Python version using uv."""
    if not is_uv_installed():
        print("uv is not installed. Please install it first.")
        return False
    
    if version:
        print(f"Installing Python {version}...")
        command = f"uv python install {version}"
    else:
        print("Installing the latest Python version...")
        command = "uv python install"
    
    result = run_command(command, capture_output=False)
    
    if result is None:
        print("Failed to install Python.")
        return False
    
    print("Python installed successfully.")
    return True

def create_venv(path, python_version=None):
    """Create a virtual environment using uv."""
    if not is_uv_installed():
        print("uv is not installed. Please install it first.")
        return False
    
    # Expand the path
    path = os.path.abspath(os.path.expanduser(path))
    
    # Create the command
    command = f"uv venv {path}"
    if python_version:
        command += f" --python {python_version}"
    
    print(f"Creating virtual environment at {path}...")
    result = run_command(command, capture_output=False)
    
    if result is None:
        print("Failed to create virtual environment.")
        return False
    
    print(f"Virtual environment created successfully at {path}")
    print(f"Activate with: source {path}/bin/activate")
    return True

def show_uv_info():
    """Show information about uv."""
    if not is_uv_installed():
        print("uv is not installed. Please install it first.")
        return False
    
    print("UV Information:")
    print(f"Version: {get_uv_version()}")
    print("\nPython Versions:")
    run_command("uv python list", capture_output=False)
    
    print("\nFor more information, visit: https://github.com/astral-sh/uv")
    return True

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Manage uv and Python installations")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Install command
    subparsers.add_parser("install", help="Install uv")
    
    # Update command
    subparsers.add_parser("update", help="Update uv to the latest version")
    
    # List Python versions command
    subparsers.add_parser("list-python", help="List available Python versions")
    
    # Install Python command
    install_python_parser = subparsers.add_parser("install-python", help="Install a Python version")
    install_python_parser.add_argument("version", nargs="?", help="Python version to install (e.g., 3.11)")
    
    # Create virtual environment command
    create_venv_parser = subparsers.add_parser("create-venv", help="Create a virtual environment")
    create_venv_parser.add_argument("path", help="Path for the virtual environment")
    create_venv_parser.add_argument("--python", help="Python version to use")
    
    # Info command
    subparsers.add_parser("info", help="Show information about uv")
    
    args = parser.parse_args()
    
    if args.command == "install":
        install_uv()
    elif args.command == "update":
        update_uv()
    elif args.command == "list-python":
        list_python_versions()
    elif args.command == "install-python":
        install_python(args.version)
    elif args.command == "create-venv":
        create_venv(args.path, args.python)
    elif args.command == "info":
        show_uv_info()
    else:
        if is_uv_installed():
            print(f"uv is installed (version {get_uv_version()})")
            parser.print_help()
        else:
            print("uv is not installed. Run 'uv_manager.py install' to install it.")
            parser.print_help()

if __name__ == "__main__":
    main()
