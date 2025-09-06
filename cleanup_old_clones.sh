#!/bin/bash

echo "🧹 WARP-BYPASS CLEANUP SCRIPT"
echo "=============================="
echo ""

# Kill any running warp-bypass Python processes
echo "🔴 Killing any running warp-bypass processes..."
pkill -f "warp_id_reset.py" 2>/dev/null
pkill -f "warp_remover.py" 2>/dev/null
pkill -f "warp-bypass" 2>/dev/null
echo "✅ Processes stopped"
echo ""

# Find all warp-bypass directories
echo "🔍 Searching for all warp-bypass directories..."
DIRECTORIES=$(find /Users/munir011 -name "warp-bypass" -type d 2>/dev/null)

if [ -z "$DIRECTORIES" ]; then
    echo "❌ No warp-bypass directories found"
    exit 0
fi

echo "📁 Found the following directories:"
echo "$DIRECTORIES"
echo ""

# Current directory check
CURRENT_DIR=$(pwd)
CURRENT_BASENAME=$(basename "$CURRENT_DIR")

echo "⚠️  WARNING: About to delete ALL warp-bypass directories except current one!"
echo "Current directory: $CURRENT_DIR"
echo ""

read -p "🚨 Are you sure? This will permanently delete all old clones! (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🗑️  Deleting directories..."
    
    # Delete each directory
    while IFS= read -r dir; do
        # Skip if it's the current directory
        if [ "$dir" = "$CURRENT_DIR" ]; then
            echo "⏭️  Skipping current directory: $dir"
            continue
        fi
        
        echo "🗂️  Deleting: $dir"
        rm -rf "$dir"
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully deleted: $dir"
        else
            echo "❌ Failed to delete: $dir"
        fi
    done <<< "$DIRECTORIES"
    
    echo ""
    echo "🧹 Cleaning Python cache directories..."
    # Clean Python cache directories that might contain references
    rm -rf "/Users/munir011/Library/Caches/com.apple.python/Users/munir011/warp-bypass" 2>/dev/null
    rm -rf "/Users/munir011/Library/Caches/com.apple.python"/**/warp-bypass 2>/dev/null
    
    echo ""
    echo "✅ CLEANUP COMPLETE!"
    echo ""
    echo "📊 Remaining warp-bypass directories:"
    find /Users/munir011 -name "warp-bypass" -type d 2>/dev/null || echo "❌ None found (all cleaned up!)"
    
else
    echo ""
    echo "❌ Cleanup cancelled by user"
fi

echo ""
echo "🏁 Script finished"
