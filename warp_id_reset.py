#!/usr/bin/env python3
"""
Warp Machine ID Reset Tool
===========================

This tool resets Warp's machine identity without removing the application.
After running this tool, Warp will think you're on a completely new machine
while keeping all your app installations intact.

Usage:
    python warp_id_reset.py
    
or make it executable:
    chmod +x warp_id_reset.py
    ./warp_id_reset.py
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
    print("║" + " "*13 + "🚀 IDENTITY RESET TOOL 🚀" + " "*12 + "║")
    print("║ 👨‍💻 Munir Ayub © 2025                         ║")
    print("║ 🔗 github.com/black12-ag/warp-bypass         ║")
    print("║ 📺 youtube.com/@black-ai-fix                ║")
    print("="*50 + "\n")


class WarpIdentityReset:
    def __init__(self):
        self.system = platform.system()
        self.home = Path.home()
        self.reset_count = 0
        
    def print_emoji(self, emoji, message):
        """Print message with emoji (works cross-platform)"""
        print(f"{emoji} {message}")
        
    def safe_remove(self, path_pattern, description=""):
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
                    self.print_emoji("🗂️", f"Reset {description}: {os.path.basename(path)}")
                elif os.path.isfile(path):
                    os.remove(path)
                    self.print_emoji("📄", f"Reset {description}: {os.path.basename(path)}")
                self.reset_count += 1
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
                self.print_emoji("🔑", f"Reset registry: {subkey}")
                self.reset_count += 1
            except Exception as e:
                self.print_emoji("⚠️", f"Could not delete {subkey}: {e}")
                
        except ImportError:
            pass  # Not Windows
        except Exception as e:
            self.print_emoji("⚠️", f"Registry error for {subkey}: {e}")
            
    def kill_browser_processes(self):
        """Kill all major browser processes to unlock files"""
        if self.system != "Windows":
            return
            
        self.print_emoji("🚫", "Closing browsers to unlock files...")
        
        browsers_to_kill = [
            'chrome.exe',
            'firefox.exe',
            'brave.exe',
            'opera.exe',
            'vivaldi.exe',
            'msedge.exe',
        ]
        
        for browser in browsers_to_kill:
            try:
                subprocess.run(['taskkill', '/F', '/IM', browser],
                             stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             check=False)
            except:
                pass
        
        time.sleep(2)  # Give time for processes to close
        self.print_emoji("✅", "Browsers closed")
    
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
            
        self.print_emoji("🌐", "Cleaning browser data (Note: Close all browsers first!)...")
        
        browser_paths = self.get_browser_data_paths()
        
        for browser_name, browser_path in browser_paths.items():
            if not browser_path.exists():
                continue
                
            self.print_emoji("🔍", f"Scanning {browser_name}...")
            
            try:
                # Method 1: Clean Local Storage (leveldb files)
                local_storage_dirs = [
                    'Default/Local Storage/leveldb',
                    'Profile */Local Storage/leveldb',
                ]
                for ls_pattern in local_storage_dirs:
                    for ls_dir in browser_path.glob(ls_pattern):
                        if ls_dir.is_dir():
                            for warp_file in ls_dir.glob('*'):
                                # Check if file contains 'warp' in content (for .log and .ldb files)
                                if warp_file.is_file():
                                    try:
                                        if 'warp' in warp_file.name.lower():
                                            self.safe_remove(str(warp_file), f"{browser_name} Local Storage")
                                    except:
                                        pass
                
                # Method 2: Clean IndexedDB
                indexeddb_patterns = [
                    'Default/IndexedDB',
                    'Profile */IndexedDB',
                ]
                for idb_pattern in indexeddb_patterns:
                    for idb_dir in browser_path.glob(idb_pattern):
                        if idb_dir.is_dir():
                            # Look for warp-related databases
                            for item in idb_dir.rglob('*'):
                                if 'warp' in str(item).lower():
                                    self.safe_remove(str(item), f"{browser_name} IndexedDB")
                
                # Method 3: Clean Session Storage
                session_storage_patterns = [
                    'Default/Session Storage',
                    'Profile */Session Storage',
                ]
                for ss_pattern in session_storage_patterns:
                    for ss_dir in browser_path.glob(ss_pattern):
                        if ss_dir.is_dir():
                            for item in ss_dir.rglob('*'):
                                if 'warp' in str(item).lower():
                                    self.safe_remove(str(item), f"{browser_name} Session Storage")
                
                # Method 4: Clean Cache (all cache directories)
                cache_patterns = [
                    'Default/Cache',
                    'Default/Code Cache',
                    'Default/GPUCache',
                    'Profile */Cache',
                    'Profile */Code Cache',
                    'Profile */GPUCache',
                    'ShaderCache',
                ]
                for cache_pattern in cache_patterns:
                    for cache_dir in browser_path.glob(cache_pattern):
                        if cache_dir.is_dir():
                            for item in cache_dir.rglob('*warp*'):
                                self.safe_remove(str(item), f"{browser_name} Cache")
                
                # Method 5: Clean Cookies (inside Cookies/Network files)
                cookie_patterns = [
                    'Default/Cookies',
                    'Default/Network/Cookies',
                    'Profile */Cookies',
                    'Profile */Network/Cookies',
                ]
                for cookie_pattern in cookie_patterns:
                    for cookie_file in browser_path.glob(cookie_pattern):
                        if cookie_file.is_file():
                            # Note: Can't selectively delete from SQLite DB while browser is running
                            # Just flag it for user awareness
                            self.print_emoji("🍪", f"Found {browser_name} cookies at: {cookie_file.name} (Close browser to clean)")
                
                # Method 6: Clean Service Workers
                sw_patterns = [
                    'Default/Service Worker',
                    'Profile */Service Worker',
                ]
                for sw_pattern in sw_patterns:
                    for sw_dir in browser_path.glob(sw_pattern):
                        if sw_dir.is_dir():
                            for item in sw_dir.rglob('*warp*'):
                                self.safe_remove(str(item), f"{browser_name} Service Worker")
                
                # Method 7: Clean Preferences (JSON files that might contain warp data)
                pref_patterns = [
                    'Default/Preferences',
                    'Profile */Preferences',
                    'Default/Secure Preferences',
                    'Profile */Secure Preferences',
                ]
                for pref_pattern in pref_patterns:
                    for pref_file in browser_path.glob(pref_pattern):
                        if pref_file.is_file():
                            try:
                                # Read and check if contains warp references
                                with open(pref_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                    if 'warp' in content.lower():
                                        self.print_emoji("⚙️", f"{browser_name}: Found warp in {pref_file.name} (needs manual edit or browser restart)")
                            except:
                                pass
                                
            except Exception as e:
                self.print_emoji("⚠️", f"{browser_name} cleanup warning: {e}")
                
    def kill_warp_processes(self):
        """Kill all Warp processes to ensure clean reset"""
        self.print_emoji("🔄", "Stopping Warp processes for identity reset...")
        
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
            self.print_emoji("✅", "Warp processes stopped")
            
        except Exception as e:
            self.print_emoji("⚠️", f"Process stop warning: {e}")
            
    def reset_macos_identity(self):
        """Reset Warp identity on macOS - keeps app installed"""
        self.print_emoji("🍎", "Resetting Warp identity on macOS...")
        
        # Note: We DON'T remove /Applications/Warp.app - that stays!
        
        # User identity and session data
        self.print_emoji("🔑", "Clearing user identity data...")
        
        # Application Support - user data, settings, machine ID
        self.safe_remove(str(self.home / "Library/Application Support/*warp*"), "user data")
        self.safe_remove(str(self.home / "Library/Application Support/*Warp*"), "user data")
        
        # Preferences - user preferences and machine-specific settings
        self.print_emoji("⚙️", "Clearing preferences and settings...")
        self.safe_remove(str(self.home / "Library/Preferences/*warp*"), "preferences")
        self.safe_remove(str(self.home / "Library/Preferences/*Warp*"), "preferences")
        
        # Caches - temporary files that might contain machine info
        self.print_emoji("🧹", "Clearing cache files...")
        self.safe_remove(str(self.home / "Library/Caches/*warp*"), "cache")
        self.safe_remove(str(self.home / "Library/Caches/*Warp*"), "cache")
        
        # Logs - might contain machine identification
        self.print_emoji("📋", "Clearing log files...")
        self.safe_remove(str(self.home / "Library/Logs/*warp*"), "logs")
        self.safe_remove(str(self.home / "Library/Logs/*Warp*"), "logs")
        
        # WebKit data - browser data that might have machine fingerprints
        self.print_emoji("🌐", "Clearing web data...")
        self.safe_remove(str(self.home / "Library/WebKit/*warp*"), "web data")
        self.safe_remove(str(self.home / "Library/WebKit/*Warp*"), "web data")
        
        # Saved Application State - window states and session info
        self.print_emoji("💾", "Clearing application state...")
        self.safe_remove(str(self.home / "Library/Saved Application State/*warp*"), "app state")
        self.safe_remove(str(self.home / "Library/Saved Application State/*Warp*"), "app state")
        
        # HTTP Storage - might contain session tokens
        self.print_emoji("🔐", "Clearing HTTP storage...")
        self.safe_remove(str(self.home / "Library/HTTPStorages/*warp*"), "HTTP storage")
        self.safe_remove(str(self.home / "Library/HTTPStorages/*Warp*"), "HTTP storage")
        
        # Clear Launch Services database (helps reset file associations)
        self.print_emoji("📊", "Updating system database...")
        try:
            lsregister_path = ("/System/Library/Frameworks/CoreServices.framework/"
                             "Frameworks/LaunchServices.framework/Support/lsregister")
            subprocess.run([lsregister_path, "-kill", "-r", "-domain", "local", 
                          "-domain", "system", "-domain", "user"], 
                         stderr=subprocess.DEVNULL, check=False)
        except Exception as e:
            self.print_emoji("⚠️", f"Database update warning: {e}")
            
    def reset_linux_identity(self):
        """Reset Warp identity on Linux - keeps app installed"""
        self.print_emoji("🐧", "Resetting Warp identity on Linux...")
        
        # XDG Base Directory paths
        xdg_config = Path(os.environ.get('XDG_CONFIG_HOME', self.home / '.config'))
        xdg_data = Path(os.environ.get('XDG_DATA_HOME', self.home / '.local/share'))
        xdg_cache = Path(os.environ.get('XDG_CACHE_HOME', self.home / '.cache'))
        xdg_state = Path(os.environ.get('XDG_STATE_HOME', self.home / '.local/state'))
        
        # User identity and session data
        self.print_emoji("🔑", "Clearing user identity data...")
        
        # Configuration files
        self.safe_remove(str(xdg_config / 'warp'), "config")
        self.safe_remove(str(xdg_config / 'Warp'), "config")
        self.safe_remove(str(self.home / '.warp'), "legacy config")
        
        # Application data
        self.print_emoji("📁", "Clearing application data...")
        self.safe_remove(str(xdg_data / 'warp'), "app data")
        self.safe_remove(str(xdg_data / 'Warp'), "app data")
        
        # Cache files
        self.print_emoji("🧹", "Clearing cache files...")
        self.safe_remove(str(xdg_cache / 'warp'), "cache")
        self.safe_remove(str(xdg_cache / 'Warp'), "cache")
        
        # State and logs
        self.print_emoji("📋", "Clearing state and logs...")
        self.safe_remove(str(xdg_state / 'warp'), "state")
        self.safe_remove(str(xdg_state / 'warp' / 'logs'), "logs")
        
        # Temporary/runtime files
        self.print_emoji("🗑️", "Clearing temporary/runtime files...")
        try:
            uid = os.getuid()
        except AttributeError:
            uid = None
        if uid is not None:
            self.safe_remove(f"/run/user/{uid}/warp", "runtime")
        self.safe_remove(f"/tmp/warp-{os.getenv('USER', '*')}", "temp files")

    def reset_windows_identity(self):
        """Reset Warp identity on Windows - keeps app installed"""
        self.print_emoji("🪟", "Resetting Warp identity on Windows...")
        
        local_appdata = Path(os.environ.get('LOCALAPPDATA', str(self.home / 'AppData/Local')))
        appdata = Path(os.environ.get('APPDATA', str(self.home / 'AppData/Roaming')))
        
        # User identity and session data
        self.print_emoji("🔑", "Clearing user identity data...")
        self.safe_remove(str(local_appdata / 'dev.warp.Warp-stable'), "user data")
        self.safe_remove(str(appdata / 'dev.warp.Warp-stable'), "user data")
        
        # IMPORTANT: Don't delete AppData/Local/Warp - it may contain the app itself!
        # Only delete specific data folders inside it
        warp_appdata = local_appdata / 'Warp'
        if warp_appdata.exists():
            # Delete only data subfolders, not the entire Warp directory
            for subfolder in ['User Data', 'Cache', 'Logs', 'Local Storage', 'Session Storage']:
                subfolder_path = warp_appdata / subfolder
                if subfolder_path.exists():
                    self.safe_remove(str(subfolder_path), f"Warp/{subfolder}")
        
        # Delete roaming data (this is safe - no app files here)
        self.safe_remove(str(appdata / 'Warp'), "user data")

        # Temp files (fixed wildcard pattern)
        self.print_emoji("🧹", "Clearing temporary files...")
        temp_dir = Path(os.environ.get('TEMP', 'C:/Windows/Temp'))
        # Use proper glob pattern
        temp_warp_files = glob.glob(str(temp_dir / "*Warp*.exe"))
        temp_warp_files.extend(glob.glob(str(temp_dir / "*warp*.exe")))
        for temp_file in temp_warp_files:
            self.safe_remove(temp_file, "temp files")

        # NOTE: We DON'T remove Start Menu shortcuts - user needs them to launch Warp!
        # The app stays installed, so shortcuts should remain

        # Registry cleanup - remove machine-specific registry entries (now recursive)
        self.print_emoji("📊", "Resetting registry entries (recursive)...")
        try:
            import winreg
            # Clean up user-specific registry locations (not system-wide)
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, "Software\\Warp"),
                (winreg.HKEY_CURRENT_USER, "Software\\dev.warp.Warp-stable"),
            ]
            
            for root, subkey in registry_paths:
                self.delete_registry_key_recursive(root, subkey)
                    
        except ImportError:
            self.print_emoji("⚠️", "Registry reset requires Windows")
        except Exception as e:
            self.print_emoji("⚠️", f"Registry reset warning: {e}")
            
        # Kill browsers before cleaning their data
        self.kill_browser_processes()
        
        # Clean browser data
        self.clean_browser_data()
            
    def verify_app_still_installed(self):
        """Verify that Warp app is still installed"""
        self.print_emoji("🔍", "Verifying Warp installation...")
        
        app_exists = False
        
        if self.system == "Darwin":  # macOS
            app_path = "/Applications/Warp.app"
            self.print_emoji("ℹ️", f"Checking for Warp at: {app_path}")
            app_exists = os.path.exists(app_path)
            if app_exists:
                self.print_emoji("✅", f"Warp app still installed: {app_path}")
            else:
                self.print_emoji("❌", "Warp app not found - may not be installed")
                
        elif self.system == "Windows":
            # Check common Windows installation paths
            program_files = Path(os.environ.get('PROGRAMFILES', 'C:/Program Files'))
            program_files_x86 = Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)'))
            local_appdata = Path(os.environ.get('LOCALAPPDATA', str(self.home / 'AppData/Local')))

            possible_paths = [
                program_files / "Warp/Warp.exe",
                program_files_x86 / "Warp/Warp.exe",
                local_appdata / "Warp/Warp.exe",
            ]
            
            for path in possible_paths:
                self.print_emoji("ℹ️", f"Checking for Warp at: {path}")
                if path.exists():
                    app_exists = True
                    self.print_emoji("✅", f"Warp app still installed: {path}")
                    break
                    
            if not app_exists:
                self.print_emoji("❌", "Warp app not found - may not be installed")
        elif self.system == "Linux":
            # Try to find the 'warp' binary or installation directories
            binary = shutil.which("warp")
            possible_paths = [
                Path("/opt/Warp"),
                Path("/usr/local/bin/warp"),
                Path("/usr/bin/warp"),
                self.home / ".local" / "bin" / "warp",
            ]
            if binary:
                app_exists = True
                self.print_emoji("✅", f"Warp binary found: {binary}")
            else:
                for path in possible_paths:
                    if Path(path).exists():
                        app_exists = True
                        self.print_emoji("✅", f"Warp found at: {path}")
                        break
            if not app_exists:
                self.print_emoji("❌", "Warp app not found - may not be installed")
                
        return app_exists
        
    def is_admin(self):
        """Check for admin privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def run(self):
        """Main identity reset process"""
        print("=" * 70)
        self.print_emoji("🔄", "Starting Warp Machine Identity Reset...")
        self.print_emoji("💻", f"Detected system: {self.system}")
        self.print_emoji("🎯", "App will remain installed - only identity data will be reset")
        print("=" * 70)

        if self.system == "Windows" and not self.is_admin():
            self.print_emoji("❌", "This tool requires administrator privileges on Windows.")
            self.print_emoji("💡", "Please re-run this script from a Command Prompt or PowerShell with 'Run as Administrator'.")
            return False
        
        # Step 1: Stop processes
        self.kill_warp_processes()
        
        # Step 2: Platform-specific identity reset
        if self.system == "Darwin":  # macOS
            self.reset_macos_identity()
        elif self.system == "Windows":
            self.reset_windows_identity()
        elif self.system == "Linux":
            self.reset_linux_identity()
        else:
            self.print_emoji("❌", f"Unsupported system: {self.system}")
            self.print_emoji("💡", "This tool supports macOS, Windows, and Linux")
            return False
            
        # Step 3: Verify app is still there
        app_still_there = self.verify_app_still_installed()
        
        # Final report
        print("\n" + "=" * 70)
        self.print_emoji("✅", "WARP IDENTITY RESET COMPLETE!")
        print(f"📈 Reset {self.reset_count} identity items")
        
        if app_still_there:
            self.print_emoji("🎉", "Perfect! Warp app is still installed")
            self.print_emoji("🆔", "Your machine now has a fresh identity to Warp")
            self.print_emoji("🚀", "Launch Warp - it will see you as a new user/machine")
        else:
            self.print_emoji("⚠️", "Warp app not detected - you may need to install it")
            
        self.print_emoji("🔄", "Next: Open Warp and enjoy your fresh machine identity!")
        print("=" * 70)
        
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
        print("💡 Note: For complete reset on Windows, run as Administrator")
        print("   Right-click Command Prompt/PowerShell -> 'Run as Administrator'")
        print()
        
    print("🔄 WARP MACHINE IDENTITY RESET")
    print("================================")
    print("This tool will:")
    print("✅ Keep Warp app installed")
    print("🔄 Reset your machine identity") 
    print("🗑️  Clear user data and preferences")
    print("🆔 Make Warp see you as a new user")
    print()
    
    # Confirm before proceeding
    response = input("⚠️  Reset Warp machine identity? Your app will stay installed (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Cancelled by user")
        return
        
    # Run the reset
    reset_tool = WarpIdentityReset()
    success = reset_tool.run()
    
    if success:
        print("\n🎯 Identity reset completed successfully!")
        print("🚀 Launch Warp to start fresh!")
    else:
        print("\n❌ Identity reset failed or incomplete")
        sys.exit(1)


if __name__ == "__main__":
    main()
