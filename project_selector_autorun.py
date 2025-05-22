import os
import subprocess
import sys
import requests
import shutil
import re

FILE_LIST_PATH = "file_list.txt"
REQUIREMENTS_FILE = "requirements.txt"
PROMPT_FILE = "prompt.txt"
REPLY_FILE = "chat_log.txt"

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
            rel_path = os.path.relpath(full_path, start=".").replace("\\", "/")
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

def inject_from_github():
    filenames = input("Enter comma-separated filenames to inject from GitHub (or press Enter to skip): ").strip()
    if not filenames:
        return

    if not os.path.exists(PROMPT_FILE):
        print("❌ No prompt.txt found.")
        return

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_body = f.read()

    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        f.write(prompt_body.strip() + "\n\n")

        for filename in [fn.strip() for fn in filenames.split(",") if fn.strip()]:
            url = f"https://raw.githubusercontent.com/niado1/ebymgr/main/{filename}"
            print(f"📡 Fetching {filename} from GitHub...")
            try:
                response = requests.get(url)
                response.raise_for_status()
                file_content = response.text
                f.write(f"# === Injected from GitHub: {filename} ===\n")
                f.write(file_content + "\n\n")
                print(f"✅ Injected {filename} into prompt.txt")
            except Exception as e:
                print(f"❌ Failed to retrieve {filename}: {e}")

def apply_gpt_response():
    if not os.path.exists(REPLY_FILE):
        print("❌ No chat_log.txt found — GPT did not return anything.")
        return

    with open(REPLY_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", content, re.DOTALL)
    filename_match = re.search(r"Enter filename to apply code block \d+.*?: ([\w_.-]+)", content)

    if code_blocks and filename_match:
        target_filename = filename_match.group(1).strip()
        print(f"💾 Preparing to auto-save into: {target_filename}")

        # Backup existing file
        if os.path.exists(target_filename):
            backup_filename = target_filename.replace(".py", ".old.py")
            shutil.copy2(target_filename, backup_filename)
            print(f"🕐 Existing file backed up as: {backup_filename}")

        with open(target_filename, "w", encoding="utf-8") as f:
            f.write(code_blocks[0].strip())
        print(f"✅ GPT code applied to: {target_filename}")
    else:
        print("⚠️ No filename or code block found in chat_log.txt")

def main():
    ensure_dependencies()
    generate_file_list()
    inject_from_github()
    subprocess.run([sys.executable, "chat_with_gpt.py"])
    apply_gpt_response()
    subprocess.run([sys.executable, "backup_and_push.py"])

if __name__ == "__main__":
    main()
