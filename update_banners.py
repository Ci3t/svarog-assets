#!/usr/bin/env python3
"""
Svarog Banner Asset Updater

Drop your source images into ignore-upload/genshin/ or ignore-upload/wuwa/
Then run: python update_banners.py

This script will:
1. Find images in ignore-upload/
2. Convert them to .webp (if not already)
3. Move them to genshin/ or wuwa/ with a dated filename
4. Regenerate index.html with embedded manifest (works without server)
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image

# Configuration
QUALITY = 85
IGNORE_DIR = Path("ignore-upload")
OUT_DIRS = {
    "genshin": Path("genshin"),
    "wuwa": Path("wuwa"),
}

def get_date_suffix():
    return datetime.now().strftime("%Y-%m")

def convert_to_webp(src: Path, dst: Path):
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(dst, "WEBP", quality=QUALITY, method=6)
    print(f"  Converted: {src.name} -> {dst.name}")

def process_game(game_name: str):
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
        stem = f.stem.replace(" ", "_").replace("'", "")
        out_name = f"{stem}-{date_suffix}.webp"
        out_path = out_dir / out_name

        if out_path.exists():
            print(f"  [Skip] Already exists: {out_name}")
            continue

        try:
            if f.suffix.lower() == ".webp":
                shutil.copy2(f, out_path)
                print(f"  Copied: {f.name} -> {out_name}")
            else:
                convert_to_webp(f, out_path)

            size_kb = out_path.stat().st_size / 1024
            print(f"  -> {size_kb:.1f} KB")
        except Exception as e:
            print(f"  [Error] {f.name}: {e}")

def load_manifest():
    try:
        with open("manifest.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Could not read manifest.json: {e}")
        return None

def generate_index_html(manifest_data):
    manifest_json = json.dumps(manifest_data, indent=2, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Svarog Banner Assets — Preview</title>
  <style>
    :root {{
      --bg: #0b0c10;
      --surface: #1f2833;
      --surface-hover: #2a3544;
      --accent: #66fcf1;
      --accent-dim: #45a29e;
      --text: #c5c6c7;
      --text-muted: #8a8d91;
      --border: #2a3544;
      --danger: #ff6b6b;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; }}
    header {{
      background: rgba(11,12,16,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border);
      padding: 1.5rem; text-align: center;
    }}
    h1 {{ margin: 0; font-size: 1.5rem; color: var(--accent); }}
    .subtitle {{ color: var(--text-muted); font-size: 0.85rem; margin-top: 0.3rem; }}
    main {{ max-width: 1200px; margin: 0 auto; padding: 1.5rem; }}
    .game-section {{ margin-bottom: 2rem; }}
    .game-title {{ font-size: 1.2rem; color: var(--accent); margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.2rem; }}
    .card {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      overflow: hidden; transition: transform 0.15s, box-shadow 0.15s;
    }}
    .card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 24px rgba(0,0,0,0.45); border-color: var(--accent-dim); }}
    .card-header {{ padding: 0.8rem 1rem; background: rgba(255,255,255,0.03); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
    .card-type {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--accent-dim); font-weight: 600; }}
    .card-name {{ font-weight: 600; font-size: 0.95rem; }}
    .card img {{ width: 100%; height: 200px; object-fit: contain; background: rgba(0,0,0,0.2); display: block; }}
    .card-footer {{ padding: 0.8rem 1rem; background: rgba(255,255,255,0.02); }}
    .filename {{ font-family: monospace; font-size: 0.8rem; color: var(--text-muted); word-break: break-all; }}
    .url {{ font-family: monospace; font-size: 0.7rem; color: var(--text-muted); margin-top: 0.3rem; word-break: break-all; opacity: 0.7; }}
    .match-tags {{ display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.5rem; }}
    .tag {{ background: rgba(102,252,241,0.1); color: var(--accent); padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.7rem; }}
    .empty {{ text-align: center; padding: 2rem; color: var(--text-muted); }}
    .info-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }}
    .info-box code {{ background: rgba(0,0,0,0.3); padding: 0.1rem 0.3rem; border-radius: 4px; font-size: 0.85rem; }}
    .status {{ font-size: 0.8rem; padding: 0.5rem 1rem; border-radius: 6px; margin-bottom: 1rem; }}
    .status.ok {{ background: rgba(102,252,241,0.1); color: var(--accent); border: 1px solid var(--accent-dim); }}
    .status.error {{ background: rgba(255,107,107,0.1); color: var(--danger); border: 1px solid var(--danger); }}
    footer {{ text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.8rem; border-top: 1px solid var(--border); }}
  </style>
</head>
<body>
  <header>
    <h1>Svarog Banner Assets</h1>
    <div class="subtitle">Local Preview &amp; Manifest Validator</div>
  </header>

  <main>
    <div class="info-box">
      <strong>Repo size:</strong> ~{get_repo_size():.0f} KB tracked | <strong>Rule:</strong> Never overwrite old filenames — jsDelivr caches aggressively.
    </div>
    <div id="content"></div>
  </main>

  <footer>
    Built for the Svarog project. Assets belong to their respective publishers.
  </footer>

  <script>
    const MANIFEST = {manifest_json};

    function render(data) {{
      const container = document.getElementById('content');
      container.innerHTML = '';

      for (const [gameKey, gameData] of Object.entries(data)) {{
        const section = document.createElement('div');
        section.className = 'game-section';

        const title = document.createElement('div');
        title.className = 'game-title';
        title.textContent = gameKey.toUpperCase();
        section.appendChild(title);

        const grid = document.createElement('div');
        grid.className = 'grid';

        for (const [typeKey, item] of Object.entries(gameData)) {{
          const card = document.createElement('div');
          card.className = 'card';

          const header = document.createElement('div');
          header.className = 'card-header';
          header.innerHTML = `<span class="card-type">${{typeKey}}</span><span class="card-name">${{item.name}}</span>`;
          card.appendChild(header);

          const img = document.createElement('img');
          img.src = item.image;
          img.alt = item.name;
          img.onerror = function() {{
            this.style.display = 'none';
            const err = document.createElement('div');
            err.style.cssText = 'padding:2rem;text-align:center;color:#ff6b6b;font-size:0.9rem;';
            err.textContent = 'Image not found locally: ' + item.image;
            card.insertBefore(err, card.querySelector('.card-footer'));
          }};
          card.appendChild(img);

          const footer = document.createElement('div');
          footer.className = 'card-footer';

          const filename = document.createElement('div');
          filename.className = 'filename';
          filename.textContent = item.image;
          footer.appendChild(filename);

          const url = document.createElement('div');
          url.className = 'url';
          url.textContent = 'https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/' + item.image;
          footer.appendChild(url);

          if (item.match && item.match.length) {{
            const tags = document.createElement('div');
            tags.className = 'match-tags';
            item.match.forEach(m => {{
              const tag = document.createElement('span');
              tag.className = 'tag';
              tag.textContent = m;
              tags.appendChild(tag);
            }});
            footer.appendChild(tags);
          }}

          card.appendChild(footer);
          grid.appendChild(card);
        }}

        section.appendChild(grid);
        container.appendChild(section);
      }}
    }}

    render(MANIFEST);
  </script>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\n  Regenerated index.html with embedded manifest (works without server)")

def get_repo_size():
    total = 0
    for root, dirs, files in os.walk('.'):
        # Skip .git and ignore-upload
        dirs[:] = [d for d in dirs if d not in ('.git', 'ignore-upload')]
        for f in files:
            fp = os.path.join(root, f)
            total += os.path.getsize(fp)
    return total / 1024

def show_manifest_template():
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

    manifest = load_manifest()
    if manifest:
        generate_index_html(manifest)
    else:
        print("[!] Skipping index.html generation (no manifest.json found)")

    show_manifest_template()

    print("\nNext steps:")
    print("  1. Update manifest.json with new image paths")
    print("  2. Run this script again to regenerate index.html")
    print("  3. Open index.html directly in browser (no server needed)")
    print("  4. git add . && git commit -m 'Update banners'")
    print("  5. git push")
    print(f"\n  Current repo size (tracked): ~{get_repo_size():.0f} KB")

if __name__ == "__main__":
    main()
