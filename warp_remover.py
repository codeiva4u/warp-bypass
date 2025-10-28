#!/usr/bin/env python3
"""
Cross-Platform Warp Complete Removal Tool
==========================================

This tool completely removes Warp terminal from your system and makes it appear
as a new machine when you reinstall. Works on both macOS and Windows.

Usage:
    python warp_remover.py
    
or make it executable:
    chmod +x warp_remover.py
    ./warp_remover.py
"""

import os
import sys
import platform
import subprocess
import shutil
import glob
import time
from pathlib import Path


def show_banner():
    """Display simple banner with WARP over MUNIR"""
    print("\n" + "="*50)
    print("""    
██╗    ██╗█████╗ ██████╗ ██████╗ 
██║    ██║██╔══██╗██╔══██╗██╔══██╗
██░ █╗ ██║███████║██████╔╝██████╔╝
██░███╗██║██╔══██║██╔══██╗██╔═══╝ 
╚███╔███╔╝██║  ██║██║  ██║██║     
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     

███╗   ██╗██╗   ██╗███╗   ██╗██╗██████╗ 
████╗ ████║██║   ██║████╗  ██║██║██╔══██╗
██╔████╔██║██║   ██║██╔██╗ ██║██║██████╔╝
██║╚██╔╝██║██║   ██║██║╚██╗██║██║██╔══██╗
██║ ╚═╝ ██║╚█████╔╝██║ ╚████║██║██║  ██║
╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
""")
    print("="*50)
    print("║" + " "*10 + "🗑️ COMPLETE REMOVAL TOOL 🗑️" + " "*9 + "║")
    print("║ 👨‍💻 Munir Ayub © 2025                         ║")
    print("║ 🔗 github.com/black12-ag/warp-bypass         ║")
    print("║ 📺 youtube.com/@black-ai-fix                ║")
    print("="*50 + "\n")


class WarpRemover:
    def __init__(self):
        self.system = platform.system()
        self.home = Path.home()
        self.removed_count = 0
        
    def print_emoji(self, emoji, message):
        """Print message with emoji (works cross-platform)"""
        print(f"{emoji} {message}")
        
    def safe_remove(self, path_pattern):
        """Safely remove files/directories matching pattern"""
        if isinstance(path_pattern, str):
            try:
                paths = glob.glob(path_pattern, recursive=True)
            except Exception as e:
                self.print_emoji("⚠️", f"Error during glob operation for {path_pattern}: {e}")
                return
        else:
            paths = [str(path_pattern)] if path_pattern.exists() else []
            
        for path in paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    self.print_emoji("🗂️", f"Removed directory: {path}")
                elif os.path.isfile(path):
                    os.remove(path)
                    self.print_emoji("📄", f"Removed file: {path}")
                self.removed_count += 1
            except PermissionError:
                self.print_emoji("❌", f"Permission denied to remove {path}. Try running as administrator.")
            except FileNotFoundError:
                self.print_emoji("🤷", f"File not found to remove: {path}")
            except OSError as e:
                self.print_emoji("⚠️", f"Could not remove {path}: {e}")
                
    def delete_registry_key_recursive(self, root, subkey):
        """Recursively delete registry key and all subkeys (Windows only)"""
        try:
            import winreg
            # Open the key
            try:
                key = winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                return  # Key doesn't exist
            except PermissionError:
                self.print_emoji("❌", f"Permission denied: {subkey}")
                return
                
            # Get all subkeys
            subkeys = []
            try:
                i = 0
                while True:
                    subkeys.append(winreg.EnumKey(key, i))
                    i += 1
            except OSError:
                pass  # No more subkeys
            
            winreg.CloseKey(key)
            
            # Recursively delete all subkeys
            for sk in subkeys:
                self.delete_registry_key_recursive(root, f"{subkey}\\{sk}")
            
            # Delete the key itself
            try:
                winreg.DeleteKey(root, subkey)
                self.print_emoji("🔑", f"Removed registry: {subkey}")
                self.removed_count += 1
            except Exception as e:
                self.print_emoji("⚠️", f"Could not delete {subkey}: {e}")
                
        except ImportError:
            pass  # Not Windows
        except Exception as e:
            self.print_emoji("⚠️", f"Registry error for {subkey}: {e}")
            
    def detect_custom_installation_paths(self):
        """Detect custom Warp installation paths from registry"""
        custom_paths = []
        
        if self.system != "Windows":
            return custom_paths
            
        try:
            import winreg
            
            # Check uninstall registry entries
            uninstall_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            
            for root, path in uninstall_paths:
                try:
                    key = winreg.OpenKey(root, path)
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            if 'warp' in subkey_name.lower():
                                subkey = winreg.OpenKey(key, subkey_name)
                                try:
                                    install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    if install_location and os.path.exists(install_location):
                                        custom_paths.append(Path(install_location))
                                except FileNotFoundError:
                                    pass
                                winreg.CloseKey(subkey)
                            i += 1
                        except OSError:
                            break
                    winreg.CloseKey(key)
                except Exception:
                    pass
                    
        except Exception as e:
            self.print_emoji("⚠️", f"Custom path detection warning: {e}")
            
        return custom_paths
        
    def remove_windows_services(self):
        """Remove Warp-related Windows services"""
        if self.system != "Windows":
            return
            
        self.print_emoji("🔧", "Checking for Warp services...")
        
        try:
            # List all services and find Warp-related ones
            result = subprocess.run(
                ['sc', 'query', 'type=', 'service', 'state=', 'all'],
                capture_output=True, text=True, check=False
            )
            
            services_to_remove = []
            for line in result.stdout.split('\n'):
                if 'SERVICE_NAME' in line and 'warp' in line.lower():
                    service_name = line.split(':')[1].strip()
                    services_to_remove.append(service_name)
            
            # Stop and delete services
            for service in services_to_remove:
                self.print_emoji("🛑", f"Stopping service: {service}")
                subprocess.run(['sc', 'stop', service], 
                             stderr=subprocess.DEVNULL, check=False)
                time.sleep(1)
                
                self.print_emoji("🗑️", f"Deleting service: {service}")
                subprocess.run(['sc', 'delete', service], 
                             stderr=subprocess.DEVNULL, check=False)
                self.removed_count += 1
                
        except Exception as e:
            self.print_emoji("⚠️", f"Service cleanup warning: {e}")
            
    def remove_scheduled_tasks(self):
        """Remove Warp-related scheduled tasks"""
        if self.system != "Windows":
            return
            
        self.print_emoji("📅", "Checking for scheduled tasks...")
        
        try:
            # List all scheduled tasks
            result = subprocess.run(
                ['schtasks', '/Query', '/FO', 'LIST'],
                capture_output=True, text=True, check=False
            )
            
            tasks_to_remove = []
            for line in result.stdout.split('\n'):
                if 'TaskName' in line and 'warp' in line.lower():
                    task_name = line.split(':', 1)[1].strip()
                    tasks_to_remove.append(task_name)
            
            # Delete tasks
            for task in tasks_to_remove:
                self.print_emoji("🗑️", f"Removing task: {task}")
                subprocess.run(['schtasks', '/Delete', '/TN', task, '/F'],
                             stderr=subprocess.DEVNULL, check=False)
                self.removed_count += 1
                
        except Exception as e:
            self.print_emoji("⚠️", f"Scheduled task cleanup warning: {e}")
            
    def get_browser_data_paths(self):
        """Get browser data paths for all major browsers"""
        browser_paths = {}
        
        if self.system == "Windows":
            local_appdata = Path(os.environ.get('LOCALAPPDATA', str(self.home / 'AppData/Local')))
            appdata = Path(os.environ.get('APPDATA', str(self.home / 'AppData/Roaming')))
            
            browser_paths = {
                'Chrome': local_appdata / 'Google/Chrome/User Data',
                # 'Edge': local_appdata / 'Microsoft/Edge/User Data',  # Excluded by user request
                'Firefox': appdata / 'Mozilla/Firefox/Profiles',
                'Brave': local_appdata / 'BraveSoftware/Brave-Browser/User Data',
                'Opera': appdata / 'Opera Software/Opera Stable',
                'Vivaldi': local_appdata / 'Vivaldi/User Data',
                'Ulaa': local_appdata / 'Ulaa/User Data',  # Added Ulaa browser support
            }
            
        return browser_paths
        
    def clean_browser_data(self):
        """Clean Warp-related data from all browsers"""
        if self.system != "Windows":
            return
            
        self.print_emoji("🌐", "Cleaning browser data...")
        
        browser_paths = self.get_browser_data_paths()
        
        for browser_name, browser_path in browser_paths.items():
            if browser_path.exists():
                try:
                    # Clean cookies
                    for cookie_file in browser_path.rglob('*Cookies*'):
                        if cookie_file.is_file():
                            try:
                                # Note: Just flagging, actual cookie cleaning would need DB access
                                self.print_emoji("🍪", f"Found {browser_name} cookies at: {cookie_file}")
                            except Exception:
                                pass
                    
                    # Clean local storage
                    local_storage_patterns = [
                        '**/Local Storage/**/*warp*',
                        '**/IndexedDB/**/*warp*',
                        '**/Session Storage/**/*warp*',
                    ]
                    
                    for pattern in local_storage_patterns:
                        for item in browser_path.glob(pattern):
                            self.safe_remove(str(item))
                            
                    # Clean cache
                    cache_paths = list(browser_path.rglob('*Cache*'))
                    for cache_path in cache_paths:
                        if cache_path.is_dir():
                            warp_cache = list(cache_path.rglob('*warp*'))
                            for warp_item in warp_cache:
                                self.safe_remove(str(warp_item))
                                
                except Exception as e:
                    self.print_emoji("⚠️", f"{browser_name} cleanup warning: {e}")
                
    def kill_warp_processes(self):
        """Kill all Warp processes (cross-platform)"""
        self.print_emoji("🔫", "Killing Warp processes...")
        
        try:
            if self.system in ("Darwin", "Linux"):  # macOS or Linux
                subprocess.run(["pkill", "-f", "-i", "warp"], 
                             stderr=subprocess.DEVNULL, check=False)
            elif self.system == "Windows":
                subprocess.run(["taskkill", "/F", "/IM", "warp.exe"], 
                             stderr=subprocess.DEVNULL, check=False)
                subprocess.run(["taskkill", "/F", "/IM", "Warp.exe"], 
                             stderr=subprocess.DEVNULL, check=False)
            
            time.sleep(2)  # Give processes time to terminate
            self.print_emoji("✅", "Warp processes terminated")
            
        except Exception as e:
            self.print_emoji("⚠️", f"Process termination warning: {e}")
            
    def remove_macos_warp(self):
        """Remove Warp from macOS"""
        self.print_emoji("🍎", "Removing Warp from macOS...")
        
        # Main application
        self.print_emoji("🗑️", "Removing main application...")
        self.safe_remove("/Applications/Warp.app")
        
        # User data and configuration
        self.print_emoji("📁", "Removing user data and configuration...")
        
        # Application Support
        self.safe_remove(str(self.home / "Library/Application Support/*warp*"))
        self.safe_remove(str(self.home / "Library/Application Support/*Warp*"))
        
        # Preferences
        self.safe_remove(str(self.home / "Library/Preferences/*warp*"))
        self.safe_remove(str(self.home / "Library/Preferences/*Warp*"))
        
        # Caches
        self.safe_remove(str(self.home / "Library/Caches/*warp*"))
        self.safe_remove(str(self.home / "Library/Caches/*Warp*"))
        
        # Logs
        self.safe_remove(str(self.home / "Library/Logs/*warp*"))
        self.safe_remove(str(self.home / "Library/Logs/*Warp*"))
        
        # WebKit data
        self.safe_remove(str(self.home / "Library/WebKit/*warp*"))
        self.safe_remove(str(self.home / "Library/WebKit/*Warp*"))
        
        # Saved Application State
        self.safe_remove(str(self.home / "Library/Saved Application State/*warp*"))
        self.safe_remove(str(self.home / "Library/Saved Application State/*Warp*"))
        
        # HTTP Storage
        self.safe_remove(str(self.home / "Library/HTTPStorages/*warp*"))
        self.safe_remove(str(self.home / "Library/HTTPStorages/*Warp*"))
        
        # Downloads
        self.safe_remove(str(self.home / "Downloads/*warp*"))
        self.safe_remove(str(self.home / "Downloads/*Warp*"))
        
        # Clear Launch Services database
        self.print_emoji("📊", "Clearing Launch Services database...")
        try:
            lsregister_path = ("/System/Library/Frameworks/CoreServices.framework/"
                             "Frameworks/LaunchServices.framework/Support/lsregister")
            subprocess.run([lsregister_path, "-kill", "-r", "-domain", "local", 
                          "-domain", "system", "-domain", "user"], 
                         stderr=subprocess.DEVNULL, check=False)
        except Exception as e:
            self.print_emoji("⚠️", f"Launch Services warning: {e}")
            
    def remove_linux_warp(self):
        """Remove Warp from Linux"""
        self.print_emoji("🐧", "Removing Warp from Linux...")
        
        # Main application (common manual install locations)
        self.print_emoji("🗑️", "Removing main application (if present)...")
        self.safe_remove("/opt/Warp")
        self.safe_remove("/usr/local/bin/warp")
        self.safe_remove("/usr/bin/warp")
        self.safe_remove(str(self.home / ".local/bin/warp"))
        
        # User data and configuration (XDG base dirs)
        self.print_emoji("📁", "Removing user data and configuration...")
        xdg_config = Path(os.environ.get('XDG_CONFIG_HOME', self.home / '.config'))
        xdg_data = Path(os.environ.get('XDG_DATA_HOME', self.home / '.local/share'))
        xdg_cache = Path(os.environ.get('XDG_CACHE_HOME', self.home / '.cache'))
        xdg_state = Path(os.environ.get('XDG_STATE_HOME', self.home / '.local/state'))
        
        # Configuration
        self.safe_remove(str(xdg_config / 'warp'))
        self.safe_remove(str(xdg_config / 'Warp'))
        self.safe_remove(str(self.home / '.warp'))
        
        # Data
        self.safe_remove(str(xdg_data / 'warp'))
        self.safe_remove(str(xdg_data / 'Warp'))
        
        # Cache
        self.safe_remove(str(xdg_cache / 'warp'))
        self.safe_remove(str(xdg_cache / 'Warp'))
        
        # Logs/State
        self.safe_remove(str(xdg_state / 'warp'))
        
        # Desktop entries
        self.print_emoji("🗂️", "Removing desktop entries...")
        self.safe_remove(str(self.home / ".local/share/applications/warp.desktop"))
        self.safe_remove("/usr/share/applications/warp.desktop")
        
        # Runtime/temp
        try:
            uid = os.getuid()
        except AttributeError:
            uid = None
        if uid is not None:
            self.safe_remove(f"/run/user/{uid}/warp")
        self.safe_remove(f"/tmp/warp-{os.getenv('USER', '*')}")
        
        # Note: If installed via package manager, removal may require:
        #  - Snap: 'sudo snap remove warp'
        #  - Flatpak: 'flatpak uninstall dev.warp.Warp'
        #  - DEB/RPM: 'sudo apt/dnf/yum remove warp'
        # We don't run these automatically to avoid requiring root.

    def remove_windows_warp(self):
        """Remove Warp from Windows"""
        self.print_emoji("🪟", "Removing Warp from Windows...")
        
        # Detect custom installation paths
        custom_paths = self.detect_custom_installation_paths()
        if custom_paths:
            self.print_emoji("🔍", f"Detected {len(custom_paths)} custom installation(s)")
        
        # Common installation paths
        program_files = Path(os.environ.get('PROGRAMFILES', 'C:/Program Files'))
        program_files_x86 = Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)'))
        local_appdata = Path(os.environ.get('LOCALAPPDATA', str(self.home / 'AppData/Local')))
        appdata = Path(os.environ.get('APPDATA', str(self.home / 'AppData/Roaming')))
        
        # Main application installations
        self.print_emoji("🗑️", "Removing main application...")
        self.safe_remove(program_files / "Warp")
        self.safe_remove(program_files_x86 / "Warp")
        self.safe_remove(local_appdata / "Warp")
        
        # Remove custom installations
        for custom_path in custom_paths:
            self.print_emoji("🗑️", f"Removing custom installation: {custom_path}")
            self.safe_remove(custom_path)

        # User data and configuration
        self.print_emoji("📁", "Removing user data and configuration...")
        self.safe_remove(str(local_appdata / 'dev.warp.Warp-stable'))
        self.safe_remove(str(appdata / 'dev.warp.Warp-stable'))
        self.safe_remove(str(local_appdata / 'Warp'))
        self.safe_remove(str(appdata / 'Warp'))

        # Temp files (fixed wildcard pattern)
        self.print_emoji("🧹", "Clearing temporary files...")
        temp_dir = Path(os.environ.get('TEMP', 'C:/Windows/Temp'))
        # Use proper glob pattern
        temp_warp_files = glob.glob(str(temp_dir / "*Warp*.exe"))
        temp_warp_files.extend(glob.glob(str(temp_dir / "*warp*.exe")))
        for temp_file in temp_warp_files:
            self.safe_remove(temp_file)

        # Start Menu link
        self.print_emoji("🔗", "Removing Start Menu link...")
        start_menu = Path(os.environ.get('APPDATA', str(self.home / 'AppData/Roaming'))) / "Microsoft/Windows/Start Menu/Programs"
        self.safe_remove(str(start_menu / "Warp.lnk"))

        # Registry cleanup (requires admin privileges) - Now with recursive deletion
        self.print_emoji("📊", "Attempting registry cleanup (recursive)...")
        try:
            import winreg
            # Clean up common registry locations
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, "Software\\Warp"),
                (winreg.HKEY_LOCAL_MACHINE, "Software\\Warp"),
                (winreg.HKEY_CURRENT_USER, "Software\\dev.warp.Warp-stable"),
                (winreg.HKEY_LOCAL_MACHINE, "Software\\dev.warp.Warp-stable"),
                (winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Warp"),
                (winreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Warp"),
                (winreg.HKEY_LOCAL_MACHINE, "Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Warp"),
            ]
            
            for root, subkey in registry_paths:
                self.delete_registry_key_recursive(root, subkey)
                    
        except ImportError:
            self.print_emoji("⚠️", "Registry cleanup requires Windows")
        except Exception as e:
            self.print_emoji("⚠️", f"Registry cleanup warning: {e}")
            
        # Remove Windows services
        self.remove_windows_services()
        
        # Remove scheduled tasks
        self.remove_scheduled_tasks()
        
        # Clean browser data
        self.clean_browser_data()
            
    def verify_removal(self):
        """Verify that Warp has been completely removed"""
        self.print_emoji("🔍", "Verifying complete removal...")
        
        # Count remaining Warp-related items
        search_paths = []
        
        if self.system == "Darwin":  # macOS
            search_paths = [
                str(self.home / "Library"),
                "/Applications"
            ]
        elif self.system == "Windows":
            search_paths = [
                str(self.home / "AppData"),
                str(Path(os.environ.get('PROGRAMFILES', 'C:/Program Files'))),
                str(Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)')))
            ]
        elif self.system == "Linux":
            search_paths = [
                str(self.home / ".config"),
                str(self.home / ".local/share"),
                str(self.home / ".cache"),
                str(self.home / ".local/state"),
                "/opt",
                "/usr/local/bin",
                "/usr/bin",
                str(self.home / ".local/bin"),
                str(self.home / ".local/share/applications"),
                "/usr/share/applications",
            ]
            
        remaining_items = 0
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for root, dirs, files in os.walk(search_path):
                        for item in dirs + files:
                            path_parts = Path(root).parts + (item,)
                            if any('warp' in part.lower() for part in path_parts):
                                full_path = os.path.join(root, item)
                                # Exclude common false positives
                                if not any(fp in full_path.lower() for fp in ['skimage', 'python', 'hp', 'google', 'chrome']):
                                    remaining_items += 1
                                    self.print_emoji("👀", f"Found: {full_path}")
                except (PermissionError, OSError):
                    pass  # Skip inaccessible directories
                    
        return remaining_items
        
    def is_admin(self):
        """Check for admin privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def run(self):
        """Main removal process"""
        print("=" * 60)
        self.print_emoji("🚀", "Starting Complete Warp Removal...")
        self.print_emoji("💻", f"Detected system: {self.system}")
        print("=" * 60)

        if self.system == "Windows" and not self.is_admin():
            self.print_emoji("❌", "This tool requires administrator privileges on Windows.")
            self.print_emoji("💡", "Please re-run this script from a Command Prompt or PowerShell with 'Run as Administrator'.")
            return False
        
        # Step 1: Kill processes
        self.kill_warp_processes()
        
        # Step 2: Platform-specific removal
        if self.system == "Darwin":  # macOS
            self.remove_macos_warp()
        elif self.system == "Windows":
            self.remove_windows_warp()
        elif self.system == "Linux":
            self.remove_linux_warp()
        else:
            self.print_emoji("❌", f"Unsupported system: {self.system}")
            self.print_emoji("💡", "This tool supports macOS, Windows, and Linux")
            return False
            
        # Step 3: Verification
        remaining = self.verify_removal()
        
        # Final report
        print("\n" + "=" * 60)
        self.print_emoji("✅", "WARP REMOVAL COMPLETE!")
        print(f"📈 Removed {self.removed_count} items")
        
        if remaining == 0:
            self.print_emoji("🎉", "Perfect! No Warp traces found.")
        else:
            self.print_emoji("⚠️", f"Found {remaining} remaining items (may be inaccessible)")
            
        self.print_emoji("🔄", "Your system will now appear as a NEW MACHINE to Warp.")
        self.print_emoji("⬇️", "You can safely reinstall Warp now.")
        print("=" * 60)
        
        return True


def main():
    """Entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__)
        return
    
    # Show banner and copyright
    show_banner()
        
    # Warn about admin privileges
    if platform.system() == "Windows":
        print("💡 Note: For complete removal on Windows, run as Administrator")
        print("   Right-click Command Prompt/PowerShell -> 'Run as Administrator'")
        print()
        
    # Confirm before proceeding
    response = input("⚠️  This will COMPLETELY remove Warp from your system. Continue? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Cancelled by user")
        return
        
    # Run the removal
    remover = WarpRemover()
    success = remover.run()
    
    if success:
        print("\n🎯 Removal completed successfully!")
    else:
        print("\n❌ Removal failed or incomplete")
        sys.exit(1)


if __name__ == "__main__":
    main()
