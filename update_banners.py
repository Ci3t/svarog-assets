#!/usr/bin/env python3
"""
Svarog Banner Asset Updater

Drop your source images into ignore-upload/genshin/ or ignore-upload/wuwa/
Then run: python update_banners.py

This script will:
1. Find images in ignore-upload/
2. Convert them to .webp (if not already)
3. Move them to genshin/ or wuwa/ with a dated filename
4. Print the manifest.json entries you need to copy
"""

import os
import sys
from pathlib import Path
from PIL import Image

# Configuration
QUALITY = 85
IGNORE_DIR = Path("ignore-upload")
OUT_DIRS = {
    "genshin": Path("genshin"),
    "wuwa": Path("wuwa"),
}

def get_date_suffix():
    """Get current year-month for filename."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m")

def convert_to_webp(src: Path, dst: Path):
    """Convert image to webp with quality setting."""
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(dst, "WEBP", quality=QUALITY, method=6)
    print(f"  Converted: {src.name} -> {dst.name}")

def process_game(game_name: str):
    """Process all images in ignore-upload/{game_name}/"""
    src_dir = IGNORE_DIR / game_name
    if not src_dir.exists():
        print(f"[!] Source folder not found: {src_dir}")
        return

    out_dir = OUT_DIRS[game_name]
    out_dir.mkdir(exist_ok=True)

    files = [f for f in src_dir.iterdir() if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    if not files:
        print(f"[!] No images found in {src_dir}")
        return

    print(f"\n=== Processing {game_name.upper()} ===")
    date_suffix = get_date_suffix()

    for f in files:
        # Build output filename: use stem (no extension) + date + .webp
        stem = f.stem.replace(" ", "_").replace("'", "")
        out_name = f"{stem}-{date_suffix}.webp"
        out_path = out_dir / out_name

        if out_path.exists():
            print(f"  [Skip] Already exists: {out_name}")
            continue

        try:
            if f.suffix.lower() == ".webp":
                # Already webp, just copy
                import shutil
                shutil.copy2(f, out_path)
                print(f"  Copied: {f.name} -> {out_name}")
            else:
                convert_to_webp(f, out_path)

            size_kb = out_path.stat().st_size / 1024
            print(f"  -> {size_kb:.1f} KB")
        except Exception as e:
            print(f"  [Error] {f.name}: {e}")

    print(f"\n  Output folder: {out_dir.absolute()}")
    print(f"  Files: {list(out_dir.iterdir())}")

def show_manifest_template():
    """Print a template for updating manifest.json"""
    print("\n" + "="*60)
    print("MANIFEST UPDATE TEMPLATE")
    print("="*60)
    print("""
Update manifest.json with your new image paths. Example:

{
  "genshin": {
    "character": {
      "name": "Character Name",
      "match": ["name", "alt name"],
      "image": "genshin/name-YYYY-MM.webp"
    },
    "weapon": {
      "name": "Weapon Name",
      "match": ["weapon", "weapon banner"],
      "image": "genshin/weapon-YYYY-MM.webp"
    }
  },
  "wuwa": {
    "character": {
      "name": "Character Name",
      "match": ["name"],
      "image": "wuwa/name-YYYY-MM.webp"
    },
    "weapon": {
      "name": "Weapon Name",
      "match": ["weapon name"],
      "image": "wuwa/weapon-YYYY-MM.webp"
    }
  }
}
""")

def main():
    print("Svarog Banner Asset Updater")
    print("="*60)

    if not IGNORE_DIR.exists():
        print(f"[!] Creating {IGNORE_DIR}/ folder...")
        for game in OUT_DIRS:
            (IGNORE_DIR / game).mkdir(parents=True, exist_ok=True)
        print("    Done. Drop your source images there and run again.")
        return

    process_game("genshin")
    process_game("wuwa")
    show_manifest_template()

    print("\nNext steps:")
    print("  1. Update manifest.json with new image paths")
    print("  2. Open index.html to verify images load")
    print("  3. git add . && git commit -m 'Update banners'")
    print("  4. git push")

if __name__ == "__main__":
    main()
