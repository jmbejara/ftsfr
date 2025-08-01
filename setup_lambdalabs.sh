#!/bin/bash

# LambdaLabs GPU Instance Setup Script for FTSFR Project
# This script automates the setup of Miniconda, Python environment, Pixi, and VS Code Server

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SETUP_STATE_FILE="$HOME/.ftsfr_setup_state"
CONDA_ENV_NAME="ftsfr"
PYTHON_VERSION="3.12.6"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if we need to restart the script after conda init
check_setup_state() {
    if [ -f "$SETUP_STATE_FILE" ]; then
        STATE=$(cat "$SETUP_STATE_FILE")
        echo "$STATE"
    else
        echo "0"
    fi
}

# Function to update setup state
update_setup_state() {
    echo "$1" > "$SETUP_STATE_FILE"
}

# Get the current setup state
SETUP_STATE=$(check_setup_state)

case $SETUP_STATE in
    0)
        print_status "Starting fresh LambdaLabs setup..."
        
        # Step 1: Install Miniconda
        print_status "Installing Miniconda..."
        mkdir -p ~/miniconda3
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
        bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
        rm ~/miniconda3/miniconda.sh
        
        # Source conda
        source ~/miniconda3/bin/activate
        
        # Initialize conda for all shells
        print_status "Initializing conda for all shells..."
        conda init --all
        
        # Download VS Code CLI
        print_status "Downloading VS Code CLI..."
        curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
        tar -xf vscode_cli.tar.gz
        rm vscode_cli.tar.gz
        
        # Update state and request restart
        update_setup_state "1"
        
        print_warning "Conda has been initialized. The shell needs to be restarted."
        print_status "Please run the following commands:"
        echo ""
        echo "    source ~/.bashrc"
        echo "    cd $SCRIPT_DIR"
        echo "    ./setup_lambdalabs.sh"
        echo ""
        print_status "Or simply close and reopen your terminal, then run the script again."
        exit 0
        ;;
        
    1)
        print_status "Continuing setup after shell restart..."
        
        # Check if conda is available
        if ! command -v conda &> /dev/null; then
            print_error "Conda is not available. Please ensure you've restarted your shell properly."
            exit 1
        fi
        
        # Step 2: Create conda environment
        print_status "Creating conda environment '$CONDA_ENV_NAME' with Python $PYTHON_VERSION..."
        conda create -n $CONDA_ENV_NAME python=$PYTHON_VERSION -y
        
        # Activate the environment
        print_status "Activating conda environment..."
        source $(conda info --base)/etc/profile.d/conda.sh
        conda activate $CONDA_ENV_NAME
        
        # Install Python packages
        if [ -f "requirements.txt" ]; then
            print_status "Installing Python packages from requirements.txt..."
            pip install -r requirements.txt
        else
            print_warning "requirements.txt not found in current directory. Skipping Python package installation."
        fi
        
        # Install Bloomberg API if needed (optional)
        print_status "Note: To install Bloomberg API, run:"
        echo "    pip install blpapi --index-url https://blpapi.bloomberg.com/repository/releases/python/simple/"
        
        # Install Pixi
        print_status "Installing Pixi..."
        curl -fsSL https://pixi.sh/install.sh | bash
        
        # Update setup state
        update_setup_state "2"
        
        print_status "Setup complete!"
        print_status ""
        print_status "Next steps:"
        echo "1. Activate the conda environment:"
        echo "    conda activate $CONDA_ENV_NAME"
        echo ""
        echo "2. Start VS Code tunnel:"
        echo "    ./code tunnel"
        echo ""
        echo "3. (Optional) Install Bloomberg API:"
        echo "    pip install blpapi --index-url https://blpapi.bloomberg.com/repository/releases/python/simple/"
        echo ""
        
        # Cleanup setup state file
        rm -f "$SETUP_STATE_FILE"
        
        # Ask if user wants to start VS Code tunnel now
        read -p "Would you like to start the VS Code tunnel now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Starting VS Code tunnel..."
            ./code tunnel
        fi
        ;;
        
    *)
        print_error "Unknown setup state. Resetting..."
        rm -f "$SETUP_STATE_FILE"
        exec "$0"
        ;;
esac