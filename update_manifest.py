#!/usr/bin/env python3
"""
Svarog Asset Manifest Generator

Drop images directly into the repo folders:
  genshin/          -> Genshin character/weapon images
  wuwa/             -> WuWa character/weapon images
  hsr/character_portrait/  -> HSR extras (March7th fallback)
  hsr/character_icon/
  hsr/lightcone_preview/

Then run: python update_manifest.py

This will:
1. Scan all folders
2. Auto-generate manifest.json (lookup table)
3. Regenerate index.html with embedded manifest
"""

import json
import re
from pathlib import Path
from datetime import datetime

HSR_PRIMARY = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/image"

# Regex to strip trailing date suffix like -2026-05 or -2026-5
DATE_SUFFIX_RE = re.compile(r'-(\d{4}-\d{1,2})$')

def extract_key(filename: str) -> str:
    """Extract lookup key from filename.
    
    Examples:
      lauma-2026-05.webp      -> lauma
      lauma-weapon-2026-05    -> lauma-weapon
      varka_splash-2026-6     -> varka_splash
      1301.png                -> 1301
      1301-1.png              -> 1301-1
    """
    # Remove extension
    stem = Path(filename).stem
    # Strip trailing date suffix
    stem = DATE_SUFFIX_RE.sub('', stem)
    # Normalize: lowercase, strip whitespace
    return stem.strip().lower()

def scan_folder(folder: Path) -> dict:
    """Scan a folder and return {key: path} for each image file."""
    result = {}
    if not folder.exists():
        return result
    
    for f in sorted(folder.iterdir()):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
            continue
        key = extract_key(f.name)
        if key:
            # Use forward slashes for URLs
            result[key] = str(f).replace('\\', '/')
    return result

def generate_manifest() -> dict:
    manifest = {
        "_meta": {
            "generated": datetime.now().isoformat(),
            "hsr_primary": HSR_PRIMARY,
            "note": "Auto-generated. Run: python update_manifest.py"
        },
        "genshin": scan_folder(Path("genshin")),
        "wuwa": scan_folder(Path("wuwa")),
        "hsr": {
            "character_portrait": scan_folder(Path("hsr/character_portrait")),
            "character_icon": scan_folder(Path("hsr/character_icon")),
            "lightcone_preview": scan_folder(Path("hsr/lightcone_preview"))
        }
    }
    return manifest

def write_manifest(manifest: dict):
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("  Written: manifest.json")

def get_repo_size_kb() -> float:
    import os
    total = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('.git', 'ignore-upload')]
        for f in files:
            fp = os.path.join(root, f)
            total += os.path.getsize(fp)
    return total / 1024

def generate_index_html(manifest: dict):
    manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
    size_kb = get_repo_size_kb()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Svarog Assets — Preview</title>
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
    main {{ max-width: 1400px; margin: 0 auto; padding: 1.5rem; }}
    .info-box {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
      padding: 1rem; margin-bottom: 1.5rem; font-size: 0.9rem;
    }}
    .info-box code {{ background: rgba(0,0,0,0.3); padding: 0.1rem 0.3rem; border-radius: 4px; font-size: 0.85rem; }}
    .game-section {{ margin-bottom: 2rem; }}
    .game-title {{
      font-size: 1.2rem; color: var(--accent); margin-bottom: 1rem;
      border-bottom: 1px solid var(--border); padding-bottom: 0.5rem;
      display: flex; justify-content: space-between; align-items: center;
    }}
    .count {{ font-size: 0.75rem; color: var(--text-muted); font-weight: normal; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; }}
    .card {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      overflow: hidden; transition: transform 0.15s, box-shadow 0.15s;
    }}
    .card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 24px rgba(0,0,0,0.45); border-color: var(--accent-dim); }}
    .card-header {{
      padding: 0.6rem 0.8rem; background: rgba(255,255,255,0.03);
      border-bottom: 1px solid var(--border); font-family: monospace;
      font-size: 0.8rem; color: var(--accent); word-break: break-all;
    }}
    .card img {{
      width: 100%; height: 180px; object-fit: contain;
      background: rgba(0,0,0,0.2); display: block;
    }}
    .card-footer {{
      padding: 0.6rem 0.8rem; background: rgba(255,255,255,0.02);
      font-size: 0.75rem; color: var(--text-muted);
      font-family: monospace; word-break: break-all;
    }}
    .empty {{ text-align: center; padding: 2rem; color: var(--text-muted); font-style: italic; }}
    .jsdelivr {{ color: var(--text-muted); opacity: 0.6; }}
    footer {{
      text-align: center; padding: 2rem; color: var(--text-muted);
      font-size: 0.8rem; border-top: 1px solid var(--border);
    }}
  </style>
</head>
<body>
  <header>
    <h1>Svarog Assets</h1>
    <div class="subtitle">Image Host Preview — {size_kb:.0f} KB tracked</div>
  </header>

  <main>
    <div class="info-box">
      <strong>This repo is a pure image host.</strong> The main Svarog app reads <code>manifest.json</code> to resolve image URLs.<br>
      HSR primary source: <code>{HSR_PRIMARY}</code><br>
      <strong>To add images:</strong> Drop files into <code>genshin/</code>, <code>wuwa/</code>, or <code>hsr/*/</code>, then run <code>python update_manifest.py</code>.
    </div>
    <div id="content"></div>
  </main>

  <footer>
    Built for the Svarog project. Assets belong to their respective publishers.
  </footer>

  <script>
    const MANIFEST = {manifest_json};
    const JSDELIVR_BASE = 'https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/';

    function createCard(key, path) {{
      const card = document.createElement('div');
      card.className = 'card';

      const header = document.createElement('div');
      header.className = 'card-header';
      header.textContent = key;
      card.appendChild(header);

      const img = document.createElement('img');
      img.src = path;
      img.alt = key;
      img.onerror = function() {{
        this.style.display = 'none';
        const err = document.createElement('div');
        err.style.cssText = 'padding:2rem;text-align:center;color:#ff6b6b;font-size:0.85rem;';
        err.textContent = 'Image not found locally';
        card.appendChild(err);
      }};
      card.appendChild(img);

      const footer = document.createElement('div');
      footer.className = 'card-footer';
      footer.textContent = path;
      const jsd = document.createElement('div');
      jsd.className = 'jsdelivr';
      jsd.textContent = JSDELIVR_BASE + path;
      footer.appendChild(jsd);
      card.appendChild(footer);

      return card;
    }}

    function renderSection(title, items) {{
      const section = document.createElement('div');
      section.className = 'game-section';

      const h2 = document.createElement('div');
      h2.className = 'game-title';
      const keys = Object.keys(items);
      h2.innerHTML = title + '<span class="count">' + keys.length + ' files</span>';
      section.appendChild(h2);

      if (keys.length === 0) {{
        section.innerHTML += '<div class="empty">No images in this folder yet.</div>';
        return section;
      }}

      const grid = document.createElement('div');
      grid.className = 'grid';
      for (const key of keys.sort()) {{
        grid.appendChild(createCard(key, items[key]));
      }}
      section.appendChild(grid);
      return section;
    }}

    function render() {{
      const container = document.getElementById('content');
      container.innerHTML = '';

      if (MANIFEST.genshin) {{
        container.appendChild(renderSection('Genshin Impact', MANIFEST.genshin));
      }}
      if (MANIFEST.wuwa) {{
        container.appendChild(renderSection('Wuthering Waves', MANIFEST.wuwa));
      }}
      if (MANIFEST.hsr) {{
        const hsr = MANIFEST.hsr;
        if (hsr.character_portrait && Object.keys(hsr.character_portrait).length) {{
          container.appendChild(renderSection('HSR Character Portraits', hsr.character_portrait));
        }}
        if (hsr.character_icon && Object.keys(hsr.character_icon).length) {{
          container.appendChild(renderSection('HSR Character Icons', hsr.character_icon));
        }}
        if (hsr.lightcone_preview && Object.keys(hsr.lightcone_preview).length) {{
          container.appendChild(renderSection('HSR Light Cones', hsr.lightcone_preview));
        }}
      }}
    }}

    render();
  </script>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("  Written: index.html")

def print_summary(manifest: dict):
    print("\n" + "="*60)
    print("MANIFEST SUMMARY")
    print("="*60)
    
    genshin_count = len(manifest.get("genshin", {}))
    wuwa_count = len(manifest.get("wuwa", {}))
    hsr = manifest.get("hsr", {})
    hsr_portrait = len(hsr.get("character_portrait", {}))
    hsr_icon = len(hsr.get("character_icon", {}))
    hsr_lc = len(hsr.get("lightcone_preview", {}))
    
    print(f"  Genshin images:     {genshin_count}")
    print(f"  WuWa images:        {wuwa_count}")
    print(f"  HSR portraits:      {hsr_portrait}")
    print(f"  HSR icons:          {hsr_icon}")
    print(f"  HSR lightcones:     {hsr_lc}")
    print(f"  Total tracked:      {genshin_count + wuwa_count + hsr_portrait + hsr_icon + hsr_lc} files")
    print(f"  Repo size:          ~{get_repo_size_kb():.0f} KB")
    
    print("\n  jsDelivr base URL:")
    print("    https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/")
    
    print("\n  Example lookups:")
    if manifest.get("genshin"):
        key = list(manifest["genshin"].keys())[0]
        print(f"    manifest.genshin['{key}']")
    if manifest.get("wuwa"):
        key = list(manifest["wuwa"].keys())[0]
        print(f"    manifest.wuwa['{key}']")
    if hsr.get("character_portrait"):
        key = list(hsr["character_portrait"].keys())[0]
        print(f"    manifest.hsr.character_portrait['{key}']")

def main():
    print("Svarog Asset Manifest Generator")
    print("="*60)
    
    manifest = generate_manifest()
    write_manifest(manifest)
    generate_index_html(manifest)
    print_summary(manifest)
    
    print("\nNext steps:")
    print("  1. Open index.html in browser to verify (no server needed)")
    print("  2. git add . && git commit -m 'Update assets'")
    print("  3. git push")

if __name__ == "__main__":
    main()
