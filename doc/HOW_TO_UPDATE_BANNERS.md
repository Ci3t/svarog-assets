# How to Update Banners

This guide explains how to add new banner images to the repository and update the manifest.

## Step 1: Add the Image
Place your new `.webp` image file in the corresponding game directory:
- For Genshin Impact: Put the image in the `genshin/` folder (e.g., `genshin/Nicole_Splash.webp`).
- For Wuthering Waves: Put the image in the `wuwa/` folder (e.g., `wuwa/new_banner.webp`).

## Step 2: Run the Update Script
Use the `update_manifest.py` script to link your new image in the `manifest.json`.

Open your terminal in the root directory of the repository and run the script with the appropriate arguments:

```bash
python update_manifest.py --game <game> --slot <slot> --name "<name>" --match "<match_strings>" --image <image_path>
```

### Argument Details:
- `--game`: Choose either `genshin` or `wuwa`.
- `--slot`: Choose either `character` or `weapon`.
- `--name`: The display name of the character or weapon (e.g., "Nicole").
- `--match`: Comma-separated alias strings used to match the banner (e.g., "nicole,nicole banner").
- `--image`: The relative path to the image you added (e.g., `genshin/Nicole_Splash.webp`).

**Example for a Genshin Character:**
```bash
python update_manifest.py --game genshin --slot character --name "Nicole" --match "nicole" --image genshin/Nicole_Splash.webp
```

## Step 3: Commit and Push
The assets are served via GitHub using jsDelivr CDN. To apply your changes, simply commit the new image and the updated `manifest.json` file, then push them to GitHub.

```bash
git add manifest.json <path_to_your_new_image>
git commit -m "Update <game> <slot> banner to <name>"
git push
```

*Note: Changes on jsDelivr may take a short time to propagate. A cache-purge URL is provided by the script output if you need it updated immediately.*