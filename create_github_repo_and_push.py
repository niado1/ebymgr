import os
import requests
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
repo_name = os.getenv("GITHUB_REPO_NAME")
token = os.getenv("GITHUB_PAT")
env_path = ".env"

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

data = {
    "name": repo_name,
    "private": True
}

print(f"Creating GitHub repo '{repo_name}' under user '{username}'...")
response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

if response.status_code == 201:
    clone_url = response.json()["clone_url"]
    print(f"Repository created: {clone_url}")

    # Update .env with GIT_REMOTE_URL
    with open(env_path, "r") as file:
        lines = file.readlines()

    with open(env_path, "w") as file:
        for line in lines:
            if not line.startswith("GIT_REMOTE_URL="):
                file.write(line)
        file.write(f"GIT_REMOTE_URL={clone_url}\n")

    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "add", "origin", clone_url])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit from GPT dev tool"])
    subprocess.run(["git", "push", "-u", "origin", "master"])
    print("Files pushed to new GitHub repository.")
else:
    print(f"Failed to create repo: {response.status_code}")
    print(response.text)
