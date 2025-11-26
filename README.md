# Webby | A fast web app creator

Create web apps from any website on **Windows**, **macOS**, and **Linux**.
Supporting 57+ browsers with app mode support.

## Features
- Beautifully designed CLI interface
- Auto-detects your installed browsers
- Supports app mode (chromeless windows) on compatible browsers
-  Icons from URLs, local files, or system themes
-  Edit, rename, or delete existing web apps
-  Cross-platform: Windows, macOS, Linux

## Installation

### Linux
```bash
git clone https://github.com/lucy407/webby.git
cd webby
chmod +x install.sh
./install.sh
```

### macOS
```bash
git clone https://github.com/lucy407/webby.git
cd webby
chmod +x install.command
./install.command
```
Or double-click `install.command` in Finder.

### Windows
1. [Download](https://github.com/lucy407/webby/archive/refs/heads/main.zip) and extract the repository
2. Double-click `install.bat`
3. Restart your terminal

**Requirements:** Python 3.6+ ([download](https://python.org))

### Manual Installation (all platforms)
```bash
git clone https://github.com/lucy407/webby.git
cd webby
chmod +x webby.py  # Linux/macOS only

# Run directly
python3 webby.py   # Linux/macOS
python webby.py    # Windows

# Or create a symlink/alias
sudo ln -s $(pwd)/webby.py /usr/local/bin/webby  # Linux/macOS
```

## Usage

### Interactive mode
```bash
webby
```

### Command line mode
```bash
webby --help                         # Show help
webby --list                         # List all web apps
webby --edit <name>                  # Edit a web app interactively
webby --edit <name> --url <url>      # Change URL
webby --edit <name> --icon <icon>    # Change icon  
webby --edit <name> --name <new>     # Rename app
webby --delete <name>                # Delete a web app
```

## Supported Browsers

Webby auto-detects and uses these browsers:

### App Mode (best experience)
Browsers that support running as a standalone app window:
- Google Chrome, Chromium, Ungoogled Chromium
- Brave, Microsoft Edge, Vivaldi, Opera
- Arc (macOS), Thorium, Yandex, Sidekick
- GNOME Web / Epiphany (Linux)

### Browser Window
Opens as a regular browser window:
- Firefox, LibreWolf, Waterfox, Floorp
- Safari (macOS), Zen Browser, Mullvad Browser
- And many more...

## Where Apps Are Created

| Platform | Location |
|----------|----------|
| **Windows** | Start Menu → Webby folder |
| **macOS** | ~/Applications/Webby Apps |
| **Linux** | Your app launcher (via ~/.local/share/applications) |

## Icon Support

Icons can be specified as:
- **URL**: `https://example.com/icon.png`
- **File path**: `/path/to/icon.png` or `~/icon.png`
- **Theme name**: `firefox` (Linux only)

## Tips

- For best icon quality, install [ImageMagick](https://imagemagick.org):
  - Linux: `sudo apt install imagemagick` or `sudo dnf install ImageMagick`
  - macOS: `brew install imagemagick`
  - Windows: [Download installer](https://imagemagick.org/script/download.php)
  
- Chrome-based browsers provide the best "app mode" experience with a dedicated window

- On Windows, make sure Python is added to PATH during installation

## License
MIT
