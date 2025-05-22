import os
import re
import difflib
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import subprocess

load_dotenv()

client = OpenAI()
LOG_FILE = "chat_log.txt"
CHANGELOG_FILE = "changelog.txt"

def log_chat(prompt, response):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n[Prompt - {datetime.now()}]\n{prompt}\n")
        f.write(f"[Response]\n{response}\n")

def log_changelog(filename, changes):
    with open(CHANGELOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n[Changes to {filename} - {datetime.now()}]\n{changes}\n")

def extract_code_blocks(text):
    return re.findall(r"```python(.*?)```", text, re.DOTALL)

def show_diff(original, updated):
    diff = difflib.unified_diff(
        original.splitlines(), 
        updated.splitlines(), 
        fromfile="original", 
        tofile="updated", 
        lineterm=""
    )
    return "\n".join(diff)

def send_prompt(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

def run_tests():
    try:
        result = subprocess.run(["python", "-m", "unittest", "discover", "-s", "tests"], capture_output=True, text=True)
        print("\n--- Test Output ---\n")
        print(result.stdout)
        if result.returncode != 0:
            error_prompt = f"Tests failed. Here is the output:\n\n{result.stdout}\n\nFix the issue."
            print("\nSending test failures to GPT for help...\n")
            response = send_prompt(error_prompt)
            log_chat(error_prompt, response)
            print("\n--- GPT Suggested Fix ---\n")
            print(response)

            issue_title = "Test Failure Detected"
            issue_body = f"Automated test failure:\n\n{result.stdout}"
            try:
                subprocess.run(["python", "create_github_issue.py", issue_title, issue_body])
            except Exception as e:
                print(f"Failed to create GitHub issue: {e}")
    except Exception as e:
        print(f"Test run error: {e}")

def main():
    prompt_file = "prompt.txt"
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        print("✅ Loaded prompt from prompt.txt")
    else:
        prompt = input("Enter your prompt: ")

    reply = send_prompt(prompt)
    log_chat(prompt, reply)
    print("\n--- GPT Reply ---\n")
    print(reply)

if __name__ == "__main__":
    main()
    run_tests()
