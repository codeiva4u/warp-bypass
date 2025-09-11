#!/usr/bin/env python3
"""
Linux Support Analysis for Warp Bypass Tools
=============================================

This script analyzes what would be needed to add Linux support
to the warp-bypass tools.
"""

import platform
import os
from pathlib import Path

def analyze_linux_warp_paths():
    """
    Analyze typical Warp installation paths on Linux systems.
    Based on standard Linux filesystem hierarchy and common practices.
    """
    
    print("=== LINUX WARP PATH ANALYSIS ===\n")
    
    # Home directory
    home = Path.home()
    
    print("📍 EXPECTED WARP LOCATIONS ON LINUX:\n")
    
    # Application installations (typical Linux paths)
    linux_app_paths = [
        "/opt/Warp",                          # Common for third-party apps
        "/usr/local/bin/warp",                # User-installed binaries
        "/usr/bin/warp",                      # System binaries
        f"{home}/.local/bin/warp",           # User local binaries
        "/snap/warp",                         # Snap package
        "/var/lib/flatpak/app/dev.warp.Warp", # Flatpak
        "/usr/share/applications/warp.desktop", # Desktop entry
    ]
    
    print("🗂️ Probable Application Locations:")
    for path in linux_app_paths:
        print(f"   - {path}")
    
    print("\n📁 User Data & Configuration (Following XDG Base Directory spec):")
    
    # XDG Base Directory Specification paths
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME', f"{home}/.config")
    xdg_data_home = os.environ.get('XDG_DATA_HOME', f"{home}/.local/share")
    xdg_cache_home = os.environ.get('XDG_CACHE_HOME', f"{home}/.cache")
    xdg_state_home = os.environ.get('XDG_STATE_HOME', f"{home}/.local/state")
    
    linux_user_paths = {
        "Configuration": [
            f"{xdg_config_home}/warp",
            f"{xdg_config_home}/Warp",
            f"{home}/.warp",              # Legacy dot-file location
            f"{home}/.config/warp-terminal",
        ],
        "Application Data": [
            f"{xdg_data_home}/warp",
            f"{xdg_data_home}/Warp",
            f"{xdg_data_home}/applications/warp.desktop",
        ],
        "Cache": [
            f"{xdg_cache_home}/warp",
            f"{xdg_cache_home}/Warp",
        ],
        "State/Runtime": [
            f"{xdg_state_home}/warp",
            "/run/user/{uid}/warp".format(uid=os.getuid() if hasattr(os, 'getuid') else '1000'),
            f"/tmp/warp-{os.getenv('USER', 'user')}",
        ],
        "Logs": [
            f"{home}/.local/state/warp/logs",
            f"{xdg_state_home}/warp/logs",
            f"{home}/.warp/logs",
        ]
    }
    
    for category, paths in linux_user_paths.items():
        print(f"\n   {category}:")
        for path in paths:
            print(f"      - {path}")
    
    print("\n🔧 PROCESS MANAGEMENT ON LINUX:\n")
    print("   Commands to kill Warp processes:")
    print("      - pkill -f -i warp")
    print("      - killall -i warp")
    print("      - systemctl --user stop warp (if running as systemd service)")
    
    print("\n📋 PACKAGE MANAGEMENT CONSIDERATIONS:\n")
    print("   Depending on installation method:")
    print("      - APT/DEB: sudo apt remove warp")
    print("      - YUM/RPM: sudo yum remove warp")
    print("      - Snap: sudo snap remove warp")
    print("      - Flatpak: flatpak uninstall dev.warp.Warp")
    print("      - AppImage: Just delete the .AppImage file")
    print("      - Manual: Remove from /opt or installation directory")
    
    return linux_user_paths

def compare_with_macos():
    """Compare Linux paths with macOS paths to understand differences."""
    
    print("\n\n=== COMPARISON: LINUX vs macOS ===\n")
    
    home = Path.home()
    
    comparison = {
        "Application Location": {
            "macOS": "/Applications/Warp.app",
            "Linux": "/opt/Warp or /usr/local/bin/warp"
        },
        "User Config": {
            "macOS": f"{home}/Library/Preferences/*warp*",
            "Linux": f"{home}/.config/warp/"
        },
        "Application Data": {
            "macOS": f"{home}/Library/Application Support/*warp*",
            "Linux": f"{home}/.local/share/warp/"
        },
        "Cache": {
            "macOS": f"{home}/Library/Caches/*warp*",
            "Linux": f"{home}/.cache/warp/"
        },
        "Logs": {
            "macOS": f"{home}/Library/Logs/*warp*",
            "Linux": f"{home}/.local/state/warp/logs/"
        },
        "Process Management": {
            "macOS": "pkill -f -i warp",
            "Linux": "pkill -f -i warp (same)"
        }
    }
    
    for category, paths in comparison.items():
        print(f"{category}:")
        print(f"   📍 macOS: {paths['macOS']}")
        print(f"   🐧 Linux: {paths['Linux']}")
        print()

def generate_linux_code_snippet():
    """Generate code snippet for Linux support."""
    
    print("\n=== PROPOSED LINUX SUPPORT CODE ===\n")
    
    code = '''def reset_linux_identity(self):
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
    self.safe_remove(str(xdg_config / "warp"), "config")
    self.safe_remove(str(xdg_config / "Warp"), "config")
    self.safe_remove(str(self.home / ".warp"), "legacy config")
    
    # Application data
    self.print_emoji("📁", "Clearing application data...")
    self.safe_remove(str(xdg_data / "warp"), "app data")
    self.safe_remove(str(xdg_data / "Warp"), "app data")
    
    # Cache files
    self.print_emoji("🧹", "Clearing cache files...")
    self.safe_remove(str(xdg_cache / "warp"), "cache")
    self.safe_remove(str(xdg_cache / "Warp"), "cache")
    
    # State and logs
    self.print_emoji("📋", "Clearing state and logs...")
    self.safe_remove(str(xdg_state / "warp"), "state")
    
    # Temporary files
    self.print_emoji("🗑️", "Clearing temporary files...")
    self.safe_remove(f"/tmp/warp-{os.getenv('USER', '*')}", "temp files")
    self.safe_remove(f"/run/user/{os.getuid()}/warp", "runtime files")'''
    
    print(code)
    
    print("\n\n=== MAIN RUN() METHOD MODIFICATION ===\n")
    
    mod_code = '''# In the run() method, add Linux support:

# Step 2: Platform-specific identity reset
if self.system == "Darwin":  # macOS
    self.reset_macos_identity()
elif self.system == "Windows":
    self.reset_windows_identity()
elif self.system == "Linux":  # ADD THIS
    self.reset_linux_identity()
else:
    self.print_emoji("❌", f"Unsupported system: {self.system}")
    return False'''
    
    print(mod_code)

def main():
    """Main analysis function."""
    
    print("\n" + "="*60)
    print("🐧 LINUX SUPPORT ANALYSIS FOR WARP-BYPASS")
    print("="*60 + "\n")
    
    current_os = platform.system()
    print(f"Current OS: {current_os}\n")
    
    if current_os == "Linux":
        print("✅ Running on Linux - analyzing actual paths...\n")
    else:
        print("📝 Not on Linux - showing expected paths...\n")
    
    # Analyze Linux paths
    analyze_linux_warp_paths()
    
    # Compare with macOS
    compare_with_macos()
    
    # Generate code snippet
    generate_linux_code_snippet()
    
    print("\n" + "="*60)
    print("📌 SUMMARY: To add Linux support, the scripts need:")
    print("   1. Add 'Linux' case to platform detection")
    print("   2. Implement Linux-specific path handling (XDG spec)")
    print("   3. Handle different package managers for removal")
    print("   4. Test on actual Linux system with Warp installed")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
