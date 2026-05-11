import sqlite3
import hashlib
import getpass

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

password_hash = hashlib.sha256(password.encode()).hexdigest()
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"

cursor.execute(query)
result = cursor.fetchall()

print(result)