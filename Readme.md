# Chrome WebApp Icon Fix Script

## Overview

On KDE Plasma, Chrome WebApps (PWAs) sometimes display the **default Google Chrome icon** instead of their individual app icons.
This happens because KDE falls back to the `google-chrome` icon when it cannot find the specific WebApp icon in the active icon theme.

For example:

* You install YouTube as a Chrome WebApp.
* KDE looks for `chrome-<app-id>.svg` or `chrome-<app-id>.png` in the current theme.
* If the icon is missing, KDE shows the generic Chrome icon instead.

---

## Problem

Chrome stores WebApp icons as PNG files in:

```
~/.config/google-chrome/Default/Web Applications/Manifest Resources/<app-id>/Icons/
```

with multiple sizes (32.png, 64.png, 128.png, 256.png, 512.png).

However:

* KDE does not automatically detect these PNGs in the Chrome profile directory.
* Themes may only have `scalable/apps/*.svg` icons, so PNG icons are ignored.
* KDE then falls back to the Google Chrome icon, causing inconsistent display.

---

## Solution

This Python script automates the process of creating scalable icons for KDE from Chrome WebApp PNGs.

### What it does:

1. Automatically detects the **active icon theme** in KDE Plasma 6.
2. Reads all Chrome WebApp `.desktop` files in `~/.local/share/applications/`.
3. Extracts the `Icon=` entry and calculates the corresponding Chrome WebApp ID.
4. Finds the **largest available PNG** for each WebApp.
5. Converts the PNG into a **scalable SVG** using Base64 embedding.
6. Saves the SVG in the appropriate theme folder:

```
~/.local/share/icons/<active-theme>/scalable/apps/chrome-<app-id>.svg
```

7. Updates the KDE icon cache (`kbuildsycoca6`) so the new icons appear immediately.

After running the script, all Chrome WebApps will show their proper icons instead of defaulting to the generic Chrome icon.

---

## Requirements

* Python 3
* `kreadconfig6` (comes with KDE Plasma 6)
* Google Chrome installed
* KDE Plasma (tested on Plasma 6, Debian 13)

---

## Usage

1. Save the script as `fix_chrome_webapp_icons.py`.
2. Make it executable:

```bash
chmod +x fix_chrome_webapp_icons.py
```

3. Run the script:

```bash
./fix_chrome_webapp_icons.py
```

4. Wait for the output; all WebApps with available PNG icons will have their SVGs generated.
5. Restart KDE Plasma or log out and back in to see updated icons.

---

## Notes

* The script uses **Base64 embedded PNG inside SVG**, ensuring compatibility with KDE scalable icons.
* Works only for WebApps installed in the default Chrome profile (`Default`).
* Automatically handles the `chrome-<id>-Default` naming scheme.
* Supports any active icon theme.

---

## License

This script is provided as-is, free to use and modify. No warranty is provided.
