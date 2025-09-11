#!/bin/bash
# 🔄 Warp Identity Reset for Linux - Standalone Script
# Keeps Warp installed but resets machine identity

echo "================================================"
echo "🐧 WARP IDENTITY RESET FOR LINUX"
echo "================================================"
echo "This will reset your Warp identity while keeping it installed"
echo ""

# Confirm before proceeding
read -p "⚠️  Reset Warp machine identity? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled by user"
    exit 1
fi

echo ""
echo "🔄 Starting identity reset..."

# Kill Warp processes
echo "🔫 Stopping Warp processes..."
pkill -f -i warp 2>/dev/null || true
sleep 2

# Get home directory and XDG paths
HOME_DIR=$HOME
XDG_CONFIG=${XDG_CONFIG_HOME:-$HOME/.config}
XDG_DATA=${XDG_DATA_HOME:-$HOME/.local/share}
XDG_CACHE=${XDG_CACHE_HOME:-$HOME/.cache}
XDG_STATE=${XDG_STATE_HOME:-$HOME/.local/state}

# Clear configuration
echo "🔑 Clearing configuration..."
rm -rf "$XDG_CONFIG/warp" 2>/dev/null || true
rm -rf "$XDG_CONFIG/Warp" 2>/dev/null || true
rm -rf "$HOME/.warp" 2>/dev/null || true

# Clear application data
echo "📁 Clearing application data..."
rm -rf "$XDG_DATA/warp" 2>/dev/null || true
rm -rf "$XDG_DATA/Warp" 2>/dev/null || true

# Clear cache
echo "🧹 Clearing cache..."
rm -rf "$XDG_CACHE/warp" 2>/dev/null || true
rm -rf "$XDG_CACHE/Warp" 2>/dev/null || true

# Clear state and logs
echo "📋 Clearing state and logs..."
rm -rf "$XDG_STATE/warp" 2>/dev/null || true

# Clear temporary/runtime files
echo "🗑️ Clearing temporary files..."
rm -rf /tmp/warp-$USER 2>/dev/null || true
rm -rf /run/user/$(id -u)/warp 2>/dev/null || true

# Verify Warp is still installed
echo ""
echo "🔍 Verifying Warp installation..."
if command -v warp &> /dev/null; then
    echo "✅ Warp binary found at: $(which warp)"
elif [ -d "/opt/Warp" ]; then
    echo "✅ Warp found at: /opt/Warp"
elif [ -f "/usr/local/bin/warp" ]; then
    echo "✅ Warp found at: /usr/local/bin/warp"
elif [ -f "$HOME/.local/bin/warp" ]; then
    echo "✅ Warp found at: $HOME/.local/bin/warp"
else
    echo "⚠️ Warp not detected - may need to be installed"
fi

echo ""
echo "================================================"
echo "✅ WARP IDENTITY RESET COMPLETE!"
echo "🆔 Your machine now has a fresh identity"
echo "🚀 Launch Warp to start fresh!"
echo "================================================"
