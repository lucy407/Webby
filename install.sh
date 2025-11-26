#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PATH="/usr/bin/webby"

echo ""
echo -e "\033[96m  Installing Webby...\033[0m"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo -e "  \033[93m⚠\033[0m  Requires sudo to install to $INSTALL_PATH"
    sudo cp "$SCRIPT_DIR/webby.py" "$INSTALL_PATH"
    sudo chmod +x "$INSTALL_PATH"
else
    cp "$SCRIPT_DIR/webby.py" "$INSTALL_PATH"
    chmod +x "$INSTALL_PATH"
fi

echo -e "  \033[92m✓\033[0m  Installed to $INSTALL_PATH"
echo ""
echo -e "  Run '\033[96mwebby\033[0m' from anywhere to create web apps!"
echo ""
