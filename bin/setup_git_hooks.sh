#!/bin/bash

# Script to set up Git hooks for the Agentic framework

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.githooks"

echo "Setting up Git hooks for Agentic framework..."

# Configure Git to use the custom hooks directory
git config --local core.hooksPath "$HOOKS_DIR"

echo "Git hooks have been set up successfully."
echo "Pre-commit hooks will now run automatically before each commit."
