import os
import subprocess
import sys

PROJECTS_DIR = "projects"
FILE_LIST_PATH = "file_list.txt"
REQUIREMENTS_FILE = "requirements.txt"

def list_projects():
    return [name for name in os.listdir(PROJECTS_DIR)
            if os.path.isdir(os.path.join(PROJECTS_DIR, name))]

def generate_file_list(project_name):
    project_path = os.path.join(PROJECTS_DIR, project_name)
    tracked_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path).replace("\\", "/")
            tracked_files.append(rel_path)

    with open(FILE_LIST_PATH, "w") as f:
        for path in sorted(tracked_files):
            f.write(path + "\n")

    print(f"file_list.txt updated for project: {project_name}")

def ensure_dependencies():
    try:
        import openai
        import dotenv
    except ImportError:
        print("Missing dependencies. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])

def main():
    ensure_dependencies()

    projects = list_projects()
    if not projects:
        print("No projects found in 'projects/' directory.")
        return

    print("Available Projects:")
    for idx, name in enumerate(projects, 1):
        print(f"{idx}. {name}")

    choice = input("Select a project by number: ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(projects):
            generate_file_list(projects[idx])
            subprocess.run([sys.executable, "chat_with_gpt.py"])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
