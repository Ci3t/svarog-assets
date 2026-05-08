# svarog-assets

Pure image host for the Svarog project. Served via **jsDelivr CDN**.

The main app reads `manifest.json` to resolve image URLs. Nothing else.

## How It Works

```
Main App                          This Repo
--------                          ---------
"Who is current banner?"    ->    (doesn't care)
"Give me image for 'varka'" ->    manifest.genshin['varka']
                                  = "genshin/varka-2026-06.webp"
```

This repo is **dumb storage**. The main app decides what is current. This repo just answers "what is the URL for X?"

## Live URLs

| File | URL |
|------|-----|
| Manifest | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/manifest.json` |
| Any image | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/{path}` |

## Folder Structure

```
svarog-assets/
  manifest.json           # AUTO-GENERATED lookup table
  index.html              # AUTO-GENERATED preview page
  update_manifest.py      # Run this after adding images
  .gitignore              # ignores ignore-upload/
  README.md               # this file
  genshin/                # Genshin character/weapon images
  wuwa/                   # WuWa character/weapon images
  hsr/
    character_portrait/   # HSR extras (fallback)
    character_icon/       # HSR extras (fallback)
    lightcone_preview/    # HSR extras (fallback)
```

## How to Add Images

### Step 1: Drop files into the right folder

- **Genshin** character/weapon images → `genshin/`
- **WuWa** character/weapon images → `wuwa/`
- **HSR** extras (only if missing from March7th) → `hsr/character_portrait/` etc.

Name your files with the character name. A date suffix is recommended but optional:
```
genshin/varka-2026-06.webp
genshin/varka-weapon-2026-06.webp
wuwa/newchar-2026-06.webp
hsr/character_portrait/9999.png
```

### Step 2: Run the generator

```bash
python update_manifest.py
```

This will:
- Scan all folders
- Auto-generate `manifest.json`
- Regenerate `index.html` with embedded manifest

### Step 3: Verify locally

Open `index.html` in your browser. It works without a server.

### Step 4: Push

```bash
git add .
git commit -m "Add varka banners"
git push
```

jsDelivr picks up the new files within minutes.

## HSR: March7th Primary, This Repo Fallback

HSR images are **not stored here by default**. The main app should use the March7th repo as primary:

```
https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/image/character_portrait/1301.png
```

Only drop HSR images into `hsr/` if:
- A new character dropped and March7th hasn't added them yet
- You need a custom/override image

The manifest includes the primary source URL in `_meta.hsr_primary`.

## Manifest Format

```json
{
  "_meta": {
    "generated": "2026-05-08T...",
    "hsr_primary": "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/image",
    "note": "Auto-generated. Run: python update_manifest.py"
  },
  "genshin": {
    "lauma": "genshin/lauma-2026-05.webp",
    "lauma-weapon": "genshin/lauma-weapon-2026-05.webp",
    "varka": "genshin/varka-2026-06.webp"
  },
  "wuwa": {
    "hiyuki": "wuwa/hiyuki-2026-05.webp",
    "frostburn": "wuwa/frostburn-2026-05.webp"
  },
  "hsr": {
    "character_portrait": {},
    "character_icon": {},
    "lightcone_preview": {}
  }
}
```

Keys are derived from filenames:
- `lauma-2026-05.webp` → key: `lauma`
- `varka_splash-2026-06.webp` → key: `varka_splash`
- `1301.png` → key: `1301`

## Rules

1. **Never overwrite old filenames** — jsDelivr caches aggressively. Always use new names.
2. **Keep old files** — the main app or users might still reference them.
3. **Prefer `.webp`** — much smaller than PNG.
4. **Don't commit `ignore-upload/`** — it's in `.gitignore` and stays local.
5. **Don't edit `manifest.json` manually** — run `update_manifest.py` instead.

## Example: Genshin 6.6 Banner Update

```bash
# 1. Drop new images
cp ~/Downloads/Varka_splash.png genshin/varka-2026-06.webp
cp ~/Downloads/Varka_weapon.png genshin/varka-weapon-2026-06.webp

# 2. Regenerate manifest
python update_manifest.py

# 3. Verify
open index.html

# 4. Push
git add . && git commit -m "Add Genshin 6.6 banners" && git push
```

The main app will now resolve `manifest.genshin['varka']` to the new image.

## Main App Integration

Your main app should fetch the manifest once at startup:

```js
const manifestUrl = 'https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/manifest.json';
const manifest = await fetch(manifestUrl).then(r => r.json());

// Resolve Genshin character image
const genshinImg = `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/${manifest.genshin['varka']}`;

// Resolve WuWa character image
const wuwaImg = `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/${manifest.wuwa['hiyuki']}`;

// Resolve HSR (fallback to this repo if not in March7th)
const hsrPrimary = manifest._meta.hsr_primary;
const hsrPortrait = `${hsrPrimary}/character_portrait/1301.png`;
```
