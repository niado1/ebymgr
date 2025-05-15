import subprocess
import os

def find_git_path():
    try:
        result = subprocess.run(["where", "git"], capture_output=True, text=True, check=True)
        git_path = result.stdout.strip().splitlines()[0]
        return os.path.dirname(git_path)
    except subprocess.CalledProcessError:
        print("Git not found on system PATH.")
        return None

def add_to_path(git_bin_path):
    current_path = os.environ.get("PATH", "")
    if git_bin_path in current_path:
        print("Git path already in PATH.")
        return
    try:
        print(f"Adding '{git_bin_path}' to your user PATH...")
        subprocess.run(["setx", "PATH", f"{current_path};{git_bin_path}"], check=True)
        print("Update successful. You may need to restart your shell.")
    except subprocess.CalledProcessError as e:
        print("Failed to update PATH:", e)

if __name__ == "__main__":
    git_bin = find_git_path()
    if git_bin:
        add_to_path(git_bin)
