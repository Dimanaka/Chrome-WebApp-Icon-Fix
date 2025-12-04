#!/usr/bin/env python3
import os
import glob
import base64
import subprocess
from pathlib import Path

# --- Detect current icon theme ---
def get_active_icon_theme():
    try:
        result = subprocess.check_output([
            "kreadconfig6", "--file", "kdeglobals", "--group", "Icons", "--key", "Theme"
        ], text=True).strip()
        return result if result else "hicolor"
    except Exception:
        return "hicolor"

# --- Directories ---
HOME = Path.home()
DESKTOP_DIR = HOME / ".local/share/applications"
WEBAPPS_DIR = HOME / ".config/google-chrome/Default/Web Applications/Manifest Resources"

# Get icon theme directory
active_theme = get_active_icon_theme()
ICON_THEME_DIR = HOME / f".local/share/icons/{active_theme}/scalable/apps"
ICON_THEME_DIR.mkdir(parents=True, exist_ok=True)

print(f"=== Fix chrome web apps icons  ===")
print(f"Active icon theme: {active_theme}")

# --- Get all chrome-*.desktop ---
for desktop_file in DESKTOP_DIR.glob("chrome-*.desktop"):
    if not desktop_file.is_file():
        continue

    icon_entry = None
    with open(desktop_file, "r") as f:
        for line in f:
            if line.startswith("Icon="):
                icon_entry = line.strip().split("=", 1)[1]
                break

    if not icon_entry:
        continue

    app_id = icon_entry.replace("chrome-", "").replace("-Default", "")

    print(f"[*] Processing {desktop_file.name} → ID: {app_id}")

    icon_dir = WEBAPPS_DIR / app_id / "Icons"
    if not icon_dir.is_dir():
        print(f"    [!] {icon_dir} not found")
        continue

    # Search biggest PNG
    png_files = sorted(icon_dir.glob("*.png"), key=lambda p: int(p.stem) if p.stem.isdigit() else 0)
    if not png_files:
        print(f"    [!] No PNG found!")
        continue

    biggest_png = png_files[-1]
    print(f"Use PNG: {biggest_png}")

    target_svg = ICON_THEME_DIR / f"{icon_entry}.svg"

    # Make SVG icon from PNG
    with open(biggest_png, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512">
  <image href="data:image/png;base64,{b64_data}" width="512" height="512"/>
</svg>
"""
    with open(target_svg, "w") as f:
        f.write(svg_content)

    print(f"Make SVG: {target_svg}")

print("Update icons cache...")
subprocess.run(["kbuildsycoca6", "--noincremental"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("All done, reaccept icon theme or reboot system")
