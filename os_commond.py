import os
import subprocess
from pathlib import Path

# Prevent execution as root
if os.geteuid() == 0:
    print('Do not run this script as root.')
    exit(1)

# Allowed directory
allowed_dir = Path('/safe/dir').resolve()

# Get user input
user_input = input("Enter the filename to delete: ")

# Resolve file path
file_path = (allowed_dir / user_input).resolve()

# Validate file path
if not file_path.is_file() or allowed_dir not in file_path.parents:
    print('Invalid file path')
else:
    # Delete file using subprocess.run
    try:
        subprocess.run(['rm', '-f', str(file_path)], check=True, shell=False)
        print(f"Deleted {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting file: {e}")