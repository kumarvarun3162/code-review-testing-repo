import os

# Directly using user-controlled input in a system command
user_input = input("Enter the filename to delete: ")
os.system(f"rm -f {user_input}")
