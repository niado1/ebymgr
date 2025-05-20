import os
import subprocess
import sys

FILE_LIST_PATH = "file_list.txt"
REQUIREMENTS_FILE = "requirements.txt"

EXCLUDED_DIRS = {"__pycache__", ".venv", "venv", ".git", "backups", "filter_history", "working_data", "tests"}
EXCLUDED_EXTENSIONS = {".pyc", ".pyd", ".log", ".DS_Store", "Thumbs.db", "desktop.ini", ".json", ".old.py"}
EXCLUDED_FILES = {
    "__init__.py",
    "chat_with_gpt.old.py",
    "file_list_ebymgr.txt",
    "raw_orders.json",
    "raw_orders_with_fulfillments.json",
    "setup_env.bat",
    "setup_env.sh",
    ".env"
}

def is_valid_file(path):
    if any(part in EXCLUDED_DIRS for part in path.split(os.sep)):
        return False
    if any(path.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
        return False
    if path in EXCLUDED_FILES:
        return False
    return True

def generate_file_list(root="."):
    tracked_files = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            full_path = os.path.join(dirpath, file)
            rel_path = os.path.relpath(full_path, start=".").replace("\\", "/").replace("\\", "/")
            if is_valid_file(rel_path):
                tracked_files.append(rel_path)

    with open(FILE_LIST_PATH, "w") as f:
        for path in sorted(tracked_files):
            f.write(path + "\n")

    print("file_list.txt updated for root project.")

def ensure_dependencies():
    try:
        import openai
        import dotenv
    except ImportError:
        print("Missing dependencies. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])

def main():
    ensure_dependencies()
    generate_file_list()
    subprocess.run([sys.executable, "chat_with_gpt.py"])
    subprocess.run([sys.executable, "backup_and_push.py"])

if __name__ == "__main__":
    main()
