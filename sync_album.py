import sqlite3
from pathlib import Path
import json
import hashlib
import os

def to_dwarf_path(full_path: Path) -> str:
    last_dir = full_path.parent.name  # gets the last directory name
    filename = full_path.name         # gets the file name
    dwarf_path = Path("/DWARF3/Astronomy") / last_dir / filename
    return str(dwarf_path).replace("\\", "/")

def compute_md5(file_path: Path) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def parse_shots_info(json_path: Path) -> dict:
    with open(json_path, "r") as f:
        return json.load(f)

def sync_directories(root_dir: Path, album_db_path: Path):
    conn = sqlite3.connect(album_db_path)
    cur = conn.cursor()
    new_files = 0

    # Ensure table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='astroInfo'")
    if not cur.fetchone():
        print("❌ Table 'astroInfo' not found.")
        conn.close()
        return

    print(f"🔍 Scanning directory: {root_dir}")
    for subdir in root_dir.rglob("*"):
        if not subdir.is_dir():
            continue

        # Basic file presence check
        json_file = subdir / "shotsInfo.json"
        stacked_img = subdir / "stacked.jpg"
        thumb_img = subdir / "stacked_thumbnail.jpg"
        fits_file = next(subdir.glob("stacked-*.fits"), None)

        if not (json_file.exists() and stacked_img.exists() and thumb_img.exists() and fits_file):
            continue

        # Check if already in DB
        dwarf_path = to_dwarf_path(stacked_img)
        cur.execute("SELECT id FROM astroInfo WHERE file_path=?", (dwarf_path,))
        if cur.fetchone():
            print(f"🟡 Already exists in DB: {dwarf_path}")
            continue  # Already present

        info = parse_shots_info(json_file)
        file_size = stacked_img.stat().st_size
        mod_time = int(stacked_img.stat().st_mtime)

        # Prepare all paths
        thumbnail_path = to_dwarf_path(thumb_img)
        fits_path = to_dwarf_path(fits_file)
        fits_md5 = compute_md5(fits_file)

        cur.execute("""
            INSERT INTO astroInfo (
                file_path, modification_time, thumbnail_path, file_size,
                dec, ra, target, binning, format, exp_time, gain,
                shotsToTake, shotsTaken, shotsStacked, ircut,
                width, height, media_type,
                stacked_fits_path, stacked_fits_md5
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dwarf_path, mod_time, thumbnail_path, file_size,
            str(info["DEC"]), str(info["RA"]), info["target"],
            info["binning"], info["format"], str(info["exp"]), int(info["gain"]),
            int(info["shotsToTake"]), int(info["shotsTaken"]),
            int(info["shotsStacked"]), info["ir"],
            "0", "0", 4,
            fits_path, fits_md5
        ))
        print(f"✅ Inserted {dwarf_path}")
        new_files += 1

    conn.commit()
    conn.close()
    print("🎉 Sync complete.")

    return new_files
