#!/usr/bin/env python3
"""
Security Enforcement System

This script provides technical enforcement mechanisms to ensure AI agents operate
only within their designated areas. It includes functions for checking path permissions,
validating operations, and logging security events.
"""

import os
import sys
import json
import logging
import hashlib
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime

# Configuration values
DEFAULT_CONFIG = {
    "security": {
        "allowed_areas": [
            "~/Agentic"
        ],
        "restricted_areas": [
            "System files",
            "Global configurations"
        ]
    }
}

# Path to the configuration file
CONFIG_PATH = os.path.expanduser("~/Agentic/agentic_config.json")

def get_config_value(key_path, default=None):
    """
    Get a configuration value by its key path.
    
    Args:
        key_path (str): The key path in dot notation (e.g., 'security.allowed_areas')
        default (Any, optional): The default value to return if the key is not found
    
    Returns:
        The configuration value, or the default value if the key is not found
    """
    # Try to load from config file
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config_data = json.load(f)
            
            # Navigate to the key
            keys = key_path.split('.')
            value = config_data
            
            for key in keys:
                if key not in value:
                    return default
                value = value[key]
            
            return value
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
    
    # Fall back to default config
    keys = key_path.split('.')
    value = DEFAULT_CONFIG
    
    try:
        for key in keys:
            if key not in value:
                return default
            value = value[key]
        
        return value
    except Exception:
        return default

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.expanduser("~/Agentic/logs/security.log"), mode='a')
    ]
)
logger = logging.getLogger("security")

# Create logs directory if it doesn't exist
os.makedirs(os.path.expanduser("~/Agentic/logs"), exist_ok=True)

# Security event log path
SECURITY_LOG_PATH = os.path.expanduser("~/Agentic/logs/security_events.log")

class SecurityViolation(Exception):
    """Exception raised for security violations."""
    pass

class SecurityEnforcement:
    """Class for enforcing security boundaries."""
    
    def __init__(self):
        """Initialize the security enforcement system."""
        self.allowed_areas = self._get_allowed_areas()
        self.restricted_areas = self._get_restricted_areas()
    
    def _get_allowed_areas(self) -> List[str]:
        """Get the list of allowed areas from the configuration."""
        allowed_areas = get_config_value("security.allowed_areas", ["~/Agentic"])
        if not isinstance(allowed_areas, list):
            logger.warning(f"Allowed areas is not a list: {allowed_areas}")
            allowed_areas = ["~/Agentic"]
        return [os.path.abspath(os.path.expanduser(area)) for area in allowed_areas]
    
    def _get_restricted_areas(self) -> List[str]:
        """Get the list of restricted areas from the configuration."""
        restricted_areas = get_config_value("security.restricted_areas", [])
        if not isinstance(restricted_areas, list):
            logger.warning(f"Restricted areas is not a list: {restricted_areas}")
            restricted_areas = []
        return restricted_areas
    
    def is_path_allowed(self, path: str) -> bool:
        """
        Check if a path is allowed according to the security configuration.
        
        Args:
            path (str): The path to check
        
        Returns:
            bool: True if the path is allowed, False otherwise
        """
        path = os.path.abspath(os.path.expanduser(path))
        
        for area in self.allowed_areas:
            if path.startswith(area):
                return True
        
        return False
    
    def validate_path(self, path: str, operation: str = "access") -> bool:
        """
        Validate a path for a specific operation.
        
        Args:
            path (str): The path to validate
            operation (str): The operation to perform (access, write, delete, execute)
        
        Returns:
            bool: True if the path is valid for the operation, False otherwise
        
        Raises:
            SecurityViolation: If the path is not allowed
        """
        if not self.is_path_allowed(path):
            error_message = f"Security violation: {operation} operation on path '{path}' is not allowed"
            self.log_security_event(error_message, "violation", path, operation)
            raise SecurityViolation(error_message)
        
        self.log_security_event(f"{operation} operation on path '{path}' is allowed", "allowed", path, operation)
        return True
    
    def validate_command(self, command: str) -> bool:
        """
        Validate a command for execution.
        
        Args:
            command (str): The command to validate
        
        Returns:
            bool: True if the command is valid, False otherwise
        
        Raises:
            SecurityViolation: If the command is not allowed
        """
        # Check for potentially dangerous commands
        dangerous_commands = [
            "rm -rf /", "rm -rf /*", "rm -rf ~", "rm -rf ~/",
            "mkfs", "dd if=/dev/zero", ":(){ :|:& };:",
            "> /dev/sda", "mv ~ /dev/null"
        ]
        
        for dangerous in dangerous_commands:
            if dangerous in command:
                error_message = f"Security violation: potentially dangerous command '{command}'"
                self.log_security_event(error_message, "violation", None, "execute", command)
                raise SecurityViolation(error_message)
        
        # Check for commands that might modify system files
        system_modifying_commands = [
            "sudo", "su", "apt", "apt-get", "yum", "dnf",
            "brew", "npm -g", "pip install --user", "pip install -g"
        ]
        
        for system_cmd in system_modifying_commands:
            if command.startswith(system_cmd) or f" {system_cmd} " in f" {command} ":
                warning_message = f"Warning: command '{command}' might modify system files"
                self.log_security_event(warning_message, "warning", None, "execute", command)
                # We don't raise an exception here, just log a warning
        
        self.log_security_event(f"Command '{command}' is allowed", "allowed", None, "execute", command)
        return True
    
    def log_security_event(self, message: str, event_type: str, path: Optional[str] = None, 
                          operation: Optional[str] = None, command: Optional[str] = None) -> None:
        """
        Log a security event.
        
        Args:
            message (str): The message to log
            event_type (str): The type of event (allowed, warning, violation)
            path (Optional[str]): The path involved in the event
            operation (Optional[str]): The operation being performed
            command (Optional[str]): The command being executed
        """
        logger.info(message)
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "message": message
        }
        
        if path:
            event["path"] = path
        
        if operation:
            event["operation"] = operation
        
        if command:
            event["command"] = command
        
        try:
            with open(SECURITY_LOG_PATH, 'a') as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            logger.error(f"Failed to write to security event log: {e}")
    
    def scan_file_for_violations(self, file_path: str) -> List[str]:
        """
        Scan a file for potential security violations.
        
        Args:
            file_path (str): The path to the file to scan
        
        Returns:
            List[str]: A list of potential security violations
        """
        self.validate_path(file_path, "read")
        
        violations = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for absolute paths outside allowed areas
            for line in content.splitlines():
                for path in self.allowed_areas:
                    if path in line:
                        continue
                
                # Look for absolute paths
                if "/" in line and not line.strip().startswith("#") and not line.strip().startswith("//"):
                    # This is a very simple check and might have false positives
                    # A more sophisticated check would use regex or AST parsing
                    if any(p in line for p in ["/usr/", "/etc/", "/var/", "/bin/", "/sbin/"]):
                        violations.append(f"Potential reference to system path in line: {line.strip()}")
            
            # Check for potentially dangerous commands
            dangerous_patterns = [
                "os.system(", "subprocess.call(", "subprocess.run(",
                "eval(", "exec(", "rm -rf", "sudo", "su"
            ]
            
            for pattern in dangerous_patterns:
                if pattern in content:
                    violations.append(f"Potentially dangerous pattern '{pattern}' found in file")
        
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            violations.append(f"Error scanning file: {e}")
        
        return violations
    
    def calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate the SHA-256 hash of a file.
        
        Args:
            file_path (str): The path to the file
        
        Returns:
            str: The SHA-256 hash of the file
        """
        self.validate_path(file_path, "read")
        
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
        except Exception as e:
            logger.error(f"Error calculating hash for file {file_path}: {e}")
            return ""
    
    def verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """
        Verify the integrity of a file by comparing its hash with an expected value.
        
        Args:
            file_path (str): The path to the file
            expected_hash (str): The expected SHA-256 hash
        
        Returns:
            bool: True if the file integrity is verified, False otherwise
        """
        actual_hash = self.calculate_file_hash(file_path)
        
        if not actual_hash:
            return False
        
        if actual_hash != expected_hash:
            self.log_security_event(
                f"File integrity check failed for {file_path}",
                "warning",
                file_path,
                "integrity_check"
            )
            return False
        
        self.log_security_event(
            f"File integrity verified for {file_path}",
            "allowed",
            file_path,
            "integrity_check"
        )
        return True

# Create a singleton instance
security = SecurityEnforcement()

def is_path_allowed(path: str) -> bool:
    """
    Check if a path is allowed according to the security configuration.
    
    Args:
        path (str): The path to check
    
    Returns:
        bool: True if the path is allowed, False otherwise
    """
    return security.is_path_allowed(path)

def validate_path(path: str, operation: str = "access") -> bool:
    """
    Validate a path for a specific operation.
    
    Args:
        path (str): The path to validate
        operation (str): The operation to perform (access, write, delete, execute)
    
    Returns:
        bool: True if the path is valid for the operation, False otherwise
    
    Raises:
        SecurityViolation: If the path is not allowed
    """
    return security.validate_path(path, operation)

def validate_command(command: str) -> bool:
    """
    Validate a command for execution.
    
    Args:
        command (str): The command to validate
    
    Returns:
        bool: True if the command is valid, False otherwise
    
    Raises:
        SecurityViolation: If the command is not allowed
    """
    return security.validate_command(command)

def scan_file_for_violations(file_path: str) -> List[str]:
    """
    Scan a file for potential security violations.
    
    Args:
        file_path (str): The path to the file to scan
    
    Returns:
        List[str]: A list of potential security violations
    """
    return security.scan_file_for_violations(file_path)

def calculate_file_hash(file_path: str) -> str:
    """
    Calculate the SHA-256 hash of a file.
    
    Args:
        file_path (str): The path to the file
    
    Returns:
        str: The SHA-256 hash of the file
    """
    return security.calculate_file_hash(file_path)

def verify_file_integrity(file_path: str, expected_hash: str) -> bool:
    """
    Verify the integrity of a file by comparing its hash with an expected value.
    
    Args:
        file_path (str): The path to the file
        expected_hash (str): The expected SHA-256 hash
    
    Returns:
        bool: True if the file integrity is verified, False otherwise
    """
    return security.verify_file_integrity(file_path, expected_hash)

def log_security_event(message: str, event_type: str, path: Optional[str] = None,
                      operation: Optional[str] = None, command: Optional[str] = None) -> None:
    """
    Log a security event.
    
    Args:
        message (str): The message to log
        event_type (str): The type of event (allowed, warning, violation)
        path (Optional[str]): The path involved in the event
        operation (Optional[str]): The operation being performed
        command (Optional[str]): The command being executed
    """
    security.log_security_event(message, event_type, path, operation, command)

def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agentic Framework Security Enforcement")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Check path command
    check_parser = subparsers.add_parser("check-path", help="Check if a path is allowed")
    check_parser.add_argument("path", help="The path to check")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate-command", help="Validate a command for execution")
    validate_parser.add_argument("command", help="The command to validate")
    
    # Scan file command
    scan_parser = subparsers.add_parser("scan-file", help="Scan a file for potential security violations")
    scan_parser.add_argument("file", help="The path to the file to scan")
    
    # Calculate hash command
    hash_parser = subparsers.add_parser("hash-file", help="Calculate the SHA-256 hash of a file")
    hash_parser.add_argument("file", help="The path to the file")
    
    # Verify integrity command
    verify_parser = subparsers.add_parser("verify-integrity", help="Verify the integrity of a file")
    verify_parser.add_argument("file", help="The path to the file")
    verify_parser.add_argument("hash", help="The expected SHA-256 hash")
    
    args = parser.parse_args()
    
    if args.command == "check-path":
        try:
            if is_path_allowed(args.path):
                print(f"Path '{args.path}' is allowed")
            else:
                print(f"Path '{args.path}' is not allowed")
        except Exception as e:
            print(f"Error checking path: {e}")
    elif args.command == "validate-command":
        try:
            if validate_command(args.command):
                print(f"Command '{args.command}' is valid")
        except SecurityViolation as e:
            print(f"Security violation: {e}")
        except Exception as e:
            print(f"Error validating command: {e}")
    elif args.command == "scan-file":
        try:
            violations = scan_file_for_violations(args.file)
            if violations:
                print(f"Potential security violations in file '{args.file}':")
                for violation in violations:
                    print(f"  - {violation}")
            else:
                print(f"No potential security violations found in file '{args.file}'")
        except SecurityViolation as e:
            print(f"Security violation: {e}")
        except Exception as e:
            print(f"Error scanning file: {e}")
    elif args.command == "hash-file":
        try:
            file_hash = calculate_file_hash(args.file)
            if file_hash:
                print(f"SHA-256 hash of file '{args.file}':")
                print(file_hash)
            else:
                print(f"Failed to calculate hash for file '{args.file}'")
        except SecurityViolation as e:
            print(f"Security violation: {e}")
        except Exception as e:
            print(f"Error calculating hash: {e}")
    elif args.command == "verify-integrity":
        try:
            if verify_file_integrity(args.file, args.hash):
                print(f"File integrity verified for '{args.file}'")
            else:
                print(f"File integrity check failed for '{args.file}'")
        except SecurityViolation as e:
            print(f"Security violation: {e}")
        except Exception as e:
            print(f"Error verifying file integrity: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
