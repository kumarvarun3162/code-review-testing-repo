import subprocess

# Directly using user-controlled input in a system command
user_input = input("Enter the filename to delete: ")
subprocess.run(["rm", "-f", user_input], check=True)