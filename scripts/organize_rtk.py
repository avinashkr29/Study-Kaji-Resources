#!/usr/bin/env python3
"""
RTK Image Organization Script for JLPT-based packs

This script organizes RTK images by JLPT level and creates downloadable packs
for the Study-Kaji-Resources GitHub repository.
"""

import json
import os
import shutil
import zipfile
from pathlib import Path
from collections import defaultdict
import re

# Configuration
RTK_JSON_PATH = "/Users/avinash.c.kumar/Documents/apps/Study Kaji/RTK/kanji_data_full.json"
RTK_IMAGES_PATH = "/Users/avinash.c.kumar/Documents/RTK/collection.media"
OUTPUT_DIR = "/Users/avinash.c.kumar/Documents/apps/Study Kaji/RTK_Organization/Study-Kaji-Resources"
GITHUB_REPO = "https://github.com/avinashkr29/Study-Kaji-Resources"

def load_kanji_data():
    """Load and parse the RTK JSON data"""
    print("Loading RTK kanji data...")
    with open(RTK_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} kanji entries")
    return data

def group_by_jlpt_level(kanji_data):
    """Group kanji by JLPT level and sort by lesson within each level"""
    print("Grouping kanji by JLPT level...")
    
    jlpt_groups = defaultdict(list)
    
    for kanji in kanji_data:
        jlpt_level = kanji.get('classification', {}).get('jlpt_level', 'Unknown')
        jlpt_groups[jlpt_level].append(kanji)
    
    # Sort each group by lesson number
    for level in jlpt_groups:
        jlpt_groups[level].sort(key=lambda x: x.get('rtk_reference', {}).get('lesson', 999))
    
    # Print statistics
    for level, kanji_list in jlpt_groups.items():
        print(f"  {level}: {len(kanji_list)} kanji")
    
    return dict(jlpt_groups)

def split_large_groups(jlpt_groups, max_size=400):
    """Split large JLPT groups into smaller packs"""
    print("Splitting large groups into manageable packs...")
    
    final_packs = {}
    
    for level, kanji_list in jlpt_groups.items():
        if len(kanji_list) <= max_size:
            final_packs[level] = kanji_list
        else:
            # Split into multiple parts
            parts = []
            for i in range(0, len(kanji_list), max_size):
                parts.append(kanji_list[i:i + max_size])
            
            for idx, part in enumerate(parts, 1):
                pack_name = f"{level}_part{idx}"
                final_packs[pack_name] = part
                print(f"  {pack_name}: {len(part)} kanji")
    
    return final_packs

def collect_images_for_pack(kanji_list):
    """Collect all image files needed for a pack"""
    images_needed = set()
    
    for kanji in kanji_list:
        mnemonic = kanji.get('mnemonic', {})
        images = mnemonic.get('images', [])
        
        for image in images:
            if image and image.strip():
                images_needed.add(image.strip())
    
    return list(images_needed)

def create_pack_directory(pack_name, kanji_list, output_dir):
    """Create a directory for a pack with images and manifest"""
    pack_dir = Path(output_dir) / "packs" / pack_name
    pack_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect images
    images_needed = collect_images_for_pack(kanji_list)
    images_copied = []
    images_missing = []
    
    print(f"  Processing {len(images_needed)} images for {pack_name}...")
    
    # Copy images
    for image_name in images_needed:
        src_path = Path(RTK_IMAGES_PATH) / image_name
        dst_path = pack_dir / image_name
        
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            images_copied.append(image_name)
        else:
            images_missing.append(image_name)
    
    # Create pack manifest
    manifest = {
        "pack_name": pack_name,
        "kanji_count": len(kanji_list),
        "images_included": len(images_copied),
        "images_missing": len(images_missing),
        "kanji_list": [
            {
                "id": k.get('id'),
                "character": k.get('character'),
                "keyword": k.get('keyword'),
                "lesson": k.get('rtk_reference', {}).get('lesson'),
                "images": k.get('mnemonic', {}).get('images', [])
            }
            for k in kanji_list
        ]
    }
    
    with open(pack_dir / "manifest.json", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    if images_missing:
        print(f"    Warning: {len(images_missing)} images missing for {pack_name}")
    
    return {
        "pack_name": pack_name,
        "kanji_count": len(kanji_list),
        "images_copied": len(images_copied),
        "images_missing": len(images_missing),
        "directory": str(pack_dir)
    }

def create_zip_archive(pack_info):
    """Create ZIP archive for a pack"""
    pack_dir = Path(pack_info["directory"])
    zip_path = pack_dir.parent.parent / "releases" / f"{pack_info['pack_name']}.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"  Creating ZIP: {zip_path.name}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file_path in pack_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(pack_dir)
                zf.write(file_path, arc_name)
    
    # Get file size
    file_size = zip_path.stat().st_size
    size_mb = round(file_size / (1024 * 1024), 2)
    
    pack_info.update({
        "zip_path": str(zip_path),
        "size_bytes": file_size,
        "size_mb": size_mb
    })
    
    print(f"    Created: {zip_path.name} ({size_mb} MB)")
    return pack_info

def generate_download_manifest(pack_infos):
    """Generate download manifest for the app"""
    print("Generating download manifest...")
    
    manifest = {
        "version": "1.0",
        "repository": GITHUB_REPO,
        "base_download_url": f"{GITHUB_REPO}/releases/download/v1.0/",
        "total_packs": len(pack_infos),
        "packs": []
    }
    
    for pack_info in pack_infos:
        pack_data = {
            "id": pack_info["pack_name"],
            "name": pack_info["pack_name"].replace('_', ' ').title(),
            "filename": f"{pack_info['pack_name']}.zip",
            "download_url": f"{manifest['base_download_url']}{pack_info['pack_name']}.zip",
            "size_bytes": pack_info["size_bytes"],
            "size_mb": pack_info["size_mb"],
            "kanji_count": pack_info["kanji_count"],
            "images_count": pack_info["images_copied"],
            "description": f"JLPT {pack_info['pack_name']} kanji with mnemonic images"
        }
        manifest["packs"].append(pack_data)
    
    # Sort packs by JLPT level order
    jlpt_order = ["n5", "n4", "n3_part1", "n3_part2", "n2_part1", "n2_part2", "n1_part1", "n1_part2"]
    manifest["packs"].sort(key=lambda x: next((i for i, order in enumerate(jlpt_order) if order in x["id"].lower()), 999))
    
    # Save manifest
    manifest_path = Path(OUTPUT_DIR) / "download_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Download manifest saved to: {manifest_path}")
    return manifest

def main():
    """Main execution function"""
    print("=== RTK Image Organization for JLPT Packs ===\n")
    
    # Load data
    kanji_data = load_kanji_data()
    
    # Group by JLPT level
    jlpt_groups = group_by_jlpt_level(kanji_data)
    
    # Split large groups
    final_packs = split_large_groups(jlpt_groups)
    
    print(f"\nCreating {len(final_packs)} packs...")
    
    # Create pack directories and collect images
    pack_infos = []
    for pack_name, kanji_list in final_packs.items():
        print(f"\nProcessing pack: {pack_name}")
        pack_info = create_pack_directory(pack_name, kanji_list, OUTPUT_DIR)
        pack_infos.append(pack_info)
    
    print(f"\nCreating ZIP archives...")
    
    # Create ZIP archives
    for pack_info in pack_infos:
        create_zip_archive(pack_info)
    
    # Generate download manifest
    manifest = generate_download_manifest(pack_infos)
    
    print(f"\n=== Organization Complete ===")
    print(f"Created {len(pack_infos)} packs")
    print(f"Total kanji processed: {sum(p['kanji_count'] for p in pack_infos)}")
    print(f"Total images copied: {sum(p['images_copied'] for p in pack_infos)}")
    print(f"Total size: {sum(p['size_mb'] for p in pack_infos):.1f} MB")
    print(f"\nFiles ready for upload to GitHub releases:")
    for pack_info in pack_infos:
        print(f"  - {pack_info['pack_name']}.zip ({pack_info['size_mb']} MB)")

if __name__ == "__main__":
    main()