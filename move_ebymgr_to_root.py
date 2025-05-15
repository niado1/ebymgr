import os
import shutil
from pathlib import Path

SOURCE = Path("projects/ebymgr")
DEST = Path(".")

def move_all_safe(src: Path, dest: Path):
    print(f"Moving contents of {src} to {dest}...")
    for item in src.rglob("*"):
        rel_path = item.relative_to(src)
        target_path = dest / rel_path

        if item.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
        else:
            if target_path.exists():
                print(f"SKIPPED (already exists): {target_path}")
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(target_path))
                print(f"MOVED: {rel_path}")

    print("Finished move. Now cleaning up empty 'projects/' directory...")
    try:
        shutil.rmtree("projects")
        print("Removed 'projects/' directory.")
    except Exception as e:
        print(f"Could not remove 'projects/': {e}")

if __name__ == "__main__":
    move_all_safe(SOURCE, DEST)
