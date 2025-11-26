#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import urllib.request
import hashlib
import argparse
import glob
from pathlib import Path

class Colors:
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
{Colors.WHITE}  Web App Creator for Linux  {Colors.DIM}•{Colors.RESET}  {Colors.MAGENTA}v1.0{Colors.RESET}
{Colors.GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
"""

BROWSERS = [
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

ICON_SIZES = [512, 256, 128, 96, 64, 48, 32, 24, 16]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

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
    return Path.home() / '.local' / 'share' / 'applications'

def get_webby_apps():
    apps_dir = get_applications_dir()
    apps = {}
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
    available = []
    seen_names = set()
    
    for cmd, flag, app_mode, name in BROWSERS:
        if shutil.which(cmd) and name not in seen_names:
            available.append((cmd, flag, app_mode, name))
            seen_names.add(name)
    
    return available

def detect_browser():
    for cmd, flag, app_mode, name in BROWSERS:
        if shutil.which(cmd):
            return cmd, flag, app_mode, name
    
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
    icons_dir = Path.home() / '.local' / 'share' / 'webby' / 'icons'
    icons_dir.mkdir(parents=True, exist_ok=True)
    return icons_dir

def get_hicolor_dir(size):
    icons_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor' / f'{size}x{size}' / 'apps'
    icons_dir.mkdir(parents=True, exist_ok=True)
    return icons_dir

def get_epiphany_profile_dir(app_name):
    profile_dir = Path.home() / '.local' / 'share' / 'webby' / 'epiphany-profiles' / sanitize_name(app_name)
    profile_dir.mkdir(parents=True, exist_ok=True)
    return profile_dir

def install_icon_to_theme(source_path, icon_name):
    source = Path(source_path)
    if not source.exists():
        return icon_name
    
    ext = source.suffix.lower()
    
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
    if not icon_name.startswith('webby-'):
        return
    
    hicolor_base = Path.home() / '.local' / 'share' / 'icons' / 'hicolor'
    
    for size in ICON_SIZES:
        icon_file = hicolor_base / f'{size}x{size}' / 'apps' / f'{icon_name}.png'
        icon_file.unlink(missing_ok=True)
    
    scalable_file = hicolor_base / 'scalable' / 'apps' / f'{icon_name}.svg'
    scalable_file.unlink(missing_ok=True)
    
    update_icon_cache()

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
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Webby/1.0'}
        )
        
        with urllib.request.urlopen(request, timeout=15) as response:
            temp_path.write_bytes(response.read())
        
        print(f"\r  {Colors.GREEN}✓{Colors.RESET} Icon downloaded       ")
        
        icon_name = install_icon_to_theme(temp_path, safe_name)
        
        temp_path.unlink(missing_ok=True)
        
        return icon_name
        
    except Exception as e:
        print(f"\r  {Colors.YELLOW}⚠{Colors.RESET} Could not download icon: {e}")
        return 'web-browser'

def find_icon(icon_input, app_name):
    if not icon_input:
        return 'web-browser'
    
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

def create_desktop_file(name, url, icon, browser, browser_flag, has_app_mode, browser_name):
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

def delete_app(app):
    app['file'].unlink(missing_ok=True)
    
    if app['icon'].startswith('webby-'):
        remove_icon_from_theme(app['icon'])
    
    update_desktop_database()
    print_success(f"Deleted '{app['name']}'")

def update_icon_cache():
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
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Icon:{Colors.RESET} {Colors.GREEN}{app['icon'][:38]}{'...' if len(app['icon']) > 38 else ''}{Colors.RESET}")
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
        app['file'].unlink(missing_ok=True)
    
    desktop_file = create_desktop_file(final_name, final_url, final_icon, browser, browser_flag, has_app_mode, browser_name)
    update_desktop_database()
    
    print_success(f"Updated '{final_name}'")
    print(f"\n{Colors.GRAY}  ┌{'─' * 44}┐{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Name:{Colors.RESET}  {Colors.CYAN}{final_name}{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}URL:{Colors.RESET}   {Colors.BLUE}{final_url[:38]}{'...' if len(final_url) > 38 else ''}{Colors.RESET}")
    print(f"{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Icon:{Colors.RESET}  {Colors.GREEN}{final_icon[:38]}{'...' if len(final_icon) > 38 else ''}{Colors.RESET}")
    print(f"{Colors.GRAY}  └{'─' * 44}┘{Colors.RESET}\n")

def interactive_mode():
    print_header()
    
    available_browsers = detect_all_browsers()
    
    if not available_browsers:
        print_error("No compatible browser found!")
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
        
        print(f"""
{Colors.GREEN}{Colors.BOLD}  ✨ Web App Created Successfully!{Colors.RESET}

{Colors.GRAY}  ┌{'─' * 44}┐{Colors.RESET}
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Name:{Colors.RESET}     {Colors.CYAN}{name}{Colors.RESET}
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}URL:{Colors.RESET}      {Colors.BLUE}{url[:35]}{'...' if len(url) > 35 else ''}{Colors.RESET}
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Browser:{Colors.RESET}  {Colors.CYAN}{browser_name}{Colors.RESET} ({mode_text})
{Colors.GRAY}  │{Colors.RESET}  {Colors.WHITE}Icon:{Colors.RESET}     {Colors.GREEN}{icon[:35]}{'...' if len(icon) > 35 else ''}{Colors.RESET}
{Colors.GRAY}  └{'─' * 44}┘{Colors.RESET}

{Colors.GRAY}  Find "{name}" in your app launcher!{Colors.RESET}
""")
        
    except Exception as e:
        print_error(f"Failed to create web app: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Webby - Web App Creator for Linux',
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
