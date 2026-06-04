import sqlite3

# Unsafe string concatenation for a SQL query
def get_user_data(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Vulnerable: attacker can inject SQL syntax
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()
