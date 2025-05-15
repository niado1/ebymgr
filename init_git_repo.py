import subprocess
import os

def init_git_repo():
    if not os.path.exists(".git"):
        print("Initializing new Git repository...")
        subprocess.run(["git", "init"], check=True)
    else:
        print("Git repository already initialized.")

    # Set up remote origin (silently skip if already set)
    remotes = subprocess.run(["git", "remote"], capture_output=True, text=True)
    if "origin" not in remotes.stdout:
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/niado1/ebymgr.git"], check=True)
    else:
        print("Remote 'origin' already exists.")

    # Create main branch
    subprocess.run(["git", "checkout", "-b", "main"], check=False)

    # Add only files listed in file_list.txt
    print("Staging files from file_list.txt...")
    with open("file_list.txt", "r") as f:
        for line in f:
            path = line.strip()
            if os.path.exists(path):
                subprocess.run(["git", "add", os.path.normpath(path)], check=True)
            else:
                print(f"Skipping missing file: {path}")

    # Commit and push
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    print("Repository initialized and pushed successfully.")

if __name__ == "__main__":
    init_git_repo()
