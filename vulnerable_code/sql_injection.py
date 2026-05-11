import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

username = input("Enter username: ")
password = input("Enter password: ")

query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

cursor.execute(query)
result = cursor.fetchall()

print(result)