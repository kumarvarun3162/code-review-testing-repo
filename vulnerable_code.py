"""
VULNERABLE CODE FOR CODE REVIEW TESTING
This file intentionally contains security vulnerabilities to test code review tools.
DO NOT USE IN PRODUCTION
"""

import subprocess
import pickle
import random
import sqlite3
import os
import hashlib
import hmac
from flask import Flask, request, render_template_string

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Credentials
DB_PASSWORD = "admin123"
API_KEY = "sk_live_51234567890abcdef"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"

# VULNERABILITY 2: SQL Injection
def get_user_by_name(username):
    """User lookup function vulnerable to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # VULNERABLE: Direct string concatenation in SQL query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()


def login_user(username, password):
    """Login function with SQL injection vulnerability"""
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    # VULNERABLE: Direct string formatting in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user


# VULNERABILITY 3: Command Injection
def execute_system_command(user_input):
    """Execute user input as shell command"""
    # VULNERABLE: Direct command execution with user input
    result = subprocess.call("echo " + user_input, shell=True)
    return result


def process_file(filename):
    """Process file with command injection vulnerability"""
    # VULNERABLE: User input passed directly to shell
    os.system(f"cat {filename}")


# VULNERABILITY 4: Insecure Deserialization
def deserialize_user_data(data):
    """Deserialize user data from pickle"""
    # VULNERABLE: pickle.loads is unsafe for untrusted data
    user_object = pickle.loads(data)
    return user_object


# VULNERABILITY 5: Cross-Site Scripting (XSS)
@app.route('/greet')
def greet_user():
    """Greeting endpoint vulnerable to XSS"""
    name = request.args.get('name', 'Guest')
    # VULNERABLE: Direct template rendering without escaping
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)


@app.route('/display')
def display_message():
    """Display user message without sanitization"""
    user_message = request.form.get('message', '')
    # VULNERABLE: Direct HTML injection
    html = f"<div>{user_message}</div>"
    return html


# VULNERABILITY 6: Weak Cryptography
def weak_hash_password(password):
    """Hash password using weak algorithm"""
    # VULNERABLE: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()


def weak_hmac_verify(message, signature, key):
    """HMAC verification with timing attack vulnerability"""
    # VULNERABLE: String comparison is susceptible to timing attacks
    expected = hmac.new(key.encode(), message.encode(), hashlib.sha1).hexdigest()
    return signature == expected  # Should use hmac.compare_digest()


# VULNERABILITY 7: Insecure Random
def generate_otp():
    """Generate OTP using weak randomness"""
    # VULNERABLE: random.randint is not cryptographically secure
    return random.randint(100000, 999999)


def generate_token():
    """Generate security token with weak random"""
    # VULNERABLE: Should use secrets.token_urlsafe()
    return str(random.random())


# VULNERABILITY 8: Path Traversal
def read_user_file(user_id, filename):
    """Read user file with path traversal vulnerability"""
    # VULNERABLE: No path validation allows directory traversal
    filepath = f"/user_data/{user_id}/{filename}"
    with open(filepath, 'r') as f:
        return f.read()


@app.route('/download')
def download_file():
    """Download file endpoint with path traversal"""
    file_param = request.args.get('file', '')
    # VULNERABLE: No validation of file path
    with open(f"/uploads/{file_param}", 'rb') as f:
        return f.read()


# VULNERABILITY 9: Missing Input Validation
def process_age(age_input):
    """Process user age without validation"""
    # VULNERABLE: No input validation or type checking
    age = int(age_input)
    return f"You are {age} years old"


def set_user_permissions(role):
    """Set user permissions without validation"""
    # VULNERABLE: No whitelist validation of role
    permissions = {
        role: True
    }
    return permissions


# VULNERABILITY 10: Use After Free / Null Pointer Issues
def unsafe_list_access(items, index):
    """Access list item without bounds checking"""
    # VULNERABLE: No bounds checking
    return items[index]


# VULNERABILITY 11: Information Disclosure
def api_error_handler(error):
    """Error handler that leaks system information"""
    # VULNERABLE: Exposing sensitive system info in error messages
    return f"Error: {str(error)} - System: {os.name} - Python: {os.sys.version}", 500


def log_sensitive_data(user_data):
    """Log sensitive information"""
    # VULNERABLE: Logging passwords and tokens
    import logging
    logging.warning(f"User login attempt: {user_data}")


# VULNERABILITY 12: Missing Authentication
@app.route('/api/admin/delete_user/<user_id>')
def delete_user(user_id):
    """Delete user endpoint with no authentication"""
    # VULNERABLE: No authentication or authorization check
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    return "User deleted"


@app.route('/api/transfer_funds')
def transfer_funds():
    """Transfer funds with no authorization"""
    # VULNERABLE: No authentication or CSRF protection
    recipient = request.form.get('recipient')
    amount = request.form.get('amount')
    # Process transfer...
    return f"Transferred {amount} to {recipient}"


# VULNERABILITY 13: Race Condition
def check_and_create_file(filename):
    """Check if file exists and create - TOCTOU vulnerability"""
    # VULNERABLE: Time-of-check-time-of-use (TOCTOU) race condition
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("Initial content")


# VULNERABILITY 14: Insufficient Logging
def perform_sensitive_operation(user_id, operation):
    """Perform sensitive operation without logging"""
    # VULNERABLE: No audit logging for sensitive operations
    if operation == "delete_all_data":
        # Delete all user data without logging
        pass


# VULNERABILITY 15: Resource Exhaustion
@app.route('/data')
def get_data():
    """Endpoint vulnerable to denial of service"""
    limit = request.args.get('limit', 1000)
    # VULNERABLE: No limit validation - user can exhaust memory
    data = [i for i in range(int(limit))]
    return data


# VULNERABILITY 16: XXE (XML External Entity)
def parse_xml_unsafe(xml_string):
    """Parse XML without disabling external entities"""
    import xml.etree.ElementTree as ET
    # VULNERABLE: XXE attack possible
    root = ET.fromstring(xml_string)
    return root


# VULNERABILITY 17: Insecure Configuration
DEBUG = True  # VULNERABLE: Debug mode enabled in production
SECRET_KEY = "development-key"  # VULNERABLE: Hardcoded secret

app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = SECRET_KEY


# VULNERABILITY 18: Missing Security Headers
@app.route('/insecure')
def insecure_endpoint():
    """Endpoint missing security headers"""
    # VULNERABLE: No HSTS, CSP, X-Frame-Options, etc.
    return "This response lacks security headers"


# VULNERABILITY 19: Weak Password Requirements
def validate_password(password):
    """Password validation with weak requirements"""
    # VULNERABLE: No complexity requirements
    return len(password) > 1  # Any password longer than 1 character accepted


# VULNERABILITY 20: Global Variable Mutation
user_cache = {}

def get_cached_user(user_id):
    """Get user with mutable global state"""
    # VULNERABLE: Global mutable state and race conditions
    global user_cache
    if user_id not in user_cache:
        user_cache[user_id] = fetch_user_from_db(user_id)
    return user_cache[user_id]


def fetch_user_from_db(user_id):
    """Fetch user from database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()


if __name__ == '__main__':
    # VULNERABLE: Running Flask with debug=True in production mode
    app.run(debug=True, host='0.0.0.0')
