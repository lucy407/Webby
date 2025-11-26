#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import urllib.request
import hashlib
import argparse
import platform
import tempfile
from pathlib import Path

# Platform detection
PLATFORM = platform.system().lower()
IS_WINDOWS = PLATFORM == 'windows'
IS_MACOS = PLATFORM == 'darwin'
IS_LINUX = PLATFORM == 'linux'

class Colors:
    # Check if colors are supported
    if IS_WINDOWS:
        try:
            os.system('')  # Enable ANSI on Windows 10+
        except:
            pass
    
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def get_platform_name():
    if IS_WINDOWS:
        return "Windows"
    elif IS_MACOS:
        return "macOS"
    else:
        return "Linux"

ASCII_ART = f"""
{Colors.CYAN}{Colors.BOLD}
 ██╗    ██╗███████╗██████╗ ██████╗ ██╗   ██╗
 ██║    ██║██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝
 ██║ █╗ ██║█████╗  ██████╔╝██████╔╝ ╚████╔╝ 
 ██║███╗██║██╔══╝  ██╔══██╗██╔══██╗  ╚██╔╝  
 ╚███╔███╔╝███████╗██████╔╝██████╔╝   ██║   
  ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═════╝    ╚═╝   
{Colors.RESET}
{Colors.GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
{Colors.WHITE}  Web App Creator  {Colors.DIM}•{Colors.RESET}  {Colors.MAGENTA}v1.1{Colors.RESET}  {Colors.DIM}•{Colors.RESET}  {Colors.CYAN}{get_platform_name()}{Colors.RESET}
{Colors.GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
"""

# Browser configurations: (command/path, flag, app_mode_support, display_name)
BROWSERS_LINUX = [
    ('google-chrome', '--app=', True, 'Google Chrome'),
    ('google-chrome-stable', '--app=', True, 'Google Chrome'),
    ('google-chrome-beta', '--app=', True, 'Google Chrome Beta'),
    ('google-chrome-unstable', '--app=', True, 'Google Chrome Dev'),
    ('chromium', '--app=', True, 'Chromium'),
    ('chromium-browser', '--app=', True, 'Chromium'),
    ('chromium-freeworld', '--app=', True, 'Chromium'),
    ('ungoogled-chromium', '--app=', True, 'Ungoogled Chromium'),
    ('brave-browser', '--app=', True, 'Brave'),
    ('brave', '--app=', True, 'Brave'),
    ('brave-browser-stable', '--app=', True, 'Brave'),
    ('brave-browser-beta', '--app=', True, 'Brave Beta'),
    ('brave-browser-nightly', '--app=', True, 'Brave Nightly'),
    ('microsoft-edge', '--app=', True, 'Microsoft Edge'),
    ('microsoft-edge-stable', '--app=', True, 'Microsoft Edge'),
    ('microsoft-edge-beta', '--app=', True, 'Microsoft Edge Beta'),
    ('microsoft-edge-dev', '--app=', True, 'Microsoft Edge Dev'),
    ('vivaldi', '--app=', True, 'Vivaldi'),
    ('vivaldi-stable', '--app=', True, 'Vivaldi'),
    ('vivaldi-snapshot', '--app=', True, 'Vivaldi Snapshot'),
    ('opera', '--app=', True, 'Opera'),
    ('opera-stable', '--app=', True, 'Opera'),
    ('opera-beta', '--app=', True, 'Opera Beta'),
    ('opera-developer', '--app=', True, 'Opera Developer'),
    ('thorium-browser', '--app=', True, 'Thorium'),
    ('yandex-browser', '--app=', True, 'Yandex Browser'),
    ('yandex-browser-stable', '--app=', True, 'Yandex Browser'),
    ('sidekick', '--app=', True, 'Sidekick'),
    ('slimjet', '--app=', True, 'Slimjet'),
    ('iridium-browser', '--app=', True, 'Iridium'),
    ('iron-browser', '--app=', True, 'SRWare Iron'),
    ('epiphany', '--application-mode --profile=', True, 'GNOME Web'),
    ('gnome-web', '--application-mode --profile=', True, 'GNOME Web'),
    ('org.gnome.Epiphany', '--application-mode --profile=', True, 'GNOME Web'),
    ('firefox', '--new-window ', False, 'Firefox'),
    ('firefox-esr', '--new-window ', False, 'Firefox ESR'),
    ('firefox-developer-edition', '--new-window ', False, 'Firefox Developer'),
    ('firefox-nightly', '--new-window ', False, 'Firefox Nightly'),
    ('librewolf', '--new-window ', False, 'LibreWolf'),
    ('waterfox', '--new-window ', False, 'Waterfox'),
    ('waterfox-g', '--new-window ', False, 'Waterfox'),
    ('floorp', '--new-window ', False, 'Floorp'),
    ('zen-browser', '--new-window ', False, 'Zen Browser'),
    ('mullvad-browser', '--new-window ', False, 'Mullvad Browser'),
    ('firedragon', '--new-window ', False, 'FireDragon'),
    ('palemoon', '-new-window ', False, 'Pale Moon'),
    ('basilisk', '-new-window ', False, 'Basilisk'),
    ('falkon', '--new-window ', False, 'Falkon'),
    ('konqueror', '--new-tab ', False, 'Konqueror'),
    ('midori', '', False, 'Midori'),
    ('eolie', '', False, 'Eolie'),
    ('surf', '', False, 'surf'),
    ('qutebrowser', '', False, 'qutebrowser'),
    ('dillo', '', False, 'Dillo'),
    ('netsurf', '', False, 'NetSurf'),
    ('luakit', '', False, 'luakit'),
    ('nyxt', '', False, 'Nyxt'),
    ('min', '', False, 'Min Browser'),
]

# macOS browser paths (in /Applications or ~/Applications)
BROWSERS_MACOS = [
    ('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--app=', True, 'Google Chrome'),
    ('/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary', '--app=', True, 'Chrome Canary'),
    ('/Applications/Chromium.app/Contents/MacOS/Chromium', '--app=', True, 'Chromium'),
    ('/Applications/Brave Browser.app/Contents/MacOS/Brave Browser', '--app=', True, 'Brave'),
    ('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', '--app=', True, 'Microsoft Edge'),
    ('/Applications/Vivaldi.app/Contents/MacOS/Vivaldi', '--app=', True, 'Vivaldi'),
    ('/Applications/Opera.app/Contents/MacOS/Opera', '--app=', True, 'Opera'),
    ('/Applications/Arc.app/Contents/MacOS/Arc', '--app=', True, 'Arc'),
    ('/Applications/Orion.app/Contents/MacOS/Orion', '--new-window ', False, 'Orion'),
    ('/Applications/Firefox.app/Contents/MacOS/firefox', '--new-window ', False, 'Firefox'),
    ('/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox', '--new-window ', False, 'Firefox Developer'),
    ('/Applications/Firefox Nightly.app/Contents/MacOS/firefox', '--new-window ', False, 'Firefox Nightly'),
    ('/Applications/LibreWolf.app/Contents/MacOS/librewolf', '--new-window ', False, 'LibreWolf'),
    ('/Applications/Waterfox.app/Contents/MacOS/waterfox', '--new-window ', False, 'Waterfox'),
    ('/Applications/Zen Browser.app/Contents/MacOS/zen', '--new-window ', False, 'Zen Browser'),
    ('/Applications/Safari.app/Contents/MacOS/Safari', '', False, 'Safari'),
]

# Windows browser paths
BROWSERS_WINDOWS = [
    # Chrome variants
    (r'C:\Program Files\Google\Chrome\Application\chrome.exe', '--app=', True, 'Google Chrome'),
    (r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', '--app=', True, 'Google Chrome'),
    (r'{LOCALAPPDATA}\Google\Chrome\Application\chrome.exe', '--app=', True, 'Google Chrome'),
    (r'C:\Program Files\Google\Chrome Beta\Application\chrome.exe', '--app=', True, 'Chrome Beta'),
    (r'C:\Program Files\Google\Chrome SxS\Application\chrome.exe', '--app=', True, 'Chrome Canary'),
    # Chromium
    (r'C:\Program Files\Chromium\Application\chrome.exe', '--app=', True, 'Chromium'),
    (r'{LOCALAPPDATA}\Chromium\Application\chrome.exe', '--app=', True, 'Chromium'),
    # Brave
    (r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe', '--app=', True, 'Brave'),
    (r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe', '--app=', True, 'Brave'),
    (r'{LOCALAPPDATA}\BraveSoftware\Brave-Browser\Application\brave.exe', '--app=', True, 'Brave'),
    # Edge
    (r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--app=', True, 'Microsoft Edge'),
    (r'C:\Program Files\Microsoft\Edge\Application\msedge.exe', '--app=', True, 'Microsoft Edge'),
    # Vivaldi
    (r'C:\Program Files\Vivaldi\Application\vivaldi.exe', '--app=', True, 'Vivaldi'),
    (r'{LOCALAPPDATA}\Vivaldi\Application\vivaldi.exe', '--app=', True, 'Vivaldi'),
    # Opera
    (r'C:\Program Files\Opera\launcher.exe', '--app=', True, 'Opera'),
    (r'{LOCALAPPDATA}\Programs\Opera\launcher.exe', '--app=', True, 'Opera'),
    # Firefox variants
    (r'C:\Program Files\Mozilla Firefox\firefox.exe', '-new-window ', False, 'Firefox'),
    (r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe', '-new-window ', False, 'Firefox'),
    (r'C:\Program Files\Firefox Developer Edition\firefox.exe', '-new-window ', False, 'Firefox Developer'),
    (r'C:\Program Files\Firefox Nightly\firefox.exe', '-new-window ', False, 'Firefox Nightly'),
    (r'C:\Program Files\LibreWolf\librewolf.exe', '-new-window ', False, 'LibreWolf'),
    (r'C:\Program Files\Waterfox\waterfox.exe', '-new-window ', False, 'Waterfox'),
    (r'C:\Program Files\Zen Browser\zen.exe', '-new-window ', False, 'Zen Browser'),
]

ICON_SIZES = [512, 256, 128, 96, 64, 48, 32, 24, 16]

def expand_windows_path(path):
    """Expand Windows environment variables in path."""
    if not IS_WINDOWS:
        return path
    path = path.replace('{LOCALAPPDATA}', os.environ.get('LOCALAPPDATA', ''))
    path = path.replace('{APPDATA}', os.environ.get('APPDATA', ''))
    path = path.replace('{PROGRAMFILES}', os.environ.get('PROGRAMFILES', r'C:\Program Files'))
    path = path.replace('{PROGRAMFILES(X86)}', os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)'))
    return path

def clear_screen():
    if IS_WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def print_header():
    clear_screen()
    print(ASCII_ART)

def styled_input(prompt, color=Colors.CYAN):
    print(f"\n{Colors.GRAY}┌{'─' * 46}┐{Colors.RESET}")
    print(f"{Colors.GRAY}│{Colors.RESET} {color}{Colors.BOLD}{prompt}{Colors.RESET}")
    print(f"{Colors.GRAY}└{'─' * 46}┘{Colors.RESET}")
    return input(f"  {Colors.WHITE}▸ {Colors.RESET}").strip()

def print_success(message):
    print(f"\n  {Colors.GREEN}✓{Colors.RESET} {message}")

def print_error(message):
    print(f"\n  {Colors.RED}✗{Colors.RESET} {message}")

def print_info(message):
    print(f"\n  {Colors.BLUE}ℹ{Colors.RESET} {message}")

def get_applications_dir():
    """Get the applications directory for the current platform."""
    if IS_WINDOWS:
        # Windows Start Menu programs folder
        start_menu = Path(os.environ.get('APPDATA', '')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Webby'
        start_menu.mkdir(parents=True, exist_ok=True)
        return start_menu
    elif IS_MACOS:
        # macOS Applications folder (user-specific)
        apps_dir = Path.home() / 'Applications' / 'Webby Apps'
        apps_dir.mkdir(parents=True, exist_ok=True)
        return apps_dir
    else:
        # Linux ~/.local/share/applications
        return Path.home() / '.local' / 'share' / 'applications'

def get_webby_apps():
    """Get all Webby-created apps for the current platform."""
    apps = {}
    
    if IS_WINDOWS:
        apps_dir = get_applications_dir()
        for shortcut_file in apps_dir.glob('*.lnk'):
            try:
                name = shortcut_file.stem
                # For Windows, we store metadata in a companion .webby file
                meta_file = shortcut_file.with_suffix('.webby')
                url = ''
                icon = ''
                if meta_file.exists():
                    for line in meta_file.read_text().split('\n'):
                        if line.startswith('URL='):
                            url = line[4:]
                        elif line.startswith('Icon='):
                            icon = line[5:]
                apps[name.lower()] = {
                    'name': name,
                    'url': url,
                    'icon': icon,
                    'file': shortcut_file
                }
            except Exception:
                pass
    elif IS_MACOS:
        apps_dir = get_applications_dir()
        for app_bundle in apps_dir.glob('*.app'):
            try:
                name = app_bundle.stem
                plist_file = app_bundle / 'Contents' / 'Info.plist'
                url = ''
                icon = ''
                # Read URL from the shell script
                script_file = app_bundle / 'Contents' / 'MacOS' / name
                if script_file.exists():
                    content = script_file.read_text()
                    for line in content.split('\n'):
                        if 'http' in line:
                            import re
                            urls = re.findall(r'https?://[^\s"\']+', line)
                            if urls:
                                url = urls[0]
                                break
                apps[name.lower()] = {
                    'name': name,
                    'url': url,
                    'icon': icon,
                    'file': app_bundle
                }
            except Exception:
                pass
    else:
        # Linux
        apps_dir = get_applications_dir()
        for desktop_file in apps_dir.glob('webby-*.desktop'):
            try:
                content = desktop_file.read_text()
                name = None
                url = None
                icon = None
                for line in content.split('\n'):
                    if line.startswith('Name='):
                        name = line[5:]
                    elif line.startswith('Exec='):
                        exec_line = line[5:]
                        if '"http' in exec_line:
                            url = exec_line.split('"')[1]
                        elif 'http' in exec_line:
                            for part in exec_line.split():
                                if part.startswith('http'):
                                    url = part
                                    break
                    elif line.startswith('Icon='):
                        icon = line[5:]
                if name:
                    apps[name.lower()] = {
                        'name': name,
                        'url': url or '',
                        'icon': icon or '',
                        'file': desktop_file
                    }
            except Exception:
                pass
    return apps

def find_app_by_name(search_name):
    apps = get_webby_apps()
    search_lower = search_name.lower()
    
    if search_lower in apps:
        return apps[search_lower]
    
    for key, app in apps.items():
        if search_lower in key or search_lower in app['name'].lower():
            return app
    
    return None

def detect_all_browsers():
    """Detect all available browsers on the current platform."""
    available = []
    seen_names = set()
    
    if IS_WINDOWS:
        browsers = BROWSERS_WINDOWS
        for path_template, flag, app_mode, name in browsers:
            path = expand_windows_path(path_template)
            if os.path.isfile(path) and name not in seen_names:
                available.append((path, flag, app_mode, name))
                seen_names.add(name)
    elif IS_MACOS:
        browsers = BROWSERS_MACOS
        for path, flag, app_mode, name in browsers:
            # Also check user Applications folder
            user_path = path.replace('/Applications/', str(Path.home() / 'Applications') + '/')
            if os.path.isfile(path) and name not in seen_names:
                available.append((path, flag, app_mode, name))
                seen_names.add(name)
            elif os.path.isfile(user_path) and name not in seen_names:
                available.append((user_path, flag, app_mode, name))
                seen_names.add(name)
    else:
        # Linux
        browsers = BROWSERS_LINUX
        for cmd, flag, app_mode, name in browsers:
            if shutil.which(cmd) and name not in seen_names:
                available.append((cmd, flag, app_mode, name))
                seen_names.add(name)
    
    return available

def detect_browser():
    browsers = detect_all_browsers()
    if browsers:
        return browsers[0]
    return None, None, False, None

def validate_url(url):
    if not url:
        return False
    if not url.startswith(('http://', 'https://')):
        return False
    return True

def sanitize_name(name):
    safe = ''.join(c if c.isalnum() or c in ' -_' else '' for c in name)
    return safe.lower().replace(' ', '-')

def get_icons_dir():
    if IS_WINDOWS:
        icons_dir = Path(os.environ.get('LOCALAPPDATA', '')) / 'Webby' / 'icons'
    elif IS_MACOS:
        icons_dir = Path.home() / 'Library' / 'Application Support' / 'Webby' / 'icons'
    else:
        icons_dir = Path.home() / '.local' / 'share' / 'webby' / 'icons'
    icons_dir.mkdir(parents=True, exist_ok=True)
    return icons_dir

def get_hicolor_dir(size):
    """Get hicolor icon directory (Linux only)."""
    icons_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor' / f'{size}x{size}' / 'apps'
    icons_dir.mkdir(parents=True, exist_ok=True)
    return icons_dir

def get_epiphany_profile_dir(app_name):
    """Get GNOME Web profile directory (Linux only)."""
    profile_dir = Path.home() / '.local' / 'share' / 'webby' / 'epiphany-profiles' / sanitize_name(app_name)
    profile_dir.mkdir(parents=True, exist_ok=True)
    return profile_dir

def install_icon_to_theme(source_path, icon_name):
    """Install icon to appropriate location for the platform."""
    source = Path(source_path)
    if not source.exists():
        return icon_name
    
    icons_dir = get_icons_dir()
    ext = source.suffix.lower()
    
    if IS_WINDOWS or IS_MACOS:
        # For Windows/macOS, just copy to icons directory
        dest = icons_dir / f'{icon_name}{ext}'
        shutil.copy2(source, dest)
        
        # On Windows, try to convert to .ico if possible
        if IS_WINDOWS and ext != '.ico':
            try:
                if shutil.which('magick') or shutil.which('convert'):
                    convert_cmd = 'magick' if shutil.which('magick') else 'convert'
                    ico_dest = icons_dir / f'{icon_name}.ico'
                    subprocess.run(
                        [convert_cmd, str(source), '-resize', '256x256', str(ico_dest)],
                        capture_output=True
                    )
                    return str(ico_dest)
            except Exception:
                pass
        
        return str(dest)
    
    # Linux: install to hicolor theme
    if ext == '.svg':
        scalable_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor' / 'scalable' / 'apps'
        scalable_dir.mkdir(parents=True, exist_ok=True)
        dest = scalable_dir / f'webby-{icon_name}.svg'
        shutil.copy2(source, dest)
        update_icon_cache()
        return f'webby-{icon_name}'
    
    has_magick = shutil.which('magick') or shutil.which('convert')
    
    if has_magick:
        convert_cmd = 'magick' if shutil.which('magick') else 'convert'
        for size in ICON_SIZES:
            size_dir = get_hicolor_dir(size)
            dest = size_dir / f'webby-{icon_name}.png'
            try:
                subprocess.run(
                    [convert_cmd, str(source), '-resize', f'{size}x{size}', '-background', 'none', '-gravity', 'center', '-extent', f'{size}x{size}', str(dest)],
                    capture_output=True,
                    check=True
                )
            except Exception:
                pass
    else:
        for size in [256, 128, 64, 48]:
            size_dir = get_hicolor_dir(size)
            dest = size_dir / f'webby-{icon_name}.png'
            shutil.copy2(source, dest)
    
    update_icon_cache()
    return f'webby-{icon_name}'

def remove_icon_from_theme(icon_name):
    """Remove icon from theme (mainly for Linux)."""
    if IS_LINUX:
        if not icon_name.startswith('webby-'):
            return
        
        hicolor_base = Path.home() / '.local' / 'share' / 'icons' / 'hicolor'
        
        for size in ICON_SIZES:
            icon_file = hicolor_base / f'{size}x{size}' / 'apps' / f'{icon_name}.png'
            icon_file.unlink(missing_ok=True)
        
        scalable_file = hicolor_base / 'scalable' / 'apps' / f'{icon_name}.svg'
        scalable_file.unlink(missing_ok=True)
        
        update_icon_cache()
    else:
        # Windows/macOS: remove from icons directory
        icons_dir = get_icons_dir()
        for ext in ['.png', '.ico', '.icns', '.jpg', '.svg']:
            icon_file = icons_dir / f'{icon_name}{ext}'
            icon_file.unlink(missing_ok=True)

def download_icon(url, app_name):
    icons_dir = get_icons_dir()
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    safe_name = sanitize_name(app_name)
    
    ext = '.png'
    url_lower = url.lower()
    if '.svg' in url_lower:
        ext = '.svg'
    elif '.jpg' in url_lower or '.jpeg' in url_lower:
        ext = '.jpg'
    elif '.ico' in url_lower:
        ext = '.ico'
    elif '.webp' in url_lower:
        ext = '.webp'
    elif '.gif' in url_lower:
        ext = '.gif'
    
    temp_path = icons_dir / f"{safe_name}-{url_hash}-temp{ext}"
    
    try:
        print(f"  {Colors.GRAY}Downloading icon...{Colors.RESET}", end='', flush=True)
        
        request = urllib.request.Request(
            url,
            headers={'User-Agent': f'Mozilla/5.0 ({get_platform_name()}) Webby/1.1'}
        )
        
        with urllib.request.urlopen(request, timeout=15) as response:
            temp_path.write_bytes(response.read())
        
        print(f"\r  {Colors.GREEN}✓{Colors.RESET} Icon downloaded       ")
        
        icon_name = install_icon_to_theme(temp_path, safe_name)
        
        temp_path.unlink(missing_ok=True)
        
        return icon_name
        
    except Exception as e:
        print(f"\r  {Colors.YELLOW}⚠{Colors.RESET} Could not download icon: {e}")
        return get_default_icon()

def get_default_icon():
    """Get the default icon for the platform."""
    if IS_WINDOWS:
        return ''  # Windows will use default
    elif IS_MACOS:
        return 'AppIcon'
    else:
        return 'web-browser'

def find_icon(icon_input, app_name):
    if not icon_input:
        return get_default_icon()
    
    if icon_input.startswith(('http://', 'https://')):
        return download_icon(icon_input, app_name)
    
    if os.path.isabs(icon_input) and os.path.exists(icon_input):
        safe_name = sanitize_name(app_name)
        return install_icon_to_theme(icon_input, safe_name)
    
    expanded = os.path.expanduser(icon_input)
    if os.path.exists(expanded):
        safe_name = sanitize_name(app_name)
        return install_icon_to_theme(os.path.abspath(expanded), safe_name)
    
    return icon_input

def create_windows_shortcut(name, url, icon, browser, browser_flag, has_app_mode, browser_name):
    """Create a Windows shortcut (.lnk file)."""
    apps_dir = get_applications_dir()
    safe_name = sanitize_name(name)
    shortcut_file = apps_dir / f"{name}.lnk"
    meta_file = apps_dir / f"{name}.webby"
    
    # Build the command
    if has_app_mode:
        target_args = f'{browser_flag}"{url}"'
    else:
        target_args = f'{browser_flag}"{url}"'
    
    # Try using PowerShell to create the shortcut
    ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_file}")
$Shortcut.TargetPath = "{browser}"
$Shortcut.Arguments = '{target_args}'
$Shortcut.WorkingDirectory = "{os.path.dirname(browser)}"
'''
    
    if icon and os.path.exists(icon):
        ps_script += f'$Shortcut.IconLocation = "{icon}"\n'
    
    ps_script += '$Shortcut.Save()\n'
    
    try:
        subprocess.run(['powershell', '-Command', ps_script], capture_output=True, check=True)
    except Exception as e:
        # Fallback: create a .url file instead
        url_file = apps_dir / f"{name}.url"
        url_content = f"""[InternetShortcut]
URL={url}
"""
        if icon:
            url_content += f"IconFile={icon}\nIconIndex=0\n"
        url_file.write_text(url_content)
        shortcut_file = url_file
    
    # Save metadata
    meta_file.write_text(f"URL={url}\nIcon={icon}\nBrowser={browser_name}\n")
    
    return shortcut_file

def create_macos_app(name, url, icon, browser, browser_flag, has_app_mode, browser_name):
    """Create a macOS .app bundle."""
    apps_dir = get_applications_dir()
    safe_name = sanitize_name(name)
    app_bundle = apps_dir / f"{name}.app"
    
    # Create app bundle structure
    contents_dir = app_bundle / 'Contents'
    macos_dir = contents_dir / 'MacOS'
    resources_dir = contents_dir / 'Resources'
    
    # Remove existing app if present
    if app_bundle.exists():
        shutil.rmtree(app_bundle)
    
    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the executable script
    if has_app_mode:
        exec_command = f'"{browser}" {browser_flag}"{url}"'
    else:
        exec_command = f'"{browser}" {browser_flag}"{url}"'
    
    script_content = f'''#!/bin/bash
exec {exec_command}
'''
    
    script_file = macos_dir / name
    script_file.write_text(script_content)
    script_file.chmod(0o755)
    
    # Create Info.plist
    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{name}</string>
    <key>CFBundleDisplayName</key>
    <string>{name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.webby.{safe_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>{name}</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
'''
    
    plist_file = contents_dir / 'Info.plist'
    plist_file.write_text(plist_content)
    
    # Copy icon if available
    if icon and os.path.exists(icon):
        icon_path = Path(icon)
        if icon_path.suffix.lower() == '.icns':
            shutil.copy2(icon, resources_dir / 'AppIcon.icns')
        else:
            # Try to convert to icns using sips
            try:
                dest_icns = resources_dir / 'AppIcon.icns'
                subprocess.run(['sips', '-s', 'format', 'icns', str(icon), '--out', str(dest_icns)], capture_output=True)
            except Exception:
                # Just copy as-is
                shutil.copy2(icon, resources_dir / f'AppIcon{icon_path.suffix}')
    
    return app_bundle

def create_linux_desktop_file(name, url, icon, browser, browser_flag, has_app_mode, browser_name):
    """Create a Linux .desktop file."""
    applications_dir = get_applications_dir()
    applications_dir.mkdir(parents=True, exist_ok=True)
    
    safe_name = sanitize_name(name)
    desktop_file = applications_dir / f"webby-{safe_name}.desktop"
    
    if 'epiphany' in browser.lower() or 'gnome-web' in browser.lower():
        profile_dir = get_epiphany_profile_dir(name)
        exec_command = f'{browser} --application-mode --profile="{profile_dir}" "{url}"'
    else:
        exec_command = f'{browser} {browser_flag}"{url}"'
    
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={name}
Comment=Web app created with Webby
Exec={exec_command}
Icon={icon}
Terminal=false
Categories=Network;WebBrowser;
StartupWMClass={safe_name}
StartupNotify=true
Keywords=web;app;{safe_name};
"""
    
    desktop_file.write_text(desktop_content)
    desktop_file.chmod(0o755)
    
    return desktop_file

def create_desktop_file(name, url, icon, browser, browser_flag, has_app_mode, browser_name):
    """Create a desktop entry/shortcut for the current platform."""
    if IS_WINDOWS:
        return create_windows_shortcut(name, url, icon, browser, browser_flag, has_app_mode, browser_name)
    elif IS_MACOS:
        return create_macos_app(name, url, icon, browser, browser_flag, has_app_mode, browser_name)
    else:
        return create_linux_desktop_file(name, url, icon, browser, browser_flag, has_app_mode, browser_name)

def delete_app(app):
    """Delete a web app."""
    if IS_MACOS and app['file'].is_dir():
        shutil.rmtree(app['file'])
    else:
        app['file'].unlink(missing_ok=True)
    
    # Also remove companion files on Windows
    if IS_WINDOWS:
        meta_file = app['file'].with_suffix('.webby')
        meta_file.unlink(missing_ok=True)
    
    if IS_LINUX and app.get('icon', '').startswith('webby-'):
        remove_icon_from_theme(app['icon'])
    
    update_desktop_database()
    print_success(f"Deleted '{app['name']}'")

def update_icon_cache():
    """Update icon cache (Linux only)."""
    if not IS_LINUX:
        return
    
    icon_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor'
    if shutil.which('gtk-update-icon-cache'):
        try:
            subprocess.run(['gtk-update-icon-cache', '-f', '-t', str(icon_dir)], capture_output=True)
        except Exception:
            pass
    if shutil.which('xdg-icon-resource'):
        try:
            subprocess.run(['xdg-icon-resource', 'forceupdate'], capture_output=True)
        except Exception:
            pass

def update_desktop_database():
    """Update desktop database (Linux only)."""
    if not IS_LINUX:
        return
    
    if shutil.which('update-desktop-database'):
        try:
            subprocess.run(
                ['update-desktop-database', str(get_applications_dir())],
                capture_output=True
            )
        except Exception:
            pass

def show_browser_selection(browsers):
    print(f"\n{Colors.GRAY}┌{'─' * 46}┐{Colors.RESET}")
    print(f"{Colors.GRAY}│{Colors.RESET} {Colors.YELLOW}{Colors.BOLD}Select Browser{Colors.RESET}")
    print(f"{Colors.GRAY}├{'─' * 46}┤{Colors.RESET}")
    
    for i, (cmd, flag, app_mode, name) in enumerate(browsers, 1):
        mode_badge = f"{Colors.GREEN}●{Colors.RESET}" if app_mode else f"{Colors.YELLOW}○{Colors.RESET}"
        print(f"{Colors.GRAY}│{Colors.RESET}  {Colors.CYAN}{i:2}{Colors.RESET}. {mode_badge} {name}")
    
    print(f"{Colors.GRAY}├{'─' * 46}┤{Colors.RESET}")
    print(f"{Colors.GRAY}│{Colors.RESET}  {Colors.GREEN}●{Colors.RESET} = App Mode  {Colors.YELLOW}○{Colors.RESET} = Browser Window")
    print(f"{Colors.GRAY}└{'─' * 46}┘{Colors.RESET}")
    
    while True:
        try:
            choice = input(f"  {Colors.WHITE}▸ {Colors.RESET}").strip()
            if not choice:
                return browsers[0]
            idx = int(choice) - 1
            if 0 <= idx < len(browsers):
                return browsers[idx]
            print(f"  {Colors.RED}Invalid choice{Colors.RESET}")
        except ValueError:
            print(f"  {Colors.RED}Enter a number{Colors.RESET}")

def handle_existing_app(app):
    print(f"\n{Colors.YELLOW}{Colors.BOLD}  ⚠ Web app '{app['name']}' already exists!{Colors.RESET}")
    print(f"\n{Colors.GRAY}  ┌{'─' * 44}┐{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}URL:{Colors.RESET}  {Colors.BLUE}{app['url'][:38]}{'...' if len(app['url']) > 38 else ''}{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Icon:{Colors.RESET} {Colors.GREEN}{str(app['icon'])[:38]}{'...' if len(str(app['icon'])) > 38 else ''}{Colors.RESET}")
    print(f"{Colors.GRAY}  └{'─' * 44}┘{Colors.RESET}")
    
    print(f"\n  {Colors.CYAN}1{Colors.RESET}. Edit this web app")
    print(f"  {Colors.CYAN}2{Colors.RESET}. Delete this web app")
    print(f"  {Colors.CYAN}3{Colors.RESET}. Create with different name")
    print(f"  {Colors.CYAN}4{Colors.RESET}. Cancel")
    
    choice = input(f"\n  {Colors.WHITE}▸ {Colors.RESET}").strip()
    
    if choice == '1':
        return 'edit'
    elif choice == '2':
        return 'delete'
    elif choice == '3':
        return 'rename'
    else:
        return 'cancel'

def cmd_list():
    print_header()
    apps = get_webby_apps()
    
    if not apps:
        print_info("No web apps found")
        return
    
    print_info(f"Found {Colors.CYAN}{len(apps)}{Colors.RESET} web app(s)")
    print(f"\n{Colors.GRAY}  ┌{'─' * 50}┐{Colors.RESET}")
    
    for app in apps.values():
        print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.CYAN}{app['name']:<20}{Colors.RESET} {Colors.BLUE}{app['url'][:25]}{'...' if len(app['url']) > 25 else ''}{Colors.RESET}")
    
    print(f"{Colors.GRAY}  └{'─' * 50}┘{Colors.RESET}\n")

def cmd_delete(name):
    print_header()
    app = find_app_by_name(name)
    
    if not app:
        print_error(f"Web app '{name}' not found")
        return
    
    print(f"\n  Delete '{Colors.CYAN}{app['name']}{Colors.RESET}'?")
    print(f"  {Colors.DIM}Type 'yes' to confirm{Colors.RESET}")
    
    confirm = input(f"\n  {Colors.WHITE}▸ {Colors.RESET}").strip().lower()
    
    if confirm == 'yes' or confirm == 'y':
        delete_app(app)
    else:
        print_info("Cancelled")

def cmd_edit(name, new_name=None, new_url=None, new_icon=None):
    print_header()
    app = find_app_by_name(name)
    
    if not app:
        print_error(f"Web app '{name}' not found")
        return
    
    print_info(f"Editing '{Colors.CYAN}{app['name']}{Colors.RESET}'")
    
    browser, browser_flag, has_app_mode, browser_name = detect_browser()
    if not browser:
        print_error("No compatible browser found!")
        return
    
    final_name = new_name if new_name else app['name']
    final_url = new_url if new_url else app['url']
    final_icon = app['icon']
    
    if new_icon:
        final_icon = find_icon(new_icon, final_name)
    
    if not final_url.startswith(('http://', 'https://')):
        final_url = 'https://' + final_url
    
    if new_name and new_name.lower() != app['name'].lower():
        delete_app(app)
    else:
        if IS_MACOS and app['file'].is_dir():
            shutil.rmtree(app['file'])
        else:
            app['file'].unlink(missing_ok=True)
    
    desktop_file = create_desktop_file(final_name, final_url, final_icon, browser, browser_flag, has_app_mode, browser_name)
    update_desktop_database()
    
    print_success(f"Updated '{final_name}'")
    print(f"\n{Colors.GRAY}  ┌{'─' * 44}┐{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Name:{Colors.RESET}  {Colors.CYAN}{final_name}{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}URL:{Colors.RESET}   {Colors.BLUE}{final_url[:38]}{'...' if len(final_url) > 38 else ''}{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Icon:{Colors.RESET}  {Colors.GREEN}{str(final_icon)[:38]}{'...' if len(str(final_icon)) > 38 else ''}{Colors.RESET}")
    print(f"{Colors.GRAY}  └{'─' * 44}┘{Colors.RESET}\n")

def interactive_mode():
    print_header()
    
    available_browsers = detect_all_browsers()
    
    if not available_browsers:
        print_error("No compatible browser found!")
        if IS_WINDOWS:
            print_info("Please install a web browser (Chrome, Edge, Firefox, Brave, etc.)")
        elif IS_MACOS:
            print_info("Please install a web browser (Chrome, Safari, Firefox, Brave, etc.)")
        else:
            print_info("Please install a web browser (Chrome, Firefox, Brave, etc.)")
        sys.exit(1)
    
    if len(available_browsers) == 1:
        browser, browser_flag, has_app_mode, browser_name = available_browsers[0]
        if has_app_mode:
            print_info(f"Using {Colors.CYAN}{browser_name}{Colors.RESET} {Colors.GREEN}(app mode){Colors.RESET}")
        else:
            print_info(f"Using {Colors.CYAN}{browser_name}{Colors.RESET} {Colors.DIM}(browser window){Colors.RESET}")
    else:
        best = available_browsers[0]
        browser, browser_flag, has_app_mode, browser_name = best
        
        app_mode_browsers = [b for b in available_browsers if b[2]]
        window_browsers = [b for b in available_browsers if not b[2]]
        
        print_info(f"Found {Colors.CYAN}{len(available_browsers)}{Colors.RESET} browsers ({Colors.GREEN}{len(app_mode_browsers)} app mode{Colors.RESET}, {Colors.YELLOW}{len(window_browsers)} window{Colors.RESET})")
        
        if has_app_mode:
            print(f"  {Colors.GRAY}Using:{Colors.RESET} {Colors.CYAN}{browser_name}{Colors.RESET} {Colors.GREEN}(app mode){Colors.RESET}")
        else:
            print(f"  {Colors.GRAY}Using:{Colors.RESET} {Colors.CYAN}{browser_name}{Colors.RESET}")
        
        print(f"  {Colors.DIM}Press Enter to continue, or type 'select' to choose{Colors.RESET}")
        choice = input(f"  {Colors.WHITE}▸ {Colors.RESET}").strip().lower()
        
        if choice == 'select' or choice == 's':
            browser, browser_flag, has_app_mode, browser_name = show_browser_selection(available_browsers)
            print(f"\n  {Colors.GREEN}✓{Colors.RESET} Selected {Colors.CYAN}{browser_name}{Colors.RESET}")
    
    name = styled_input("App Name", Colors.MAGENTA)
    if not name:
        print_error("App name is required!")
        sys.exit(1)
    
    existing_app = find_app_by_name(name)
    if existing_app:
        action = handle_existing_app(existing_app)
        
        if action == 'cancel':
            print_info("Cancelled")
            sys.exit(0)
        elif action == 'delete':
            delete_app(existing_app)
            sys.exit(0)
        elif action == 'edit':
            url = styled_input(f"Website URL [{existing_app['url']}]", Colors.BLUE)
            url = url if url else existing_app['url']
            
            print(f"\n{Colors.GRAY}  {Colors.DIM}Icon: theme name, file path, or image URL{Colors.RESET}")
            icon_input = styled_input(f"Icon [{existing_app['icon']}]", Colors.GREEN)
            icon = find_icon(icon_input, name) if icon_input else existing_app['icon']
            
            if IS_MACOS and existing_app['file'].is_dir():
                shutil.rmtree(existing_app['file'])
            else:
                existing_app['file'].unlink(missing_ok=True)
        elif action == 'rename':
            name = styled_input("New App Name", Colors.MAGENTA)
            if not name:
                print_error("App name is required!")
                sys.exit(1)
            
            url = styled_input("Website URL", Colors.BLUE)
            print(f"\n{Colors.GRAY}  {Colors.DIM}Icon: theme name, file path, or image URL{Colors.RESET}")
            icon_input = styled_input("Icon (optional)", Colors.GREEN)
            icon = find_icon(icon_input, name)
    else:
        url = styled_input("Website URL", Colors.BLUE)
        print(f"\n{Colors.GRAY}  {Colors.DIM}Icon: theme name, file path, or image URL{Colors.RESET}")
        icon_input = styled_input("Icon (optional)", Colors.GREEN)
        icon = find_icon(icon_input, name)
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if not validate_url(url):
        print_error("Invalid URL format!")
        sys.exit(1)
    
    print(f"\n{Colors.GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    try:
        desktop_file = create_desktop_file(name, url, icon, browser, browser_flag, has_app_mode, browser_name)
        update_desktop_database()
        
        mode_text = f"{Colors.GREEN}App Mode{Colors.RESET}" if has_app_mode else f"{Colors.YELLOW}Browser Window{Colors.RESET}"
        
        # Platform-specific location hint
        if IS_WINDOWS:
            location_hint = "Find it in your Start Menu under 'Webby'!"
        elif IS_MACOS:
            location_hint = f"Find it in ~/Applications/Webby Apps!"
        else:
            location_hint = f'Find "{name}" in your app launcher!'
        
        print(f"""
{Colors.GREEN}{Colors.BOLD}  ✨ Web App Created Successfully!{Colors.RESET}

{Colors.GRAY}  ┌{'─' * 44}┐{Colors.RESET}
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Name:{Colors.RESET}     {Colors.CYAN}{name}{Colors.RESET}
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}URL:{Colors.RESET}      {Colors.BLUE}{url[:35]}{'...' if len(url) > 35 else ''}{Colors.RESET}
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Browser:{Colors.RESET}  {Colors.CYAN}{browser_name}{Colors.RESET} ({mode_text})
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Icon:{Colors.RESET}     {Colors.GREEN}{str(icon)[:35]}{'...' if len(str(icon)) > 35 else ''}{Colors.RESET}
{Colors.GRAY}  └{'─' * 44}┘{Colors.RESET}

{Colors.GRAY}  {location_hint}{Colors.RESET}
""")
        
    except Exception as e:
        print_error(f"Failed to create web app: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description=f'Webby - Web App Creator for {get_platform_name()}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.CYAN}Examples:{Colors.RESET}
  webby                              Interactive mode
  webby --list                       List all web apps
  webby --edit youtube               Edit YouTube web app interactively
  webby --edit youtube --url new.com Change URL
  webby --edit youtube --icon /path  Change icon
  webby --edit youtube --name "YT"   Rename app
  webby --delete youtube             Delete web app
"""
    )
    
    parser.add_argument('--list', '-l', action='store_true', help='List all web apps')
    parser.add_argument('--edit', '-e', metavar='NAME', help='Edit an existing web app')
    parser.add_argument('--delete', '-d', metavar='NAME', help='Delete a web app')
    parser.add_argument('--name', '-n', metavar='NAME', help='New name (with --edit)')
    parser.add_argument('--url', '-u', metavar='URL', help='New URL (with --edit)')
    parser.add_argument('--icon', '-i', metavar='ICON', help='New icon (with --edit)')
    
    args = parser.parse_args()
    
    if args.list:
        cmd_list()
    elif args.delete:
        cmd_delete(args.delete)
    elif args.edit:
        cmd_edit(args.edit, args.name, args.url, args.icon)
    else:
        interactive_mode()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GRAY}  Cancelled by user.{Colors.RESET}\n")
        sys.exit(0)
