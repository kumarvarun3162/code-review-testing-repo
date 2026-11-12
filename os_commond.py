import os
from pathlib import Path
import subprocess

# Define a safe directory for deletions
SAFE_DIR = Path.home() / "safe_delete"
SAFE_DIR.mkdir(parents=True, exist_ok=True)

user_input = input("Enter the filename to delete: ")
# Resolve the path and ensure it is within SAFE_DIR
file_path = (SAFE_DIR / user_input).resolve()
if not str(file_path).startswith(str(SAFE_DIR.resolve())):
    print("Error: Attempt to delete file outside allowed directory.")
    exit(1)

try:
    # Delete the file safely using subprocess.run
    subprocess.run(["rm", "-f", str(file_path)], check=True, shell=False)
    print(f"Deleted {file_path}")
except subprocess.CalledProcessError as e:
    print(f"Error deleting file: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")