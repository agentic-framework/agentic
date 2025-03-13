#!/bin/bash
# setup_agentic.sh
#
# DEPRECATED: This script is deprecated. Please use the new 'ag setup' commands instead.
#
# New usage:
#   ./ag setup all                    # Run all setup steps
#   ./ag setup install-dependencies   # Install required dependencies
#   ./ag setup create-directories     # Create the required directory structure
#   ./ag setup initialize-registry    # Initialize the virtual environment registry
#   ./ag setup make-scripts-executable # Make utility scripts executable
#
# This script provides a comprehensive setup for the Agentic framework.
# It can install dependencies, create all necessary directories, and initialize the registry.
#
# Legacy usage:
#   ./setup_agentic.sh [options]
#
# Options:
#   --install-dependencies    Install required dependencies (uv, etc.)
#   --create-directories      Create the Agentic directory structure
#   --initialize-registry     Initialize the virtual environment registry
#   --all                     Perform all setup steps (default)
#   --help                    Display this help message

set -e  # Exit immediately if a command exits with a non-zero status

# Display deprecation warning
echo -e "\033[1;33mWARNING: This script is deprecated.\033[0m"
echo -e "\033[1;33mPlease use the new 'ag setup' commands instead:\033[0m"
echo -e "  ./ag setup all                     # Run all setup steps"
echo -e "  ./ag setup install-dependencies    # Install required dependencies"
echo -e "  ./ag setup create-directories      # Create the required directory structure"
echo -e "  ./ag setup initialize-registry     # Initialize the virtual environment registry"
echo -e "  ./ag setup make-scripts-executable # Make utility scripts executable"
echo ""
echo -e "\033[1;33mContinuing with legacy script in 5 seconds...\033[0m"
sleep 5
echo ""

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
INSTALL_DEPENDENCIES=false
CREATE_DIRECTORIES=false
INITIALIZE_REGISTRY=false
ALL=false

# Parse command line arguments
if [ $# -eq 0 ]; then
    ALL=true
else
    for arg in "$@"; do
        case $arg in
            --install-dependencies)
                INSTALL_DEPENDENCIES=true
                ;;
            --create-directories)
                CREATE_DIRECTORIES=true
                ;;
            --initialize-registry)
                INITIALIZE_REGISTRY=true
                ;;
            --all)
                ALL=true
                ;;
            --help)
                echo "Usage: ./setup_agentic.sh [options]"
                echo ""
                echo "Options:"
                echo "  --install-dependencies    Install required dependencies (uv, etc.)"
                echo "  --create-directories      Create the Agentic directory structure"
                echo "  --initialize-registry     Initialize the virtual environment registry"
                echo "  --all                     Perform all setup steps (default)"
                echo "  --help                    Display this help message"
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $arg${NC}"
                echo "Use --help for usage information."
                exit 1
                ;;
        esac
    done
fi

# If --all is specified, enable all options
if [ "$ALL" = true ]; then
    INSTALL_DEPENDENCIES=true
    CREATE_DIRECTORIES=true
    INITIALIZE_REGISTRY=true
fi

# Define paths
AGENTIC_ROOT="$HOME/Agentic"
AGENTIC_REPO="$AGENTIC_ROOT/agentic"
PROJECTS_DIR="$AGENTIC_ROOT/projects"
SHARED_DIR="$AGENTIC_ROOT/shared"
TMP_DIR="$AGENTIC_ROOT/tmp"
LOGS_DIR="$AGENTIC_ROOT/logs"
CACHE_DIR="$AGENTIC_ROOT/cache"
BACKUPS_DIR="$AGENTIC_ROOT/backups"
REGISTRY_PATH="$AGENTIC_ROOT/venv_registry.json"

# Function to create a directory if it doesn't exist
create_directory() {
    local dir=$1
    local description=$2
    
    if [ ! -d "$dir" ]; then
        echo -e "${BLUE}Creating $description: $dir${NC}"
        mkdir -p "$dir"
        echo -e "${GREEN}✓ Created $description${NC}"
    else
        echo -e "${GREEN}✓ $description already exists: $dir${NC}"
    fi
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install uv
install_uv() {
    echo -e "${BLUE}Installing uv package manager...${NC}"
    
    if command_exists uv; then
        echo -e "${GREEN}✓ uv is already installed${NC}"
        uv --version
        return 0
    fi
    
    # Check if curl is installed
    if ! command_exists curl; then
        echo -e "${RED}Error: curl is not installed. Please install curl and try again.${NC}"
        return 1
    fi
    
    # Install uv using the official installer
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to the current PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Verify installation
    if command_exists uv; then
        echo -e "${GREEN}✓ uv installed successfully${NC}"
        uv --version
    else
        echo -e "${RED}Error: Failed to install uv${NC}"
        return 1
    fi
}

# Function to initialize the registry
initialize_registry() {
    echo -e "${BLUE}Initializing virtual environment registry...${NC}"
    
    if [ -f "$REGISTRY_PATH" ]; then
        echo -e "${YELLOW}Registry file already exists: $REGISTRY_PATH${NC}"
        echo -e "${YELLOW}Creating backup before reinitializing...${NC}"
        
        # Create backup directory if it doesn't exist
        mkdir -p "$BACKUPS_DIR"
        
        # Create backup with timestamp
        BACKUP_PATH="$BACKUPS_DIR/venv_registry_$(date +%Y%m%d_%H%M%S).json"
        cp "$REGISTRY_PATH" "$BACKUP_PATH"
        echo -e "${GREEN}✓ Created backup: $BACKUP_PATH${NC}"
    fi
    
    # Create new registry file
    cat > "$REGISTRY_PATH" << EOF
{
  "virtual_environments": [],
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "registry_version": "1.0.0",
  "metadata": {
    "description": "Registry of active Python virtual environments managed by uv",
    "managed_by": "agentic framework",
    "created_by": "setup_agentic.sh"
  }
}
EOF
    
    echo -e "${GREEN}✓ Initialized registry file: $REGISTRY_PATH${NC}"
}

# Function to make utility scripts executable
make_scripts_executable() {
    echo -e "${BLUE}Making utility scripts executable...${NC}"
    
    # List of utility scripts
    SCRIPTS=(
        "check_environment.py"
        "venv_manager.py"
        "create_project.py"
        "uv_manager.py"
        "cleanup_manager.py"
        "rule_loader.py"
        "setup_agentic.sh"
    )
    
    for script in "${SCRIPTS[@]}"; do
        script_path="$AGENTIC_REPO/$script"
        if [ -f "$script_path" ]; then
            chmod +x "$script_path"
            echo -e "${GREEN}✓ Made executable: $script${NC}"
        else
            echo -e "${YELLOW}! Script not found: $script${NC}"
        fi
    done
}

# Main setup process
echo -e "${BLUE}=== Agentic Framework Setup ===${NC}"
echo -e "${BLUE}Starting setup process...${NC}"

# Install dependencies
if [ "$INSTALL_DEPENDENCIES" = true ]; then
    echo -e "${BLUE}\n=== Installing Dependencies ===${NC}"
    install_uv
fi

# Create directories
if [ "$CREATE_DIRECTORIES" = true ]; then
    echo -e "${BLUE}\n=== Creating Directory Structure ===${NC}"
    create_directory "$AGENTIC_ROOT" "Agentic root directory"
    create_directory "$PROJECTS_DIR" "Projects directory"
    create_directory "$SHARED_DIR" "Shared resources directory"
    create_directory "$TMP_DIR" "Temporary files directory"
    create_directory "$LOGS_DIR" "Logs directory"
    create_directory "$CACHE_DIR" "Cache directory"
    create_directory "$BACKUPS_DIR" "Backups directory"
    
    # Create shared subdirectories
    create_directory "$SHARED_DIR/templates" "Templates directory"
    create_directory "$SHARED_DIR/scripts" "Shared scripts directory"
    create_directory "$SHARED_DIR/data" "Shared data directory"
    
    # Make utility scripts executable
    if [ -d "$AGENTIC_REPO" ]; then
        make_scripts_executable
    else
        echo -e "${YELLOW}! Agentic repository not found at $AGENTIC_REPO${NC}"
        echo -e "${YELLOW}! Skipping making scripts executable${NC}"
    fi
fi

# Initialize registry
if [ "$INITIALIZE_REGISTRY" = true ]; then
    echo -e "${BLUE}\n=== Initializing Registry ===${NC}"
    initialize_registry
fi

echo -e "${GREEN}\n=== Setup Complete ===${NC}"
echo -e "${GREEN}The Agentic framework has been set up successfully.${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Run ${YELLOW}./check_environment.py${NC} to verify the environment"
echo -e "2. Read the ${YELLOW}README.md${NC} for more information about the framework"
echo -e "3. Use ${YELLOW}./create_project.py${NC} to create your first project"

exit 0
