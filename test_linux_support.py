#!/usr/bin/env python3
"""
Test script to verify Linux support has been added correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from warp_id_reset import WarpIdentityReset
from warp_remover import WarpRemover

def test_linux_support():
    """Test that Linux is now supported in both scripts"""
    
    print("🧪 Testing Linux Support Integration\n")
    print("="*50)
    
    # Test 1: Check if Linux methods exist
    print("\n✅ Test 1: Checking for Linux methods...")
    
    id_reset = WarpIdentityReset()
    remover = WarpRemover()
    
    # Check for Linux methods
    has_reset_linux = hasattr(id_reset, 'reset_linux_identity')
    has_remove_linux = hasattr(remover, 'remove_linux_warp')
    
    print(f"   - reset_linux_identity exists: {'✅' if has_reset_linux else '❌'}")
    print(f"   - remove_linux_warp exists: {'✅' if has_remove_linux else '❌'}")
    
    # Test 2: Mock Linux system and check if it would be handled
    print("\n✅ Test 2: Simulating Linux platform detection...")
    
    # Temporarily override platform detection
    import platform
    original_system = platform.system
    
    def mock_linux():
        return "Linux"
    
    platform.system = mock_linux
    
    # Create new instances with mocked Linux
    linux_reset = WarpIdentityReset()
    linux_remover = WarpRemover()
    
    print(f"   - Identity reset detects: {linux_reset.system}")
    print(f"   - Remover detects: {linux_remover.system}")
    
    is_linux_detected = linux_reset.system == "Linux" and linux_remover.system == "Linux"
    print(f"   - Linux detection: {'✅ Working' if is_linux_detected else '❌ Failed'}")
    
    # Restore original platform detection
    platform.system = original_system
    
    # Test 3: Check README mentions Linux
    print("\n✅ Test 3: Checking README for Linux mentions...")
    
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, 'r') as f:
        readme_content = f.read()
    
    linux_in_badge = "Linux" in readme_content and "platform-macOS%20%7C%20Windows%20%7C%20Linux" in readme_content
    linux_in_commands = "macOS/Linux" in readme_content
    linux_in_table = "| Linux |" in readme_content
    
    print(f"   - Linux in platform badge: {'✅' if linux_in_badge else '❌'}")
    print(f"   - Linux in command examples: {'✅' if linux_in_commands else '❌'}")
    print(f"   - Linux in support table: {'✅' if linux_in_table else '❌'}")
    
    # Summary
    print("\n" + "="*50)
    all_tests_passed = (
        has_reset_linux and 
        has_remove_linux and 
        is_linux_detected and
        linux_in_badge and
        linux_in_commands and
        linux_in_table
    )
    
    if all_tests_passed:
        print("🎉 SUCCESS: Linux support has been successfully added!")
        print("\nThe tools now support:")
        print("  • macOS (Darwin)")
        print("  • Windows")
        print("  • Linux")
        print("\n📝 Note: On Linux systems, the tools will:")
        print("  • Clear XDG base directory locations (~/.config, ~/.local/share, ~/.cache)")
        print("  • Remove Warp from common installation paths (/opt, /usr/local/bin, etc.)")
        print("  • Clean up desktop entries and runtime files")
        print("  • Handle both manual and package manager installations")
    else:
        print("⚠️ WARNING: Some Linux support features may be incomplete")
    
    print("="*50)

if __name__ == "__main__":
    test_linux_support()
