from flask import Flask, render_template, request, redirect

from twilio.rest import Client
import random
import sqlite3
import os
app = Flask(__name__)

# Placeholder user data for demonstration purposes
users = {
    'john': {
        'password': 'password123',
        'phone_number': '+1234567890'  # Replace with your phone number
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        return redirect(f'/verify/{username}/{password}')
    else:
        return "Invalid username or password."

@app.route('/verify/<username>/<password>', methods=['GET', 'POST'])
def verify(username, password):
    if request.method == 'GET':
        return render_template('verification.html', username=username, password=password)

    # Verify the entered verification code (you can add your own verification logic)
    # For this example, we assume the verification code is correct
    return "Verification successful. You are now logged in."

if __name__ == '__main__':
    app.run(debug=True)
