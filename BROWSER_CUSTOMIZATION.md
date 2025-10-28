# 🌐 Browser Cleanup - Customization Notes

## ✅ Changes Made (User Request)

### 1. **Microsoft Edge - EXCLUDED** ❌
```python
# 'Edge': local_appdata / 'Microsoft/Edge/User Data',  # Excluded by user request
```

**Reason:** User preference - Edge ko clean nahi karna hai

**Location:** 
- `warp_remover.py` - Line 252
- `warp_id_reset.py` - Line 143

---

### 2. **Ulaa Browser - ADDED** ✅
```python
'Ulaa': local_appdata / 'Ulaa/User Data',  # Added Ulaa browser support
```

**Browser Info:**
- Name: Ulaa Browser
- Type: Indian browser (Made in India)
- Path: `C:\Users\Admin\AppData\Local\Ulaa\User Data`

**Location:**
- `warp_remover.py` - Line 257
- `warp_id_reset.py` - Line 148

---

## 📊 Updated Browser List

### Browsers that WILL be cleaned:
1. ✅ **Google Chrome** - `%LOCALAPPDATA%\Google\Chrome\User Data`
2. ✅ **Mozilla Firefox** - `%APPDATA%\Mozilla\Firefox\Profiles`
3. ✅ **Brave Browser** - `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data`
4. ✅ **Opera** - `%APPDATA%\Opera Software\Opera Stable`
5. ✅ **Vivaldi** - `%LOCALAPPDATA%\Vivaldi\User Data`
6. ✅ **Ulaa Browser** - `%LOCALAPPDATA%\Ulaa\User Data`

### Browsers that will NOT be cleaned:
1. ❌ **Microsoft Edge** - Excluded by user preference

---

## 🔧 How to Add More Browsers

अगर आप और browsers add करना चाहें:

```python
# warp_remover.py और warp_id_reset.py दोनों में
def get_browser_data_paths(self):
    browser_paths = {
        'Chrome': local_appdata / 'Google/Chrome/User Data',
        'YourBrowser': local_appdata / 'YourBrowserPath/User Data',  # Add here
    }
```

### Popular Browsers की Paths:

**Chromium-based:**
```python
'Arc': local_appdata / 'Arc/User Data'
'Sidekick': local_appdata / 'Sidekick/User Data'
'Iridium': local_appdata / 'Iridium/User Data'
'Cent': local_appdata / 'CentBrowser/User Data'
```

**Other Browsers:**
```python
'Tor': appdata / 'tor browser/Browser/TorBrowser/Data/Browser'
'Waterfox': appdata / 'Waterfox/Profiles'
'Pale Moon': appdata / 'Moonchild Productions/Pale Moon/Profiles'
```

---

## ⚙️ How to Exclude More Browsers

किसी browser को exclude करने के लिए:

```python
# Method 1: Comment out (recommended)
# 'BrowserName': path,  # Excluded because...

# Method 2: Delete the line completely
# (not recommended - कम से कम comment रखें)
```

---

## 🔍 What Gets Cleaned in Each Browser?

```
Browser Path/
├── Local Storage/
│   └── *warp* files ✅ (Cleaned)
├── IndexedDB/
│   └── *warp* entries ✅ (Cleaned)
├── Session Storage/
│   └── *warp* data ✅ (Cleaned)
├── Cache/
│   └── *warp* files ✅ (Cleaned)
├── Cookies ⚠️ (Detected only, not cleaned)
└── Other files ❌ (Not touched)
```

---

## 💡 Pro Tips:

1. **Browser band rakhein** cleanup ke time
   - Browser open ho तो कुछ files locked रह सकती हैं

2. **Backup important data**
   - हालांकि सिर्फ Warp-related data clean होता है
   - लेकिन सावधानी के लिए

3. **Check browser path**
   - अगर custom location में install है browser
   - तो manually path verify करें

4. **Portable browsers**
   - Portable versions के लिए अलग paths हो सकते हैं
   - Those won't be cleaned automatically

---

## 📝 Testing Notes:

**Before running script:**
```powershell
# Check if Ulaa is installed
Test-Path "$env:LOCALAPPDATA\Ulaa\User Data"

# Check if Edge exists (but won't be cleaned)
Test-Path "$env:LOCALAPPDATA\Microsoft\Edge\User Data"
```

**After running script:**
```powershell
# Verify Ulaa was cleaned
Get-ChildItem "$env:LOCALAPPDATA\Ulaa\User Data" -Recurse -Filter "*warp*"

# Verify Edge was NOT touched
Get-ChildItem "$env:LOCALAPPDATA\Microsoft\Edge\User Data" -Recurse -Filter "*warp*"
# Should still exist if Edge had Warp data
```

---

## ✅ Summary:

- **Total Browsers Supported:** 6 (was 6, still 6)
- **Edge:** ❌ Removed from cleanup list
- **Ulaa:** ✅ Added to cleanup list
- **Other Browsers:** Unchanged

**All changes applied to both:**
- ✅ `warp_remover.py`
- ✅ `warp_id_reset.py`

---

**Last Updated:** 2025-10-28  
**Customized for:** User preference (Edge exclusion + Ulaa support)
