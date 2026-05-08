# svarog-banner-assets

Tiny public repo hosting only the current Genshin Impact and Wuthering Waves banner images for the Svarog project.

## Purpose

The main Svarog app reads `manifest.json` at runtime to resolve current banner art. Updating banner images only requires pushing new files to this repo — no rebuild of the main app needed.

## jsDelivr URLs

After pushing to GitHub:

```
https://cdn.jsdelivr.net/gh/<GITHUB_USER>/svarog-assets@main/manifest.json
https://cdn.jsdelivr.net/gh/<GITHUB_USER>/svarog-assets@main/genshin/lauma-2026-05.webp
https://cdn.jsdelivr.net/gh/<GITHUB_USER>/svarog-assets@main/genshin/lauma-weapon-2026-05.webp
https://cdn.jsdelivr.net/gh/<GITHUB_USER>/svarog-assets@main/wuwa/hiyuki-2026-05.webp
https://cdn.jsdelivr.net/gh/<GITHUB_USER>/svarog-assets@main/wuwa/frostburn-2026-05.webp
```

Replace `<GITHUB_USER>` with your actual GitHub username or organization.

## Rules

- Keep the repo tiny.
- Do not commit the full 1GB image dump.
- Use versioned filenames when banners rotate.
- Do not overwrite old filenames unless necessary — jsDelivr caches aggressively.
- Prefer `.webp` for smaller file sizes.
