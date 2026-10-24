import os
import subprocess
from pathlib import Path

# Directly using user-controlled input in a system command
user_input = input("Enter the filename to delete: ")
safe_path = Path(user_input).resolve()
if not safe_path.is_file() or safe_path.parent != Path.cwd():
    print('Invalid file')
    exit(1)

# Use subprocess.run to delete file safely
subprocess.run(['rm', '-f', str(safe_path)], check=True)