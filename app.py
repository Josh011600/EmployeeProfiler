from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import sqlite3
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


# Function to validate user credentials and return the role

def validate_user(username_or_email, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Check if the input is an email or username
    if '@' in username_or_email:  # Assuming email addresses have '@'
        query = "SELECT username, usertype FROM employees WHERE email=? AND password=?"
    else:
        query = "SELECT username, usertype FROM employees WHERE username=? AND password=?"

    cursor.execute(query, (username_or_email, password))
    user = cursor.fetchone()

    conn.close()
    
    return user if user else None

# Simulating user authentication
def authenticate_user(username, password):
    # Logic to authenticate user and fetch user ID
    # Replace this with your actual authentication logic
    if username == username and password == password:
        return 1  # Return a user ID
    return None



def getEmployees():
  conn = sqlite3.connect('mydatabase.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM employees')
  employees = cursor.fetchall()
  conn.close()
  return employees

def get_user_data(user_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


def get_current_user_id():
    return session.get('user_id')



def getName():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM employees')
    name = cursor.fetchall()
    conn.close()
    return name[0] if name else None



@app.route('/index', methods=['POST'])
def index():
    
    username = request.form['username']
    password = request.form['password']

    user = validate_user(username, password)
    
    if user:
        username, usertype = user
          # Access 'username' at index 2
        usertype = user[1] 
        if usertype:
            # Add the logic for admin login (e.g., session management, redirect to admin dashboard)
            user_id = authenticate_user(username, password)
            employees = getEmployees()
            name = getName()
            '''user_id = get_current_user_id()''' # Replace this with your method to get the user's ID
            user_data = get_user_data(user_id)
            
            if user_id:
                session['id'] = user_id  # Store user ID in session
                return render_template('admin.html', username=username, usertype=usertype, employees=employees, name=name, user_data=user_data)
    elif usertype == 'employee':
            # Add the logic for user login (e.g., session management, redirect to user dashboard)
            return render_template('user.html', username=username, usertype=usertype)
    
        
       
        
        
    # Add the logic for failed login (e.g., display an error message)
    return render_template('index.html', login_failed=True)




'''
@app.route('/')
def display_table():

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, email, dateOfBirth, usertype FROM employees") 
    employees = cursor.fetchall()
    conn.close()

    return render_template('admin.html', employees=employees)
'''






@app.route('/register')
def register():
    return render_template('registeruser.html')

@app.route('/register', methods=['POST'])
def register_submit():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    name = request.form['name']
    age = int(request.form['age'])
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    dateOfBirth = request.form['date_of_birth']
    # Convert the date string to a datetime object
    dateOfBirth = datetime.strptime(dateOfBirth, '%m-%d-%Y').date()

     # Check if the username or email already exists in the database
    cursor.execute("SELECT * FROM employees WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        return redirect(url_for('registration_failed', reason='Username or email already exists'))
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Insert the data into the 'users' table
    cursor.execute("INSERT INTO employees (name, age, email, username, password, dateOfBirth, usertype) VALUES (?, ?, ?, ?, ?, ?, 'employee')",
               (name, age, email, username, password, dateOfBirth))

    conn.commit()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    

    return render_template('success.html')

@app.route('/registration_failed')
def registration_failed():
    reason = request.args.get('reason', 'Unknown error')
    return render_template('registration_failed.html', reason=reason)


#for logout purposes
@app.route('/')
def index_page():
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)