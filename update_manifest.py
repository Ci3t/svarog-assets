#!/usr/bin/env python3
"""
Svarog Asset Manifest Updater
Updates manifest.json for Genshin/WuWa banner images.
Usage:
  python update_manifest.py --game genshin --slot character --name "Lauma" --match "lauma,lauma / nefer,nefer" --image genshin/lauma-2026-05.webp
  python update_manifest.py --game genshin --slot weapon --name "Current Genshin Weapon" --match "weapon,weapon_banner,current weapon banner" --image genshin/lauma-weapon-2026-05.webp
  python update_manifest.py --game wuwa --slot character --name "Hiyuki" --match "hiyuki" --image wuwa/hiyuki-2026-05.webp
  python update_manifest.py --game wuwa --slot weapon --name "Frostburn" --match "frostburn" --image wuwa/frostburn-2026-05.webp
"""

import argparse
import json
import os
import sys

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "manifest.json")
BASE_URL = "https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/"
PURGE_URL = "https://purge.jsdelivr.net/gh/Ci3t/svarog-assets@main/manifest.json"


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_manifest(data):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_manifest(game, slot, name, match_list, image):
    if game not in ("genshin", "wuwa"):
        print(f"Error: --game must be 'genshin' or 'wuwa', got '{game}'")
        sys.exit(1)
    if slot not in ("character", "weapon"):
        print(f"Error: --slot must be 'character' or 'weapon', got '{slot}'")
        sys.exit(1)

    # Validate image file exists
    repo_root = os.path.dirname(MANIFEST_PATH)
    image_path = os.path.join(repo_root, image)
    if not os.path.isfile(image_path):
        print(f"Error: image file not found: {image_path}")
        sys.exit(1)

    manifest = load_manifest()

    if game not in manifest:
        manifest[game] = {}
    if slot not in manifest[game]:
        manifest[game][slot] = {}

    manifest[game][slot] = {
        "name": name,
        "match": [m.strip() for m in match_list.split(",") if m.strip()],
        "image": image,
    }

    save_manifest(manifest)

    print(f"Updated manifest.json:")
    print(f"  [{game}][{slot}] = {name}")
    print(f"  image: {image}")
    print(f"  match: {manifest[game][slot]['match']}")
    print()
    print(f"jsDelivr image URL:")
    print(f"  {BASE_URL}{image}")
    print()
    print(f"Purge URL (if jsDelivr is stale):")
    print(f"  {PURGE_URL}")


def main():
    parser = argparse.ArgumentParser(
        description="Update svarog-assets manifest.json for Genshin/WuWa banner images."
    )
    parser.add_argument("--game", required=True, choices=["genshin", "wuwa"])
    parser.add_argument("--slot", required=True, choices=["character", "weapon"])
    parser.add_argument("--name", required=True, help="Display name")
    parser.add_argument(
        "--match", required=True, help="Comma-separated match strings"
    )
    parser.add_argument(
        "--image", required=True, help="Relative image path, e.g. genshin/lauma-2026-05.webp"
    )
    args = parser.parse_args()

    update_manifest(args.game, args.slot, args.name, args.match, args.image)


if __name__ == "__main__":
    main()
