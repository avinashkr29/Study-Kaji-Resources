# Study Kaji Resources

This repository contains downloadable image packs for the **Study Kaji** RTK (Remembering the Kanji) learning application.

## Overview

The RTK dataset contains 2,198 kanji with mnemonic images to help with memorization. Instead of downloading all 973MB of images at once, users can download specific JLPT-level packs based on their study needs.

## Available Downloads

| Pack | Kanji Count | Images | Size | Description |
|------|-------------|--------|------|-------------|
| **N5** | 79 | 100 | 17.8 MB | Essential kanji for JLPT N5 |
| **N4** | 170 | 364 | 66.9 MB | JLPT N4 level kanji |
| **N3** | 370 | 953 | 171.9 MB | JLPT N3 level kanji |
| **N2** | 380 | 921 | 173.6 MB | JLPT N2 level kanji |
| **N1 Part 1** | 400 | 729 | 139.2 MB | JLPT N1 kanji (Part 1) |
| **N1 Part 2** | 400 | 1,439 | 269.3 MB | JLPT N1 kanji (Part 2) |
| **N1 Part 3** | 331 | 647 | 107.3 MB | JLPT N1 kanji (Part 3) |
| **Other** | 68 | 152 | 27.3 MB | Miscellaneous kanji |

**Total**: 2,198 kanji, 5,305 images, 973.2 MB

## Download URLs

All packs are available through GitHub Releases:

```
https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/[PACK_NAME].zip
```

### Direct Download Links:
- [N5.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N5.zip) (17.8 MB)
- [N4.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N4.zip) (66.9 MB)
- [N3.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N3.zip) (171.9 MB)
- [N2.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N2.zip) (173.6 MB)
- [N1_part1.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N1_part1.zip) (139.2 MB)
- [N1_part2.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N1_part2.zip) (269.3 MB)
- [N1_part3.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N1_part3.zip) (107.3 MB)
- [er.zip](https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/er.zip) (27.3 MB)

## Pack Structure

Each ZIP file contains:
- **Images**: PNG files with mnemonic illustrations
- **manifest.json**: Pack metadata including kanji list and image references

### Manifest Structure
```json
{
  "pack_name": "N5",
  "kanji_count": 79,
  "images_included": 100,
  "images_missing": 0,
  "kanji_list": [
    {
      "id": 1,
      "character": "二",
      "keyword": "two",
      "lesson": 1,
      "images": ["ltrtk4863823-140430173826.png"]
    }
  ]
}
```

## Integration with Study Kaji App

The app uses the `download_manifest.json` file to:
1. Display available packs to users
2. Show download sizes and kanji counts
3. Fetch packs from GitHub Releases
4. Extract and cache images locally

### Download Manifest
The manifest provides structured information about all available packs:
- Pack IDs and names
- Download URLs
- File sizes and content counts
- Descriptions

## Organization

Kanji within each JLPT pack are ordered by RTK lesson number (ascending), maintaining the logical learning progression from Heisig's "Remembering the Kanji" methodology.

## Usage in Apps

### Loading the Manifest
```javascript
const manifest = await fetch('https://raw.githubusercontent.com/avinashkr29/Study-Kaji-Resources/main/download_manifest.json');
const packs = await manifest.json();
```

### Downloading a Pack
```javascript
const packUrl = 'https://github.com/avinashkr29/Study-Kaji-Resources/releases/download/v1.0/N5.zip';
const response = await fetch(packUrl);
const zipBlob = await response.blob();
```

## Scripts

### Organization Script
The `scripts/organize_rtk.py` script handles the complete organization process:
- Parses RTK JSON data
- Groups kanji by JLPT level
- Sorts by lesson number within groups
- Copies relevant images
- Creates ZIP archives
- Generates download manifest

To regenerate packs:
```bash
cd Study-Kaji-Resources
python3 scripts/organize_rtk.py
```

## License

This repository contains educational resources for Japanese kanji learning. The images and mnemonics are user-contributed content from the RTK community.

## Related Projects

- **Study Kaji App**: Main application repository
- **RTK Database**: Original RTK kanji data and mnemonics

---

**Note**: After downloading this repository, you'll need to upload the ZIP files from the `releases/` directory to GitHub Releases for the download URLs to work.
