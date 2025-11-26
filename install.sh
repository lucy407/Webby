#!/bin/bash

# Linux installer for Webby

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
CYAN='\033[96m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
RESET='\033[0m'

echo ""
echo -e "${CYAN}  Installing Webby...${RESET}"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "  ${RED}✗${RESET} Python 3 is not installed"
    echo ""
    echo "  Please install Python 3 using your package manager:"
    echo "    Ubuntu/Debian: sudo apt install python3"
    echo "    Fedora:        sudo dnf install python3"
    echo "    Arch:          sudo pacman -S python"
    echo ""
    exit 1
fi

# Try user-local install first, fall back to system install
USER_INSTALL_DIR="$HOME/.local/bin"
SYSTEM_INSTALL_PATH="/usr/local/bin/webby"

# Prefer user installation (no sudo needed)
if [[ -d "$USER_INSTALL_DIR" ]] || mkdir -p "$USER_INSTALL_DIR" 2>/dev/null; then
    INSTALL_PATH="$USER_INSTALL_DIR/webby"
    cp "$SCRIPT_DIR/webby.py" "$INSTALL_PATH"
    chmod +x "$INSTALL_PATH"
    
    echo -e "  ${GREEN}✓${RESET}  Installed to $INSTALL_PATH"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$USER_INSTALL_DIR:"* ]]; then
        echo ""
        echo -e "  ${YELLOW}⚠${RESET}  $USER_INSTALL_DIR is not in your PATH"
        echo ""
        echo "  Add this to your shell config (~/.bashrc or ~/.zshrc):"
        echo -e "    ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
    fi
else
    # Fall back to system-wide installation
    echo -e "  ${YELLOW}⚠${RESET}  Installing system-wide (requires sudo)"
    
    if [ "$EUID" -ne 0 ]; then
        sudo cp "$SCRIPT_DIR/webby.py" "$SYSTEM_INSTALL_PATH"
        sudo chmod +x "$SYSTEM_INSTALL_PATH"
    else
        cp "$SCRIPT_DIR/webby.py" "$SYSTEM_INSTALL_PATH"
        chmod +x "$SYSTEM_INSTALL_PATH"
    fi
    
    echo -e "  ${GREEN}✓${RESET}  Installed to $SYSTEM_INSTALL_PATH"
fi

echo ""
echo -e "  Run '${CYAN}webby${RESET}' from anywhere to create web apps!"
echo ""
