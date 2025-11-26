#!/bin/bash

# macOS installer for Webby
# Double-click this file to install, or run from Terminal

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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
    echo "  Please install Python from https://python.org"
    echo "  or via Homebrew: brew install python3"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Copy the script
cp "$SCRIPT_DIR/webby.py" "$INSTALL_DIR/webby"
chmod +x "$INSTALL_DIR/webby"

echo -e "  ${GREEN}✓${RESET}  Installed to $INSTALL_DIR/webby"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo -e "  ${YELLOW}⚠${RESET}  Adding $INSTALL_DIR to your PATH..."
    
    # Determine shell and config file
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        zsh)
            CONFIG_FILE="$HOME/.zshrc"
            ;;
        bash)
            if [[ -f "$HOME/.bash_profile" ]]; then
                CONFIG_FILE="$HOME/.bash_profile"
            else
                CONFIG_FILE="$HOME/.bashrc"
            fi
            ;;
        *)
            CONFIG_FILE="$HOME/.profile"
            ;;
    esac
    
    # Add to PATH if not already present
    if ! grep -q "$INSTALL_DIR" "$CONFIG_FILE" 2>/dev/null; then
        echo "" >> "$CONFIG_FILE"
        echo "# Added by Webby installer" >> "$CONFIG_FILE"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$CONFIG_FILE"
        echo -e "  ${GREEN}✓${RESET}  Added to $CONFIG_FILE"
        echo ""
        echo -e "  ${YELLOW}Note:${RESET} Run 'source $CONFIG_FILE' or restart terminal"
    fi
fi

echo ""
echo -e "  Run '${CYAN}webby${RESET}' from Terminal to create web apps!"
echo ""

# If running from Finder (double-click), keep window open
if [[ "$TERM_PROGRAM" != "Apple_Terminal" ]] && [[ "$TERM_PROGRAM" != "iTerm.app" ]] && [[ -z "$SSH_TTY" ]]; then
    read -p "  Press Enter to close..."
fi

