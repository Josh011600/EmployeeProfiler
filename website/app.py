
from flask import Flask, render_template, request, redirect, url_for
from website import create_app
import sqlite3
from datetime import datetime
app = Flask(__name__)

app = create_app()

# Function to validate user credentials and return the role
def validate_user(username, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Replace 'users' with the actual table name in your database
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()
    
    return user if user else None

if __name__ == '__app__':
    app.run(debug=True)


