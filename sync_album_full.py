import shutil
from pathlib import Path
import argparse
from sync_album import sync_directories  # Assume previous logic is in sync_album.py

def prepare_album_db(original_path: Path) -> Path:
    backup = original_path.with_suffix('.db.backup')
    backup_old = original_path.with_suffix('.db.backup.old')
    new_db = original_path.with_suffix('.db.new')

    if backup.exists():
        print(f"🔁 Moving existing backup to: {backup_old}")
        shutil.copy2(backup, backup_old)

    print(f"📦 Backing up original DB to: {backup}")
    shutil.copy2(original_path, backup)

    print(f"🆕 Creating new working DB at: {new_db}")
    shutil.copy2(original_path, new_db)

    return new_db

def update_album_db(original_path: Path, album_db_path: Path) -> Path:
    backup = original_path.with_suffix('.db.backup')

    if backup.exists():
        print(f"🔁 Existing backup in: {backup}")
    else:
        print(f"📦 Backing up original DB to: {backup}")
        shutil.copy2(original_path, backup)

    if album_db_path.exists():
        print(f"🔁 Existing new database in: {album_db_path}")
        shutil.copy2(album_db_path, original_path)

        print(f"📦 original DB has been updated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', required=True, help="Path to Astronomy data, e.g. g:\\Astronomy")
    parser.add_argument('--album-db', default="G:\\album.db", help="Path to original album.db on Dwarf")
    parser.add_argument("--update-db", action="store_true", help="Update original album.db if new entries were inserted")
    args = parser.parse_args()

    orig_db = Path(args.album_db)
    new_db = prepare_album_db(orig_db)

    new_files = sync_directories(Path(args.source_dir), new_db)

    if new_files > 0:
        print(f"🆕 {new_files} new entries inserted.")
        if args.update_db:
            update_album_db(orig_db, new_db)
    else:
        print("✅ No new data to sync.")