
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from datetime import datetime
app = Flask(__name__)



# Function to validate user credentials and return the role
def validate_user(username, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Replace 'users' with the actual table name in your database
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()
    
    return user if user else None




@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index():
    username = request.form['username']
    password = request.form['password']

    user = validate_user(username, password)
    
    if user:
        username, role = user
          # Access 'username' at index 2
        role = user[1]  # Access 'role' at index 4
        if role == 'admin':
            # Add the logic for admin login (e.g., session management, redirect to admin dashboard)
            return render_template('admin.html', username=username, role=role)
        elif role == 'user':
            # Add the logic for user login (e.g., session management, redirect to user dashboard)
            return render_template('user.html', username=username, role=role)
    
    # Add the logic for failed login (e.g., display an error message)
    return "Invalid credentials. Please try again."


@app.route('/admin.html')
def admin_dashboard():

    # Add the logic for the admin dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('admin.html', username=username, )
@app.route('/user.html')
def user_dashboard():

    # Add the logic for the user dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('user.html', username=username)

@app.route('/register')
def register_form():
    return render_template('registeruser.html')

@app.route('/register', methods=['POST'])
def register_submit():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    name = request.form['name']
    age = int(request.form['age'])
    username = request.form['username']
    password = request.form['password']
    date_of_birth = request.form['date_of_birth']
    # Convert the date string to a datetime object
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    # Insert the data into the 'users' table
    cursor.execute("INSERT INTO users (name, age, username, password, date_of_birth, role) VALUES (?, ?, ?, ?, ?, 'user')",
                   (name, age, username, password, date_of_birth))
    conn.commit()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    

    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)

    app.debug = True 
