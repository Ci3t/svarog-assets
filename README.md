# svarog-banner-assets

Tiny public repo for current Genshin Impact & Wuthering Waves banner images.
Served via **jsDelivr CDN** to the main Svarog app.

## Live URLs

Replace `Ci3t` with your GitHub username if you fork this.

| File | jsDelivr URL |
|------|-------------|
| Manifest | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/manifest.json` |
| Genshin Character | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/genshin/lauma-2026-05.webp` |
| Genshin Weapon | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/genshin/lauma-weapon-2026-05.webp` |
| WuWa Character | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/wuwa/hiyuki-2026-05.webp` |
| WuWa Weapon | `https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/wuwa/frostburn-2026-05.webp` |

## How to Update Banner Images

### Option 1: Copy + Convert Script (Recommended)

Drop your new source images into `ignore-upload/` (your local backup folder, not tracked by git), then run:

```bash
# 1. Convert source images to webp
python update_banners.py

# 2. Update manifest.json with new filenames
# 3. Commit & push
git add .
git commit -m "Update banners for 2026-06"
git push
```

### Option 2: Manual

1. Convert your image to `.webp` (use any tool, e.g. `cwebp`, Photoshop, or an online converter)
2. Name it with the pattern: `<character>-YYYY-MM.webp`
3. Drop it into `genshin/` or `wuwa/`
4. Update `manifest.json` to point to the new file
5. `git add . && git commit -m "Update banners" && git push`

### Important Rules

- **Never overwrite old filenames** — jsDelivr caches aggressively. Always use new dated filenames.
- **Keep old files in the repo** — the main app may still reference them. Only delete after confirming no references exist.
- **Prefer `.webp`** — much smaller than PNG without quality loss.
- **Do not commit `ignore-upload/`** — this folder is in `.gitignore` and should stay local.

## Local Preview

Open `index.html` in your browser to see all current banner images and verify the manifest is correct.

## File Structure

```
svarog-assets/
  .gitignore           # ignores ignore-upload/
  manifest.json         # the single source of truth
  README.md             # this file
  index.html            # local preview gallery
  update_banners.py     # helper script to convert images
  genshin/              # Genshin banner images
  wuwa/                 # WuWa banner images
  ignore-upload/        # your local backup dump (not in git)
```

## Manifest Format

```json
{
  "genshin": {
    "character": {
      "name": "Lauma",
      "match": ["lauma", "lauma / nefer", "nefer"],
      "image": "genshin/lauma-2026-05.webp"
    },
    "weapon": {
      "name": "Nightweaver's Looking Glass",
      "match": ["weapon", "weapon_banner", "current weapon banner"],
      "image": "genshin/lauma-weapon-2026-05.webp"
    }
  },
  "wuwa": {
    "character": {
      "name": "Hiyuki",
      "match": ["hiyuki"],
      "image": "wuwa/hiyuki-2026-05.webp"
    },
    "weapon": {
      "name": "Frostburn",
      "match": ["frostburn"],
      "image": "wuwa/frostburn-2026-05.webp"
    }
  }
}
```

The `match` array lets the main app resolve banner names from user input.
