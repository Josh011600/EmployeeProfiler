import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to validate user credentials and return the role
def validate_user(username, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Replace 'users' with the actual table name in your database
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()

    return user[0] if user else None

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    role = validate_user(username, password)

    if role == 'admin':
        # Add the logic for admin login (e.g., session management, redirect to admin dashboard)
        return redirect(url_for('admin.html', username=username))
    elif role == 'user':
        # Add the logic for user login (e.g., session management, redirect to user dashboard)
        return redirect(url_for('user.html', username=username))
    else:
        # Add the logic for failed login (e.g., display an error message)
        return "Invalid credentials. Please try again."

@app.route('/admin.html')
def admin_dashboard():
    # Add the logic for the admin dashboard here
    return "Welcome to the admin dashboard!"

@app.route('/user.html')
def user_dashboard():
    # Add the logic for the user dashboard here
    return "Welcome to the user dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
