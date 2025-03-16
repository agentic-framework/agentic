#!/bin/bash

# setup_agentic.sh
# Automated setup script for the Agentic framework with issues and notes support

set -e  # Exit on error

# Print colored output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}==== $1 ====${NC}\n"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print warning messages
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Set AGHOME
if [ -z "$AGHOME" ]; then
    export AGHOME="$HOME/Agentic"
    print_warning "AGHOME environment variable not set. Using default: $AGHOME"
    echo "export AGHOME=$AGHOME" >> ~/.bashrc
    echo "export AGHOME=$AGHOME" >> ~/.zshrc
    print_success "Added AGHOME to .bashrc and .zshrc"
else
    print_success "AGHOME is set to $AGHOME"
fi

# Create directory structure
print_section "Creating Directory Structure"
mkdir -p "$AGHOME"/{projects,shared,tmp,logs,cache,backups}
print_success "Created directory structure"

# Check if Python is installed
print_section "Checking Python Installation"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python is installed: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if command_exists pip3; then
    PIP_VERSION=$(pip3 --version)
    print_success "pip is installed: $PIP_VERSION"
else
    print_error "pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if git is installed
if command_exists git; then
    GIT_VERSION=$(git --version)
    print_success "git is installed: $GIT_VERSION"
else
    print_error "git is not installed. Please install git and try again."
    exit 1
fi

# Create virtual environment
print_section "Creating Virtual Environment"
if [ -d "$AGHOME/.venv" ]; then
    print_warning "Virtual environment already exists at $AGHOME/.venv"
else
    python3 -m venv "$AGHOME/.venv"
    print_success "Created virtual environment at $AGHOME/.venv"
fi

# Activate virtual environment
source "$AGHOME/.venv/bin/activate"
print_success "Activated virtual environment"

# Upgrade pip
print_section "Upgrading pip"
pip install --upgrade pip
print_success "Upgraded pip"

# Clone repositories
print_section "Cloning Repositories"

# Check if agentic-core repository exists
if [ -d "$AGHOME/projects/agentic-core" ]; then
    print_warning "agentic-core repository already exists"
    cd "$AGHOME/projects/agentic-core"
    git pull
    print_success "Updated agentic-core repository"
else
    git clone git@github.com:agentic-framework/agentic-core.git "$AGHOME/projects/agentic-core"
    print_success "Cloned agentic-core repository"
fi

# Check if agentic-issues repository exists
if [ -d "$AGHOME/projects/agentic-issues" ]; then
    print_warning "agentic-issues repository already exists"
    cd "$AGHOME/projects/agentic-issues"
    git pull
    print_success "Updated agentic-issues repository"
else
    git clone git@github.com:agentic-framework/agentic-issues.git "$AGHOME/projects/agentic-issues"
    print_success "Cloned agentic-issues repository"
fi

# Check if agentic-notes repository exists
if [ -d "$AGHOME/projects/agentic-notes" ]; then
    print_warning "agentic-notes repository already exists"
    cd "$AGHOME/projects/agentic-notes"
    git pull
    print_success "Updated agentic-notes repository"
else
    git clone git@github.com:agentic-framework/agentic-notes.git "$AGHOME/projects/agentic-notes"
    print_success "Cloned agentic-notes repository"
fi

# Install packages
print_section "Installing Packages"

# Install agentic-core
cd "$AGHOME/projects/agentic-core"
pip install -e .
print_success "Installed agentic-core"

# Install agentic-issues
cd "$AGHOME/projects/agentic-issues"
pip install -e .
print_success "Installed agentic-issues"

# Install agentic-notes
cd "$AGHOME/projects/agentic-notes"
pip install -e .
print_success "Installed agentic-notes"

# Register virtual environment
print_section "Registering Virtual Environment"
ag venv add "$AGHOME/.venv" agentic-core --description "Main virtual environment for Agentic framework" || true
print_success "Registered virtual environment"

# Run environment check
print_section "Running Environment Check"
ag env check
print_success "Environment check completed"

# Fix any issues
print_section "Fixing Issues"
ag env fix
print_success "Fixed issues"

# Create test note
print_section "Creating Test Note"
ag note create "Test Note" "This is a test note to verify that the note system is working properly."
print_success "Created test note"

# Create test issue
print_section "Creating Test Issue"
ag issues submit --title "Test Issue" --description "This is a test issue to verify that the issues system is working properly." --priority medium --labels test
print_success "Created test issue"

# List notes and issues
print_section "Listing Notes and Issues"
echo "Notes:"
ag note list
echo ""
echo "Issues:"
ag issues list

# Print completion message
print_section "Setup Complete"
echo "The Agentic framework has been successfully set up with issues and note support."
echo ""
echo "To use the framework, activate the virtual environment:"
echo "  source $AGHOME/.venv/bin/activate"
echo ""
echo "Then use the ag command to manage your projects and environments:"
echo "  ag env check"
echo "  ag note list"
echo "  ag issues list"
echo ""
echo "For more information, see the documentation in $AGHOME/agentic/docs/"
