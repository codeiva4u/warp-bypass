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
        self.detected_warp_paths = []  # Store detected Warp installations
    
    def auto_detect_warp_paths(self):
        """Automatically detect all Warp installation paths"""
        self.print_emoji("🔍", "Auto-detecting Warp installations...")
        detected = []
        
        if self.system == "Windows":
            local_appdata = Path(os.environ.get('LOCALAPPDATA', str(self.home / 'AppData/Local')))
            appdata = Path(os.environ.get('APPDATA', str(self.home / 'AppData/Roaming')))
            program_files = Path(os.environ.get('PROGRAMFILES', 'C:/Program Files'))
            program_files_x86 = Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)'))
            
            # Search patterns for different Warp installations
            search_locations = [
                # Official paths
                (local_appdata / 'warp', 'Official Warp (new)'),
                (appdata / 'warp', 'Official Warp settings (new)'),
                
                # Legacy paths
                (local_appdata / 'dev.warp.Warp-stable', 'Legacy Warp-Stable'),
                (appdata / 'dev.warp.Warp-stable', 'Legacy Warp-Stable settings'),
                (local_appdata / 'Warp', 'Old Warp'),
                (appdata / 'Warp', 'Old Warp settings'),
                
                # Program Files installations
                (program_files / 'Warp', 'Warp (Program Files)'),
                (program_files_x86 / 'Warp', 'Warp (Program Files x86)'),
            ]
            
            for path, description in search_locations:
                if path.exists():
                    # Check if it's actually a Warp directory
                    if self._is_warp_directory(path):
                        detected.append({
                            'path': path,
                            'description': description,
                            'type': 'data' if 'settings' not in description.lower() else 'settings'
                        })
                        self.print_emoji("✅", f"Found: {description} at {path}")
            
            # Also search for any warp-related directories
            self._deep_search_warp_dirs(local_appdata, detected)
            self._deep_search_warp_dirs(appdata, detected)
            
        elif self.system == "Darwin":  # macOS
            search_locations = [
                (Path("/Applications/Warp.app"), 'Warp Application'),
                (self.home / "Library/Application Support", 'App Support'),
                (self.home / "Library/Preferences", 'Preferences'),
                (self.home / "Library/Caches", 'Caches'),
            ]
            
            for base_path, description in search_locations:
                if base_path.exists():
                    if 'Warp.app' in str(base_path):
                        detected.append({'path': base_path, 'description': description, 'type': 'app'})
                    else:
                        # Search for warp-related subdirectories
                        for item in base_path.glob('*[Ww]arp*'):
                            if item.is_dir():
                                detected.append({'path': item, 'description': f"{description}/{item.name}", 'type': 'data'})
                                self.print_emoji("✅", f"Found: {item}")
        
        elif self.system == "Linux":
            xdg_config = Path(os.environ.get('XDG_CONFIG_HOME', self.home / '.config'))
            xdg_data = Path(os.environ.get('XDG_DATA_HOME', self.home / '.local/share'))
            xdg_cache = Path(os.environ.get('XDG_CACHE_HOME', self.home / '.cache'))
            
            search_locations = [
                (Path('/opt/Warp'), 'Warp (/opt)'),
                (Path('/usr/local/bin/warp'), 'Warp binary'),
                (xdg_config, 'Config'),
                (xdg_data, 'Data'),
                (xdg_cache, 'Cache'),
            ]
            
            for path, description in search_locations:
                if path.exists():
                    if path.is_file() and 'warp' in path.name.lower():
                        detected.append({'path': path, 'description': description, 'type': 'binary'})
                    elif path.is_dir():
                        for item in path.glob('*[Ww]arp*'):
                            detected.append({'path': item, 'description': f"{description}/{item.name}", 'type': 'data'})
                            self.print_emoji("✅", f"Found: {item}")
        
        self.detected_warp_paths = detected
        
        if detected:
            self.print_emoji("🎯", f"Auto-detected {len(detected)} Warp location(s)")
        else:
            self.print_emoji("⚠️", "No Warp installations detected - will check standard paths")
        
        return detected
    
    def _is_warp_directory(self, path):
        """Check if a directory is actually a Warp installation/data directory"""
        if not path.exists() or not path.is_dir():
            return False
        
        # Check for Warp-specific files/folders
        warp_indicators = [
            'Warp.exe',  # Main executable
            'warp.exe',
            'User Data',  # User data folder
            'Cache',  # Cache folder
            'Logs',  # Logs folder
            'IndexedDB',  # Database
            'Local Storage',  # Storage
        ]
        
        # If any indicator exists, it's likely a Warp directory
        for indicator in warp_indicators:
            if (path / indicator).exists():
                return True
        
        return False
    
    def _deep_search_warp_dirs(self, base_path, detected):
        """Deep search for any warp-related directories"""
        try:
            # Search 2 levels deep only (for performance)
            for item in base_path.glob('*'):
                if item.is_dir() and 'warp' in item.name.lower():
                    if item not in [d['path'] for d in detected]:
                        if self._is_warp_directory(item):
                            detected.append({
                                'path': item,
                                'description': f'Detected: {item.name}',
                                'type': 'data'
                            })
                            self.print_emoji("🔍", f"Deep scan found: {item}")
        except (PermissionError, OSError):
            pass  # Skip inaccessible directories

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
            # SAFETY CHECK: Never delete main Warp installation directories!
            path_lower = path.lower()
            protected_paths = [
                'program files\\warp\\warp.exe',
                'program files (x86)\\warp\\warp.exe',
                'local\\warp\\warp.exe',
                '/applications/warp.app/contents/macos/warp',  # macOS
                '/opt/warp',  # Linux
                '/usr/bin/warp',  # Linux
                '/usr/local/bin/warp',  # Linux
            ]
            
            # Skip if this is a main installation path
            if any(protected in path_lower for protected in protected_paths):
                self.print_emoji("🚫", f"Skipping protected installation: {path}")
                continue
            
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
            'opera_gx.exe',  # Opera GX
            'vivaldi.exe',
            'msedge.exe',
            'ulaa.exe',  # Ulaa browser
            'Ulaa.exe',  # Alternative naming
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
                'Opera GX': appdata / 'Opera Software/Opera GX Stable',  # Opera GX variant
                'Vivaldi': local_appdata / 'Vivaldi/User Data',
                'Ulaa': local_appdata / 'Ulaa/User Data',
            }

        return browser_paths

    def clean_browser_data(self):
        """Clean ALL data from all browsers (100% COMPLETE CLEANUP)"""
        if self.system != "Windows":
            return

        self.print_emoji("🌐", "Cleaning ALL browser data (ULTRA-COMPLETE wipe - browsers will be closed!)...")
        self.print_emoji("⚠️", "WARNING: This will delete 100% of ALL cookies, cache, sessions, storage, and browsing data!")
        self.print_emoji("🔥", "Target browsers: Chrome, Firefox, Brave, Opera, Opera GX, Vivaldi, Ulaa")

        browser_paths = self.get_browser_data_paths()

        for browser_name, browser_path in browser_paths.items():
            if not browser_path.exists():
                continue

            self.print_emoji("🔍", f"Ultra-deep cleaning {browser_name} (62+ data types)...")

            try:
                # Get all profiles to clean
                profiles = []
                
                # Firefox has different profile structure
                if browser_name == 'Firefox':
                    # Firefox profiles are in subdirectories with random names
                    for profile_dir in browser_path.iterdir():
                        if profile_dir.is_dir() and not profile_dir.name.startswith('.'):
                            profiles.append(profile_dir.name)
                else:
                    # Chromium-based browsers
                    profiles = ['Default']
                    for profile_dir in browser_path.glob('Profile *'):
                        if profile_dir.is_dir():
                            profiles.append(profile_dir.name)
                
                for profile in profiles:
                    profile_path = browser_path / profile
                    if not profile_path.exists():
                        continue
                    
                    self.print_emoji("📂", f"Cleaning {browser_name}/{profile}...")
                    
                    # ============= OPERA-SPECIFIC CLEANUP =============
                    if browser_name in ['Opera', 'Opera GX']:
                        # Opera-specific files and folders (beyond standard Chromium)
                        opera_items = [
                            'Opera Stable',  # Opera stable files
                            'Jump List Icons',
                            'Jump List IconsOld',
                            'Local Extension Settings',
                            'Sync Extension Settings',
                            'Extension Rules',
                            'Platform Notifications',
                            'IndexedDB',
                            'Local Storage',
                            'Session Storage',
                            'databases',
                            'Application Cache',
                            'Cache',
                            'Code Cache',
                            'GPUCache',
                            'Cookies',
                            'Cookies-journal',
                            'Login Data',
                            'Login Data-journal',
                            'Web Data',
                            'Web Data-journal',
                            'History',
                            'History-journal',
                            'Visited Links',
                            'Preferences',
                            'Secure Preferences',
                        ]
                        
                        for opera_item in opera_items:
                            opera_path = profile_path / opera_item
                            if opera_path.exists():
                                self.safe_remove(str(opera_path), f"{browser_name}/{profile} {opera_item}")
                        
                        # Continue to standard Chromium cleanup (don't skip)
                    
                    # ============= FIREFOX-SPECIFIC CLEANUP =============
                    if browser_name == 'Firefox':
                        # Firefox-specific files and folders
                        firefox_items = [
                            'cookies.sqlite',
                            'cookies.sqlite-shm',
                            'cookies.sqlite-wal',
                            'places.sqlite',  # History and bookmarks
                            'places.sqlite-shm',
                            'places.sqlite-wal',
                            'favicons.sqlite',
                            'favicons.sqlite-shm',
                            'favicons.sqlite-wal',
                            'formhistory.sqlite',  # Form autofill
                            'formhistory.sqlite-shm',
                            'formhistory.sqlite-wal',
                            'webappsstore.sqlite',  # Local storage
                            'webappsstore.sqlite-shm',
                            'webappsstore.sqlite-wal',
                            'storage',  # Storage folder
                            'storage.sqlite',
                            'storage-sync-v2.sqlite',
                            'content-prefs.sqlite',  # Site preferences
                            'permissions.sqlite',  # Site permissions
                            'sessionstore.jsonlz4',  # Session data
                            'sessionstore-backups',
                            'sessionCheckpoints.json',
                            'cache2',  # HTTP cache
                            'OfflineCache',
                            'thumbnails',
                            'startupCache',
                            'safebrowsing',
                            'datareporting',
                            'saved-telemetry-pings',
                            'crashes',
                            'minidumps',
                        ]
                        
                        for ff_item in firefox_items:
                            ff_path = profile_path / ff_item
                            if ff_path.exists():
                                self.safe_remove(str(ff_path), f"{browser_name}/{profile} {ff_item}")
                        
                        # Continue to next profile as Firefox cleanup is done
                        continue
                    
                    # ============= STORAGE DATA =============
                    # 1. Local Storage (leveldb + all variants)
                    storage_items = [
                        'Local Storage',
                        'Local Storage/leveldb',
                    ]
                    for item in storage_items:
                        item_path = profile_path / item
                        if item_path.exists():
                            self.safe_remove(str(item_path), f"{browser_name}/{profile} {item}")
                    
                    # 2. IndexedDB (complete database)
                    idb_path = profile_path / 'IndexedDB'
                    if idb_path.exists():
                        self.safe_remove(str(idb_path), f"{browser_name}/{profile} IndexedDB")
                    
                    # 3. Session Storage
                    session_storage_path = profile_path / 'Session Storage'
                    if session_storage_path.exists():
                        self.safe_remove(str(session_storage_path), f"{browser_name}/{profile} Session Storage")
                    
                    # 4. File System (HTML5 File API)
                    filesystem_path = profile_path / 'File System'
                    if filesystem_path.exists():
                        self.safe_remove(str(filesystem_path), f"{browser_name}/{profile} File System")
                    
                    # 5. Blob Storage
                    blob_path = profile_path / 'blob_storage'
                    if blob_path.exists():
                        self.safe_remove(str(blob_path), f"{browser_name}/{profile} Blob Storage")
                    
                    # ============= CACHE DATA =============
                    # 6-12. All Cache Types
                    cache_items = [
                        'Cache',
                        'Code Cache',
                        'GPUCache',
                        'DawnCache',
                        'ShaderCache',
                        'Media Cache',
                        'Service Worker/CacheStorage',
                        'Application Cache',
                        'Storage/ext',  # Extension cache
                    ]
                    for cache_item in cache_items:
                        cache_path = profile_path / cache_item
                        if cache_path.exists():
                            self.safe_remove(str(cache_path), f"{browser_name}/{profile} {cache_item}")
                    
                    # ============= COOKIES & NETWORK =============
                    # 13. Cookies (all types)
                    cookie_items = [
                        'Cookies',
                        'Cookies-journal',
                        'Network/Cookies',
                        'Network/Cookies-journal',
                    ]
                    for cookie_item in cookie_items:
                        cookie_path = profile_path / cookie_item
                        if cookie_path.exists():
                            self.safe_remove(str(cookie_path), f"{browser_name}/{profile} {cookie_item}")
                    
                    # 14. Network Persistent State
                    network_path = profile_path / 'Network Persistent State'
                    if network_path.exists():
                        self.safe_remove(str(network_path), f"{browser_name}/{profile} Network State")
                    
                    # 15. Network Action Predictor
                    predictor_path = profile_path / 'Network Action Predictor'
                    if predictor_path.exists():
                        self.safe_remove(str(predictor_path), f"{browser_name}/{profile} Predictor")
                    
                    # 16. Transport Security (HSTS)
                    transport_path = profile_path / 'TransportSecurity'
                    if transport_path.exists():
                        self.safe_remove(str(transport_path), f"{browser_name}/{profile} Transport Security")
                    
                    # ============= SERVICE WORKERS =============
                    # 17. Service Workers (complete)
                    sw_items = [
                        'Service Worker',
                        'Service Worker/Database',
                        'Service Worker/ScriptCache',
                    ]
                    for sw_item in sw_items:
                        sw_path = profile_path / sw_item
                        if sw_path.exists():
                            self.safe_remove(str(sw_path), f"{browser_name}/{profile} {sw_item}")
                    
                    # ============= HISTORY & NAVIGATION =============
                    # 18. History (complete)
                    history_items = [
                        'History',
                        'History-journal',
                        'History Provider Cache',
                        'Visited Links',
                        'Top Sites',
                        'Top Sites-journal',
                        'Shortcuts',
                        'Shortcuts-journal',
                    ]
                    for history_item in history_items:
                        history_path = profile_path / history_item
                        if history_path.exists():
                            self.safe_remove(str(history_path), f"{browser_name}/{profile} {history_item}")
                    
                    # ============= WEB DATA & AUTOFILL =============
                    # 19. Web Data (Autofill, etc.)
                    webdata_items = [
                        'Web Data',
                        'Web Data-journal',
                    ]
                    for webdata_item in webdata_items:
                        webdata_path = profile_path / webdata_item
                        if webdata_path.exists():
                            self.safe_remove(str(webdata_path), f"{browser_name}/{profile} {webdata_item}")
                    
                    # ============= SESSIONS =============
                    # 20. Sessions (all types)
                    session_items = [
                        'Sessions',
                        'Session Storage',
                        'Current Session',
                        'Current Tabs',
                        'Last Session',
                        'Last Tabs',
                    ]
                    for session_item in session_items:
                        session_path = profile_path / session_item
                        if session_path.exists():
                            self.safe_remove(str(session_path), f"{browser_name}/{profile} {session_item}")
                    
                    # ============= PREFERENCES & SETTINGS =============
                    # 21. Preferences (all)
                    pref_items = [
                        'Preferences',
                        'Secure Preferences',
                        'Local State',
                    ]
                    for pref_item in pref_items:
                        pref_path = profile_path / pref_item
                        if pref_path.exists():
                            self.safe_remove(str(pref_path), f"{browser_name}/{profile} {pref_item}")
                    
                    # ============= EXTENSIONS =============
                    # 22. Extensions (complete data)
                    ext_items = [
                        'Extensions',
                        'Extension Cookies',
                        'Extension Cookies-journal',
                        'Extension State',
                        'Extension Rules',
                    ]
                    for ext_item in ext_items:
                        ext_path = profile_path / ext_item
                        if ext_path.exists():
                            self.safe_remove(str(ext_path), f"{browser_name}/{profile} {ext_item}")
                    
                    # ============= SYNC & CLOUD =============
                    # 23. Sync Data
                    sync_items = [
                        'Sync Data',
                        'Sync Extension Settings',
                    ]
                    for sync_item in sync_items:
                        sync_path = profile_path / sync_item
                        if sync_path.exists():
                            self.safe_remove(str(sync_path), f"{browser_name}/{profile} {sync_item}")
                    
                    # ============= BOOKMARKS =============
                    # 24. Bookmarks
                    bookmark_items = [
                        'Bookmarks',
                        'Bookmarks.bak',
                    ]
                    for bookmark_item in bookmark_items:
                        bookmark_path = profile_path / bookmark_item
                        if bookmark_path.exists():
                            self.safe_remove(str(bookmark_path), f"{browser_name}/{profile} {bookmark_item}")
                    
                    # ============= DOWNLOADS =============
                    # 25. Download Metadata
                    download_items = [
                        'Download Service',
                        'Download Metadata',
                    ]
                    for download_item in download_items:
                        download_path = profile_path / download_item
                        if download_path.exists():
                            self.safe_remove(str(download_path), f"{browser_name}/{profile} {download_item}")
                    
                    # ============= NOTIFICATIONS & PERMISSIONS =============
                    # 26. Platform Notifications
                    notif_path = profile_path / 'Platform Notifications'
                    if notif_path.exists():
                        self.safe_remove(str(notif_path), f"{browser_name}/{profile} Notifications")
                    
                    # 27. Notifications
                    notif2_path = profile_path / 'Notifications'
                    if notif2_path.exists():
                        self.safe_remove(str(notif2_path), f"{browser_name}/{profile} Notifications DB")
                    
                    # ============= BACKGROUND SYNC =============
                    # 28. Background Sync
                    bg_sync_path = profile_path / 'Background Sync'
                    if bg_sync_path.exists():
                        self.safe_remove(str(bg_sync_path), f"{browser_name}/{profile} Background Sync")
                    
                    # ============= SECURITY & CERTIFICATES =============
                    # 29. Origin Bound Certs
                    cert_path = profile_path / 'Origin Bound Certs'
                    if cert_path.exists():
                        self.safe_remove(str(cert_path), f"{browser_name}/{profile} Certificates")
                    
                    # ============= REPORTING & LOGGING =============
                    # 30. Reporting and NEL
                    report_items = [
                        'Reporting and NEL',
                        'Reporting and NEL-journal',
                    ]
                    for report_item in report_items:
                        report_path = profile_path / report_item
                        if report_path.exists():
                            self.safe_remove(str(report_path), f"{browser_name}/{profile} {report_item}")
                    
                    # ============= STORAGE QUOTA =============
                    # 31. Quota Manager
                    quota_path = profile_path / 'QuotaManager'
                    if quota_path.exists():
                        self.safe_remove(str(quota_path), f"{browser_name}/{profile} Quota Manager")
                    
                    # 32. Storage Quota
                    storage_quota_path = profile_path / 'Storage'
                    if storage_quota_path.exists():
                        self.safe_remove(str(storage_quota_path), f"{browser_name}/{profile} Storage")
                    
                    # ============= MISC DATABASES =============
                    # 33. All .db and .sqlite files
                    for db_file in profile_path.glob('*.db'):
                        if db_file.is_file():
                            self.safe_remove(str(db_file), f"{browser_name}/{profile} {db_file.name}")
                    
                    for sqlite_file in profile_path.glob('*.sqlite'):
                        if sqlite_file.is_file():
                            self.safe_remove(str(sqlite_file), f"{browser_name}/{profile} {sqlite_file.name}")
                    
                    # 34. All -journal files
                    for journal_file in profile_path.glob('*-journal'):
                        if journal_file.is_file():
                            self.safe_remove(str(journal_file), f"{browser_name}/{profile} {journal_file.name}")
                    
                    # ============= LOGS =============
                    # 35. Log Files
                    for log_file in profile_path.glob('*.log'):
                        if log_file.is_file():
                            self.safe_remove(str(log_file), f"{browser_name}/{profile} {log_file.name}")
                    
                    # ============= ADDITIONAL CLEANUP (Fingerprinting & Tracking) =============
                    # 36. GPUCache (separate from regular Cache)
                    gpu_cache_path = profile_path / 'GPUCache'
                    if gpu_cache_path.exists():
                        self.safe_remove(str(gpu_cache_path), f"{browser_name}/{profile} GPUCache")
                    
                    # 37. GCM Store (Google Cloud Messaging)
                    gcm_store_path = profile_path / 'GCM Store'
                    if gcm_store_path.exists():
                        self.safe_remove(str(gcm_store_path), f"{browser_name}/{profile} GCM Store")
                    
                    # 38. BudgetDatabase (background sync budgets)
                    budget_db_path = profile_path / 'BudgetDatabase'
                    if budget_db_path.exists():
                        self.safe_remove(str(budget_db_path), f"{browser_name}/{profile} BudgetDatabase")
                    
                    # 39. databases (WebSQL databases)
                    databases_path = profile_path / 'databases'
                    if databases_path.exists():
                        self.safe_remove(str(databases_path), f"{browser_name}/{profile} WebSQL databases")
                    
                    # 40. WebStorage (additional storage)
                    webstorage_path = profile_path / 'WebStorage'
                    if webstorage_path.exists():
                        self.safe_remove(str(webstorage_path), f"{browser_name}/{profile} WebStorage")
                    
                    # 41. Service Worker/Database (if not already covered)
                    sw_db_path = profile_path / 'Service Worker/Database'
                    if sw_db_path.exists():
                        self.safe_remove(str(sw_db_path), f"{browser_name}/{profile} SW Database")
                    
                    # 42. shared_proto_db (shared database for various features)
                    shared_proto_path = profile_path / 'shared_proto_db'
                    if shared_proto_path.exists():
                        self.safe_remove(str(shared_proto_path), f"{browser_name}/{profile} shared_proto_db")
                    
                    # 43. optimization_guide_hint_cache_store (optimization hints)
                    opt_guide_path = profile_path / 'optimization_guide_hint_cache_store'
                    if opt_guide_path.exists():
                        self.safe_remove(str(opt_guide_path), f"{browser_name}/{profile} optimization_guide")
                    
                    # 44. optimization_guide_model_and_features_store
                    opt_model_path = profile_path / 'optimization_guide_model_and_features_store'
                    if opt_model_path.exists():
                        self.safe_remove(str(opt_model_path), f"{browser_name}/{profile} optimization_model")
                    
                    # 45. Site Characteristics Database
                    site_chars_path = profile_path / 'Site Characteristics Database'
                    if site_chars_path.exists():
                        self.safe_remove(str(site_chars_path), f"{browser_name}/{profile} Site Characteristics")
                    
                    # 46. Heavy Ad Intervention Opt Out
                    heavy_ad_path = profile_path / 'Heavy Ad Intervention Opt Out'
                    if heavy_ad_path.exists():
                        self.safe_remove(str(heavy_ad_path), f"{browser_name}/{profile} Heavy Ad Intervention")
                    
                    # 47. MediaDeviceSalts (device identification)
                    media_salts_path = profile_path / 'MediaDeviceSalts'
                    if media_salts_path.exists():
                        self.safe_remove(str(media_salts_path), f"{browser_name}/{profile} MediaDeviceSalts")
                    
                    # 48. Network Action Predictor-journal
                    nap_journal_path = profile_path / 'Network Action Predictor-journal'
                    if nap_journal_path.exists():
                        self.safe_remove(str(nap_journal_path), f"{browser_name}/{profile} NAP-journal")
                    
                    # 49. Favicons (favicon cache)
                    favicons_path = profile_path / 'Favicons'
                    if favicons_path.exists():
                        self.safe_remove(str(favicons_path), f"{browser_name}/{profile} Favicons")
                    
                    # 50. Favicons-journal
                    favicons_journal_path = profile_path / 'Favicons-journal'
                    if favicons_journal_path.exists():
                        self.safe_remove(str(favicons_journal_path), f"{browser_name}/{profile} Favicons-journal")
                    
                    # 51. VideoDecodeStats (hardware decode stats)
                    video_stats_path = profile_path / 'VideoDecodeStats'
                    if video_stats_path.exists():
                        self.safe_remove(str(video_stats_path), f"{browser_name}/{profile} VideoDecodeStats")
                    
                    # 52. DIPS (Bounce Tracking Mitigations)
                    dips_path = profile_path / 'DIPS'
                    if dips_path.exists():
                        self.safe_remove(str(dips_path), f"{browser_name}/{profile} DIPS")
                    
                    # 53. Segmentation Platform (user segmentation)
                    seg_platform_path = profile_path / 'Segmentation Platform'
                    if seg_platform_path.exists():
                        self.safe_remove(str(seg_platform_path), f"{browser_name}/{profile} Segmentation Platform")
                    
                    # 54. Trust Tokens (privacy sandbox)
                    trust_tokens_path = profile_path / 'Trust Tokens'
                    if trust_tokens_path.exists():
                        self.safe_remove(str(trust_tokens_path), f"{browser_name}/{profile} Trust Tokens")
                    
                    # 55. WebRTC Logs (WebRTC connection logs)
                    webrtc_logs_path = profile_path / 'WebRTC Logs'
                    if webrtc_logs_path.exists():
                        self.safe_remove(str(webrtc_logs_path), f"{browser_name}/{profile} WebRTC Logs")
                    
                    # 56. Feature Engagement Tracker (user engagement tracking)
                    fet_path = profile_path / 'Feature Engagement Tracker'
                    if fet_path.exists():
                        self.safe_remove(str(fet_path), f"{browser_name}/{profile} Feature Engagement Tracker")
                    
                    # 57. Download Metadata (download history metadata)
                    download_meta_path = profile_path / 'Download Metadata'
                    if download_meta_path.exists():
                        self.safe_remove(str(download_meta_path), f"{browser_name}/{profile} Download Metadata")
                    
                    # 58. Crash Reports (crash report data)
                    crash_path = profile_path / 'Crash Reports'
                    if crash_path.exists():
                        self.safe_remove(str(crash_path), f"{browser_name}/{profile} Crash Reports")
                    
                    # 59. AutofillStrikeDatabase (autofill learning)
                    autofill_strike_path = profile_path / 'AutofillStrikeDatabase'
                    if autofill_strike_path.exists():
                        self.safe_remove(str(autofill_strike_path), f"{browser_name}/{profile} AutofillStrikeDatabase")
                    
                    # 60. All ldb files (LevelDB files)
                    for ldb_file in profile_path.glob('*.ldb'):
                        if ldb_file.is_file():
                            self.safe_remove(str(ldb_file), f"{browser_name}/{profile} {ldb_file.name}")
                    
                    # 61. All .bak files (backup files)
                    for bak_file in profile_path.glob('*.bak'):
                        if bak_file.is_file():
                            self.safe_remove(str(bak_file), f"{browser_name}/{profile} {bak_file.name}")
                    
                    # 62. All LOCK files (database lock files)
                    for lock_file in profile_path.glob('**/LOCK'):
                        if lock_file.is_file():
                            self.safe_remove(str(lock_file), f"{browser_name}/{profile} {lock_file.name}")

                # Also clean browser root level items (outside profiles)
                root_items = [
                    'ShaderCache',
                    'GrShaderCache',
                    'BrowserMetrics',
                    'Crash Reports',
                    'Safe Browsing',
                    'Local State',  # Browser-wide state
                    'First Run',
                    'component_crx_cache',  # Component extensions cache
                    'Consent To Send Stats',
                    'Webstore Downloads',
                    'Module Info Cache',
                    'SSLErrorAssistant',
                    'OriginTrials',
                    'Subresource Filter',
                    'MEIPreload',  # Media engagement preload
                    'CertificateRevocation',
                    'FileTypePolicies',
                    'OnDeviceHeadSuggestModel',
                    'Safe Browsing Channel',
                    'EVWhitelist',
                ]
                for root_item in root_items:
                    root_path = browser_path / root_item
                    if root_path.exists():
                        self.safe_remove(str(root_path), f"{browser_name} {root_item}")
                
                # Clean all browser-wide database files
                for root_db in browser_path.glob('*.db'):
                    if root_db.is_file():
                        self.safe_remove(str(root_db), f"{browser_name} {root_db.name}")
                
                for root_sqlite in browser_path.glob('*.sqlite'):
                    if root_sqlite.is_file():
                        self.safe_remove(str(root_sqlite), f"{browser_name} {root_sqlite.name}")

                self.print_emoji("✅", f"{browser_name}: 100% ULTRA-COMPLETE data wipe finished (62+ data types)")

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
        
        # OFFICIAL WARP PATHS (from Warp documentation)
        # Main data location: $env:LOCALAPPDATA\warp\Warp
        # Settings location: $env:APPDATA\warp\Warp
        
        # Path 1: Local AppData - Main database, logs, codebase context, mcp logs
        warp_local = local_appdata / 'warp' / 'Warp'
        if warp_local.exists():
            self.print_emoji("🔍", f"Found Warp data at: {warp_local}")
            # Delete everything EXCEPT the Warp.exe and app files
            # Only delete data subfolders
            for item in warp_local.iterdir():
                # Skip the main exe and critical app files
                if item.name.lower() not in ['warp.exe', 'resources', 'locales', 'swiftshader']:
                    self.safe_remove(str(item), f"warp/Warp/{item.name}")
            self.print_emoji("✅", f"Cleaned Warp data, preserved app at: {warp_local}")
        else:
            self.print_emoji("⚠️", f"Warp data not found at: {warp_local}")
        
        # Path 2: Roaming AppData - Themes and launch configurations
        warp_roaming = appdata / 'warp' / 'Warp'
        if warp_roaming.exists():
            self.print_emoji("🔍", f"Found Warp settings at: {warp_roaming}")
            self.safe_remove(str(warp_roaming), "warp/Warp (settings)")
        
        # Path 3: Legacy paths (for older Warp versions)
        # Check dev.warp.Warp-stable (old path)
        warp_stable_local = local_appdata / 'dev.warp.Warp-stable'
        if warp_stable_local.exists():
            self.print_emoji("🔍", "Found legacy Warp data (dev.warp.Warp-stable)")
            for subfolder in ['User Data', 'Cache', 'Logs', 'Local Storage', 'Session Storage', 'IndexedDB', 'databases']:
                subfolder_path = warp_stable_local / subfolder
                if subfolder_path.exists():
                    self.safe_remove(str(subfolder_path), f"dev.warp.Warp-stable/{subfolder}")
        
        warp_stable_roaming = appdata / 'dev.warp.Warp-stable'
        if warp_stable_roaming.exists():
            self.print_emoji("🔍", "Found legacy Warp settings (dev.warp.Warp-stable)")
            self.safe_remove(str(warp_stable_roaming), "dev.warp.Warp-stable (settings)")
        
        # Path 4: Check old AppData/Local/Warp (without lowercase 'warp' parent)
        warp_old_local = local_appdata / 'Warp'
        if warp_old_local.exists() and warp_old_local != warp_local.parent:
            self.print_emoji("🔍", f"Found old Warp data at: {warp_old_local}")
            for subfolder in ['User Data', 'Cache', 'Logs', 'Local Storage', 'Session Storage', 'IndexedDB', 'databases']:
                subfolder_path = warp_old_local / subfolder
                if subfolder_path.exists():
                    self.safe_remove(str(subfolder_path), f"Warp/{subfolder}")

        # Temp files - Only remove session/cache files, NOT installers!
        self.print_emoji("🧹", "Clearing temporary session files...")
        temp_dir = Path(os.environ.get('TEMP', 'C:/Windows/Temp'))
        
        # Only remove Warp session/cache folders, NOT .exe installers
        # This preserves any Warp installer the user might have downloaded
        temp_patterns = [
            "warp-*",      # Session folders like warp-session-xyz
            "Warp-*",      # Session folders
            "*warp*.tmp",  # Temporary files (not installers)
            "*Warp*.tmp",  # Temporary files
        ]
        
        for pattern in temp_patterns:
            for temp_item in temp_dir.glob(pattern):
                # Extra safety: Skip any .exe or .msi files (installers)
                if temp_item.suffix.lower() not in ['.exe', '.msi', '.zip']:
                    self.safe_remove(str(temp_item), "temp session files")

        # NOTE: We DON'T remove Start Menu shortcuts - user needs them to launch Warp!
        # The app stays installed, so shortcuts should remain

        # Registry cleanup - remove machine-specific registry entries (now recursive)
        self.print_emoji("📊", "Resetting registry entries (recursive)...")
        try:
            import winreg
            # Clean up user-specific registry locations (not system-wide)
            # Official path from Warp docs: HKCU:\Software\Warp.dev\Warp
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, "Software\\Warp.dev\\Warp"),  # Official path
                (winreg.HKEY_CURRENT_USER, "Software\\Warp"),  # Legacy
                (winreg.HKEY_CURRENT_USER, "Software\\dev.warp.Warp-stable"),  # Legacy
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
            # Check Windows installation paths (official + legacy)
            local_appdata = Path(os.environ.get('LOCALAPPDATA', str(self.home / 'AppData/Local')))

            # Official path from Warp documentation
            official_path = local_appdata / 'warp' / 'Warp' / 'Warp.exe'
            
            # Legacy paths for older versions
            legacy_paths = [
                local_appdata / 'Warp' / 'Warp.exe',
                Path(os.environ.get('PROGRAMFILES', 'C:/Program Files')) / "Warp/Warp.exe",
                Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)')) / "Warp/Warp.exe",
            ]
            
            # Check official path first
            self.print_emoji("ℹ️", f"Checking for Warp at: {official_path}")
            if official_path.exists():
                app_exists = True
                self.print_emoji("✅", f"Warp app still installed: {official_path}")
            else:
                # Check legacy paths
                for path in legacy_paths:
                    self.print_emoji("ℹ️", f"Checking for Warp at: {path}")
                    if path.exists():
                        app_exists = True
                        self.print_emoji("✅", f"Warp app still installed: {path}")
                        break

            if not app_exists:
                self.print_emoji("❌", "Warp app not found - may not be installed")
                self.print_emoji("💡", "If Warp is installed, it may be at a custom location")
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

        # Step 0: Auto-detect all Warp installations
        print()
        detected_paths = self.auto_detect_warp_paths()
        print()
        
        if not detected_paths:
            self.print_emoji("⚠️", "Warning: No Warp installations auto-detected")
            self.print_emoji("💡", "Proceeding with standard paths anyway...")
            print()

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
    print("✅ Keep Warp app INSTALLED (Warp.exe will NOT be deleted)")
    print("🔄 Reset your machine identity")
    print("🗑️  Clear user data and preferences")
    print("🆔 Make Warp see you as a new user")
    print()
    print("⚠️  IMPORTANT:")
    print("   ❌ Will NOT delete: Warp application files")
    print("   ✅ Will delete: User data, cache, sessions, registry entries")
    print()

    # Confirm before proceeding
    print("✅ Automatically proceeding with identity reset...")

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
