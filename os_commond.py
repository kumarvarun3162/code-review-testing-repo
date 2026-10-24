import os
import pathlib
import subprocess

# Directly using user-controlled input in a system command
def delete_file(filename):
    # Restrict deletion to a safe directory and validate the filename
    safe_dir = pathlib.Path('/tmp/safe_dir').resolve()
    target = (safe_dir / filename).resolve()
    if not str(target).startswith(str(safe_dir)):
        raise ValueError('Invalid file path')
    subprocess.run(['rm', '-f', str(target)], check=True, shell=False)

user_input = input('Enter the filename to delete: ')
delete_file(user_input)