# Webby | A fast web app creator for linux
Supporting every linux distro & 57 browsers.

## Features
- Beautifully designed
- Uses your default terminal
- Auto-detects your browser
- Supports icons from URLs, files, or theme names
- Edit, rename, or delete existing web apps

## Installation
You must first begin by cloning the git repo.
```bash
git clone https://github.com/lucy407/webby.git
cd webby
chmod +x webby.py
```
Optionally, make it usable system-wide
```bash
sudo ln -s $(pwd)/webby.py /usr/local/bin/webby
```
## Usage
### Interactive mode
```bash
webby
```
### Command line mode
```bash
webby --help                         Show help
webby --list                         List all web apps
webby --edit <name>                  Edit a web app interactively
webby --edit <name> --url <url>      Change URL
webby --edit <name> --icon <icon>    Change icon  
webby --edit <name> --name <new>     Rename app
webby --delete <name>                Delete a web app
```
## Supported Browsers

Webby auto-detects and uses these browsers:

**App Mode (best experience):**
- Google Chrome, Chromium, Ungoogled Chromium
- Brave, Microsoft Edge, Vivaldi, Opera
- Thorium, Yandex, Sidekick, and more
- GNOME Web / Epiphany

**Browser Window:**
- Firefox, LibreWolf, Waterfox, Floorp
- Zen Browser, Mullvad Browser
- And many more...

## Icon Support

Icons can be specified as:
- **URL**: `https://example.com/icon.png`
- **File path**: `/path/to/icon.png` or `~/icon.png`

## Quick Tip!
For best icon quality, install ImageMagick!
