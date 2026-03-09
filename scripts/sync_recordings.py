#!/usr/bin/env python3
"""Sync recordings from Google Drive Recorder folder to local recordings/ directory."""

import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RECORDINGS_DIR = PROJECT_ROOT / "recordings"
AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".ogg", ".flac", ".aac", ".mp4", ".webm", ".mov"}


def get_gdrive_path() -> Path:
    config_path = PROJECT_ROOT / "config.json"
    if not config_path.exists():
        print("Error: config.json not found. Create it with a 'gdrive_recorder_path' field.", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    raw_path = config.get("gdrive_recorder_path", "")
    if not raw_path or raw_path.startswith("~/Library/CloudStorage/GoogleDrive-YOUR_EMAIL"):
        print("Error: Update 'gdrive_recorder_path' in config.json with your actual path.", file=sys.stderr)
        print("", file=sys.stderr)
        print("To find it, look for your Google Drive Recorder folder:", file=sys.stderr)
        print("  ls ~/Library/CloudStorage/", file=sys.stderr)
        print("", file=sys.stderr)
        print("Then set the full path in config.json, e.g.:", file=sys.stderr)
        print('  "gdrive_recorder_path": "~/Library/CloudStorage/GoogleDrive-you@gmail.com/My Drive/Recorder"', file=sys.stderr)
        sys.exit(1)

    return Path(raw_path).expanduser()


def sync():
    gdrive_path = get_gdrive_path()

    if not gdrive_path.exists():
        print(f"Error: Google Drive path not found: {gdrive_path}", file=sys.stderr)
        print("Make sure Google Drive for Desktop is installed and syncing.", file=sys.stderr)
        sys.exit(1)

    RECORDINGS_DIR.mkdir(exist_ok=True)
    existing = {f.name for f in RECORDINGS_DIR.iterdir()}

    copied = []
    for item in sorted(gdrive_path.rglob("*")):
        if item.is_file() and item.suffix.lower() in AUDIO_EXTENSIONS and item.name not in existing:
            shutil.copy2(item, RECORDINGS_DIR / item.name)
            copied.append(item.name)

    if copied:
        print(f"Synced {len(copied)} new recording(s):")
        for name in copied:
            print(f"  {name}")
    else:
        print("No new recordings to sync.")

    total = len(list(RECORDINGS_DIR.iterdir()))
    print(f"\nTotal recordings in recordings/: {total}")


if __name__ == "__main__":
    sync()
