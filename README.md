# svarog-assets

Tiny public GitHub repo for only current Genshin and WuWa banner images.
Served through jsDelivr.

No Cloudinary.  
No Cloudflare R2.  
No 1GB asset dump.  
No build step.

The main Svarog app reads `manifest.json` at runtime.  
Updating current banner art does not require rebuilding the main app.

## jsDelivr URLs

Manifest:
```
https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/manifest.json
```

Images:
```
https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/genshin/lauma-2026-05.webp
https://cdn.jsdelivr.net/gh/Ci3t/svarog-assets@main/wuwa/hiyuki-2026-05.webp
```
