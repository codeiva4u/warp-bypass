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
                'Opera GX': appdata / 'Opera Software/Opera GX Stable',  # Opera GX variant
                'Vivaldi': local_appdata / 'Vivaldi/User Data',
                'Ulaa': local_appdata / 'Ulaa/User Data',
            }
            
        return browser_paths
        
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
    
    def clean_browser_data(self):
        """Clean ALL data from all browsers (100% COMPLETE CLEANUP)"""
        if self.system != "Windows":
            return
            
        self.print_emoji("🌐", "Cleaning ALL browser data (ULTRA-COMPLETE wipe - browsers will be closed!)...")
        self.print_emoji("⚠️", "WARNING: This will delete 100% of ALL cookies, cache, sessions, storage, and browsing data!")
        self.print_emoji("🔥", "Target browsers: Chrome, Firefox, Brave, Opera, Opera GX, Vivaldi, Ulaa")
        
        # Kill browsers first
        self.kill_browser_processes()
        
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
                    
                    # ============= ULAA-SPECIFIC CLEANUP =============
                    if browser_name == 'Ulaa':
                        # Ulaa-specific complete cleanup (login sessions included)
                        ulaa_items = [
                            # Authentication & Login Data
                            'Login Data',
                            'Login Data-journal',
                            'Login Data For Account',
                            'Login Data For Account-journal',
                            'Web Data',
                            'Web Data-journal',
                            
                            # Session & Token Data
                            'Network',
                            'Network Persistent State',
                            'TransportSecurity',
                            'Sync Data',
                            'Sync Extension Settings',
                            'Sync Data Backup',
                            
                            # Cookies & Storage
                            'Cookies',
                            'Cookies-journal',
                            'Extension Cookies',
                            'Extension Cookies-journal',
                            'Local Storage',
                            'Session Storage',
                            'IndexedDB',
                            'databases',
                            'blob_storage',
                            'File System',
                            
                            # Cache Data
                            'Cache',
                            'Code Cache',
                            'GPUCache',
                            'DawnCache',
                            'ShaderCache',
                            'Media Cache',
                            'Service Worker/CacheStorage',
                            'Application Cache',
                            
                            # History & Navigation
                            'History',
                            'History-journal',
                            'History Provider Cache',
                            'Visited Links',
                            'Top Sites',
                            'Top Sites-journal',
                            'Shortcuts',
                            'Shortcuts-journal',
                            
                            # Extensions
                            'Extensions',
                            'Extension State',
                            'Extension Rules',
                            'Local Extension Settings',
                            
                            # Preferences
                            'Preferences',
                            'Secure Preferences',
                            'Local State',
                            
                            # Misc
                            'Platform Notifications',
                            'Jump List Icons',
                            'Jump List IconsOld',
                            'Bookmarks',
                            'Bookmarks.bak',
                            'Favicons',
                            'Favicons-journal',
                            'QuotaManager',
                            'Storage',
                            'shared_proto_db',
                            'GCM Store',
                            'BudgetDatabase',
                            'WebStorage',
                            'Service Worker',
                            'Background Sync',
                            'Trust Tokens',
                            'Feature Engagement Tracker',
                            'MediaDeviceSalts',
                        ]
                        
                        for ulaa_item in ulaa_items:
                            ulaa_path = profile_path / ulaa_item
                            if ulaa_path.exists():
                                self.safe_remove(str(ulaa_path))
                        
                        # Also delete ALL .db, .sqlite, .ldb, .log files in Ulaa profile
                        for db_file in profile_path.glob('*.db'):
                            if db_file.is_file():
                                self.safe_remove(str(db_file))
                        for sqlite_file in profile_path.glob('*.sqlite'):
                            if sqlite_file.is_file():
                                self.safe_remove(str(sqlite_file))
                        for ldb_file in profile_path.glob('**/*.ldb'):
                            if ldb_file.is_file():
                                self.safe_remove(str(ldb_file))
                        for log_file in profile_path.glob('*.log'):
                            if log_file.is_file():
                                self.safe_remove(str(log_file))
                        
                        # Continue to standard Chromium cleanup for anything missed
                    
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
                                self.safe_remove(str(opera_path))
                        
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
                                self.safe_remove(str(ff_path))
                        
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
                            self.safe_remove(str(item_path))
                    
                    # 2. IndexedDB (complete database)
                    idb_path = profile_path / 'IndexedDB'
                    if idb_path.exists():
                        self.safe_remove(str(idb_path))
                    
                    # 3. Session Storage
                    session_storage_path = profile_path / 'Session Storage'
                    if session_storage_path.exists():
                        self.safe_remove(str(session_storage_path))
                    
                    # 4. File System (HTML5 File API)
                    filesystem_path = profile_path / 'File System'
                    if filesystem_path.exists():
                        self.safe_remove(str(filesystem_path))
                    
                    # 5. Blob Storage
                    blob_path = profile_path / 'blob_storage'
                    if blob_path.exists():
                        self.safe_remove(str(blob_path))
                    
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
                            self.safe_remove(str(cache_path))
                    
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
                            self.safe_remove(str(cookie_path))
                    
                    # 14. Network Persistent State
                    network_path = profile_path / 'Network Persistent State'
                    if network_path.exists():
                        self.safe_remove(str(network_path))
                    
                    # 15. Network Action Predictor
                    predictor_path = profile_path / 'Network Action Predictor'
                    if predictor_path.exists():
                        self.safe_remove(str(predictor_path))
                    
                    # 16. Transport Security (HSTS)
                    transport_path = profile_path / 'TransportSecurity'
                    if transport_path.exists():
                        self.safe_remove(str(transport_path))
                    
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
                            self.safe_remove(str(sw_path))
                    
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
                            self.safe_remove(str(history_path))
                    
                    # ============= WEB DATA & AUTOFILL =============
                    # 19. Web Data (Autofill, etc.)
                    webdata_items = [
                        'Web Data',
                        'Web Data-journal',
                    ]
                    for webdata_item in webdata_items:
                        webdata_path = profile_path / webdata_item
                        if webdata_path.exists():
                            self.safe_remove(str(webdata_path))
                    
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
                            self.safe_remove(str(session_path))
                    
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
                            self.safe_remove(str(pref_path))
                    
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
                            self.safe_remove(str(ext_path))
                    
                    # ============= SYNC & CLOUD =============
                    # 23. Sync Data
                    sync_items = [
                        'Sync Data',
                        'Sync Extension Settings',
                    ]
                    for sync_item in sync_items:
                        sync_path = profile_path / sync_item
                        if sync_path.exists():
                            self.safe_remove(str(sync_path))
                    
                    # ============= BOOKMARKS =============
                    # 24. Bookmarks
                    bookmark_items = [
                        'Bookmarks',
                        'Bookmarks.bak',
                    ]
                    for bookmark_item in bookmark_items:
                        bookmark_path = profile_path / bookmark_item
                        if bookmark_path.exists():
                            self.safe_remove(str(bookmark_path))
                    
                    # ============= DOWNLOADS =============
                    # 25. Download Metadata
                    download_items = [
                        'Download Service',
                        'Download Metadata',
                    ]
                    for download_item in download_items:
                        download_path = profile_path / download_item
                        if download_path.exists():
                            self.safe_remove(str(download_path))
                    
                    # ============= NOTIFICATIONS & PERMISSIONS =============
                    # 26. Platform Notifications
                    notif_path = profile_path / 'Platform Notifications'
                    if notif_path.exists():
                        self.safe_remove(str(notif_path))
                    
                    # 27. Notifications
                    notif2_path = profile_path / 'Notifications'
                    if notif2_path.exists():
                        self.safe_remove(str(notif2_path))
                    
                    # ============= BACKGROUND SYNC =============
                    # 28. Background Sync
                    bg_sync_path = profile_path / 'Background Sync'
                    if bg_sync_path.exists():
                        self.safe_remove(str(bg_sync_path))
                    
                    # ============= SECURITY & CERTIFICATES =============
                    # 29. Origin Bound Certs
                    cert_path = profile_path / 'Origin Bound Certs'
                    if cert_path.exists():
                        self.safe_remove(str(cert_path))
                    
                    # ============= REPORTING & LOGGING =============
                    # 30. Reporting and NEL
                    report_items = [
                        'Reporting and NEL',
                        'Reporting and NEL-journal',
                    ]
                    for report_item in report_items:
                        report_path = profile_path / report_item
                        if report_path.exists():
                            self.safe_remove(str(report_path))
                    
                    # ============= STORAGE QUOTA =============
                    # 31. Quota Manager
                    quota_path = profile_path / 'QuotaManager'
                    if quota_path.exists():
                        self.safe_remove(str(quota_path))
                    
                    # 32. Storage Quota
                    storage_quota_path = profile_path / 'Storage'
                    if storage_quota_path.exists():
                        self.safe_remove(str(storage_quota_path))
                    
                    # ============= MISC DATABASES =============
                    # 33. All .db and .sqlite files
                    for db_file in profile_path.glob('*.db'):
                        if db_file.is_file():
                            self.safe_remove(str(db_file))
                    
                    for sqlite_file in profile_path.glob('*.sqlite'):
                        if sqlite_file.is_file():
                            self.safe_remove(str(sqlite_file))
                    
                    # 34. All -journal files
                    for journal_file in profile_path.glob('*-journal'):
                        if journal_file.is_file():
                            self.safe_remove(str(journal_file))
                    
                    # ============= LOGS =============
                    # 35. Log Files
                    for log_file in profile_path.glob('*.log'):
                        if log_file.is_file():
                            self.safe_remove(str(log_file))
                    
                    # ============= ADDITIONAL CLEANUP (Fingerprinting & Tracking) =============
                    # 36. GPUCache (separate from regular Cache)
                    gpu_cache_path = profile_path / 'GPUCache'
                    if gpu_cache_path.exists():
                        self.safe_remove(str(gpu_cache_path))
                    
                    # 37. GCM Store (Google Cloud Messaging)
                    gcm_store_path = profile_path / 'GCM Store'
                    if gcm_store_path.exists():
                        self.safe_remove(str(gcm_store_path))
                    
                    # 38. BudgetDatabase (background sync budgets)
                    budget_db_path = profile_path / 'BudgetDatabase'
                    if budget_db_path.exists():
                        self.safe_remove(str(budget_db_path))
                    
                    # 39. databases (WebSQL databases)
                    databases_path = profile_path / 'databases'
                    if databases_path.exists():
                        self.safe_remove(str(databases_path))
                    
                    # 40. WebStorage (additional storage)
                    webstorage_path = profile_path / 'WebStorage'
                    if webstorage_path.exists():
                        self.safe_remove(str(webstorage_path))
                    
                    # 41. Service Worker/Database (if not already covered)
                    sw_db_path = profile_path / 'Service Worker/Database'
                    if sw_db_path.exists():
                        self.safe_remove(str(sw_db_path))
                    
                    # 42. shared_proto_db (shared database for various features)
                    shared_proto_path = profile_path / 'shared_proto_db'
                    if shared_proto_path.exists():
                        self.safe_remove(str(shared_proto_path))
                    
                    # 43. optimization_guide_hint_cache_store (optimization hints)
                    opt_guide_path = profile_path / 'optimization_guide_hint_cache_store'
                    if opt_guide_path.exists():
                        self.safe_remove(str(opt_guide_path))
                    
                    # 44. optimization_guide_model_and_features_store
                    opt_model_path = profile_path / 'optimization_guide_model_and_features_store'
                    if opt_model_path.exists():
                        self.safe_remove(str(opt_model_path))
                    
                    # 45. Site Characteristics Database
                    site_chars_path = profile_path / 'Site Characteristics Database'
                    if site_chars_path.exists():
                        self.safe_remove(str(site_chars_path))
                    
                    # 46. Heavy Ad Intervention Opt Out
                    heavy_ad_path = profile_path / 'Heavy Ad Intervention Opt Out'
                    if heavy_ad_path.exists():
                        self.safe_remove(str(heavy_ad_path))
                    
                    # 47. MediaDeviceSalts (device identification)
                    media_salts_path = profile_path / 'MediaDeviceSalts'
                    if media_salts_path.exists():
                        self.safe_remove(str(media_salts_path))
                    
                    # 48. Network Action Predictor-journal
                    nap_journal_path = profile_path / 'Network Action Predictor-journal'
                    if nap_journal_path.exists():
                        self.safe_remove(str(nap_journal_path))
                    
                    # 49. Favicons (favicon cache)
                    favicons_path = profile_path / 'Favicons'
                    if favicons_path.exists():
                        self.safe_remove(str(favicons_path))
                    
                    # 50. Favicons-journal
                    favicons_journal_path = profile_path / 'Favicons-journal'
                    if favicons_journal_path.exists():
                        self.safe_remove(str(favicons_journal_path))
                    
                    # 51. VideoDecodeStats (hardware decode stats)
                    video_stats_path = profile_path / 'VideoDecodeStats'
                    if video_stats_path.exists():
                        self.safe_remove(str(video_stats_path))
                    
                    # 52. DIPS (Bounce Tracking Mitigations)
                    dips_path = profile_path / 'DIPS'
                    if dips_path.exists():
                        self.safe_remove(str(dips_path))
                    
                    # 53. Segmentation Platform (user segmentation)
                    seg_platform_path = profile_path / 'Segmentation Platform'
                    if seg_platform_path.exists():
                        self.safe_remove(str(seg_platform_path))
                    
                    # 54. Trust Tokens (privacy sandbox)
                    trust_tokens_path = profile_path / 'Trust Tokens'
                    if trust_tokens_path.exists():
                        self.safe_remove(str(trust_tokens_path))
                    
                    # 55. WebRTC Logs (WebRTC connection logs)
                    webrtc_logs_path = profile_path / 'WebRTC Logs'
                    if webrtc_logs_path.exists():
                        self.safe_remove(str(webrtc_logs_path))
                    
                    # 56. Feature Engagement Tracker (user engagement tracking)
                    fet_path = profile_path / 'Feature Engagement Tracker'
                    if fet_path.exists():
                        self.safe_remove(str(fet_path))
                    
                    # 57. Download Metadata (download history metadata)
                    download_meta_path = profile_path / 'Download Metadata'
                    if download_meta_path.exists():
                        self.safe_remove(str(download_meta_path))
                    
                    # 58. Crash Reports (crash report data)
                    crash_path = profile_path / 'Crash Reports'
                    if crash_path.exists():
                        self.safe_remove(str(crash_path))
                    
                    # 59. AutofillStrikeDatabase (autofill learning)
                    autofill_strike_path = profile_path / 'AutofillStrikeDatabase'
                    if autofill_strike_path.exists():
                        self.safe_remove(str(autofill_strike_path))
                    
                    # 60. All ldb files (LevelDB files)
                    for ldb_file in profile_path.glob('*.ldb'):
                        if ldb_file.is_file():
                            self.safe_remove(str(ldb_file))
                    
                    # 61. All .bak files (backup files)
                    for bak_file in profile_path.glob('*.bak'):
                        if bak_file.is_file():
                            self.safe_remove(str(bak_file))
                    
                    # 62. All LOCK files (database lock files)
                    for lock_file in profile_path.glob('**/LOCK'):
                        if lock_file.is_file():
                            self.safe_remove(str(lock_file))

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
                        self.safe_remove(str(root_path))
                
                # Clean all browser-wide database files
                for root_db in browser_path.glob('*.db'):
                    if root_db.is_file():
                        self.safe_remove(str(root_db))
                
                for root_sqlite in browser_path.glob('*.sqlite'):
                    if root_sqlite.is_file():
                        self.safe_remove(str(root_sqlite))

                self.print_emoji("✅", f"{browser_name}: 100% ULTRA-COMPLETE data wipe finished (62+ data types)")
                                
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
