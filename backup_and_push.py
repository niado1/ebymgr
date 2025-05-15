import os
import shutil
import datetime
import subprocess
from dotenv import load_dotenv

load_dotenv()

FILE_LIST_PATH = "file_list.txt"
BACKUP_DIR = "backups"

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PAT = os.getenv("GITHUB_PAT")
GIT_REMOTE_URL = os.getenv("GIT_REMOTE_URL")

def load_file_list(path=FILE_LIST_PATH):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def backup_and_commit():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)

    file_list = load_file_list()
    for file in file_list:
        if os.path.exists(file):
            dest = os.path.join(backup_path, os.path.basename(file))
            shutil.copy(file, dest)
            print(f"Backed up: {file}")
        else:
            print(f"Skipped missing file: {file}")

    try:
        staged = False
        for file in file_list:
            normalized_path = os.path.normpath(file)
            if os.path.exists(normalized_path):
                subprocess.run(["git", "add", normalized_path], check=True)
                staged = True

        if not staged:
            print("No files to stage. Exiting.")
            return

        result = subprocess.run(["git", "commit", "-m", f"Backup at {timestamp}"])
        if result.returncode != 0:
            print("Nothing to commit. Skipping push.")
            return

        if GITHUB_USERNAME and GITHUB_PAT and GIT_REMOTE_URL:
            auth_url = GIT_REMOTE_URL.replace("https://", f"https://{GITHUB_USERNAME}:{GITHUB_PAT}@")
            subprocess.run(["git", "push", auth_url, "main"], check=True)
        else:
            subprocess.run(["git", "push"], check=True)

        print("Backup committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print("Git operation failed:", e)
    except FileNotFoundError as fnf:
        print("Git command not found. Make sure Git is installed and in your PATH.")

if __name__ == "__main__":
    backup_and_commit()
